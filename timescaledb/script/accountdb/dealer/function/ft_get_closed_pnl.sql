drop function if exists dealer.ft_get_closed_pnl;

CREATE or replace function dealer.ft_get_closed_pnl(
	start_date date,
	end_date date
)
returns table(
	entry_date date,
	exit_date date,
    strategy int,
	security_type char(1),
    code varchar(10),
    qty int,
    buy_amt double precision,
    sell_amt double precision,
    pnl double precision,
	tax double precision,
	tx_fee double precision,
	pnl_after_tax_fee double precision,
	profit_trade boolean

)
/*
	select * from dealer.ft_get_closed_pnl(CURRENT_DATE-30, CURRENT_DATE) order by strategy, code;
*/

AS $$
BEGIN
	RETURN QUERY

	with cteTrades as (
		select t0.id, t0.strategy, t0.security_type, t0.code, t0.action, t0.price, t0.qty, t0.trade_date, t0.trade_time,
			sum(t0.qty) over (PARTITION BY t0.strategy, t0.code, t0.action order by t0.trade_date + t0.trade_time, t0.id) as rolling_qty
		from dealer.trades t0
		where t0.trade_date >= start_date
			and t0.trade_date <= end_date

	), cteRollingQty as(
		select 
			t0.id, t0.strategy, t0.security_type, t0.code, t0.action, t0.price, t0.qty, t0.trade_date, t0.trade_time,
			COALESCE(lag(t0.rolling_qty, 1) over 
				(PARTITION BY t0.strategy, t0.code, t0.action order by t0.trade_date + t0.trade_time, t0.id),
				0
			) as from_qty,
			t0.rolling_qty as to_qty
		from cteTrades t0

	), cteTradeMapping as (
		select
			tb.id,
			tb.strategy,
			tb.trade_date as b_trade_date,
			tb.trade_time as b_trade_time,
			tb.security_type,
			tb.code, 
			-- buy
			tb.price as b_price,
			tb.qty as b_qty,
			tb.from_qty as b_from_qty,
			tb.to_qty as b_to_qty,
			-- sell
			ts.trade_date as s_trade_date,
			ts.trade_time as s_trade_time,
			ts.price as s_price,
			ts.qty as s_qty,
			ts.from_qty as s_from_qty,
			ts.to_qty as s_to_qty,
			(
				(case when tb.to_qty >= ts.to_qty then ts.to_qty else tb.to_qty end)
				- (case when tb.from_qty <= ts.from_qty then ts.from_qty else tb.from_qty end)
			) as use_qty
		from cteRollingQty tb
		LEFT JOIN cteRollingQty ts on ts.action = 'S'
			and ts.strategy = tb.strategy
			and ts.code = tb.code
			and tb.to_qty > ts.from_qty
			and tb.from_qty < ts.to_qty
		where tb.action = 'B' and ts.from_qty is not NULL

	), cteCost as (
		select
			t0.b_trade_date as entry_date,
			last(t0.s_trade_date, t0.s_trade_date) as exit_date,
			t0.strategy, t0.security_type, t0.code, 
			sum(t0.use_qty)::INT as qty,
			sum(t0.b_price * t0.use_qty) * 1000 as buy_amt,
			sum(t0.s_price * t0.use_qty) * 1000 as sell_amt,
			sum((t0.s_price - t0.b_price)*t0.use_qty)*1000  as pnl
		from cteTradeMapping t0
		group by t0.b_trade_date, t0.strategy, t0.security_type, t0.code

	), cteFee as (
		select t0.*,
			t0.sell_amt * 0.003 as tax,
			0.0::double precision as tx_fee
		from cteCost t0
	)

	select t0.*,
		(t0.pnl - t0.tax - t0.tx_fee)::double precision as pnl_after_tax_fee,
		case when t0.sell_amt - t0.tax - t0.tx_fee >= t0.buy_amt then true else false end as profit_trade
	from cteFee t0;


END;
$$ 
LANGUAGE plpgsql;
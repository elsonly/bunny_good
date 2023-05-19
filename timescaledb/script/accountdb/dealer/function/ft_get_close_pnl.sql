
drop function if exists dealer.ft_get_close_pnl;

CREATE or replace function dealer.ft_get_close_pnl(
	in_date date
)
returns table(
	tdate date,
    strategy int,
    code varchar(10),
    qty int,
    buy_amt double precision,
    sell_amt double precision,
    pnl double precision
)
/*
	select * from dealer.ft_get_close_pnl(CURRENT_DATE) order by strategy, code;
*/

AS $$
BEGIN
	RETURN QUERY


	-- CURRENT_DATE date,
	-- 'B' char(1) 	-- B: long position, 
	-- 					-- S: short position

	with cteTrades as (
		select t0.id, t0.strategy, t0.code, t0.action, t0.price, t0.qty, t0.trade_date, t0.trade_time,
			sum(t0.qty) over (PARTITION BY t0.strategy, t0.code, t0.action order by t0.id, t0.trade_date, t0.trade_time) as rolling_qty
		from dealer.trades t0
		where t0.trade_date <= CURRENT_DATE

	), cteRollingQty as(
		select 
			t0.id, t0.strategy, t0.code, t0.action, t0.price, t0.qty, t0.trade_date, t0.trade_time,
			COALESCE(lag(t0.rolling_qty, 1) over 
				(PARTITION BY t0.strategy, t0.code, t0.action order by t0.id, t0.trade_date, t0.trade_time),
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
			tb.code, 
			tb.price as b_price,
			tb.qty as b_qty,
			tb.from_qty as b_from_qty,
			tb.to_qty as b_to_qty,
			--
			ts.trade_date as s_trade_date,
			ts.trade_time as s_trade_time,
			ts.price as s_price,
			ts.qty as s_qty,
			ts.from_qty as s_from_qty,
			ts.to_qty as s_to_qty,
			(
				(case when tb.to_qty >= ts.to_qty then ts.to_qty else tb.to_qty end)
				- (case when tb.from_qty >= ts.from_qty then tb.from_qty else tb.from_qty end)
			) as use_qty
		from cteRollingQty tb
		LEFT JOIN cteRollingQty ts on ts.action = 'S'
			and ts.strategy = tb.strategy
			and ts.code = tb.code
			and tb.to_qty >= ts.from_qty
			and tb.from_qty < ts.to_qty
		where tb.action = 'B' and ts.from_qty is not NULL
	)

	select
        in_date as end_date, 
        t0.strategy, t0.code, 
		sum(t0.use_qty)::INT as qty,
		sum(t0.b_price * t0.use_qty) * 1000 as buy_amt,
		sum(t0.s_price * t0.use_qty) * 1000 as sell_amt,
		sum((t0.s_price - t0.b_price)*t0.use_qty)*1000  as pnl
	from cteTradeMapping t0
	group by t0.strategy, t0.code;

END;
$$ 
LANGUAGE plpgsql;
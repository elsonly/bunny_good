
drop function if exists dealer.ft_get_positions_fifo;

CREATE or replace function dealer.ft_get_positions_fifo(
	in_date date,
	in_action char(1), 	-- B: long position, 
						-- S: short position
	is_concat boolean default true
)
returns table(
	tdate date,
    strategy int,
	security_type char(1),
    code varchar(10),
    action char(1),
    qty int,
    cost_amt double precision,
    avg_prc double precision,
	first_entry_date date
)
/*
	select * from dealer.ft_get_positions_fifo(CURRENT_DATE, 'B');
	select * from dealer.ft_get_positions_fifo(CURRENT_DATE, 'B', true);
*/

AS $$
BEGIN
	RETURN QUERY

	with ctePosition as (
		select 
			-1*row_number() over(order by t0.first_entry_date) as id,
			t0.strategy, t0.security_type, t0.code, t0.action, 
			t0.avg_prc as price, t0.qty,
			t0.first_entry_date as trade_date,
			'13:30:00'::time as trade_time,
			0 as rid,
			t0.tdate
		from dealer.positions t0
		where is_concat
			and t0.tdate = (select max(tt0.tdate) from dealer.positions tt0 where tt0.tdate < in_date)
	
	), cteTrades as (
		select t0.id, t0.strategy, t0.security_type, t0.code, t0.action, 
			t0.price, t0.qty, t0.trade_date, t0.trade_time, t0.rid
		from ctePosition t0
		
		UNION ALL
		select t0.id, t0.strategy, t0.security_type, t0.code, t0.action, 
			t0.price, t0.qty, t0.trade_date, t0.trade_time,
			row_number() over(
				PARTITION by t0.strategy, t0.security_type, t0.code 
				order by (t0.trade_date + t0.trade_time), t0.id
			) as rid
		from dealer.trades t0
		where t0.trade_date <= in_date
			and t0.trade_date > (select COALESCE(max(tt0.tdate), '1990-01-01'::date) from ctePosition tt0)

	), cteStockSum as(
		select 
			t0.strategy, t0.code, t0.security_type,
			case when sum(case t0.action when 'B' then 1 else -1 end * t0.qty ) >= 0 
				then 'B' else 'S' end as action,
			abs(sum(case t0.action when 'B' then 1 else -1 end * t0.qty )) as tot_qty
		from cteTrades t0
		group by t0.strategy, t0.security_type, t0.code

	), cteReverseInSum as(
		select
			t0.id,
			t0.rid,
			t0.trade_date, 
			t0.trade_time, 
			t0.strategy,
			t0.code, 
			t0.qty,
			(
				select sum(tt0.qty) 
				from cteTrades tt0 
				where tt0.strategy = t0.strategy
					and tt0.code = t0.code
					and tt0.action = t0.action
					and tt0.rid >= t0.rid
					and tt0.trade_date + tt0.trade_time >= t0.trade_date + t0.trade_time

				group by tt0.strategy, tt0.security_type, tt0.code
			) as rolling_qty		
		from cteTrades t0
		where t0.action = in_action

	), cteWithLastTranDate as(
		select 
			t1.*,
			t0.tot_qty,
			t0.tot_qty - (t1.rolling_qty - t1.qty)  as use_qty,
			t0.security_type
		from cteStockSum t0
		LEFT JOIN LATERAL (
			select tt1.*
			from cteReverseInSum tt1
			where tt1.strategy = t0.strategy
				and tt1.code = t0.code 
				and tt1.rolling_qty >= t0.tot_qty 
			order by tt1.trade_date desc, tt1.trade_time desc, tt1.id desc
			limit 1
		) t1 on true
		where t0.action = in_action

	), ctePrice as(
		select 
			t2.strategy, t1.code, t2.price, t0.security_type,
			case t0.id when t1.id then t0.use_qty else t1.qty end as qty,
			-- entry_date is not good enough, If entry more than once, it may encounter some problems.
			t0.trade_date as entry_date
		from cteWithLastTranDate t0
		JOIN cteReverseInSum t1 on t1.strategy = t0.strategy
			and t1.code = t0.code 
			and t1.trade_date + t1.trade_time>= t0.trade_date + t0.trade_time
			and t1.rid >= t0.rid
		LEFT JOIN cteTrades t2 on t2.id = t1.id

	)

	select 
		in_date as tdate,
		t0.strategy,
		t0.security_type, 
		t0.code, 
		in_action as action,
		sum(t0.qty)::INT as qty,
		sum(t0.price * t0.qty) * 1000 as cost_amt,
		sum(t0.price * t0.qty) / sum(t0.qty) as avg_prc,
		min(entry_date) as first_entry_date
	from ctePrice t0
	where t0.qty > 0
	group by t0.strategy, t0.security_type, t0.code;

END;
$$ 
LANGUAGE plpgsql;
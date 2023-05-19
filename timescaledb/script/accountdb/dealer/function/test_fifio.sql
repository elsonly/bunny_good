drop table if exists t_trades;
create temp table t_trades(
    id BIGSERIAL PRIMARY KEY,
    strategy INT,
    trade_date date,
    trade_time time,
    code varchar(10),
    action char(1), -- B, S
    price double precision,
    qty int
);
insert into t_trades(strategy, trade_date, trade_time, code, action, price, qty)
values
	(1, '2023-05-01', '09:00:00', '2330', 'B', 600, 1),
	(1, '2023-05-01', '09:00:00', '2330', 'B', 602, 3),
	(1, '2023-05-01', '09:00:01', '2330', 'B', 603, 1),
	(1, '2023-05-02', '09:00:00', '2330', 'S', 605, 2),
	(1, '2023-05-03', '09:00:00', '2330', 'S', 607, 2),
	(1, '2023-05-04', '09:00:00', '2330', 'B', 610, 1),
	--
	(2, '2023-05-02', '09:00:00', '2330', 'S', 605, 3),
	(2, '2023-05-04', '09:00:00', '2330', 'S', 610, 1),
	(2, '2023-05-06', '09:00:00', '2330', 'B', 600, 3),
	(2, '2023-05-06', '09:00:05', '2330', 'S', 605, 1);


with cteTrades as (
	select t0.id, t0.strategy, t0.code, t0.action, t0.price, t0.qty, t0.trade_date, t0.trade_time
	from t_trades t0
	where t0.trade_date <= '2023.05.13'--in_tdate
		--and t0.strategy = 1--in_strategy_id
		--and t0.status = 'Filled'

), cteStockSum as(
	select 
		t0.strategy, t0.code,
		case when sum(case t0.action when 'B' then 1 else -1 end * t0.qty ) > 0 
			then 'B' else 'S' end as action,
		abs(sum(case t0.action when 'B' then 1 else -1 end * t0.qty )) as tot_qty
	from cteTrades t0
	group by t0.strategy, t0.code

), cteReverseInSum as(
	select
		t0.id,
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
				and tt0.id >= t0.id
				and tt0.trade_date + tt0.trade_time >= t0.trade_date + t0.trade_time

			group by t0.strategy, tt0.code
		) as rolling_qty		
	from cteTrades t0
	where t0.action = 'S'

), cteWithLastTranDate as(
	select 
		t1.*,
		t0.tot_qty,
		t0.tot_qty - (t1.rolling_qty - t1.qty)  as use_qty
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
	where t0.action = 'S'

), ctePrice as(
	select 
		t2.strategy, t1.code, t2.price,
		case t0.id when t1.id then t0.use_qty else t1.qty end as qty
	from cteWithLastTranDate t0
	JOIN cteReverseInSum t1 on t1.strategy = t0.strategy
		and t1.code = t0.code 
		and t1.trade_date + t1.trade_time>= t0.trade_date + t0.trade_time
		and t1.id >= t0.id
	LEFT JOIN cteTrades t2 on t2.id = t1.id

)


select t0.strategy, t0.code,
	sum(t0.qty) as qty,
	sum(t0.price * t0.qty) as cost_amt,
	sum(t0.price * t0.qty) / sum(t0.qty) as avg_prc
from ctePrice t0
group by t0.strategy, t0.code





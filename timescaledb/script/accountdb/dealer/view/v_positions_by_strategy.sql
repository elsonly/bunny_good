
DROP VIEW IF EXISTS dealer.v_positions_by_strategy;
CREATE OR REPLACE VIEW dealer.v_positions_by_strategy  AS
-- select * from dealer.v_positions_by_strategy

with w0 as(
    select tdate, strategy, strategy_name,
        sum(cost_amt) as cost_amt,
        max(sum(cost_amt)) over (partition by strategy order by tdate) as roll_max_cost_amt,
        sum(open_pnl) as open_pnl,
        sum(closed_pnl) as closed_pnl,
        sum(tot_pnl) as tot_pnl
    from dealer.v_positions_by_stock
    group by tdate, strategy, strategy_name
), w_max as(
    select strategy, 
        max(cost_amt) as max_cost_amt
    from w0 group by strategy

), w_cost as(
    select tdate, 
        sum(cost_amt) as tot_cost_amt
    from w0
    group by tdate
)

select w0.*, 
    w_max.max_cost_amt,
    w_cost.tot_cost_amt
from w0 
left join w_max on w_max.strategy=w0.strategy
left join w_cost on w_cost.tdate=w0.tdate


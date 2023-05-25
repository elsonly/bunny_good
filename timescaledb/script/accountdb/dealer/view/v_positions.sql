
DROP VIEW IF EXISTS dealer.v_positions;
CREATE OR REPLACE VIEW dealer.v_positions AS
-- select * from dealer.v_positions


with w_agg as (
    select tdate, 
        sum(open_pnl) as open_pnl,
        sum(closed_pnl) as closed_pnl,
        sum(tot_pnl) as tot_pnl,
        sum(cost_amt) as cost_amt,
        10000000 + sum(tot_pnl) as balance
    from dealer.v_positions_by_stock t0
    group by t0.tdate

), w_bal as (
    select *,
        lag(balance, 1) over(order by tdate) as prev_balance,
        max(balance) over (order by tdate) as max_balance
    from w_agg t0

), w_dd as (
    select *,
        balance - prev_balance as balance_chg,
        (balance - max_balance) as "dd",
        (balance / max_balance - 1) * 100 as "dd%"
    from w_bal
)

select * from w_dd;

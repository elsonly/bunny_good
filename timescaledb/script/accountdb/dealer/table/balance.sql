select 
    to_char(t0.tdate, 'MM-DD') as tdate, 
    t0.open_pnl, t0.closed_pnl, 
    t0.cost_amt, 
    (10000000 + COALESCE(t0.closed_pnl, 0) - t0.cost_amt) as available_balance, 
    COALESCE(t0.closed_pnl, 0) + open_pnl as total_pnl,
    t0.balance, 
    t0.balance - t0.prev_balance as balance_chg,
    --max_balance,
    (t0.balance - t0.max_balance) as "dd",
    (t0.balance / t0.max_balance - 1) * 100 as "dd%"
    
    
from(
    select tdate,
        sum(open_pnl) as open_pnl,
        sum(closed_pnl) as closed_pnl,
        sum(tot_pnl) as tot_pnl,
        sum(cost_amt) as cost_amt,
        10000000 + sum(tot_pnl) as balance,
        lag(10000000 + sum(tot_pnl), 1) over(order by tdate) as prev_balance,
        max(10000000 + sum(tot_pnl)) over (order by tdate) as max_balance
    from(
        -- history
        select 
            COALESCE(t_pos.tdate, t_cl.tdate) as tdate,
            COALESCE(t_pos.strategy, t_cl.strategy) as strategy,
            COALESCE(t_pos.code, t_cl.code) as code,
            --t_pos.action,
            --t_pos.qty,
            t_pos.cost_amt,
            --t_pos.avg_prc,
            --t_pos.close,
            t_pos.pnl as open_pnl,
            t_cl.pnl as closed_pnl,
            COALESCE(t_pos.pnl, 0) + COALESCE(t_cl.pnl, 0) as tot_pnl
            
        from dealer.positions t_pos
        full outer join dealer.closed_pnl t_cl on t_cl.tdate = t_pos.tdate
            and t_cl.strategy = t_pos.strategy
            and t_cl.code = t_pos.code
    )tt0
    group by tt0.tdate
)t0
order by t0.tdate
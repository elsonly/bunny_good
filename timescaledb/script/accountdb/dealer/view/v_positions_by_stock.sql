
DROP VIEW IF EXISTS dealer.v_positions_by_stock;
CREATE OR REPLACE VIEW dealer.v_positions_by_stock  AS
-- select * from dealer.v_positions_by_stock
with w_his as (
    -- history
    select *
    from(
        select 
            COALESCE(t_pos.tdate, t_cl.tdate) as tdate,
            COALESCE(t_pos.strategy, t_cl.strategy) as strategy,
            COALESCE(t_pos.code, t_cl.code) as code,
            t_pos.action,
            t_pos.qty,
            t_pos.cost_amt,
            t_pos.avg_prc,
            t_pos.close,
            t_pos.pnl as open_pnl,
            t_cl.pnl as closed_pnl,
            COALESCE(t_pos.pnl, 0) + COALESCE(t_cl.pnl, 0) as tot_pnl
            
        from dealer.positions t_pos
        full outer join dealer.closed_pnl t_cl on t_cl.tdate = t_pos.tdate
            and t_cl.strategy = t_pos.strategy
            and t_cl.code = t_pos.code
    )t0
    where t0.tdate < CURRENT_DATE

), w_cur as (
    -- current
    select 
        COALESCE(t_pos.tdate, t_cl.tdate) as tdate,
        COALESCE(t_pos.strategy, t_cl.strategy) as strategy,
        COALESCE(t_pos.code, t_cl.code) as code,
        t_pos.action,
        t_pos.qty,
        t_pos.cost_amt,
        t_pos.avg_prc,
        t_pos.close,
        t_pos.pnl as open_pnl,
        t_cl.pnl as closed_pnl,
        COALESCE(t_pos.pnl, 0) + COALESCE(t_cl.pnl, 0) as tot_pnl
    from dealer.ft_get_position_open_pnl(CURRENT_DATE, true) t_pos
    full outer join dealer.ft_get_closed_pnl(CURRENT_DATE) t_cl on t_cl.tdate = t_pos.tdate
        and t_cl.strategy = t_pos.strategy
        and t_cl.code = t_pos.code
), w_pos as(
    select * from w_his
    UNION ALL
    select * from w_cur
)

select w_pos.* , 
    t_st.name as strategy_name
from w_pos
left join dealer.strategy t_st on t_st.id = w_pos.strategy;
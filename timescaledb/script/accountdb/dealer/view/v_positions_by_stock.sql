DROP VIEW IF EXISTS dealer.v_positions_by_stock;
CREATE OR REPLACE VIEW dealer.v_positions_by_stock  AS
-- select * from dealer.v_positions_by_stock

with w_pos as (
    select 
        tdate, strategy, security_type, code,
        action, qty, cost_amt, avg_prc, close, pnl, first_entry_date
    from dealer.positions
    where tdate < CURRENT_DATE

    UNION ALL

    select 
        tdate, strategy, security_type, code,
        action, qty, cost_amt, avg_prc, close, pnl, first_entry_date
    from dealer.ft_get_position_open_pnl(CURRENT_DATE, true)

), w_closed as (
    select * 
    from (select DISTINCT tt0.tdate from w_pos tt0) t_date,
        dealer.ft_get_closed_pnl(date_trunc('year', CURRENT_DATE)::date, CURRENT_DATE) t_cls
    where t_cls.exit_date <= t_date.tdate

), w_agg as (
    select   
        COALESCE(t_pos.tdate, t_cls.tdate) as tdate,
        COALESCE(t_pos.strategy, t_cls.strategy) as strategy,
        COALESCE(t_pos.code, t_cls.code) as code,
        t_pos.action,
        t_pos.qty,
        t_pos.cost_amt,
        t_pos.avg_prc,
        t_pos.close,
        t_pos.pnl as open_pnl,
        t_cls.pnl as closed_pnl,
        COALESCE(t_pos.pnl, 0) + COALESCE(t_cls.pnl, 0) as tot_pnl,
        t_cls.pnl_after_tax_fee as closed_pnl_after_tax_fee,
        COALESCE(t_pos.pnl, 0) + COALESCE(t_cls.pnl_after_tax_fee, 0) as tot_pnl_after_tax_fee,
        t_cls.profit_trade
    from w_pos t_pos
    FULL OUTER JOIN w_closed t_cls on t_cls.tdate = t_pos.tdate
        and t_cls.strategy = t_pos.strategy
        and t_cls.code = t_pos.code
)
select t0.*, 
    t_str.name as strategy_name
from w_agg t0
left JOIN dealer.strategy t_str on t0.strategy = t_str.id
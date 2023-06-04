DROP PROCEDURE IF EXISTS dealer.sp_update_cashflow;
CREATE OR REPLACE PROCEDURE dealer.sp_update_cashflow(job_id INT, config JSONB)
LANGUAGE plpgsql
AS $$
	
BEGIN
    with w_cashflow as (
        select t0.trade_date as tdate,
            sum(
                (case t0.action when 'B' then -1 else 1 end) * t0.price * t0.qty * 1000 
            )as  cashflow
        from dealer.trades t0
        where t0.trade_date > (select max(tdate) from dealer.cashflow)
        group by tdate

    ), w_cumulative_cashflow as (

        select t0.tdate,
            t0.cashflow,
            sum(t0.cashflow) over (order by t0.tdate) as cum_cashflow,
            (select last(tt0.balance, tt0.tdate) from dealer.cashflow tt0) as init_balance
        from w_cashflow t0

    ), w_balance as (
        select 
            t0.tdate,
            (
                t0.init_balance + COALESCE(lag(t0.cum_cashflow, 1) over (order by t0.tdate), 0)
            ) as prev_balance,
            t0.cashflow,
            (t0.init_balance + t0.cum_cashflow) as balance
        from w_cumulative_cashflow t0
    )
    insert into dealer.cashflow(tdate, prev_balance, cashflow, balance)
    select tdate, prev_balance, cashflow, balance from w_balance;

END;
$$
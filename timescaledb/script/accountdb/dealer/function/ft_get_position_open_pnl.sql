
drop function if exists dealer.ft_get_position_open_pnl;

CREATE or replace function dealer.ft_get_position_open_pnl(
	in_date date,
    in_use_realtime boolean
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
    first_entry_date date,
    close double precision,
    pnl double precision
)
/*
	select * from dealer.ft_get_position_open_pnl(CURRENT_DATE, true) order by code;
*/

AS $$
BEGIN
	RETURN QUERY
    select 
        t_pos.tdate,
        t_pos.strategy,
        t_pos.security_type,
        t_pos.code,
        t_pos.action,
        t_pos.qty,
        t_pos.cost_amt,
        t_pos.avg_prc,
        t_pos.first_entry_date,
        COALESCE(t_prc.close, t_prc_rt.close) as close,
        (
            (case t_pos.action when 'B' then 1 else -1 end)*
            (COALESCE(t_prc.close, t_prc_rt.close) - t_pos.avg_prc) * t_pos.qty * 1000
        ) as pnl
    from (
        select * from dealer.ft_get_positions_fifo(in_date, 'B')
        union all
        select * from dealer.ft_get_positions_fifo(in_date, 'S')
    )t_pos
    left join(
        select tt0.tdate, tt0.code, tt0.close
        from cmoney.daily_price tt0
        where tt0.code in (select distinct trd.code from dealer.trades trd)
            and tt0.tdate=in_date
    )t_prc on t_prc.code=t_pos.code
    left join public.quote_snapshots t_prc_rt on in_use_realtime and t_prc_rt.code=t_pos.code;

END;
$$ 
LANGUAGE plpgsql;

drop function if exists dealer.ft_get_positions_order_manager;

CREATE or replace function dealer.ft_get_positions_order_manager()
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
	low_since_entry double precision,
	high_since_entry double precision
)
/*
	select * from dealer.ft_get_positions_order_manager();
*/

AS $$
BEGIN
	RETURN QUERY

	with w_pos as (
		select * from dealer.ft_get_positions_fifo(CURRENT_DATE, 'B', false)
		UNION
		select * from dealer.ft_get_positions_fifo(CURRENT_DATE, 'S', false)
	), w_prc as (
		select t0.tdate, t0.code, t0.open, t0.high, t0.low, t0.close
		from cmoney.daily_price t0
		where t0.code in (select tt.code from w_pos tt)
			and t0.tdate >= (select min(tt.first_entry_date) from w_pos tt)
	)

	select *,
		(
			select min(tt.low) from w_prc tt where tt.code=t0.code and tt.tdate>=t0.first_entry_date
		) as low_since_entry,
		(
			select max(tt.high) from w_prc tt where tt.code=t0.code and tt.tdate>=t0.first_entry_date
		) as high_since_entry
	from w_pos t0;

END;
$$ 
LANGUAGE plpgsql;
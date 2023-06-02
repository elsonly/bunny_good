
DROP PROCEDURE IF EXISTS dealer.sp_update_positions;
CREATE OR REPLACE PROCEDURE dealer.sp_update_positions(job_id INT, config JSONB)
LANGUAGE plpgsql
AS $$
DECLARE
	t_row cmoney.institute_invest%rowtype;
	
BEGIN
	RAISE NOTICE 'Executing job % with config %', job_id, config;
    for t_row in (
        select distinct tdate 
		-- TODO: change source table for trading dates
        from cmoney.institute_invest 
        where tdate > CURRENT_DATE-20
            and tdate not in (select distinct tdate from dealer.positions)
    ) LOOP
		RAISE NOTICE 'date: %', t_row.tdate;

		insert into dealer.positions(
			tdate, strategy, code, action, qty, cost_amt, avg_prc, close, pnl, first_entry_date
		)
			select tdate, strategy, code, action, 
				qty, cost_amt, avg_prc, close, pnl, first_entry_date 
			from dealer.ft_get_position_open_pnl(t_row.tdate, false);

    END LOOP;
END;
$$
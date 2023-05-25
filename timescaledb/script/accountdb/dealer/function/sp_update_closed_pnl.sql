
DROP PROCEDURE IF EXISTS dealer.sp_update_closed_pnl;
CREATE OR REPLACE PROCEDURE dealer.sp_update_closed_pnl(job_id INT, config JSONB)
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
            and tdate not in (select distinct tdate from dealer.closed_pnl)
    ) LOOP
		RAISE NOTICE 'date: %', t_row.tdate;

		insert into dealer.closed_pnl(
			tdate, strategy, code, qty, buy_amt, sell_amt, pnl
		)
			select * from dealer.ft_get_closed_pnl(t_row.tdate);

    END LOOP;
END;
$$
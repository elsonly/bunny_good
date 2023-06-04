SELECT * FROM timescaledb_information.jobs;
-- select delete_job(1001);

SELECT add_job(
    'dealer.sp_update_positions',
    '1 day', 
    initial_start => '2023-05-17 20:00:00'::timestamptz, 
    timezone => 'Asia/Taipei'
);

CALL run_job(1002);
-- select * from dealer.positions where tdate = CURRENT_DATE;
-- truncate table dealer.positions


SELECT add_job(
    'dealer.sp_update_cashflow',
    '1 day', 
    initial_start => '2023-05-17 20:00:00'::timestamptz, 
    timezone => 'Asia/Taipei'
);

CALL run_job(1003);
-- select * from dealer.cashflow order by tdate desc limit 10;
-- truncate table dealer.cashflow
SELECT * FROM timescaledb_information.jobs;

SELECT add_job(
    'dealer.sp_update_positions',
    '1 day', 
    initial_start => '2023-05-17 15:00:00'::timestamptz, 
    timezone => 'Asia/Taipei'
);

CALL run_job(1000);
-- select * from dealer.positions where tdate = CURRENT_DATE;
-- truncate table dealer.positions


SELECT add_job(
    'dealer.sp_update_closed_pnl',
    '1 day', 
    initial_start => '2023-05-17 15:00:00'::timestamptz, 
    timezone => 'Asia/Taipei'
);

CALL run_job(1001);
-- select * from dealer.closed_pnl where tdate = CURRENT_DATE - 1;
-- truncate table dealer.closed_pnl
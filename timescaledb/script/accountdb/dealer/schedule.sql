SELECT add_job(
    'dealer.sp_update_positions',
    '1 day', 
    initial_start => '2023-05-17 15:00:00'::timestamptz, 
    timezone => 'Asia/Taipei'
);

SELECT * FROM timescaledb_information.jobs;

CALL run_job(1000);
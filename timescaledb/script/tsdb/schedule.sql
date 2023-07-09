SELECT * FROM timescaledb_information.jobs;
-- select delete_job(1013);

SELECT add_job(
    'cmoney.sp_update_calendar',
    '1 day', 
    initial_start => '2023-06-27 20:00:00'::timestamptz, 
    timezone => 'Asia/Taipei'
);

CALL run_job(1013);
-- select * from cmoney.calendar where tdate >= CURRENT_DATE order by tdate limit 100;
-- truncate table cmoney.calendar;

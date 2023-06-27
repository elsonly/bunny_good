DROP PROCEDURE IF EXISTS cmoney.sp_update_calendar;
CREATE OR REPLACE PROCEDURE cmoney.sp_update_calendar(job_id INT, config JSONB)
LANGUAGE plpgsql
AS $$
	
BEGIN
    truncate table tsdb.cmoney.calendar;

    with w_calendar as(
        select t0.tdate::date as tdate,
            extract('isodow' from t0.tdate) as dow,
            case WHEN t1.tdate is NULL then false else true end as is_trading_date,
            t2.name as holiday
        from generate_series(
            '1997-02-01'::date, 
            CURRENT_DATE + INTERVAL '3 year', 
            interval '1d'
        ) as t0(tdate)
        left join(
            select distinct tdate 
            from cmoney.institute_invest
        )t1 on t0.tdate = t1.tdate
        left join cmoney.holidays t2 on t2.code='TW.TWSE'
            and t2.hdate=t0.tdate

    )

    insert into cmoney.calendar(exchange, tdate, dow, holiday, is_trading_date)
    select 
        'TWSE' as exchange,
        tdate, dow, holiday,
        case when is_trading_date 
                then true
            else 
                case when dow <= 5 and holiday is NULL 
                    then true 
                else 
                    false 
            end
        end as is_trading_date
    from w_calendar;

END;
$$
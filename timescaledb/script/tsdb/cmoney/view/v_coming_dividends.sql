
DROP VIEW IF EXISTS cmoney.v_coming_dividends;
CREATE OR REPLACE VIEW cmoney.v_coming_dividends  AS
-- select * from cmoney.v_coming_dividends

with w_div_q as (
    select code, 
        'Q' as freq,
        0 as rid,
        first(ex_dividend_date, ex_dividend_date) as ex_dividend_date, 
        first(total_cash_dividend, ex_dividend_date) as total_cash_dividend, 
        first(ex_rights_date, ex_rights_date) as ex_rights_date,
        first(total_stock_dividend, ex_rights_date) as total_stock_dividend,
        first(total_dividend, ex_dividend_date) as total_dividend,
        first(cash_dividend_yield, ex_dividend_date) as cash_dividend_yield,
        first(announcement_date, announcement_date) as announcement_date

    from cmoney.dividend_policy_quarterly 
    where ex_dividend_date >= CURRENT_DATE
        or ex_rights_date >= CURRENT_DATE
    group by code

), w_div_y as (
    select code, 
        'Y' as freq,
        1 as rid,
        first(ex_dividend_date, ex_dividend_date) as ex_dividend_date, 
        first(total_cash_dividend, ex_dividend_date) as total_cash_dividend, 
        first(ex_rights_date, ex_rights_date) as ex_rights_date,
        first(total_stock_dividend, ex_rights_date) as total_stock_dividend,
        first(total_dividend, ex_dividend_date) as total_dividend,
        first(cash_dividend_yield, ex_dividend_date) as cash_dividend_yield,
        first(announcement_date, announcement_date) as announcement_date
    from cmoney.dividend_policy 
    where ex_dividend_date >= CURRENT_DATE
        or ex_rights_date >= CURRENT_DATE
    group by code

), w_div as (
    SELECT
        t0.code,
        first(freq, rid) as freq, 
        first(ex_dividend_date, rid) as ex_dividend_date, 
        first(total_cash_dividend, rid) as total_cash_dividend, 
        first(ex_rights_date, rid) as ex_rights_date,
        first(total_stock_dividend, rid) as total_stock_dividend,
        first(total_dividend, rid) as total_dividend,
        first(cash_dividend_yield, rid) as cash_dividend_yield,
        first(announcement_date, rid) as announcement_date

    from (
        select * from w_div_q
        UNION ALL
        select * from w_div_y
    )t0
    group by t0.code
)

select *,
    COALESCE(ex_dividend_date, ex_rights_date) as ex_date
from w_div;
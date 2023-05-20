DROP TABLE IF EXISTS tsdb.cmoney.dividend_policy;
CREATE TABLE tsdb.cmoney.dividend_policy(
    code VARCHAR(10) NOT NULL,
    year INT NOT NULL,
    distribution_frequency smallint,
    ex_rights_date date,
    ex_rights_last_compensation_date date,
    ex_dividend_date date,
    ex_dividend_last_compensation_date date,
    ex_rights_allotment_reference_date date,
    ex_dividend_allotment_reference_date date,
    share_receipt_date date,
    dividend_receipt_date date,
    earnings_stock_dividend double precision,
    surplus_stock_dividend double precision,
    total_stock_dividend double precision,
    earnings_cash_dividend double precision,
    surplus_cash_dividend double precision,
    total_cash_dividend double precision,
    total_dividend double precision,
    stock_dividend_payout_ratio double precision,
    cash_dividend_payout_ratio double precision,
    dividend_payout_ratio double precision,
    ex_rights_opening_reference_price double precision,
    ex_dividend_opening_reference_price double precision,
    ex_rights_reference_price double precision,
    ex_dividend_reference_price double precision,
    pre_ex_rights_stock_price double precision,
    pre_ex_dividend_stock_price double precision,
    pre_ex_rights_share_capital double precision,
    post_ex_rights_share_capital double precision,
    pre_ex_rights_market_value_ratio double precision,
    pre_ex_dividend_market_value_ratio double precision,
    cash_dividend_yield double precision,
    total_shareholders_stock_dividend_allotment_shares INT,
    total_shareholders_cash_dividend_amount INT,
    employee_compensation_stock_allotment_shares INT,
    employee_stock_allotment_amount INT,
    employee_bonus_stock_allotment_ratio_to_earnings_stock_dividend double precision,
    employee_cash_compensation INT,
    directors_and_supervisors_compensation INT,
    compensation_difference INT,
    eps_after_deducting_dividends_and_directors_compensation double precision,
    board_remarks text,
    shareholders_meeting_remarks text,
    dividend_distribution_date_approved_by_the_board_of_directors date,
    shareholders_meeting_date date,
    announcement_date date,
    ex_rights_announcement_date date,
    ex_dividend_announcement_date date,
    rights_offering_date_for_capital_increase date,
    type_of_capital_increase varchar(20),
    subscription_price_for_capital_increase double precision,
    stock_allotment_for_capital_increase_shares double precision,
    total_amount_for_capital_increase double precision,
    year_of_directors_and_supervisors_resignation_and_election INT,
    CONSTRAINT pk_dividend_policy PRIMARY KEY (year, code)
);
CREATE INDEX idx_dividend_policy_code ON tsdb.cmoney.dividend_policy(code);

comment on column tsdb.cmoney.dividend_policy.code is 'stock code';
comment on column tsdb.cmoney.dividend_policy.year is '年度';
comment on column tsdb.cmoney.dividend_policy.distribution_frequency is '配發次數';
comment on column tsdb.cmoney.dividend_policy.ex_rights_date is '除權日';
comment on column tsdb.cmoney.dividend_policy.ex_rights_last_compensation_date is '除權最後回補日';
comment on column tsdb.cmoney.dividend_policy.ex_dividend_date is '除息日';
comment on column tsdb.cmoney.dividend_policy.ex_dividend_last_compensation_date is '除息最後回補日';
comment on column tsdb.cmoney.dividend_policy.ex_rights_allotment_reference_date is '除權分派基準日';
comment on column tsdb.cmoney.dividend_policy.ex_dividend_allotment_reference_date is '除息分派基準日';
comment on column tsdb.cmoney.dividend_policy.share_receipt_date is '領股日期';
comment on column tsdb.cmoney.dividend_policy.dividend_receipt_date is '領息日期';
comment on column tsdb.cmoney.dividend_policy.earnings_stock_dividend is '盈餘配股(元)';
comment on column tsdb.cmoney.dividend_policy.surplus_stock_dividend is '公積配股(元)';
comment on column tsdb.cmoney.dividend_policy.total_stock_dividend is '股票股利合計(元)';
comment on column tsdb.cmoney.dividend_policy.earnings_cash_dividend is '盈餘配息(元)';
comment on column tsdb.cmoney.dividend_policy.surplus_cash_dividend is '公積配息(元)';
comment on column tsdb.cmoney.dividend_policy.total_cash_dividend is '現金股利合計(元)';
comment on column tsdb.cmoney.dividend_policy.total_dividend is '股利合計(元)';
comment on column tsdb.cmoney.dividend_policy.stock_dividend_payout_ratio is '股票股利發放率(%)';
comment on column tsdb.cmoney.dividend_policy.cash_dividend_payout_ratio is '現金股利發放率(%)';
comment on column tsdb.cmoney.dividend_policy.dividend_payout_ratio is '股利發放率(%)';
comment on column tsdb.cmoney.dividend_policy.ex_rights_opening_reference_price is '除權開盤競價基準';
comment on column tsdb.cmoney.dividend_policy.ex_dividend_opening_reference_price is '除息開盤競價基準';
comment on column tsdb.cmoney.dividend_policy.ex_rights_reference_price is '除權參考價';
comment on column tsdb.cmoney.dividend_policy.ex_dividend_reference_price is '除息參考價';
comment on column tsdb.cmoney.dividend_policy.pre_ex_rights_stock_price is '除權前股價';
comment on column tsdb.cmoney.dividend_policy.pre_ex_dividend_stock_price is '除息前股價';
comment on column tsdb.cmoney.dividend_policy.pre_ex_rights_share_capital is '除權前股本(百萬)';
comment on column tsdb.cmoney.dividend_policy.post_ex_rights_share_capital is '除權後股本(百萬)';
comment on column tsdb.cmoney.dividend_policy.pre_ex_rights_market_value_ratio is '除權前市值比重(%)';
comment on column tsdb.cmoney.dividend_policy.pre_ex_dividend_market_value_ratio is '除息前市值比重(%)';
comment on column tsdb.cmoney.dividend_policy.cash_dividend_yield is '現金股利殖利率(%)';
comment on column tsdb.cmoney.dividend_policy.total_shareholders_stock_dividend_allotment_shares is '股東股票股利總配股數(張)';
comment on column tsdb.cmoney.dividend_policy.total_shareholders_cash_dividend_amount is '股東現金紅利總金額(千)';
comment on column tsdb.cmoney.dividend_policy.employee_compensation_stock_allotment_shares is '員工酬勞配股(張)';
comment on column tsdb.cmoney.dividend_policy.employee_stock_allotment_amount is '員工配股金額(千)';
comment on column tsdb.cmoney.dividend_policy.employee_bonus_stock_allotment_ratio_to_earnings_stock_dividend is '員工紅利配股佔盈餘配股比例(%)';
comment on column tsdb.cmoney.dividend_policy.employee_cash_compensation is '員工酬勞現金(千)';
comment on column tsdb.cmoney.dividend_policy.directors_and_supervisors_compensation is '董監酬勞(千)';
comment on column tsdb.cmoney.dividend_policy.compensation_difference is '酬勞差異數(千)';
comment on column tsdb.cmoney.dividend_policy.eps_after_deducting_dividends_and_directors_compensation is '扣除紅利及董監酬勞後之EPS';
comment on column tsdb.cmoney.dividend_policy.board_remarks is '董事會備註';
comment on column tsdb.cmoney.dividend_policy.shareholders_meeting_remarks is '股東會備註';
comment on column tsdb.cmoney.dividend_policy.dividend_distribution_date_approved_by_the_board_of_directors is '董事會決議通過股利分派日';
comment on column tsdb.cmoney.dividend_policy.shareholders_meeting_date is '股東會日期';
comment on column tsdb.cmoney.dividend_policy.announcement_date is '公告日期';
comment on column tsdb.cmoney.dividend_policy.ex_rights_announcement_date is '除權公告日期';
comment on column tsdb.cmoney.dividend_policy.ex_dividend_announcement_date is '除息公告日期';
comment on column tsdb.cmoney.dividend_policy.rights_offering_date_for_capital_increase is '現增除權日';
comment on column tsdb.cmoney.dividend_policy.type_of_capital_increase is '現增類別';
comment on column tsdb.cmoney.dividend_policy.subscription_price_for_capital_increase is '現增認購價';
comment on column tsdb.cmoney.dividend_policy.stock_allotment_for_capital_increase_shares is '現增配股(股)';
comment on column tsdb.cmoney.dividend_policy.total_amount_for_capital_increase is '現增總額(百萬)';
comment on column tsdb.cmoney.dividend_policy.year_of_directors_and_supervisors_resignation_and_election is '董監改選年度';


-- select * from tsdb.cmoney.dividend_policy where code = '2330';

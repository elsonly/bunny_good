DROP TABLE IF EXISTS tsdb.cmoney.holidays;

CREATE TABLE
    tsdb.cmoney.holidays(
        code name NOT NULL,
        hdate date,
        name name,
        week smallint,
        is_dayoff smallint,
        country name,
        CONSTRAINT pk_holidays PRIMARY KEY (code, hdate)
    );

comment
    on column tsdb.cmoney.holidays.code is 'code';

comment on column tsdb.cmoney.holidays.hdate is '日期';

comment on column tsdb.cmoney.holidays.name is '假日名稱';

comment on column tsdb.cmoney.holidays.week is '星期';

comment on column tsdb.cmoney.holidays.is_dayoff is '是否放假';

comment on column tsdb.cmoney.holidays.country is '國家';
DROP TABLE IF EXISTS tsdb.cmoney.calendar;

CREATE TABLE
    tsdb.cmoney.calendar(
        exchange name NOT NULL,
        tdate date NOT NULL,
        dow smallint,
        holiday name,
        is_trading_date boolean NOT NULL,
        CONSTRAINT pk_calendar PRIMARY KEY (exchange, tdate)
    );
DROP TABLE IF EXISTS accountdb.dealer.cashflow;
CREATE TABLE accountdb.dealer.cashflow(
	tdate date,
    prev_balance bigint,
    cashflow bigint,
    balance bigint
);
CREATE INDEX idx_cashflow_date ON accountdb.dealer.cashflow(tdate);

INSERT INTO accountdb.dealer.cashflow(tdate, prev_balance, cashflow, balance) 
values('2023-05-03', 0, 50000000, 50000000);
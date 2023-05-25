DROP TABLE IF EXISTS accountdb.dealer.closed_pnl;
CREATE TABLE accountdb.dealer.closed_pnl(
	tdate date,
    strategy int,
    code varchar(10),
    qty int,
    buy_amt double precision,
    sell_amt double precision,
    pnl double precision,
    CONSTRAINT fk_strategy FOREIGN KEY(strategy) REFERENCES dealer.strategy(id)
);
CREATE INDEX idx_closed_pnl_date ON accountdb.dealer.closed_pnl(tdate);
CREATE INDEX idx_closed_pnl_date_strategy ON accountdb.dealer.closed_pnl(tdate, strategy);
CREATE INDEX idx_closed_pnl_date_code ON accountdb.dealer.closed_pnl(tdate, code);
DROP TABLE IF EXISTS accountdb.dealer.positions;
CREATE TABLE accountdb.dealer.positions(
	tdate date,
    strategy int,
    code varchar(10),
    action char(1),
    qty int,
    cost_amt double precision,
    avg_prc double precision,
    close double precision,
    pnl double precision,
    first_entry_date date,
    CONSTRAINT fk_strategy FOREIGN KEY(strategy) REFERENCES dealer.strategy(id)
);
CREATE INDEX idx_positions_date ON accountdb.dealer.positions(tdate);
CREATE INDEX idx_positions_date_strategy ON accountdb.dealer.positions(tdate, strategy);
CREATE INDEX idx_positions_date_code ON accountdb.dealer.positions(tdate, code);
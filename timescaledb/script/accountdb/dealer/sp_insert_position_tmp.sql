DROP PROCEDURE IF EXISTS dealer.sp_insert_position_tmp;
CREATE OR REPLACE PROCEDURE dealer.sp_insert_position_tmp(
        in_tdate date,
        in_strategy int,
        in_code varchar(10),
        in_qty int,
        in_close double precision,
        in_pnl_pct double precision,
        in_first_entry_date date
    ) LANGUAGE plpgsql AS $$ BEGIN
insert into dealer.positions(
        tdate,
        strategy,
        code,
        action,
        qty,
        cost_amt,
        avg_prc,
        close,
        pnl,
        first_entry_date,
        security_type
    )
values(
        in_tdate,
        in_strategy,
        in_code,
        'B',
        in_qty,
        in_close / (1 + in_pnl_pct / 100) * 1000 * in_qty,
        in_close / (1 + in_pnl_pct / 100),
        in_close,
        in_close / (1 + in_pnl_pct / 100) * 1000 * in_qty * in_pnl_pct / 100,
        in_first_entry_date,
        'S'
    );
END;
$$
DROP TABLE IF EXISTS cmoney.institute_invest;

CREATE TABLE
    cmoney.institute_invest(
        tdate date NOT NULL,
        inst_id INT NOT NULL,
        tse_buy double precision,
        tse_sell double precision,
        tse_net double precision,
        otc_buy double precision,
        otc_sell double precision,
        otc_net double precision,
        total_buy double precision,
        total_sell double precision,
        total_net double precision,
        otc_stock_buy double precision,
        otc_stock_sell double precision,
        otc_stock_net double precision,
        oes_buy double precision,
        oes_sell double precision,
        oes_net double precision,
        CONSTRAINT fk_inst FOREIGN KEY(inst_id) REFERENCES cmoney.institute_info(id)
    );

CREATE INDEX
    idx_institute_invest_tdate ON cmoney.institute_invest(tdate);

CREATE INDEX
    idx_institute_invest_tdate_inst_id ON cmoney.institute_invest(tdate, inst_id);

comment on column cmoney.institute_invest.tdate is 'trading date';

comment on column cmoney.institute_invest.inst_id is 'institue id';

comment
    on column cmoney.institute_invest.tse_buy is 'tse buy amount (M NTD)';

comment
    on column cmoney.institute_invest.tse_sell is 'tse sell amount (M NTD)';

comment
    on column cmoney.institute_invest.tse_net is 'tse net amount (M NTD)';

comment
    on column cmoney.institute_invest.otc_buy is 'otc buy amount (M NTD)';

comment
    on column cmoney.institute_invest.otc_sell is 'otc sell amount (M NTD)';

comment
    on column cmoney.institute_invest.otc_net is 'otc net amount (M NTD)';

comment
    on column cmoney.institute_invest.total_buy is 'total(tse, otc) buy amount (M NTD)';

comment
    on column cmoney.institute_invest.total_sell is 'total(tse, otc) sell amount (M NTD)';

comment
    on column cmoney.institute_invest.total_net is 'total(tse, otc) net amount (M NTD)';

comment
    on column cmoney.institute_invest.otc_stock_buy is 'otc buy amount (M NTD), stock only';

comment
    on column cmoney.institute_invest.otc_stock_sell is 'otc sell amount (M NTD), stock only';

comment
    on column cmoney.institute_invest.otc_stock_net is 'otc net amount (M NTD), stock only';

comment
    on column cmoney.institute_invest.oes_buy is 'oes buy amount (M NTD)';

comment
    on column cmoney.institute_invest.oes_sell is 'oes sell amount (M NTD)';

comment
    on column cmoney.institute_invest.oes_net is 'oes net amount (M NTD)';

-- select * from ft_get_table_description('institute_invest');

-- select * from cmoney.institute_invest order by tdate desc limit 10;
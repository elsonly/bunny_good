DROP TABLE IF EXISTS tsdb.sino.kbars;
CREATE TABLE tsdb.sino.kbars(
    dt timestamp not null,
    code name not null,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    vol double precision,
    amt double precision
);
SELECT create_hypertable(
        'tsdb.sino.kbars',
        'dt',
        partitioning_column => 'code',
        number_partitions => 1,
        chunk_time_interval => INTERVAL '30 day'
    );
ALTER TABLE tsdb.sino.kbars
SET (
        timescaledb.compress,
        timescaledb.compress_segmentby = 'code'
    );
SELECT add_compression_policy('tsdb.sino.kbars', INTERVAL '7 days');

-- select * from tsdb.sino.kbars;
-- truncate table tsdb.sino.kbars;
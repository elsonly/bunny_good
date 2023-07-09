select 
    decompress_chunk(concat(chunk_schema, '.', chunk_name))
from chunk_compression_stats('cmoney.daily_price') 
where compression_status='Compressed';

ALTER TABLE tsdb.cmoney.daily_price
SET (
        timescaledb.compress=false
    );


ALTER TABLE tsdb.cmoney.daily_price
ALTER COLUMN shares type double precision;
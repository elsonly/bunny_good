-- CREATE EXTENSION postgres_fdw;
-- CREATE SERVER tsdb_server
-- FOREIGN DATA WRAPPER postgres_fdw
-- OPTIONS (host '127.0.0.1', dbname 'tsdb', port '5432');

-- CREATE USER MAPPING FOR CURRENT_USER SERVER tsdb_server
-- OPTIONS (user 'postgres', password 'password');


-- create SCHEMA sino;
-- create SCHEMA cmoney;
-- IMPORT FOREIGN SCHEMA sino FROM SERVER tsdb_server INTO sino;
-- IMPORT FOREIGN SCHEMA cmoney FROM SERVER tsdb_server INTO cmoney;

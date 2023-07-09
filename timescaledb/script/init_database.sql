-- CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
-- metabase
CREATE DATABASE metabase;
CREATE USER metabase with encrypted password 'bunnygood';
grant all PRIVILEGES on database metabase to metabase;
-- accountdb
CREATE DATABASE accountdb;
CREATE USER chiubj with encrypted password 'bunnygood';
grant all PRIVILEGES on database accountdb to chiubj;
CREATE SCHEMA dealer;
-- airflow
CREATE DATABASE airflow;
CREATE USER airflow with encrypted password 'airflow';
grant all PRIVILEGES on database airflow to airflow;
-- tsdb
CREATE SCHEMA cmoney;
CREATE SCHEMA sino;
CREATE SCHEMA twse;
#!/bin/sh

psql -w -tc "SELECT 1 FROM pg_database WHERE datname = 'bybit'" | grep -q 1 || psql -w -c "CREATE DATABASE bybit"
psql -w -tc "SELECT 1 FROM pg_roles WHERE rolname = 'u_bybit'" | grep -q 1 || psql -w -c "CREATE USER u_bybit PASSWORD 'DummyPassword'"
psql -w -tc "ALTER DATABASE bybit OWNER TO u_bybit"
psql -w -tc "GRANT ALL ON SCHEMA public TO u_bybit"
psql -w -tc "GRANT ALL PRIVILEGES ON DATABASE bybit TO u_bybit"


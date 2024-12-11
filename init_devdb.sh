#!/bin/sh

# DEVEL DB
psql -w -tc "SELECT 1 FROM pg_database WHERE datname = 'dbybit'" | grep -q 1 || psql -w -c "CREATE DATABASE dbybit"
psql -w -tc "SELECT 1 FROM pg_roles WHERE rolname = 'du_bybit'" | grep -q 1 || psql -w -c "CREATE USER du_bybit PASSWORD 'DummyPassword'"
psql -w -tc "GRANT ALL PRIVILEGES ON DATABASE dbybit TO du_bybit"

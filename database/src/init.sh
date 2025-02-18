#!/usr/bin/env bash

MY_SQL_FILES="$(ls ./sql)"
SQL_CODE=""

for f in $MY_SQL_FILES; do
    SQL_CODE+="$(cat ./sql/$f)"
done

echo "$SQL_CODE" > ./sql/output.sql

psql -h localhost -U julien_guitard -d ai_chats -f ./sql/output.sql

rm ./sql/output.sql

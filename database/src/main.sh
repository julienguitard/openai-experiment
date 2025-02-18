#!/usr/bin/env bash

echo "sql -h localhost -U julien_guitard -d postgres -f ./sql/99_vacuum.sql" > ./vacuum.sh
* 3 * * * ./vacuum.sh &
rm ./vacuum.sh
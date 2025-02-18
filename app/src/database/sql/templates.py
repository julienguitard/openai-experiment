import os
from common.constants import  SQL_PATH
from common.collections import lfilter

sql_templates_ = {
    "list_tables": """SELECT tablename from  pg_catalog.pg_tables""",
    "create": """CREATE TABLE {table_name} ({variables_with_format});""",
    "create_from_select": """CREATE TABLE {table_name} AS {select};""",
    "insert": """ INSERT INTO {table_name} ({select});""",
    "drop": "DROP TABLE IF EXISTS  {table_name};",
    "overwrite": "DROP TABLE IF EXISTS  {table_name}; {create}",
    "delete": """DELETE from  {table_name} {where}""",
    "variable_with_format": """{variable} {format}""",
    "select": """SELECT {distinct} {selects} from  {table_name} {joins} {where} {groupby} {sortby} {limit}""",
    "where": """WHERE {wheres}""",
    "groupby": """GROUP BY {groupbys}""",
    "sortby": """SORT BY {sortbys}""",
    "limit": """LIMIT {n}""",
    "cast": """CAST({castable} AS {format})""",
}


def complete_templates(templates_: dict) -> dict:
    path = SQL_PATH
    f = [
        fi
        for fi in lfilter(lambda x: "." in x, os.listdir(path))
        if fi.split(".")[1] == "sql"
    ]
    new_templates_ = dict(templates_.items())
    for fi in f:
        new_templates_[fi.split(".")[0]] = open("{}{}".format(path, fi)).read()

    return new_templates_


sql_templates = complete_templates(sql_templates_)

from typing import Set, Tuple

import psycopg2

db_table_map = {
    "debit_card_specializing": [
        "customers",
        "gasstations",
        "products",
        "transactions_1k",
        "yearmonth",
    ],
    "student_club": [
        "major",
        "member",
        "attendance",
        "budget",
        "event",
        "expense",
        "income",
        "zip_code",
    ],
    "thrombosis_prediction": ["Patient", "Examination", "Laboratory"],
    "european_football_2": [
        "League",
        "Match",
        "Player",
        "Player_Attributes",
        "Team",
        "Team_Attributes",
    ],
    "formula_1": [
        "circuits",
        "seasons",
        "races",
        "constructors",
        "constructorResults",
        "constructorStandings",
        "drivers",
        "driverStandings",
        "lapTimes",
        "pitStops",
        "qualifying",
        "status",
        "results",
    ],
    "superhero": [
        "alignment",
        "attribute",
        "colour",
        "gender",
        "publisher",
        "race",
        "superpower",
        "superhero",
        "hero_attribute",
        "hero_power",
    ],
    "codebase_community": [
        "posts",
        "users",
        "badges",
        "comments",
        "postHistory",
        "postLinks",
        "tags",
        "votes",
    ],
    "card_games": [
        "cards",
        "foreign_data",
        "legalities",
        "rulings",
        "set_translations",
        "sets",
    ],
    "toxicology": ["molecule", "atom", "bond", "connected"],
    "california_schools": ["satscores", "frpm", "schools"],
    "financial": [
        "district",
        "account",
        "client",
        "disp",
        "card",
        "loan",
        "order",
        "trans",
    ],
}


def nice_look_table(column_names: list, values: list) -> str:
    """
    Returns a string representing a nicely formatted table of rows.
    Each element in 'values' corresponds to a row, while 'column_names'
    are the headers for each column.
    """
    # Determine the maximum width of each column
    widths = [
        max(len(str(value[i])) for value in values + [column_names])
        for i in range(len(column_names))
    ]

    # Construct the header
    header = "".join(
        f"{column.rjust(width)} " for column, width in zip(column_names, widths)
    )

    # Construct each row
    rows_str_list = []
    for value in values:
        row = "".join(f"{str(v).rjust(width)} " for v, width in zip(value, widths))
        rows_str_list.append(row)

    rows_str = "\n".join(rows_str_list)
    final_output = header + "\n" + rows_str
    return final_output


def format_postgresql_create_table(table_name: str, columns_info: list) -> str:
    """
    Given a table name and a list of columns_info,
    returns a valid PostgreSQL CREATE TABLE statement.

    columns_info should be a list of tuples/lists in the form:
      (column_name, data_type, is_nullable)
    For example: ("customerid", "bigint", "YES")
    """
    lines = [f"CREATE TABLE {table_name}\n("]
    for i, (column_name, data_type, is_nullable) in enumerate(columns_info):
        null_status = "NULL" if is_nullable.upper() == "YES" else "NOT NULL"
        postgres_data_type = data_type.upper()
        column_line = f"    `{column_name}` {postgres_data_type} {null_status}"
        if i < len(columns_info) - 1:
            column_line += ","
        lines.append(column_line)

    lines.append(");")
    return "\n".join(lines)


def execute_query_and_get_rows(sql_query: str, cursor) -> Set[Tuple]:
    """
    Execute a SQL query and return the result as a set of tuples
    for row-level comparison.
    """
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Convert rows to a set of tuples
        row_set = {tuple(row) for row in rows}
    except Exception as err:
        print(f"Failed to execute query: {sql_query}")
        return set()

    return row_set

def connect_postgresql():
    """
    Establishes a connection to a PostgreSQL database using hardcoded credentials.
    Returns a psycopg2 connection object.

    Adjust credentials as needed:
      dbname, user, host, password, port.
    """
    db = psycopg2.connect(
        dbname="BIRD",
        user="postgres",
        host="localhost",
        password="postgres",
        port="5432"
    )
    return db

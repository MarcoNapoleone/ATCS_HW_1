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


def nice_look_table(column_names: list, values: list):
    rows = []
    # Determine the maximum width of each column
    widths = [
        max(len(str(value[i])) for value in values + [column_names])
        for i in range(len(column_names))
    ]

    # Print the column names
    header = "".join(
        f"{column.rjust(width)} " for column, width in zip(column_names, widths)
    )
    # print(header)
    # Print the values
    for value in values:
        row = "".join(f"{str(v).rjust(width)} " for v, width in zip(value, widths))
        rows.append(row)
    rows = "\n".join(rows)
    final_output = header + "\n" + rows
    return final_output


def format_postgresql_create_table(table_name, columns_info):
    lines = [f"CREATE TABLE {table_name}\n("]
    for i, (column_name, data_type, is_nullable) in enumerate(columns_info):
        null_status = "NULL" if is_nullable == "YES" else "NOT NULL"
        postgres_data_type = data_type.upper()
        column_line = f"    `{column_name}` {postgres_data_type} {null_status}"
        if i < len(columns_info) - 1:
            column_line += ","
        lines.append(column_line)

    lines.append(");")
    return "\n".join(lines)


def connect_postgresql():
    # Open database connection
    # Connect to the database
    db = psycopg2.connect(
        "dbname=BIRD user=postgres host=localhost password=postgres port=5432"
    )
    return db


def generate_schema_prompt_postgresql(db_path):
    db = connect_postgresql()
    cursor = db.cursor()
    db_name = db_path.split("/")[-1].split(".sqlite")[0]
    tables = [table for table in db_table_map[db_name]]
    schemas = {}
    for table in tables:
        cursor.execute(
            f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table}';
            """
        )
        raw_schema = cursor.fetchall()
        pretty_schema = format_postgresql_create_table(table, raw_schema)
        schemas[table] = pretty_schema
    schema_prompt = "\n\n".join(schemas.values())
    db.close()
    return schema_prompt


def generate_schema_prompt(db_path=None):
    return generate_schema_prompt_postgresql(db_path)

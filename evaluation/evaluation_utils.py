import re

# Dizionario dei nomi delle tabelle disponibili per ogni db_id
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
    "thrombosis_prediction": ["patient", "examination", "laboratory"],
    "european_football_2": [
        "league",
        "match",
        "player",
        "player_attributes",
        "team",
        "team_attributes",
    ],
    "formula_1": [
        "circuits",
        "seasons",
        "races",
        "constructors",
        "constructorresults",
        "constructorstandings",
        "drivers",
        "driverstandings",
        "laptimes",
        "pitstops",
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
        "posthistory",
        "postlinks",
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

def extract_tables_from_query(query: str):
    """
    Estrae (in modo semplificato) i nomi delle tabelle da una query SQL.
    Cerca pattern tipici come FROM <table> e JOIN <table>.
    Restituisce un set con i nomi delle tabelle trovate (in minuscolo).
    """
    if not query:
        return set()

    query_lower = query.lower()

    # Regex semplice per catturare pattern (FROM|JOIN) <nome_tabella>
    pattern = r'(?:from|join)\s+([a-zA-Z0-9_."]+)'
    matches = re.findall(pattern, query_lower)

    # Ripuliamo eventuali doppi apici o spazi
    tables_found = set(m.replace('"', '').strip() for m in matches)

    return tables_found


def filter_valid_tables(tables_found, db_id):
    """
    Interseca le tabelle trovate con quelle realmente disponibili per db_id,
    secondo il dizionario db_table_map.
    """
    valid_tables = set(db_table_map.get(db_id, []))  # tabelle disponibili per questo db
    # Intersechiamo tabelle estratte con quelle note/valide
    return tables_found.intersection(valid_tables)


def precision_recall_f1(true_set, pred_set):
    """
    Calcola precision, recall e F1 score dati due set di "elementi".
    In questo caso, gli "elementi" saranno i nomi delle tabelle utilizzate.
    """
    tp = len(true_set.intersection(pred_set))
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall    = tp / (tp + fn) if (tp + fn) else 0.0

    if (precision + recall) > 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    else:
        f1 = 0.0

    return precision, recall, f1

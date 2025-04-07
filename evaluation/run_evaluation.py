import decimal
import json
from datetime import date, datetime, timedelta
from decimal import Decimal

from evaluation.evaluation_utils import precision_recall_f1
from pgdb.pg_utils import execute_query_and_get_rows, connect_postgresql
import psycopg2
from sql_metadata import Parser


def evaluate_item(item):
    """Evaluate a single item using table and row-level metrics."""
    db_id = item["db_id"]
    db = connect_postgresql()
    cursor = db.cursor()
    valid_query = True

    try:
        # Set schema to match DB ID (schema name)
        cursor.execute(f"SET search_path TO {db_id}, public;")
    except psycopg2.Error as e:
        print(f"Error setting schema for {db_id}: {e}")
        return None

    true_sql = item["true_sql"]
    predicted_sql = item["text_2_sql"]

    # ---- Table-level evaluation ----
    gt_tables = Parser(true_sql).tables
    pred_tables = Parser(predicted_sql).tables
    p_tab, r_tab, f_tab = precision_recall_f1(gt_tables, pred_tables)

    # ---- Row-level evaluation (by executing queries) ----

    rowset_gt = execute_query_and_get_rows(true_sql, cursor)
    rowset_pred = execute_query_and_get_rows(predicted_sql, cursor)

    if not rowset_pred:
        valid_query = False


    p_row, r_row, f_row = precision_recall_f1(rowset_gt, rowset_pred)

    # close connection
    cursor.close()

    # Return the evaluation results

    return {
        "question_id": item["question_id"],
        "difficulty": item["difficulty"],
        "db_id": db_id,
        "valid_query": valid_query,
        "tables": {
            "groundtruth": list(gt_tables),
            "predicted": list(pred_tables),
            "precision": p_tab,
            "recall": r_tab,
            "f1": f_tab
        },
        "rows": {
            "groundtruth": list(rowset_gt),
            "predicted": list(rowset_pred),
            "precision": p_row,
            "recall": r_row,
            "f1": f_row
        }
    }

def avg(lst):
    return sum(lst) / len(lst) if lst else 0.0

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, (date, datetime)):
            return o.isoformat()
        elif isinstance(o, set):
            return list(o)
        elif isinstance(o, timedelta):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def evaluate_llm_outputs(json_path: str, output_log_path: str):
    """
    Main evaluation routine:
    - Loads the input JSON
    - Connects to PostgreSQL
    - Evaluates table and row-level metrics
    - Logs and prints results
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Flatten if wrapped in an extra list
    if isinstance(data, list) and len(data) == 1 and isinstance(data[0], list):
        data = data[0]

    table_precision_list = []
    table_recall_list = []
    table_f1_list = []

    row_precision_list = []
    row_recall_list = []
    row_f1_list = []

    evaluation_log = []

    # dropping all not valid queries
    original_len = len(data)
    data = [item for item in data if item["is_valid"]]
    print(f"Evaluating {json_path} of length {original_len}...")
    print(f"Number of valid queries: {len(data)}")
    print(f"Number of invalid queries: {original_len - len(data)}")

    for item in data:

        result = evaluate_item(item)
        if result is None:
            continue

        evaluation_log.append(result)

        table_precision_list.append(result["tables"]["precision"])
        table_recall_list.append(result["tables"]["recall"])
        table_f1_list.append(result["tables"]["f1"])

        row_precision_list.append(result["rows"]["precision"])
        row_recall_list.append(result["rows"]["recall"])
        row_f1_list.append(result["rows"]["f1"])

    print("=== Table Usage Evaluation ===")
    print(f"Precision: {avg(table_precision_list):.4f}")
    print(f"Recall:    {avg(table_recall_list):.4f}")
    print(f"F1:        {avg(table_f1_list):.4f}\n")

    print("=== Row-Level Evaluation ===")
    print(f"Precision: {avg(row_precision_list):.4f}")
    print(f"Recall:    {avg(row_recall_list):.4f}")
    print(f"F1:        {avg(row_f1_list):.4f}")

    with open(output_log_path, "w", encoding="utf-8") as fout:
        json.dump(evaluation_log, fout, ensure_ascii=False, indent=2, cls=DecimalEncoder)
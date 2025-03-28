#!/usr/bin/env python3
import argparse
import json

from evaluation_utils import (
    extract_tables_from_query,
    filter_valid_tables,
    precision_recall_f1
)

def main():
    parser = argparse.ArgumentParser(description='Esegue la valutazione delle query SQL previste.')
    parser.add_argument('--predicted_sql_path', type=str, required=True,
                        help='Percorso al file JSON di output del LLM.')
    parser.add_argument('--sql_dialect', type=str, default='PostgreSQL',
                        help='Dialetto SQL usato (non usato in questa demo, ma per coerenza con lo script).')

    args = parser.parse_args()

    with open(args.predicted_sql_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Liste per metriche su TABELLE
    table_precision_list = []
    table_recall_list = []
    table_f1_list = []

    # Se data è un singolo dict o una lista di dict
    if isinstance(data, dict):
        data = [data]

    # Cicliamo su ogni "riga" (domanda) del JSON
    for item in data:
        # Recuperiamo dal JSON la ground truth, la predizione e il db_id
        db_id        = item.get("db_id", "")
        true_sql     = item.get("true_sql", "")     # ground truth
        predicted_sql= item.get("text_2_sql", "")   # la query generata dal modello

        # 1) Estraiamo le tabelle dalla groundtruth e dalla predizione
        gt_tables_found   = extract_tables_from_query(true_sql)
        pred_tables_found = extract_tables_from_query(predicted_sql)

        # 2) Filtriamo le tabelle con quelle effettivamente esistenti per quel db (db_table_map)
        gt_tables_filtered   = filter_valid_tables(gt_tables_found, db_id)
        pred_tables_filtered = filter_valid_tables(pred_tables_found, db_id)

        # 3) Calcolo di precision, recall e f1
        p_tab, r_tab, f_tab = precision_recall_f1(gt_tables_filtered, pred_tables_filtered)
        table_precision_list.append(p_tab)
        table_recall_list.append(r_tab)
        table_f1_list.append(f_tab)

    # Calcolo delle medie finali sulle tabelle
    if len(table_precision_list) > 0:
        avg_p_tab = sum(table_precision_list) / len(table_precision_list)
        avg_r_tab = sum(table_recall_list) / len(table_recall_list)
        avg_f_tab = sum(table_f1_list) / len(table_f1_list)
    else:
        avg_p_tab, avg_r_tab, avg_f_tab = 0.0, 0.0, 0.0

    # Stampa risultati
    print("=== RISULTATI SULLE TABELLE (USAGE) ===")
    print(f"Precision: {avg_p_tab:.4f}")
    print(f"Recall:    {avg_r_tab:.4f}")
    print(f"F1 Score:  {avg_f_tab:.4f}")

if __name__ == "__main__":
    main()

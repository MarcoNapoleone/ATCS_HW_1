import json
import spacy
import logging
from pathlib import Path
from rapidfuzz import fuzz  # pip install rapidfuzz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# We'll assume you already have an enriched dataset with informative_tokens
# Example: 'informative_tokens': { 'popularity': 0.2725, '1945': 0.3655, ... }

# 1. Load the existing enriched dataset & schema
logging.info("Loading enriched dataset...")
data_path = Path("../data/train_enriched.json")  # your enriched dataset
schema_path = Path("../data/train_tables.json")  # your schema

with open(data_path) as f:
    dataset = json.load(f)

logging.info("Loading table schema...")
with open(schema_path) as f:
    table_list = json.load(f)

table_data = {table["db_id"]: table for table in table_list}

# 2. Preprocessing function for column names

def preprocess_column_name(col_name: str):
    """
    Lowercase, replace punctuation with underscores, etc.
    Return as a list of subwords for fuzzy matching.
    """
    return col_name.lower().replace(",", "").replace(".", "").replace("-", "_").split("_")


# 3. Fuzzy matching function

def best_column_for_token(token: str, possible_columns: list, threshold=60):
    """Return the best matching column (and score) for a single token, or None if below threshold."""
    best_score = 0
    best_col = None
    token_lower = token.lower()

    for col in possible_columns:
        subwords = preprocess_column_name(col)
        for sub in subwords:
            score = fuzz.partial_ratio(token_lower, sub)
            if score > best_score:
                best_score = score
                best_col = col

    if best_score >= threshold:
        return best_col, best_score
    return None, best_score

# 4. Enrich dataset with token→column mappings (for informative tokens only)
enriched_mappings = []
logging.info("Matching only informative tokens to columns...")

for idx, item in enumerate(dataset):
    db_id = item.get("db_id")
    if not db_id or db_id not in table_data:
        # No schema info
        enriched_mappings.append(item)
        continue

    # Get columns for this DB
    raw_cols = table_data[db_id]["column_names"]
    columns = [col[1] for col in raw_cols if col[1]]

    # We'll only match the keys from informative_tokens
    # Example: 'informative_tokens': { 'popularity': 0.27, 'year': 0.25, ... }
    info_tokens = item.get("informative_tokens", {})  # dict

    token_column_map = []
    for tok in info_tokens.keys():
        best_col, score = best_column_for_token(tok, columns, threshold=60)
        if best_col:
            token_column_map.append({
                "token": tok,
                "column": best_col,
                "score": score
            })

    # Store results
    new_item = dict(item)
    new_item["info_token_column_map"] = token_column_map
    enriched_mappings.append(new_item)

    if idx % 100 == 0:
        logging.info(f"Processed {idx}/{len(dataset)} items...")

# 5. Save output
out_path = Path("../data/train_enriched_mapping.json")
logging.info(f"Saving final results to {out_path}")
with out_path.open("w") as f:
    json.dump(enriched_mappings, f, indent=2)

logging.info("Done! The dataset now has 'info_token_column_map' for each question.")

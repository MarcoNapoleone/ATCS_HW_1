import json
import spacy
from nltk.tokenize import word_tokenize
from pathlib import Path
import logging
from sql_metadata import Parser
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load spaCy model
logging.info("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")

# --- Load Data ---
data_path = Path("data/train.json")
schema_path = Path("data/train_tables.json")

with open(data_path) as f:
    dataset = json.load(f)

with open(schema_path) as f:
    table_list = json.load(f)

# Convert schema list to dict by db_id
table_data = {table["db_id"]: table for table in table_list}

# --- Compute TF-IDF for All Questions ---
logging.info("Computing TF-IDF scores for all questions...")
questions = [item["question"] for item in dataset]
vectorizer = TfidfVectorizer(stop_words="english", lowercase=True)
tfidf_matrix = vectorizer.fit_transform(questions)
feature_names = np.array(vectorizer.get_feature_names_out())

# --- Enrich Dataset ---
enriched = []
logging.info("Enriching dataset with token tagging and SQL metadata parsing...")

for idx, item in enumerate(dataset):
    question = item["question"]
    db_id = item["db_id"]
    sql = item.get("SQL", "")

    # spaCy doc for full token info
    doc = nlp(question)
    tokens_info = [(token.text, token.lemma_, token.pos_, token.ent_type_) for token in doc]

    # Extract TF-IDF terms and scores for this question
    row = tfidf_matrix[idx].toarray().flatten()
    top_indices = row.argsort()[::-1][:10]  # Top 10 tokens
    informative_tokens = {feature_names[i]: float(row[i]) for i in top_indices if row[i] > 0}

    # Extract table and column names using sql-metadata
    try:
        parser = Parser(sql)
        sql_tables = parser.tables
        sql_columns = parser.columns
    except Exception:
        sql_tables = []
        sql_columns = []

    enriched.append({
        **item,
        "tokens": tokens_info,
        "informative_tokens": informative_tokens,
        "sql_tables": sql_tables,
        "sql_columns": sql_columns,
    })

    if idx % 100 == 0:
        logging.info(f"Processed {idx}/{len(dataset)} questions...")

# --- Save Enriched File ---
logging.info("Saving enriched dataset to file...")
with open("data/enriched_dataset.json", "w") as f:
    json.dump(enriched, f, indent=2)

logging.info("Done! Enriched dataset saved as enriched_dataset.json")
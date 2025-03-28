#!/usr/bin/env bash
set -e  # Exit if any command fails

# Default parameters; you can override with environment variables or arguments
INPUT_FILE="data/sample_input.json"
OUTPUT_FILE="data/output_response.json"

# available models:
# meta.llama3-70b-instruct-v1:0
# amazon.titan-tg1-large

MODEL_ID="meta.llama3-70b-instruct-v1:0"

echo "[RUN] Calling LLM..."
python llm/run_llm_exp.py \
 --input_file "$INPUT_FILE" \
  --output_file "$OUTPUT_FILE" \
  --model_id "$MODEL_ID"

echo "[RUN] Cleaning up the output..."
python llm/clean_output.py \
  --input_file "$OUTPUT_FILE" \
  --output_file "$OUTPUT_FILE" \
  --model_id "$MODEL_ID"

echo "[RUN] Validating LLM output with run_evaluation.py ..."
# Example usage (you can adjust parameters):
python evaluation/run_evaluation.py \
  --predicted_sql_path "$OUTPUT_FILE" \
  --sql_dialect "PostgreSQL" \

echo "[RUN] All done!"

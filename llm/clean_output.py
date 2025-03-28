#!/usr/bin/env python3
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Clean LLM JSON output by removing newlines and excess whitespace.")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input JSON file.")
    parser.add_argument("--output_file", type=str, required=True, help="Path to the output JSON file.")
    parser.add_argument("--model_id", type=str, default=None, help="Optional: model identifier.")
    args = parser.parse_args()

    # Fields in each JSON object to clean up
    fields_to_clean = ["true_sql", "text_2_sql", "prompt"]

    with open(args.input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Make sure `data` is a list of items
    if isinstance(data, dict):
        data = [data]

    for item in data:
        # 1. Clean top-level fields (replace all whitespace sequences with a single space)
        for field in fields_to_clean:
            if field in item and item[field]:
                item[field] = " ".join(item[field].split())

        # 2. Optionally clean nested fields, e.g. "response_metadata.generation"
        if "response_metadata" in item and "generation" in item["response_metadata"]:
            gen_text = item["response_metadata"]["generation"]
            if gen_text:
                item["response_metadata"]["generation"] = " ".join(gen_text.split())

    # Write the cleaned data
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

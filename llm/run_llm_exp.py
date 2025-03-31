# run_llm_exp.py

import os
import json
import argparse

from llm.llm_request import call_llm_model
from llm.prompt import generate_combined_prompts


def run_llm_process(input_file: str, output_file: str, model_id: str):
    # 1. Read input data (JSON list of questions)
    with open(input_file, "r", encoding="utf-8") as f:
        questions = json.load(f)

    all_responses = []

    # 2. Process each question in the input
    for question in questions:
        # Create a combined prompt for schema alignment.
        # We can embed db_id, question text, and any evidence or knowledge
        prompt = generate_combined_prompts(
            db_path=question["db_id"],
            question=question["question"],
            sql_dialect='PostgreSQL',
            knowledge=question.get("knowledge")
        )

        # 3. Call the LLM model
        txt2sql = call_llm_model({
            "prompt": prompt,
            "temperature": 0.1,
            "max_tokens": 1024,
            "top_k": 2,
            "top_p": 0.9,
        }, model_id=model_id)

        # Collect the result. You can also store the original question, db_id, etc.
        all_responses.append({
            "question_id": question["question_id"],
            "db_id": question["db_id"],
            "question": question["question"],
            "true_sql": question["SQL"],
            "text_2_sql": txt2sql,
            "prompt": prompt,
            "difficulty": question["difficulty"]
        })

        print(f"[LLM] Processed question_id={question['question_id']}, progress={len(all_responses)}/{len(questions)}")

    # 4. Write all responses to a single JSON file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_responses, f, ensure_ascii=False, indent=2)

    print(f"[LLM] All responses saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run LLM call and save response for schema alignment.")
    parser.add_argument(
        "--input_file",
        type=str,
        default="data/sample_input.json",
        help="Path to the JSON input data."
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="data/output_response.json",
        help="Path to save the LLM response."
    )
    parser.add_argument(
        "--model_id",
        type=str,
        default="your-bedrock-model-id",
        help="Bedrock model ID or ARN."
    )
    args = parser.parse_args()

    run_llm_process(args.input_file, args.output_file, args.model_id)

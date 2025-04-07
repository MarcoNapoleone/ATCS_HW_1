#!/usr/bin/env python3
from llm.run_llm_exp import run_llm_process
from llm.clean_output import clean_llm_output
from evaluation.run_evaluation import evaluate_llm_outputs


def main():

    # Parameters
    input_file = "data/dev_enriched.json"

    raw_output_file = f"results/{input_file.split('/')[-1].replace('.json', '_raw.json')}"
    cleaned_output_file = f"results/{input_file.split('/')[-1].replace('.json', '_cleaned.json')}"
    output_log_path = f"results/{input_file.split('/')[-1].replace('.json', '_log.json')}"

    # AWS bedrock model_id
    model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    print("[RUN] Calling LLM...")
    run_llm_process(input_file=input_file, output_file=raw_output_file, model_id=model_id)

    print("[RUN] Cleaning LLM output...")
    clean_llm_output(input_file=raw_output_file, output_file=cleaned_output_file, model_id=model_id)

    print("[RUN] Evaluating LLM output...")
    evaluate_llm_outputs(json_path=cleaned_output_file, output_log_path=output_log_path)

    print("[RUN] All done!")


if __name__ == "__main__":
    main()

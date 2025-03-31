import json
import re

def clean_sql_for_execution(sql: str) -> str:
    """
    Clean LLM-generated SQL to remove markdown, trailing junk, and incomplete clauses.
    """

    # remove the /* */ comments
    q = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql)

    # remove whole line -- and # comments
    lines = [line for line in q.splitlines() if not re.match("^\s*(--|#)", line)]

    # remove trailing -- and # comments
    q = " ".join([re.split("--|#", line)[0] for line in lines])

    return q



def clean_llm_output(input_file: str, output_file: str, model_id: str = None):
    fields_to_clean = ["true_sql", "text_2_sql", "prompt"]

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = [data]

    for item in data:
        for field in fields_to_clean:
            if field in item and item[field]:
                item[field] = " ".join(item[field].split())

        # Clean predicted SQL
        if "text_2_sql" in item:
            item["text_2_sql"] = clean_sql_for_execution(item["text_2_sql"])

        # Clean generation inside response_metadata
        if "response_metadata" in item and "generation" in item["response_metadata"]:
            gen_text = item["response_metadata"]["generation"]
            if gen_text:
                item["response_metadata"]["generation"] = " ".join(gen_text.split())

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[CLEAN] Cleaned output saved to {output_file}")

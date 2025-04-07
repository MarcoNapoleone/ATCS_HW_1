# Schema Alignment with Large Language Models on the BIRD Benchmark

This repository contains the code and experiments for the project titled:

> Schema Alignment with Large Language Models on the BIRD Benchmark:  
> A Hybrid LLM and Semantic Matching Approach for Table and Row-Level Text-to-SQL Evaluation

## 📄 Overview

This project investigates schema alignment for natural language to SQL translation using Large Language Models (LLMs). The task is evaluated on the BIRD benchmark and consists of identifying relevant source tables (STs) and, optionally, source attributes (SAs) for domain-diverse databases.

We explore two approaches:

1. A pure LLM-based pipeline using dynamic text-to-SQL prompting and table extraction.
2. A hybrid approach that augments LLMs with SpaCy-based token annotation and TF-IDF-based semantic filtering.

## 🔍 Motivation

Schema alignment remains a core challenge in natural language interfaces to databases due to ambiguous query language and inconsistent schema terminology. LLMs offer strong semantic reasoning capabilities, but require structural and contextual support to be effective in complex, domain-specific settings.

## 🧪 Results

| Evaluation Type     | Precision | Recall | F1-score |
|---------------------|-----------|--------|----------|
| Table Usage         | 0.9125    | 0.9382 | 0.9126   |
| Row-Level Execution | 0.3162    | 0.3143 | 0.3078   |

🔧 Queries were executed on PostgreSQL.

## 🛠️ Technologies

- BIRD Benchmark dataset (dev split)
- Python 3.x
- SpaCy (for token annotation)
- Scikit-learn (TF-IDF vectorizer)
- Amazon Bedrock (API access to LLMs)
- PostgreSQL (for query execution)
- Claude 3.5 Sonnet, LLaMA 3 70B, Amazon Titan (LLMs)


## 🚀 Reproducibility

1. Clone the repo:
   ```bash
   git clone https://github.com/MarcoNapoleone/ATCS_HW_1.git
   cd ATCS_HW_1
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download BIRD (dev set):
   Follow instructions in data/README.md to retrieve and preprocess the BIRD benchmark.

4. Run experiments:
   ```bash
   python run.py
   ```


## 📝 License

This project is released under the MIT License.

---

Feel free to submit an issue if you have feedback or questions!
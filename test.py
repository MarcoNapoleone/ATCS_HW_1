# Suppose you have a script or a test snippet:
from llm.llm_request import call_llm_model

if __name__ == "__main__":

    """
    Test the LLM request function.
    Usage:
        export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
        export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
        export AWS_DEFAULT_REGION=us-east-1
        python run.py
    """
    
    input_data = {
        "system": "You are a helpful assistant.",
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "prompt": "Provide a concise summary of the following text: AWS Bedrock is a fully managed service...",
        "temperature": 0.1
    }

    response = call_llm_model(input_data, model_id="anthropic.claude-3-5-sonnet-20240620-v1:0")
    print("LLM response:", response)


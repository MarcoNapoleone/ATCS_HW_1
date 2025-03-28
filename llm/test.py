# Suppose you have a script or a test snippet:
from llm.utils.llm_request import call_llm_model

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
        "prompt": "Provide a concise summary of the following text: AWS Bedrock is a fully managed service...",
        "max_tokens": 100,
        "temperature": 0.5
    }

    response = call_llm_model(input_data, model_id="amazon.titan-tg1-large")
    print("LLM response:", response)

    # Typically, you'd retrieve generated text from:
    # response["results"][0]["outputText"]  (assuming Titan returns a results array)


import json
import boto3


def call_llm_model(input_data: dict, model_id: str = "amazon.titan-tg1-large") -> dict:
    """
    Calls the Amazon Titan model on AWS Bedrock using Boto3.

    Args:
        input_data (dict): The payload you want to send to the LLM.
                           For Titan, you'll pass a 'prompt' key in your payload.
        model_id (str): The specific Bedrock model ID.
                        For Titan, options might include:
                        "amazon.titan-tg1-large",
                        "amazon.titan-tg1-xlarge", etc.

    Returns:
        dict: The raw response from the LLM.
    """
    # Create an AWS session (if needed, you can pass AWS creds/region directly to the session)
    session = boto3.Session(region_name="us-east-1")  # or "us-west-2"
    bedrock_client = session.client(service_name="bedrock-runtime")

    # The Titan text model typically expects a JSON body with this structure:
    # {
    #   "inputText": "<your prompt>"
    #   "textGenerationConfig": {
    #       "maxTokenCount": <int>,
    #       "temperature": <float>,
    #       "topP": <float>,
    #       "topK": <int>
    #   }
    # }
    #
    # llamas model expects a JSON body with this structure:
    # {
    #   "prompt": string,
    #   "temperature": float,
    #   "top_p": float,
    #   "max_gen_len": int
    # }
    #

    # Prepare the payload
    match model_id:
        case "amazon.titan-tg1-large":
            payload = {
                "inputText": input_data["prompt"],
                "textGenerationConfig": {
                    "maxTokenCount": input_data.get("max_tokens", 100),
                    "temperature": input_data.get("temperature", 0.5),
                    "topP": input_data.get("top_p", 0.9),
                    "topK": input_data.get("top_k", 50)
                }
            }
        case "meta.llama3-70b-instruct-v1:0":
            payload = {
                "prompt": input_data["prompt"],
                "temperature": input_data.get("temperature", 0.5),
                "top_p": input_data.get("top_p", 0.9),
                "max_gen_len": input_data.get("max_gen_len", 100)
            }
        case _:
            raise ValueError(f"Model ID '{model_id}' not recognized.")

    # Invoke the model
    response = bedrock_client.invoke_model(
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
        body=json.dumps(payload)
    )

    # The response "body" is a StreamingBody. We need to read and decode it.
    response_body = response["body"].read().decode("utf-8")
    result = json.loads(response_body)

    return result

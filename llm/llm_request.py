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

    ### The Titan text model typically expects a JSON body with this structure:
    # {
    #   "inputText": "<your prompt>"
    #   "textGenerationConfig": {
    #       "maxTokenCount": <int>,
    #       "temperature": <float>,
    #       "topP": <float>,
    #       "topK": <int>
    #   }
    # }

    ### llamas model expects a JSON body with this structure:
    # {
    #   "prompt": string,
    #   "temperature": float,
    #   "top_p": float,
    #   "max_gen_len": int
    # }

    ### Claude model expects a JSON body with this structure:
    # {
    #   "max_tokens": 1024,
    #   "system": "Today is January 1, 2024. Only respond in Haiku",
    #   "messages": [{"role": "user", "content": "Hello, Claude"}],
    #   "anthropic_version": "bedrock-2023-05-31"
    # }

    # Prepare the payload
    match model_id:
        case "amazon.titan-tg1-large":
            payload = {
                "inputText": input_data["prompt"],
                "textGenerationConfig": {
                    "maxTokenCount": input_data.get("max_tokens", 1024),
                    "temperature": input_data.get("temperature", 0.1),
                    "topP": input_data.get("top_p", 0.9),
                    "topK": input_data.get("top_k", 2)
                }
            }
        case "meta.llama3-70b-instruct-v1:0":
            payload = {
                "prompt": input_data["prompt"],
                "temperature": input_data.get("temperature", 0.5),
                "top_p": input_data.get("top_p", 0.9),
                "max_gen_len": input_data.get("max_tokens", 1024)
            }
        case "anthropic.claude-3-5-sonnet-20240620-v1:0":
            payload = {
                "max_tokens": input_data.get("max_tokens", 1024),
                "system": input_data.get("system", ""),
                "temperature": input_data.get("temperature", 0.1),
                "top_p": input_data.get("top_p", 0.9),
                "top_k": input_data.get("top_k", 2),
                "messages": [
                    {"role": "user", "content": input_data["prompt"]}
                ],
                "anthropic_version": input_data.get("anthropic_version", "bedrock-2023-05-31")
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

    # Adapt the response to the model id

    match model_id:
        case "amazon.titan-tg1-large":
            # Extract the generated text from the Titan response
            result = result["outputText"]
        case "meta.llama3-70b-instruct-v1:0":
            # Extract the generated text from the Llama response
            result = result["text"]
        case "anthropic.claude-3-5-sonnet-20240620-v1:0":
            # Extract the generated text from the Claude response
            result = result["content"][0]["text"] if isinstance(result["content"], list) else result["content"]
        case _:
            raise ValueError(f"Model ID '{model_id}' not recognized.")

    return result

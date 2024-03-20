def openai_api_calculate_cost(usage, model="gpt-3.5-turbo"):
    pricing = {
        "gpt-3.5-turbo": {
            "prompt": 0.0005,
            "completion": 0.0015,
        }
    }

    try:
        model_pricing = pricing[model]
    except KeyError as e:
        raise ValueError("Invalid model specified") from e

    prompt_cost = usage.prompt_tokens * model_pricing["prompt"] / 1000
    completion_cost = usage.completion_tokens * model_pricing["completion"] / 1000

    total_cost = prompt_cost + completion_cost

    return total_cost

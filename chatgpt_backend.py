import requests
import openai
import os
import json

# Set your OpenAI API key (recommended via environment variable)
client = openai.OpenAI(api_key="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")  # or set directly: openai.api_key = "sk-..."

response = client.models.list()
print("Available models:", [m.id for m in response.data])
# Define your function schema for the MCP Adapter endpoint
function_schema = {
    "name": "get_opportunities",
    "description": "Fetches open opportunities above a specified amount",
    "parameters": {
        "type": "object",
        "properties": {
            "min_amount": {
                "type": "number",
                "description": "Minimum value for opportunity amount"
            },
            "close_date": {
                "type": "string",
                "description": "Close date filter"
            }
        },
        "required": ["min_amount"]
    }
}

def get_opportunities_from_mcp(min_amount, close_date=None):
    # Adjust MCP Adapter URL and parameters as needed
    url = "http://localhost:5000/opportunities"
    params = {"min_amount": min_amount}
    if close_date:
        params["close_date"] = close_date
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

def main():
    user_message = "Show me open opportunities above $50K closing this month."

    # Step 1: Call OpenAI with user message + function schema
    response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": user_message}],
        functions=[function_schema],
        function_call="auto"
    )

    message = response.choices[0].message

    # Step 2: Check if OpenAI decided to call function
    if message.function_call and message.function_call.name == "get_opportunities":
        arguments = json.loads(message.function_call.arguments)
        min_amount = arguments.get("min_amount")
        close_date = arguments.get("close_date")

        # Step 3: Call MCP Adapter API with parameters
        opportunities_data = get_opportunities_from_mcp(min_amount, close_date)

        # Step 4: Send the data back to OpenAI for summarization
        followup_messages = [
            {"role": "user", "content": user_message},
            {
                "role": "function",
                "name": "get_opportunities",
                "content": json.dumps(opportunities_data)
            }
        ]

        summary_response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=followup_messages
        )

        print("\n=== AI-Generated Summary and Recommendations ===\n")
        print(summary_response.choices[0].message.content)

    else:
        print("OpenAI did not trigger a function call. Response:")
        print(message.content)

if __name__ == "__main__":
    main()

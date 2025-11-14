import os
import openai
from flask import Flask, jsonify, request
from flask_cors import CORS

# Load environment variables (e.g., for API key)
openai.api_key = os.getenv("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")

app = Flask(__name__)
CORS(app)

def get_ai_summary(opportunity):
    prompt = f"""Summarize this Salesforce Opportunity for sales follow-up priority:
    Name: {opportunity.get("Name")}
    Amount: {opportunity.get("Amount")}
    Stage: {opportunity.get("StageName")}
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=24
    )
    return response.choices[0].text.strip()

@app.route('/opportunities')
def serve_opportunities():
    # Example: Static data sample. Replace with actual database or Salesforce fetch logic.
    records = [
        {
            "Id": "0061",
            "Name": "Dickenson Mobile Generators",
            "Amount": 15000.0,
            "CloseDate": "2024-11-16",
            "StageName": "Qualification"
        },
        {
            "Id": "0062",
            "Name": "United Oil Office Portable Generators",
            "Amount": 125000.0,
            "CloseDate": "2024-11-04",
            "StageName": "Negotiation/Review"
        }
        # ... more records
    ]
    # Add AI summary for each record
    for op in records:
        op['summary'] = get_ai_summary(op)
    return jsonify({"records": records, "totalSize": len(records)})

@app.route('/ai-summary', methods=['POST'])
def ai_summary():
    user_question = request.json.get('query')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_question,
        max_tokens=48
    )
    return jsonify({"summary": response.choices[0].text.strip()})

if __name__ == "__main__":
    app.run(debug=True)

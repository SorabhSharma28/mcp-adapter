import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
from flask_cors import CORS

CORS(app)
load_dotenv()
app = Flask(__name__)

# Set your Salesforce credentials from environment variables
SF_CLIENT_ID = os.getenv("SF_CLIENT_ID")
SF_CLIENT_SECRET = os.getenv("SF_CLIENT_SECRET")
SF_USERNAME = os.getenv("SF_USERNAME")
SF_PASSWORD = os.getenv("SF_PASSWORD")

def get_salesforce_token():
    token_url = "https://login.salesforce.com/services/oauth2/token"
    params = {
        "grant_type": "password",
        "client_id": '3MVG9JJwBBbcN47KLGCtmf5EfwpnUfvH2qTTHN2WzOLoC1x7xwZXSy2S4gfwbi4Dw9q49YmI5qpIJl7lWBK5L',
        "client_secret": '49090F461022CC079D0D1AB44379F39C1FB815881A4146FA4DFE482E376F55CC',
        "username": SF_USERNAME,
        "password": SF_PASSWORD   # Password + Security token concatenated (no spaces)
    }
    response = requests.post(token_url, data=params)
    data = response.json()
    print("Salesforce OAuth response:", data)  # Debug log
    return data["access_token"], data["instance_url"]

@app.route('/opportunities', methods=['GET'])
def get_opportunities():
    access_token, instance_url = get_salesforce_token()
    min_amount = request.args.get('min_amount', 0)
    
    soql = f"SELECT Id, Name, Amount, CloseDate, StageName FROM Opportunity WHERE Amount > {min_amount} AND IsClosed = False"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{instance_url}/services/data/v54.0/query"
    params = {"q": soql}
    
    resp = requests.get(url, headers=headers, params=params)
    return jsonify(resp.json())

if __name__ == '__main__':
    app.run(debug=True)

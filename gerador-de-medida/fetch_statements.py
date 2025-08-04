import requests

RALPH_URL = "http://localhost:8100/xAPI/statements"
AUTH = ("ralph", "secret")

def fetch_statements(params=None):
    if params is None:
        params = {}

    response = requests.get(RALPH_URL, params=params, auth=AUTH)
    
    if response.status_code != 200:
        raise Exception(f"Erro ao consultar RALPH: {response.text}")
    
    return response.json().get("statements", [])

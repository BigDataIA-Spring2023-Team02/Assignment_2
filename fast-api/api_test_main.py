import json
from apimain import app
from dotenv import load_dotenv
from fastapi.testclient import TestClient

client = TestClient(app)
#load env variables
load_dotenv()

def test_get_product_goes():
    response = client.get("/noaa-database/goes18")
    assert response.status_code == 200
    json_resp = json.loads(response.text)
    assert len(json_resp) == 1
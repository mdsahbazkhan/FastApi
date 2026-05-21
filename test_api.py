from fastapi.testclient import TestClient
from cors import app

client= TestClient(app)

# Test the home endpoint
def test_home():
    
    res=client.get("/")
    
    # Assert the status code and response content
    assert res.status_code == 200
    # Response data check
    assert res.json() == {"message": "Welcome to the Home Page"}
    
# Test the add endpoint
def test_add():
    
    res=client.get("/add?a=5&b=3")
    
    # Assert the status code and response content
    assert res.status_code == 200
    # Response data check
    assert res.json() == {"result": 8}
    
# Test the subtract endpoint
def test_subtract():
    
    res=client.get("/subtract?a=5&b=3")
    
    # Assert the status code and response content
    assert res.status_code == 200
    # Response data check
    assert res.json() == {"result": 2}
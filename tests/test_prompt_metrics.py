import pytest
import pandas as pd
from datetime import datetime
from app import create_app
from dvclive import Live

# Function to log metric
def log_metric(workarounds):
    timestamp = datetime.now().isoformat() + "Z"  # ISO 8601 format
    data = {'timestamp': timestamp, 'workarounds': workarounds, "used_tokens":800}

    with Live() as live:
        live.log_metric("used_tokens",800)
    
    # Append to CSV file
    df = pd.DataFrame([data])
    df.to_csv('metrics/llm_metrics.csv', mode='a', header=not pd.io.common.file_exists('metrics/token_metrics.csv'), index=False)

@pytest.fixture
def client():
    app = create_app(testing=True)  # Adjust this according to your app's initialization
    with app.test_client() as client:
        yield client

@pytest.fixture
def login(client):

    response = client.post('/login', data={
        'username':'',
        'password':''
    })

    assert response.status_code == 302
    return client

def test_your_function(login):
    # Simulate the function call or HTTP endpoint
    process_description = "I want to bake a pizza"

    client = login  # This will be the authenticated client
    
    # Act
    response = client.post('/start_map', json={"process_description": process_description})
    
    # Assert the response
    assert response.status_code == 200  # Check successful response

    # Get tokens used from the response
    workarounds = response.json  # Assuming your API returns this

    # Log metrics
    log_metric(workarounds)

    # Example assertion for quality measure (based on your evaluation)
    # assert response.json.get("quality_measure") == expected_quality_measure  # Ensure the calculated quality matches expectations

    # # Additionally check the output of the API
    # assert b'Some expected output' in response.data  # Adjust according to expected output message

if __name__ == '__main__':
    pytest.main()
import pandas as pd
from datetime import datetime
from app import create_app
from dvclive import Live
import openai
import os
import json

app = create_app(testing=True)
client = app.test_client()

response = client.post('/login', data={
        'username': '',
        'password': ''
    })



# Function to log metric
def assess_workarounds(workarounds):
    timestamp = datetime.now().isoformat() + "Z"  # ISO 8601 format
    data = {'timestamp': timestamp, 'workarounds': workarounds, "used_tokens": 800}

    client = openai.AzureOpenAI(
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2023-12-01-preview'),
        azure_endpoint=os.getenv('AZURE_OPENAI_API_URL')
    )
    
    prompts = []  # Define prompts here as needed
    completion = client.beta.chat.completions.parse(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt} for prompt in prompts],
        response_format={"type": "json_object"},
    )

    with Live() as live:
        live.log_metric("used_tokens", 800)

    # Append to CSV file
    df = pd.DataFrame([data])
    df.to_csv('metrics/llm_metrics.csv', mode='a', header=not pd.io.common.file_exists('metrics/token_metrics.csv'), index=False)


def test_your_function(login):
    # Simulate the function call or HTTP endpoint
    processes = [
        {"id": 1, "process_description": "A pizza is baked", "generated_workarounds": ["test_workaround_1", "test_workaround_2"],'quality':0.8},
        {"id": 2, "process_description": "In the logistics industry I want to fill up my trucks at night.", "generated_workarounds": ["test_workaround_1", "test_workaround_2"],'quality':0.7},
        {"id": 3, "process_description": "In the pharma industry I am producing individual medicine on requests.", "generated_workarounds": ["test_workaround_1", "test_workaround_2"],'quality':0.6},
    ]
    
    client = login  # This will be the authenticated client

    filename = 'performance_tests/llm_performance.json'

    with open(filename, 'w') as json_file:
        json.dump({'processes':processes}, json_file, indent=4)




    # with Live() as live:

    #     for process in processes:
    #         # Example API call, assuming you will uncomment and define response handling
    #         # response = client.post('/start_map', json={"process_description": process["process_description"]})
    #         # processes[process["id"]-1]["generated_workarounds"] = response.json
        
    #         live.log_metric("quality", 0.8)
    #         live.log_metric("id", process["id"])
    #         live.log_metric(f"{process["id"]}/quality", 0.8)

    #         print(process)
    #         # Log metrics (example, you'll need to call your log function)
    #         # assess_workarounds(process["generated_workarounds"])
    #     live.log_params({"processes": processes})


if __name__ == '__main__':
    app = create_app(testing=True)
    client = app.test_client()

    response = client.post('/login', data={
        'username': '',
        'password': ''
    })

    test_your_function(client)
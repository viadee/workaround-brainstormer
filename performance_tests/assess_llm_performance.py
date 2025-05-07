from app import create_app
import openai
import os
import json
from performance_tests.performance_assessment_prompts import PERFORMANCE_ASSESSMENT_PROMPTS
from performance_tests.processes_descriptions import PROCESS_DESCRIPTIONS

# Function to log metric
def assess_workarounds(app_client):

    client = openai.AzureOpenAI(
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2023-12-01-preview'),
        azure_endpoint=os.getenv('AZURE_OPENAI_API_URL')
    )

    template = PERFORMANCE_ASSESSMENT_PROMPTS["en"]["workaround_quality"]

    results = []

    for index, process_description in enumerate(PROCESS_DESCRIPTIONS):

        # Get output from the app
        response = app_client.post('/start_map', json={"process_description": process_description})

        workarounds_list = response.json

        workarounds_list_string = "\n".join(f"- {wa}" for wa in workarounds_list)

        prompt = template.format(
            process_description=process_description,
            workaround_list = workarounds_list_string
        )

        assessment = client.beta.chat.completions.parse(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        workaround_assessments = json.loads(assessment.choices[0].message.content)['workaround_assessments']

        generated_workarounds = [{'workaround':workaround,'assessment':workaround_assessments[index]["assessment"],'assessment_explaination':workaround_assessments[index]["explaination"]} for index, workaround in enumerate(workarounds_list)]

        total_assessments = len(workaround_assessments)
        true_assessment_count = sum(1 for assessment in workaround_assessments if assessment["assessment"])

        result = {
            'id' : index,
            'description' : process_description,
            'generated workarounds' : generated_workarounds,
            'quality':true_assessment_count/total_assessments
        }

        results.append(result)

    filename = 'performance_tests/llm_performance.json'

    with open(filename, 'w') as json_file:
        json.dump({'processes':results}, json_file, indent=4)

if __name__ == '__main__':
    app = create_app(testing=True)
    app_client = app.test_client()

    response = app_client.post('/login', data={
        'username': '',
        'password': ''
    })

    assess_workarounds(app_client)
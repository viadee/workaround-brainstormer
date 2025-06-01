
import openai
import os
import json
from performance_tests.performance_assessment_prompts import PERFORMANCE_ASSESSMENT_PROMPTS
from ProcessWorkarounds import ProcessWorkaroundsAssesmentEntry
from dataclasses import dataclass
 

# Function to log metric
def run(app_client, entry: ProcessWorkaroundsAssesmentEntry) -> ProcessWorkaroundsAssesmentEntry:

    client = openai.AzureOpenAI(
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2023-12-01-preview'),
        azure_endpoint=os.getenv('AZURE_OPENAI_API_URL')
    )

    template = PERFORMANCE_ASSESSMENT_PROMPTS["en"]["workaround_quality"]

    result = entry

    workarounds_list = [obj.text for obj in entry.workarounds]

    workarounds_list_string = "\n".join(f"- {wa}" for wa in workarounds_list)

    prompt = template.format(
        process_description=entry.process_description,
        workaround_list = workarounds_list_string
    )

    assessment = client.beta.chat.completions.parse(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    workaround_assessments = json.loads(assessment.choices[0].message.content)['workaround_assessments']

    for index, workaround in enumerate(workarounds_list):
        assesment = workaround_assessments[index]
        assessment_explaination = workaround_assessments[index]["explaination"]
        match = next((obj for obj in result.workarounds if obj.text == workaround), None)

        if match is None:
            print("Could not find workaround in entry", workaround)
        else:
            match.test_results.llm_judge_domain_relevance.assessment = assesment
            match.test_results.llm_judge_domain_relevance.assessment_explaination = assessment_explaination
            
        total_assessments = len(workaround_assessments)
        true_assessment_count = sum(1 for assessment in workaround_assessments if assessment["assessment"])

        result.test_results.llm_judge_domain_relevance_quality = true_assessment_count/total_assessments

    return result

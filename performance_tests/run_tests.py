import sys
import os

# Get the parent directory of the current file’s directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from flask import current_app
from processes_descriptions import PROCESS_DESCRIPTIONS
from typing import List
from ProcessWorkarounds import ProcessWorkaroundsAssesmentEntry
import json
from dotenv import load_dotenv, find_dotenv
from app import create_app
from flask import Flask
from ProcessWorkarounds import ProcessWorkaroundsAssesmentEntry,WorkaroundAssesmentEntry,ProcessWorkaroundsMetricResults
from typing import List, Callable,TypedDict 
from app.llm import LLMService, ProcessContext
import time
from metrics import MetricResults,LLMJudgeDomainRelevanceMetric
from dataclasses import asdict, replace
from test_llm_judge_domain_relevance import run as run_test_llm_judge_domain_relevance


class WorkaroundResult(TypedDict):
     workarounds: List[str]
     token_usage: object

def run_strategy(
        process_descriptions: dict[str, dict[str, str]],
        flask_app: Flask
        ) -> List[ProcessWorkaroundsAssesmentEntry]:
    
    result: List[ProcessWorkaroundsAssesmentEntry] = []
    
    with flask_app.test_request_context():
        
        llm_service = LLMService()
        strategys: dict[str, Callable[[], WorkaroundResult]] = {
            ##'DivideThree': llm_service.get_workarounds_strategy_divide_into_three,
            'SinglePrompt': llm_service.get_workarounds
        }

        for name, func in strategys.items():
            for index, process_description in enumerate(process_descriptions):

                process = ProcessContext(
                    description=process_description,
                    additional_context="",
                    base64_image=None
                )
                
                # Language detection timing
                lang_detect_start = time.time()
            
                process.language = "en"
                
                # API call timing
                api_call_start = time.time()
                llm_result = func(process)
                
                api_call_end = time.time()

                if(isinstance(llm_result, List)):
                    continue
                workarounds = []
                if name == 'DivideThree':
                    for roleName, workarounds_list in llm_result['workarounds'].items():
                        for workaround in workarounds_list:
                            w = WorkaroundAssesmentEntry(text=workaround['workaround'], test_results=MetricResults(llm_judge_domain_relevance=LLMJudgeDomainRelevanceMetric()))
                            workarounds.append(w)

                            
                    entry = ProcessWorkaroundsAssesmentEntry(
                        id=index,
                        prompt_strategy=name,
                        process_description=process_description,
                        workarounds=workarounds,
                        token_count=llm_result['token_usage'],
                        test_results=ProcessWorkaroundsMetricResults(avg_bert_score=None, llm_judge_domain_relevance_quality=None)
                        )
                    
                    test_result_merged_entry = run_performance_tests(current_app=flask_app, entry=entry)
                    result.append(test_result_merged_entry)
                else: 
                    for workaround in llm_result['workarounds']:                   
                        w = WorkaroundAssesmentEntry(text=workaround, test_results=MetricResults(llm_judge_domain_relevance=LLMJudgeDomainRelevanceMetric()))
                        workarounds.append(w)

                            
                    entry = ProcessWorkaroundsAssesmentEntry(
                        id=index,
                        prompt_strategy=name,
                        process_description=process_description,
                        workarounds=workarounds,
                        token_count=llm_result['token_usage'],
                        test_results=ProcessWorkaroundsMetricResults(avg_bert_score=None, llm_judge_domain_relevance_quality=None)
                        )
                    
                    test_result_merged_entry = run_performance_tests(current_app=flask_app, entry=entry)
                    result.append(test_result_merged_entry)
        
    return result

def run_performance_tests(current_app, entry: ProcessWorkaroundsAssesmentEntry) -> ProcessWorkaroundsAssesmentEntry:

    tests: dict[str, Callable[[], ProcessWorkaroundsAssesmentEntry]] = {
            'llm_judge_domain_relevance': run_test_llm_judge_domain_relevance
        }
    
    result = entry
    for name, func in tests.items():
        r = func(current_app, entry)
        result = replace(entry, **asdict(r))
        
    
    return result

def run(flask_app):
   
    process_descriptions = PROCESS_DESCRIPTIONS 

    result: List[ProcessWorkaroundsAssesmentEntry] = run_strategy(process_descriptions=process_descriptions, flask_app=flask_app)

    filename = 'performance_tests/results/llm_workarounds.json'

    with open(filename, 'w') as json_file:
        json.dump({'results':[entry.to_dict() for entry in result]}, json_file, indent=4)

 
if __name__ == '__main__':
    load_dotenv(find_dotenv())
    current_app = create_app(testing=True)
    
    with current_app.app_context():
        current_app.secret_key = os.getenv('APPSECRETKEY')
        current_app.testing = True
        current_app.config.update(
            MAX_CONTENT_LENGTH=5 * 1024 * 1024,  # 5MB limit
            ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'pdf'},
             # OpenAI settings
            AZURE_API_KEY=os.getenv('AZURE_OPENAI_API_KEY'),
            AZURE_API_VERSION=os.getenv('AZURE_OPENAI_API_VERSION', '2023-12-01-preview'),
            AZURE_API_URL=os.getenv('AZURE_OPENAI_API_URL'),
            AZURE_CHAT_MODEL=os.getenv('AZURE_OPENAI_CHAT_MODEL'),
            AZURE_EMBEDDING_MODEL=os.getenv('AZURE_OPENAI_EMBEDDING_MODEL'),
            AUTH_LOGIN_REQUIRED=False,
            DAILY_COST_THRESHOLD=float(os.getenv('DAILYCOSTTHRESHOLD', '10.0')),
            # Q-Drant settings
            QDRANT_URL = os.getenv('QDRANT_URL'),
            QDRANT_WORKAROUNDS_READ_KEY = os.getenv('QDRANT_WORKAROUNDS_READ_KEY'),
        )
    
        run(current_app)
        
    

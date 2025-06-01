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

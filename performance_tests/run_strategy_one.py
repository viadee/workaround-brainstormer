from flask import Flask, jsonify
from ProcessWorkarounds import ProcessWorkaroundsAssesmentEntry,WorkaroundAssesmentEntry, PromptStrategys
from typing import List
from app.llm import LLMService, ProcessContext
import time
import json
def run_strategy_one(
        process_descriptions: dict[str, dict[str, str]],
        flask_app: Flask
        ) -> List[ProcessWorkaroundsAssesmentEntry]:
    
    result: List[ProcessWorkaroundsAssesmentEntry] = []

    for index, process_description in enumerate(process_descriptions):

        llm_result = call_llm(process_description=process_description, additional_context="", base64_image=None, flask_app=flask_app)
        
        if(isinstance(llm_result, List)):
             continue
        workarounds = []
        for workaround in llm_result['workarounds']:
            w = WorkaroundAssesmentEntry(text=workaround, test_results=None)
            workarounds.append(w)

        result.append(ProcessWorkaroundsAssesmentEntry(
            id=index,
            prompt_strategy=PromptStrategys.SinglePrompt.value,
            process_description=process_description,
            workarounds=workarounds,
            token_count=llm_result['token_usage']
            )
        )
    
    return result

def call_llm(process_description: str, additional_context: str, base64_image, flask_app: Flask):
    # Generate workarounds

        with flask_app.test_request_context():
            llm_service = LLMService()
            process = ProcessContext(
                description=process_description,
                additional_context=additional_context,
                base64_image=base64_image
            )
            
            # Language detection timing
            lang_detect_start = time.time()
        
            process.language = "en"
            
            # API call timing
            api_call_start = time.time()
            result = llm_service.get_workarounds(process)
            
            api_call_end = time.time()
            

            return result
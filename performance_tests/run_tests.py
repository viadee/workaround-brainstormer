import sys
import os

# Get the parent directory of the current file’s directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from flask import current_app
from run_strategy_one import run_strategy_one
from processes_descriptions import PROCESS_DESCRIPTIONS
from typing import List
from ProcessWorkarounds import ProcessWorkaroundsAssesmentEntry
import json
from dotenv import load_dotenv, find_dotenv
from app import create_app


def run_tests(flask_app):

        
            process_descriptions = PROCESS_DESCRIPTIONS 

            result: List[ProcessWorkaroundsAssesmentEntry] = []

            result_one: List[ProcessWorkaroundsAssesmentEntry] = run_strategy_one(process_descriptions=process_descriptions, flask_app=flask_app)

            result.extend(result_one)

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
    
        run_tests(current_app)

    

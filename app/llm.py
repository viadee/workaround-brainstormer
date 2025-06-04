# app/llm.py
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import json
import os
from flask import session
from datetime import datetime, timedelta
import logging
import openai
from flask import current_app, session, has_request_context
from .language_service import LanguageService
from .prompts import PROMPTS, DEFAULT_FEW_SHOT_EXAMPLES

# RAG dependencies
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_openai import AzureOpenAIEmbeddings

# Configure logger
logger = logging.getLogger('llm_calls')
logger.setLevel(logging.INFO)


def setup_logging():
    """Setup rotating file handler for LLM calls."""
    logger = logging.getLogger('llm_calls')
    if logger.handlers:
        logger.handlers.clear()
    
    # Ensure log directory exists
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_dir = os.path.join(project_root, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    handler = logging.handlers.RotatingFileHandler(
        os.path.join(logs_dir, 'llm_calls.log'),
        maxBytes=5*1024*1024,
        backupCount=5
    )
    
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            # For API call logs (containing all required fields)
            if all(hasattr(record, field) for field in 
                  ['function', 'input', 'output', 'estimated_cost']):
                log_record = {
                    'timestamp': self.formatTime(record, self.datefmt),
                    'level': record.levelname,
                    'type': 'api_call',
                    'session_id': getattr(record, 'session_id', 'unknown'),
                    'function': getattr(record, 'function'),
                    'input': getattr(record, 'input'),
                    'output': getattr(record, 'output'),
                    'estimated_cost': getattr(record, 'estimated_cost'),
                    'input_tokens': getattr(record, 'input_tokens'),
                    'output_tokens': getattr(record, 'output_tokens'),
                    'total_tokens': getattr(record, 'total_tokens')
                }
            # For regular logs
            else:
                log_record = {
                    'timestamp': self.formatTime(record, self.datefmt),
                    'level': record.levelname,
                    'type': 'info',
                    'session_id': getattr(record, 'session_id', 'unknown'),
                    'message': record.getMessage()
                }
            return json.dumps(log_record)

    handler.setFormatter(JsonFormatter(datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(handler)
    logger.propagate = False



@dataclass
class PromptSettings:
    roles_quantity: int = 3 # Defining the type of 'quantity' property
    workarounds_quantity: int = 2
    challenges_quantity: int = 2

@dataclass
class ProcessContext:
    """Container for process analysis input data."""
    description: str
    additional_context: str = ""
    base64_image: Optional[str] = None
    language: str = "en" 

    prompt_settings: PromptSettings = field(default_factory=PromptSettings)

class CostLimitExceeded(Exception):
    """Raised when daily API cost threshold is exceeded."""
    pass


class LLMService:
    """Service for handling LLM operations with cost tracking."""
    
    def __init__(self, session_id: Optional[str] = None):
        """Initialize OpenAI client with Azure configuration.
        
        Args:
            session_id: Optional session ID. If not provided, will try to get from Flask session.
        """

        api_key = current_app.config.get('AZURE_API_KEY')
        api_version = current_app.config.get('AZURE_API_VERSION')
        azure_endpoint = current_app.config.get('AZURE_API_URL')

        if not all([api_key, api_version, azure_endpoint]):
            raise ValueError("Missing configuration for Azure OpenAI API.")

        self.client = openai.AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
        
        
        self.chat_model = current_app.config['AZURE_CHAT_MODEL']
        self.language_service = LanguageService()
        self.session_id = session_id or self._get_session_id()

    def _get_session_id(self) -> str:
        """Retrieve session ID safely."""
        if has_request_context() and 'id' in session:
            return session['id']
        return 'no_session'

    
    def _log_info(self, message: str) -> None:
        """Log general information with session ID."""
        logger.info(message, extra={'session_id': self.session_id})

    def _log_api_call(self, function: str, input_data: str, 
                     output_data: Any, token_usage: Dict[str, int]) -> None:
        """Log API call details with cost estimation."""
        try:
            cost = (
                token_usage['prompt_tokens'] * (5 / 1_000_000) +  
                token_usage['completion_tokens'] * (15 / 1_000_000)
            )
            logger.info('', extra={
                'session_id': self.session_id,
                'function': function,
                'input': input_data,
                'output': output_data,
                'estimated_cost': round(cost, 5),
                'input_tokens': token_usage['prompt_tokens'],
                'output_tokens': token_usage['completion_tokens'],
                'total_tokens': token_usage['total_tokens'],
            })
        except Exception as e:
            self._log_info(f'Error logging API call: {str(e)}')

    def _get_prompt(self, key: str, process: ProcessContext, **kwargs) -> str:
        """
        Get prompt template and format it with parameters.
        """
        try:
            template = PROMPTS[process.language][key]
        except KeyError:
            logger.error(f"Prompt template not found: {process.language}/{key}")
            template = PROMPTS['en'][key]

        # Retrieve the stored few-shot examples from session.
        stored = session.get('few_shot_examples')
        
        # If stored is not a dict (or is missing), convert if it is a list or use an empty dict.
        if not isinstance(stored, dict):
            stored = {"en": stored} if isinstance(stored, list) else {}
            session['few_shot_examples'] = stored

        # Get the examples for the current language directly.
        user_examples = stored.get(process.language)
        if not user_examples:
            user_examples = DEFAULT_FEW_SHOT_EXAMPLES.get(process.language, [])
        else:
            # Filter: keep only examples with selected == True.
            user_examples = [ex['text'] for ex in user_examples if ex.get('selected', True)]

        few_shot_str = "\n".join(f"- {ex}" for ex in user_examples)
        
        return template.format(
            process_description=process.description,
            additional_context=process.additional_context,
            few_shot_examples=few_shot_str,
            roles_quantity=process.prompt_settings.roles_quantity,
            challenges_quantity=process.prompt_settings.challenges_quantity,
            workarounds_quantity=process.prompt_settings.workarounds_quantity,
            **kwargs
        )

    def detect_language(self, process: ProcessContext) -> str:
        """Detect language for a process."""
        detected_language = self.language_service.detect_language(
            text=process.description,
            base64_image=process.base64_image
        )
        self._log_info(f"Language detected: {detected_language}")
        return detected_language

    def get_workarounds(self, process: ProcessContext) -> List[str]:
        """Get initial workaround suggestions for a process."""
        if not self._check_cost_threshold():
            raise CostLimitExceeded("Daily cost threshold exceeded")

        # Get appropriate prompt template
        key = "start_with_image" if process.base64_image else "start_no_image"
        prompt = self._get_prompt(key, process)
        messages = self._create_messages(prompt, process)

        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.chat_model,
                max_tokens=20000,
                messages=messages,
                response_format={"type": "json_object"},
            )
            self._log_api_call(
                function="get_workarounds",
                input_data=prompt,
                output_data=completion.choices[0].message.content,
                token_usage=completion.usage.model_dump()
            )
            return json.loads(completion.choices[0].message.content)['workarounds']
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error on get_workarounds: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during get_workarounds: {str(e)}")
            return []
        
    def get_misfits(self, process: ProcessContext, roles):
        key = "GenerateMisfitsPrompt"
        prompt = self._get_prompt(key, process, roles=roles)
        messages = self._create_messages(prompt, process)

        try:
            completion = self.client.beta.chat.completions.parse(
                model= self.chat_model,
                messages=messages,
                max_tokens=20000,
                response_format={"type": "json_object"}
            )
            self._log_api_call(
                function="get_misfits",
                input_data=prompt,
                output_data=completion.choices[0].message.content,
                token_usage=completion.usage.model_dump()
            )
            return json.loads(completion.choices[0].message.content)
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error on get_misfits: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during get_misfits: {str(e)}")
            return []
    def get_workarounds_from_misfits(self, process: ProcessContext, misfits):
        
        key = "GenerateWorkaroundsPrompt"
        prompt = self._get_prompt(key, process, misfits=misfits)
        messages = self._create_messages(prompt, process)

        try:
            completion = self.client.beta.chat.completions.parse(
                model= self.chat_model,
                messages=messages,
                max_tokens=20000,
                response_format={"type": "json_object"}
            )
            self._log_api_call(
                function="get_workarounds_from_misfits",
                input_data=prompt,
                output_data=completion.choices[0].message.content,
                token_usage=completion.usage.model_dump()
            )
            return json.loads(completion.choices[0].message.content)
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error on get_workarounds_from_misfits: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during get_workarounds_from_misfits: {str(e)}")
            return []

    def get_roles(self, process: ProcessContext) -> List[str]:

        key = "GenerateRolesPrompt"
        prompt = self._get_prompt(key, process)
        messages = self._create_messages(prompt, process)

        try:
            completion = self.client.beta.chat.completions.parse(
                model= self.chat_model,
                messages=messages,
                max_completion_tokens=3000,
                response_format={"type": "json_object"}
            )
            self._log_api_call(
                function="get_roles",
                input_data=prompt,
                output_data=completion.choices[0].message.content,
                token_usage=completion.usage.model_dump()
            )
            return json.loads(completion.choices[0].message.content)['roles']
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error on get_roles: {str(e)}")
            return []
        except openai.InternalServerError as e:
            logger.error(f"OpenAI API internal server error on get_roles: {str(e)}")
            return []
        except openai.APIStatusError as e:
            logger.error(f"OpenAI API status error on get_roles: {str(e)}")
            return []
        except openai.RateLimitError as e:
            logger.error(f"OpenAI API rate limit error on get_roles: {str(e)}")
            return []
        except openai.APIResponseValidationError as e:
            logger.error(f"OpenAI API response validation error on get_roles: {str(e)}")
            return []
        except openai.BadRequestError as e:
            logger.error(f"OpenAI API bad request error on get_roles: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during get_roles: {str(e)}")
            return []

    def get_similar_workarounds(
        self,
        process: ProcessContext,
        similar_workaround: str,
        workaround_quantity: int
    ) -> List[str]:
        """Get workarounds similar to a reference workaround."""
        if not self._check_cost_threshold():
            raise CostLimitExceeded("Daily cost threshold exceeded")
        # Get appropriate prompt template
        key = "similar_with_image_or_diagram"
        prompt = self._get_prompt(key, process, similar_workaround=similar_workaround, workaround_quantity=workaround_quantity)
        messages = self._create_messages(prompt, process)
        
        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.chat_model,
                messages=messages,
                response_format={"type": "json_object"},
            )
            self._log_api_call(
                function="get_similar_workarounds",
                input_data=prompt,
                output_data=completion.choices[0].message.content,
                token_usage=completion.usage.model_dump()
            )
            return json.loads(completion.choices[0].message.content)['workarounds']
        
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error on get_similar_workarounds: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during get_similar_workarounds: {str(e)}")
            return []

    def generate_node_label(
        self,
        workaround: str,
        other_workarounds: List[str]
    ) -> str:
        """Generate a label for a workaround node."""
        if not self._check_cost_threshold():
            raise CostLimitExceeded("Daily cost threshold exceeded")

        prompt = get_node_label_prompt(workaround, other_workarounds)

        try:
            completion = self.client.chat.completions.create(
                model=self.chat_model,
                messages=[{"role": "user", "content": prompt}]
            )

            self._log_api_call(
                function="generate_node_label",
                input_data=prompt,
                output_data=completion.choices[0].message.content,
                token_usage=completion.usage.model_dump()
            )

            return completion.choices[0].message.content.strip()
        
        except openai.OpenAIError as e:
            logger.error(f"OpenAI API error on generate_node_label: {str(e)}")
            return ""
        except Exception as e:
            logger.error(f"Unexpected error during generate_node_label: {str(e)}")
            return ""

    def _check_cost_threshold(self) -> bool:
        """Check if API usage is within daily cost threshold."""
        threshold = float(current_app.config.get('DAILY_COST_THRESHOLD', 10.0))
        cutoff_time = datetime.now() - timedelta(hours=24)
        total_cost = 0.0
        
        # Get logs directory from app config
        log_file = os.path.join(current_app.config['LOGS_DIR'], 'llm_calls.log')

        try:
            with open(log_file, 'r') as log_file:
                for line in log_file:
                    try:
                        log_entry = json.loads(line.strip())
                        timestamp = datetime.strptime(
                            log_entry['timestamp'],
                            '%Y-%m-%d %H:%M:%S'
                        )
                        if timestamp >= cutoff_time:
                            total_cost += float(log_entry.get('estimated_cost', 0))
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue

            # Log current cost status
            self._log_info(f"Current 24h API cost: ${total_cost:.4f}")
                
        except FileNotFoundError:
            self._log_info("No cost log file found - starting fresh")
            return True

        return total_cost < threshold

    def _create_messages(
        self,
        prompt: str,
        process: ProcessContext
    ) -> List[Dict]:
        """Create message list for API call, handling images if present."""
        if process.base64_image:
            return [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{process.base64_image}"
                        }
                    }
                ]
            }]
        return [{"role": "user", "content": prompt}]


def get_node_label_prompt(workaround, other_workarounds):
    formatted_other_workarounds = '\n'.join(f"- {w}" for w in other_workarounds) or "None"
    prompt = f"""
        You are a helpful assistant that generates short, descriptive labels for workarounds. Generate a concise label (maximum of 3 words) that highlights what is unique or distinctive about the following workaround compared to others. The label should be clear, action-oriented, or outcome-focused to help users quickly understand its unique aspect.
        It is crucial, that the label is the same language as the current workaround.

        Current Workaround:
        {workaround}

        Other Workarounds:
        {formatted_other_workarounds}
        """
    return prompt

class RAGService:

    def __init__(self, session_id: Optional[str] = None):
        """Initialize OpenAI client with Azure configuration.
        
        Args:
            session_id: Optional session ID. If not provided, will try to get from Flask session.
        """
        self.embedding_model_name = current_app.config['AZURE_EMBEDDING_MODEL']
        self.embeddings_client = AzureOpenAIEmbeddings(
            model=self.embedding_model_name,
            api_key = current_app.config['AZURE_API_KEY'],
            azure_endpoint = current_app.config['AZURE_API_URL'],
            openai_api_version = current_app.config['AZURE_API_VERSION']
        )

        self.qdrant_client = QdrantClient(
            url=current_app.config['QDRANT_URL'],
            api_key=current_app.config['QDRANT_WORKAROUNDS_READ_KEY']
        )

        self.vector_store = QdrantVectorStore(
            client = self.qdrant_client,
            collection_name="workarounds",
            embedding = self.embeddings_client
        )

        self.language_service = LanguageService()
        self.session_id = session_id or self._get_session_id()

    def _get_session_id(self) -> str:
        """Retrieve session ID safely."""
        if has_request_context() and 'id' in session:
            return session['id']
        return 'no_session'

    def retreive_similar_workarounds(self, process_description:str) -> List[str]:
        """Retrieve similar workarounds using vector store."""
        try:
            results = self.vector_store.similarity_search_with_score(process_description,k=5)
            formated_results = [result[0].page_content for result in results]
            return formated_results
        
        except Exception as e:
            logger.error(f'Error retreiving similar workarounds: {str(e)}')
            return []
    
        

# Initialize logging when module is imported
setup_logging()
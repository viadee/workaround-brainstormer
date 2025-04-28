# app/routes.py
from flask import (
    Blueprint, render_template, jsonify, request, send_file,
    redirect, url_for, session, flash, current_app
)
from io import BytesIO
import os
import json
import time
import uuid

from .prompts import DEFAULT_FEW_SHOT_EXAMPLES
from .auth import login_required, admin_required, check_credentials, setUserCredentialVariables
from .utils import save_uploaded_file, process_image, format_workarounds_tree
from .llm import LLMService, ProcessContext, CostLimitExceeded, RAGService
import logging

# Create blueprints
auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)
info_bp = Blueprint('info', __name__)

def add_timing_headers(response, **kwargs):
    """Add timing information to response headers."""
    for key, value in kwargs.items():
        response.headers[f'X-{key}'] = str(value)
    return response

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        current_app.logger.info("Login attempt for user: %s", username)

        if check_credentials(username, password):
            session['username'] = username
            # Generate a unique session ID
            session['id'] = str(uuid.uuid4())
            if username == 'admin':
                session['is_admin'] = True
            else:
                session['is_admin'] = False
            current_app.logger.info("Login successful: %s (Session ID: %s)", 
                                  username, session['id'])
            return redirect(url_for('main.brainstormer'))

        current_app.logger.warning("Invalid login attempt: %s", username)
        flash('Invalid username or password.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    username = session.pop('username', None)
    current_app.logger.info("User logged out: %s", username)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/setCredentials', methods=['POST'])
@login_required
@admin_required
def setCredentials():
    if request.method == 'POST':

        try:
            username = request.form['username']
            password = request.form['password']

            setUserCredentialVariables(username=username, password=password)

            return redirect(url_for('main.admin'))
        except Exception as e:
            current_app.logger.error("Error setting user credentials in environment variable")
            return jsonify({'error': e}), 500
    
    return 405



# Main routes (including API endpoints)
@main_bp.route('/')
def index():
    """Render main application page."""
    current_app.logger.info("Rendering index for: %s", session.get('username'))
    return render_template(
        'landingpage/landingpage.html',
        app_version=current_app.config['APP_VERSION'],
                default_few_shot_examples=DEFAULT_FEW_SHOT_EXAMPLES
    )

@main_bp.route('/brainstormer')
@login_required
def brainstormer():
    """Render main application page."""
    current_app.logger.info("Rendering index for: %s", session.get('username'))
    return render_template(
        'index.html',
        app_version=current_app.config['APP_VERSION'],
                default_few_shot_examples=DEFAULT_FEW_SHOT_EXAMPLES
    )




@main_bp.route('/admin', methods=['POST', 'GET'])
@login_required
@admin_required
def admin():
    return render_template(
        'admin.html',
        app_version=current_app.config['APP_VERSION'],
         default_few_shot_examples=DEFAULT_FEW_SHOT_EXAMPLES
    )


@main_bp.route('/download_logs')
@login_required
@admin_required
def download_logs():
    """Download LLM API call logs (admin only)."""
    try:
        log_path = os.path.join(current_app.config['LOGS_DIR'], 'llm_calls.log')
        if not os.path.exists(log_path):
            current_app.logger.error("Log file not found at: %s", log_path)
            flash('Log file not found.', 'error')
            return redirect(url_for('main.brainstormer'))
            
        return send_file(
            log_path,
            as_attachment=True,
            download_name='llm_calls.log',
            mimetype='text/plain'
        )
    except Exception as e:
        current_app.logger.exception("Error downloading logs: %s", e)
        flash('Error downloading log file.', 'error')
        return redirect(url_for('main.brainstormer'))

@main_bp.route('/start_map', methods=['POST'])
@login_required
def start_map():
    """Initialize workaround map generation."""
    start_time = time.time()
    process_description = request.form.get('process_description', '')
    additional_context = request.form.get('additional_context', '')
    
    current_app.logger.info("Starting map generation")
    base64_image = None
    temp_file_path = None
    file_processing_start = file_processing_end = None

    try:
        # Handle file upload with timing
        if 'file' in request.files and request.files['file'].filename:
            file_processing_start = time.time()
            temp_file_path, filename = save_uploaded_file(request.files['file'])
            base64_image = process_image(temp_file_path, filename)
            file_processing_end = time.time()

        # Generate workarounds
        llm_service = LLMService(session_id=session.get('id'))
        process = ProcessContext(
            description=process_description,
            additional_context=additional_context,
            base64_image=base64_image
        )
        
        # Language detection timing
        lang_detect_start = time.time()
        session['detected_language'] = llm_service.detect_language(process)
        process.language = session['detected_language']
        lang_detect_end = time.time()
        
        # API call timing
        api_call_start = time.time()
        workarounds = llm_service.get_workarounds(process)
        api_call_end = time.time()
        
        session['workarounds'] = workarounds
        
        current_app.logger.info("Successfully generated workarounds")
        response = jsonify(workarounds)
        
        # Add all timing headers including file processing if present
        timing_headers = {
            'Language_Detection_Start': lang_detect_start,
            'Language_Detection_End': lang_detect_end,
            'API_Call_Start': api_call_start,
            'API_Call_End': api_call_end
        }
        
        if file_processing_start and file_processing_end:
            timing_headers.update({
                'File_Processing_Start': file_processing_start,
                'File_Processing_End': file_processing_end
            })
            
        return add_timing_headers(response, **timing_headers)

    except CostLimitExceeded:
        current_app.logger.error("Cost threshold exceeded")
        return jsonify({'error': 'API cost threshold exceeded'}), 429
        
    except Exception as e:
        current_app.logger.exception("Error in map generation: %s", e)
        return jsonify({'error': str(e)}), 500

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@main_bp.route('/get_similar_workarounds', methods=['POST'])
@login_required
def get_similar_workarounds():
    start_time = time.time()
    try:
        current_app.logger.info("Received get_similar_workarounds request")
        temp_file_path = None
        base64_image = None
        file_processing_start = file_processing_end = None
        
        # If there's a file, handle it
        if 'file' in request.files and request.files['file'].filename:
            file_processing_start = time.time()
            temp_file_path, filename = save_uploaded_file(request.files['file'])
            base64_image = process_image(temp_file_path, filename)
            file_processing_end = time.time()

        # Parse data based on content type
        if request.is_json:
            data = request.get_json()
        else:
            # Always parse from request.form
            raw_other_workarounds = request.form.get('other_workarounds', '[]')
            try:
                other_w = json.loads(raw_other_workarounds)
            except json.JSONDecodeError:
                other_w = []

            data = {
                'process_description': request.form.get('process_description', ''),
                'additional_context': request.form.get('additional_context', ''),
                'similar_workaround': request.form.get('similar_workaround', ''),
                'other_workarounds': other_w
            }

        # Use stored language
        process = ProcessContext(
            description=data['process_description'],
            additional_context=data['additional_context'],
            base64_image=base64_image,
            language=session.get('detected_language', 'en')
        )

        llm_service = LLMService(session_id=session.get('id'))

        api_call_start = time.time()
        similar_workarounds = llm_service.get_similar_workarounds(
            process,
            data['similar_workaround']
        )
        similar_workarounds_end = time.time()

        node_label = llm_service.generate_node_label(
            data['similar_workaround'],
            data['other_workarounds']
        )
        api_call_end = time.time()

        response = jsonify({
            'label': node_label,
            'workarounds': similar_workarounds
        })

        # Build timing headers
        timing_data = {
            'File_Processing_Start': file_processing_start or 0,
            'File_Processing_End': file_processing_end or 0,
            'API_Call_Start': api_call_start,
            'Similar_Workarounds_End': similar_workarounds_end,
            'API_Call_End': api_call_end,
            'Total_Processing_Time': time.time() - start_time
        }
        return add_timing_headers(response, **timing_data)

    except ValueError as e:
        current_app.logger.error(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400

    except CostLimitExceeded:
        current_app.logger.error("Cost threshold exceeded")
        return jsonify({'error': 'API cost threshold exceeded'}), 429

    except Exception as e:
        current_app.logger.exception("Error generating similar workarounds: %s", e)
        return jsonify({'error': str(e)}), 500

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)



@main_bp.route('/update_workarounds', methods=['POST'])
@login_required
def update_workarounds():
    """Update and format workarounds list."""
    try:
        data = request.get_json()
        workarounds_tree = data.get('workarounds_tree')
        
        formatted_text = format_workarounds_tree(workarounds_tree)
        session['workarounds_text'] = formatted_text
        
        return jsonify({'status': 'success'})

    except Exception as e:
        current_app.logger.exception("Error updating workarounds: %s", e)
        return jsonify({'error': str(e)}), 500

@main_bp.route('/download_workarounds', methods=['GET'])
@login_required
def download_workarounds():
    """Download formatted workarounds as text file."""
    try:
        workarounds_text = session.get('workarounds_text', '')
        buffer = BytesIO(workarounds_text.encode())
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name='workarounds.txt',
            mimetype='text/plain'
        )
    except Exception as e:
        current_app.logger.exception("Error downloading workarounds: %s", e)
        flash('Error downloading workarounds file.', 'error')
        return redirect(url_for('main.brainstormer'))
    
@main_bp.route('/test_logging')
@login_required
@admin_required
def test_logging():
    """Test route to verify logging is working."""
    current_app.logger.info('Test log message from app logger')
    
    llm_logger = logging.getLogger('llm_calls')
    llm_logger.info('', extra={
        'function': 'test',
        'input': 'test input',
        'output': 'test output',
        'estimated_cost': 0.0,
        'input_tokens': 0,
        'output_tokens': 0,
        'total_tokens': 0,
    })
    
    return jsonify({'status': 'Logging test complete'})

@main_bp.route('/update_few_shot_examples', methods=['POST'])
@login_required
def update_few_shot_examples():
    """Update the few shot examples based on user input."""
    try:
        data = request.get_json()
        # Expecting data in the form: { "few_shot_examples": { "en": { "start_no_image": [ ... ] } } }
        session['few_shot_examples'] = data.get('few_shot_examples', {})
        current_app.logger.info("Few shot examples updated.")
        return jsonify({"status": "success"})
    except Exception as e:
        current_app.logger.exception("Error updating few shot examples: %s", e)
        return jsonify({"error": str(e)}), 500
    

@info_bp.route('/impressum')
def impressum():

    return render_template(
        '/landingpage/impressum.html'
    )


@info_bp.route('/datenschutz')
def datenschutz():

    return render_template(
        '/landingpage/datenschutz.html'
    )
    

@main_bp.route('/retreive_similar_few_shot_examples', methods=['POST'])
@login_required
def retreive_similar_few_shot_examples():
    """Retreive few shot examples based on user input."""
    try:
        data = request.get_json()
        # Expecting data in the form: { "few_shot_examples": { "en": { "start_no_image": [ ... ] } } }
        process_description = data.get('process_description', {})

        rag_service = RAGService(session_id=session.get('id'))
        retreived_similar_workarounds = rag_service.retreive_similar_workarounds(process_description=process_description)

        response = jsonify({
            'status': 'success',
            'data': retreived_similar_workarounds,
            'message': 'Retreived similar workarounds successfully.'
        })

        current_app.logger.info("Similar few shot examples generated.")

        response.status_code = 200
        return response
    
    except Exception as e:
        current_app.logger.exception("Error generating similar few shot examples: %s", e)
        return jsonify({"error": str(e)}), 500
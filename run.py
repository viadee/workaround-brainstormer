# run.py
from dotenv import load_dotenv, find_dotenv
from app import create_app

# Load environment variables
load_dotenv(find_dotenv())

## required environment variables
# AZURE_API_KEY
# AZURE_API_URL
# APP_SECRET_KEY
# WA_PASSWORD_HASH
# WA_USERNAME
# ADMIN_PASSWORD_HASH
# DAILY_COST_THRESHOLD

# Create application instance
app = create_app()

if __name__ == '__main__':

    app.run(debug=False, port=5001, host='0.0.0.0')
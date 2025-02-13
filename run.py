# run.py
from dotenv import load_dotenv, find_dotenv
from app import create_app

# Load environment variables
load_dotenv(find_dotenv())

## required environment variables
# AZUREAPIKEY
# AZUREAPIURL
# APPSECRETKEY
# WAPASSWORDHASH
# WAUSERNAME
# ADMINPASSWORDHASH
# DAILYCOSTTHRESHOLD

# Create application instance
app = create_app()

if __name__ == '__main__':

    app.run(debug=False, port=5000, host='0.0.0.0')
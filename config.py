import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Crypto.com API configuration
API_KEY = os.getenv('CRYPTOCOM_API_KEY')
API_SECRET = os.getenv('CRYPTOCOM_API_SECRET')
API_BASE_URL = 'https://api.crypto.com/v2'
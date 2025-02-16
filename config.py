from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Crypto.com API configuration
API_KEY = os.getenv('CRYPTOCOM_API_KEY')
API_SECRET = os.getenv('CRYPTOCOM_API_SECRET')
API_BASE_URL = 'https://api.crypto.com/v2'

if not API_KEY or not API_SECRET:
    raise ValueError("Missing API key or secret. Please check your .env file.")

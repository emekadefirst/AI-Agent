import os
from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = str(os.getenv('GEMINI_API_KEY'))
AMADEUS_BASE_URL = str(os.getenv('AMADEUS_BASE_URL'))
AMADEUS_CLIENT_ID = str(os.getenv('AMADEUS_CLIENT_ID'))
AMADEUS_CLIENT_SECRET = str(os.getenv('AMADEUS_CLIENT_SECRET'))

import os
from dotenv import load_dotenv

load_dotenv()
#the data in env file should be as follows
OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')

RAPIDAPI_LINKEDIN_KEY = os.getenv('RAPIDAPI_LINKEDIN_KEY')

DATABASE_URI = os.getenv('DATABASE_URI')

# Define your RapidAPI key
GROQ_key = os.getenv('GROQ_key')

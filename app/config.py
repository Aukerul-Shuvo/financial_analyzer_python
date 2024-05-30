# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    # Database URIs
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_TEST_URI = os.getenv('MONGO_TEST_URI')
    
    # Database names
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    TEST_DATABASE_NAME = os.getenv('TEST_DATABASE_NAME')
    
    # Database to use based on the environment
    USE_TEST_DB = os.getenv('USE_TEST_DB', 'false').lower() == 'true'
    
    # OpenAI API Key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPEN_AI_MODEL = os.getenv('OPEN_AI_MODEL')
    
    # Choose the database name based on whether testing is enabled
    @staticmethod
    def get_database_name():
        if Config.USE_TEST_DB:
            return Config.TEST_DATABASE_NAME
        return Config.DATABASE_NAME

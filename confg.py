import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN') or ''
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or ''
BASE_URL = 'https://openrouter.ai/api/v1'
MODEL = 'stepfun/step-3.5-flash:free'
DEFAULT_SYSTEM_PROMPT = 'Нет особых инструкций. Отвечай как обычно.'

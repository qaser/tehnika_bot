import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')  # тестовый чат
TEST_CHAT_ID = '-1001555422626'  # тестовый чат
CHAT_ID_GKS = os.getenv('CHAT_ID_GKS')
MY_TELEGRAM_ID = os.getenv('MY_TELEGRAM_ID')

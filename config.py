import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Токены (лежат в .env)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_KEY")

DB_HOST = os.getenv("DB_HOST", "localhost")     # где сервер БД (localhost = на этом же компе)
DB_PORT = os.getenv("DB_PORT", "5432")          # порт PostgreSQL по умолчанию
DB_NAME = os.getenv("DB_NAME", "friendbot")     # имя базы данных
DB_USER = os.getenv("DB_USER", "botuser")       # имя пользователя
DB_PASSWORD = os.getenv("DB_PASSWORD", "botpassword")  # пароль

# Строка подключения - собирается из параметров
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

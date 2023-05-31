import psycopg2
from environs import Env

# Используем библиотеку environs
env = Env()
env.read_env()

# Считываем данные из .env
con = psycopg2.connect(
    database=env.str('POSTGRES_DB'),
    user=env.str('POSTGRES_USER'),
    password=env.str('POSTGRES_PASSWORD'),
    host=env.str('POSTGRES_HOST'),
    port=env.str('POSTGRES_PORT')
)
# Считываем данные из .env
cur = con.cursor()
cur.execute("SELECT * from main_token")
token = cur.fetchall()
BOT_TOKEN = token[0][2]  # Токен бота
CHANNELS = [token[0][3]]
cur.execute("SELECT * from main_adminstg")
admin = cur.fetchall()
ADMINS = []  # Список админов
for i in admin:
    ADMINS.append(str(i[1]))
DB_USER = env.str("POSTGRES_USER")
DB_PASS = env.str("POSTGRES_PASSWORD")
DB_NAME = env.str("POSTGRES_DB")
DB_HOST = env.str("POSTGRES_HOST")
DB_PORT = env.str("POSTGRES_PORT")

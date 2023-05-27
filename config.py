import psycopg2
import time

host = 'localhost'
user = 'postgres'
password = 'Makcemjoi990'
db_name = 'my_db'

connection = psycopg2.connect(
    user=user,
    password=password,
    host=host,
    database=db_name
)

TOKEN_KINOGO = '5958293925:AAGh2IVIUkvGfygLO-ebFbIzU-r0QfZJnAA'
TOKEN_DESSERT = '6044389119:AAEWU6CAcKuijKGUXhvUShjChHBJRhbOq_U'
strings_date = time.strftime("%Y-%m-%d %H:%M:%S")


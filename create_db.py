import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_NAME = "tasks_manager"
USER = "postgres"
PASSWORD = "mysecretpassword"
HOST = "localhost"
PORT = 5433


def execute_sql_from_file(filename, connection):
    # Читаем SQL файл и выполняем команды по одной
    with open(filename, 'r') as file:
        sql_commands = file.read().split(';')  # Разделяем команды по символу ';'
        cur = connection.cursor()
        for command in sql_commands:
            if command.strip():  # Проверяем, не является ли команда пустой строкой
                cur.execute(command)
        connection.commit()
        cur.close()


def create_db_structure():
    conn = psycopg2.connect(dbname=DB_NAME, user=USER,
                            password=PASSWORD, host=HOST, port=PORT)
    try:
        execute_sql_from_file('tasks_manager.sql', conn)
        print(f"Таблицы в базе {DB_NAME} созданы успешно.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании таблиц в базе {DB_NAME}: {e}")
    finally:
        conn.close()


def create_db():
    conn = psycopg2.connect(dbname='postgres', user=USER,
                            password=PASSWORD, host=HOST, port=PORT)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    try:
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"База данных {DB_NAME} успешно создана.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    create_db()
    create_db_structure()

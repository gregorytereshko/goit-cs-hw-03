from faker import Faker
import psycopg2
import random

DB_NAME = "tasks_manager"
USER = "postgres"
PASSWORD = "mysecretpassword"
HOST = "localhost"
PORT = 5433
conn = psycopg2.connect(dbname=DB_NAME, user=USER,
                        password=PASSWORD, host=HOST, port=PORT)
cur = conn.cursor()

# Налаштування Faker
fake = Faker()


def seed_db(cur):
    # Генерування даних для таблиці users
    for _ in range(20):
        fullname = fake.name()
        email = fake.email()
        cur.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT DO NOTHING", (fullname, email))

    # Генерування даних для таблиці tasks
    status_ids = [1, 2, 3]  # відповідають статусам new, in progress, completed
    user_ids = list(range(1, 101))  # припускаємо, що ми маємо 100 користувачів

    for _ in range(200):
        title = fake.sentence()
        description = fake.text()
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                    (title, description, status_id, user_id))


if __name__ == "__main__":
    seed_db(cur)
    # Збереження змін і закриття з'єднання
    conn.commit()
    cur.close()
    conn.close()

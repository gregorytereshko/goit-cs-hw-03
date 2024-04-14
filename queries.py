import psycopg2
from prettytable import PrettyTable

# Параметри підключення до бази даних
DB_NAME = "tasks_manager"
USER = "postgres"
PASSWORD = "mysecretpassword"
HOST = "localhost"
PORT = 5433

# Встановлення з'єднання
conn = psycopg2.connect(dbname=DB_NAME, user=USER,
                        password=PASSWORD, host=HOST, port=PORT)
cur = conn.cursor()


def get_tasks_by_user_id(user_id):
    """Повертає всі завдання конкретного користувача."""
    cur.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    return cur.fetchall()


def get_tasks_by_status(status_name):
    """Повертає завдання за певним статусом."""
    cur.execute(
        "SELECT * FROM tasks WHERE status_id IN (SELECT id FROM status WHERE name = %s)", (status_name,))
    return cur.fetchall()


def update_task_status(task_id, new_status):
    """Оновлює статус конкретного завдання."""
    cur.execute(
        "UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s) WHERE id = %s", (new_status, task_id))
    conn.commit()


def get_users_with_no_tasks():
    """Повертає список користувачів, які не мають жодного завдання."""
    cur.execute(
        "SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)")
    return cur.fetchall()


def add_new_task(title, description, status_id, user_id):
    """Додає нове завдання для конкретного користувача."""
    cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                (title, description, status_id, user_id))
    conn.commit()


def get_uncompleted_tasks():
    """Повертає всі завдання, які ще не завершено."""
    cur.execute(
        "SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed')")
    return cur.fetchall()


def delete_task(task_id):
    """Видаляє конкретне завдання."""
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()


def find_users_by_email(email_pattern):
    """Знаходить користувачів з певною електронною поштою."""
    cur.execute("SELECT * FROM users WHERE email LIKE %s", (email_pattern,))
    return cur.fetchall()


def update_user_name(user_id, new_name):
    """Оновлює ім'я користувача."""
    cur.execute("UPDATE users SET fullname = %s WHERE id = %s",
                (new_name, user_id))
    conn.commit()


def get_task_count_by_status():
    """Повертає кількість завдань для кожного статусу."""
    cur.execute(
        "SELECT status.name, COUNT(tasks.id) FROM status LEFT JOIN tasks ON status.id = tasks.status_id GROUP BY status.name")
    return cur.fetchall()


def get_tasks_by_user_email_domain(email_domain):
    """Повертає завдання, призначені користувачам з певною доменною частиною електронної пошти."""
    cur.execute("""
        SELECT t.* FROM tasks t
        JOIN users u ON t.user_id = u.id
        WHERE u.email LIKE %s
    """, ('%' + email_domain,))
    return cur.fetchall()


def get_tasks_without_description():
    """Повертає завдання, у яких відсутній опис."""
    cur.execute(
        "SELECT * FROM tasks WHERE description = '' OR description IS NULL")
    return cur.fetchall()


def get_users_and_their_tasks_with_status_in_progress():
    """Повертає список користувачів та їхні завдання із статусом 'in progress'."""
    cur.execute("""
        SELECT u.fullname, t.* FROM users u
        INNER JOIN tasks t ON u.id = t.user_id
        INNER JOIN status s ON t.status_id = s.id
        WHERE s.name = 'in progress'
    """)
    return cur.fetchall()


def get_users_and_their_task_counts():
    """Повертає користувачів та кількість їхніх завдань."""
    cur.execute("""
        SELECT u.fullname, COUNT(t.id) FROM users u
        LEFT JOIN tasks t ON u.id = t.user_id
        GROUP BY u.fullname
    """)
    return cur.fetchall()


def print_table(data, headers):
    """Друк результатів у вигляді таблиці."""
    table = PrettyTable()
    table.field_names = headers
    for row in data:
        table.add_row(row)
    print(table)


if __name__ == "__main__":
    print("Отримати всі завдання певного користувача:")
    print_table(get_tasks_by_user_id(1), [
                "ID", "Title", "Description", "Status ID", "User ID"])

    print("Отримати всі завдання за певним статусом new:")
    print_table(get_tasks_by_status('new'), [
                "ID", "Title", "Description", "Status ID", "User ID"])

    print("Оновити статус завдання:")
    update_task_status(1, 'in progress')

    print("Отримати користувачів, які не мають жодного завдання:")
    print_table(get_users_with_no_tasks(), ["ID", "Fullname", "Email"])

    print("Додати нове завдання:")
    add_new_task("New Task", "Description here", 1, 1)

    print("Отримати всі не завершені завдання:")
    print_table(get_uncompleted_tasks(), [
                "ID", "Title", "Description", "Status ID", "User ID"])

    print("Видалити завдання:")
    delete_task(1)

    print("Знаходити користувачів з певною електронною поштою:")
    print_table(find_users_by_email("%test%"), ["ID", "Fullname", "Email"])

    print("Оновити ім'я користувача:")
    update_user_name(1, "Updated Name")

    print("Отримати кількість завдань для кожного статусу:")
    print_table(get_task_count_by_status(), ["Status", "Count"])

    print("Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти:")
    print_table(get_tasks_by_user_email_domain("example.com"), [
                "ID", "Title", "Description", "Status ID", "User ID"])

    print("Отримати завдання, у яких відсутній опис:")
    print_table(get_tasks_without_description(), [
                "ID", "Title", "Description", "Status ID", "User ID"])

    print("Отримати користувачів та їхні завдання із статусом 'in progress':")
    print_table(get_users_and_their_tasks_with_status_in_progress(), [
                "Fullname", "ID", "Title", "Description", "Status ID", "User ID"
                ])

    print("Отримати користувачів та кількість їхніх завдань:")
    print_table(get_users_and_their_task_counts(), ["Fullname", "Task count"])

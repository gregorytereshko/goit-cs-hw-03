from pymongo import MongoClient

# Ініціалізація клієнта MongoDB
client = MongoClient(
    "mongodb+srv://gregorytereshko1:e3UdLkqGVHsNqw5g@cluster0.uonsvje.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.test
collection = db.cats

# Читання (Read)


def read_all_entries():
    """ Виводить всі записи з колекції. """
    for cat in collection.find():
        print(cat)


def read_cat_by_name(name):
    """ Виводить інформацію про кота за ім'ям. """
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print("Кота з таким іменем не знайдено.")

# Оновлення (Update)


def update_cat_age(name, age):
    """ Оновлює вік кота за ім'ям. """
    result = collection.update_one({"name": name}, {"$set": {"age": age}})
    print(f"Оновлено документів: {result.modified_count}")


def add_feature_to_cat(name, feature):
    """ Додає нову характеристику до списку features кота за ім'ям. """
    result = collection.update_one(
        {"name": name}, {"$push": {"features": feature}})
    print(f"Оновлено документів: {result.modified_count}")

# Видалення (Delete)


def delete_cat_by_name(name):
    """ Видаляє запис з колекції за ім'ям кота. """
    result = collection.delete_one({"name": name})
    print(f"Видалено документів: {result.deleted_count}")


def delete_all_entries():
    """ Видаляє всі записи з колекції. """
    result = collection.delete_many({})
    print(f"Видалено документів: {result.deleted_count}")


if __name__ == "__main__":
    read_all_entries()
    read_cat_by_name("barsik")
    update_cat_age("barsik", 5)
    add_feature_to_cat("barsik", "спить на подушці")
    delete_cat_by_name("barsik")
    delete_all_entries()

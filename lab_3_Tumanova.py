import sqlite3
import matplotlib.pyplot as plt
from collections import Counter

# Лабораторная работа №3
# Графический вывод информации

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("=== ЛАБОРАТОРНАЯ РАБОТА №3 ===")

# 1. Гистограмма возраста пользователей
cursor.execute("SELECT age FROM Users")
ages = [row[0] for row in cursor.fetchall()]

plt.figure()
plt.hist(ages)
plt.title("Распределение возраста пользователей")
plt.xlabel("Возраст")
plt.ylabel("Количество")
plt.show()

# 2. Соотношение мужчин и женщин
cursor.execute("SELECT gender FROM Users")
genders = [row[0] for row in cursor.fetchall()]

gender_counts = Counter(genders)

plt.figure()
plt.bar(list(gender_counts.keys()), list(gender_counts.values()))
plt.title("Соотношение мужчин и женщин")
plt.xlabel("Пол")
plt.ylabel("Количество")
plt.show()

# 3. Количество заказов на пользователя
cursor.execute("SELECT user_id, COUNT(*) FROM Orders GROUP BY user_id")
orders = cursor.fetchall()
counts = [row[1] for row in orders]

plt.figure()
plt.hist(counts)
plt.title("Количество заказов на пользователя")
plt.xlabel("Число заказов")
plt.ylabel("Количество пользователей")
plt.show()

# 4. Количество пользователей по профессии
cursor.execute("SELECT profession, COUNT(*) FROM Users GROUP BY profession")
data = cursor.fetchall()

professions = [row[0] for row in data]
counts = [row[1] for row in data]

plt.figure()
plt.bar(professions, counts)
plt.xticks(rotation=45)
plt.title("Количество пользователей по профессии")
plt.xlabel("Профессия")
plt.ylabel("Количество")
plt.show()

conn.close()

print("Лабораторная работа №3 выполнена!")

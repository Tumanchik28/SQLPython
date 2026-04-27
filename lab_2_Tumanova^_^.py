import sqlite3

# Лабораторная работа №2
# Анализ с помощью SQL. Запросы.
# Перед запуском этого файла должна быть создана база database.db из лабораторной №1.

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

print("=== ЛАБОРАТОРНАЯ РАБОТА №2 ===")

# На всякий случай удаляем старую таблицу, чтобы файл можно было запускать повторно
cursor.execute('DROP TABLE IF EXISTS Message')

# 1. Создание таблицы Message
cursor.execute('''
CREATE TABLE Message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    message_text TEXT NOT NULL
)
''')

print("\nТаблица Message создана.")

# 2. Изменение структуры таблицы с помощью ALTER TABLE
cursor.execute('''
ALTER TABLE Message
ADD COLUMN status TEXT DEFAULT 'active'
''')

cursor.execute('''
ALTER TABLE Message
ADD COLUMN rating INTEGER DEFAULT 5
''')

print("В таблицу Message добавлены столбцы status и rating.")

# 3. Добавление данных в таблицу Message
message_data = [
    (1, "Отличный товар, рекомендую к покупке!", 'active', 5),
    (2, "Хорошее качество, быстрая доставка.", 'inactive', 4),
    (3, "Средний товар, ожидал лучшего качества.", 'moderated', 3),
    (4, "Отличное соотношение цены и качества.", 'active', 5),
    (5, "Неплохой товар, но есть небольшие недостатки.", 'active', 4),
    (6, "Очень удобная мышь.", 'active', 5),
    (7, "Планшет работает нормально.", 'inactive', 3),
    (8, "Камера понравилась.", 'active', 4),
    (9, "Микрофон записывает звук хорошо.", 'moderated', 5),
    (10, "Колонки громкие и качественные.", 'active', 5)
]

cursor.executemany('''
INSERT INTO Message (product_id, message_text, status, rating)
VALUES (?, ?, ?, ?)
''', message_data)

conn.commit()
print("Данные в таблицу Message добавлены.")

# 4. SELECT + LIMIT
print("\n1) LIMIT: первые 5 отзывов")
cursor.execute('''
SELECT *
FROM Message
LIMIT 5
''')
for row in cursor.fetchall():
    print(row)

# 5. DISTINCT
print("\n2) DISTINCT: уникальные статусы отзывов")
cursor.execute('''
SELECT DISTINCT status
FROM Message
''')
for row in cursor.fetchall():
    print(row)

# 6. ORDER BY
print("\n3) ORDER BY: отзывы по рейтингу от высокого к низкому")
cursor.execute('''
SELECT id, product_id, message_text, rating
FROM Message
ORDER BY rating DESC
''')
for row in cursor.fetchall():
    print(row)

# 7. GROUP BY
print("\n4) GROUP BY: количество отзывов по статусу")
cursor.execute('''
SELECT status, COUNT(*) AS count_messages
FROM Message
GROUP BY status
''')
for row in cursor.fetchall():
    print(row)

# 8. Агрегатные функции SUM, AVG, MIN, MAX, COUNT
print("\n5) Агрегатные функции по рейтингу")
cursor.execute('''
SELECT
    SUM(rating) AS sum_rating,
    AVG(rating) AS avg_rating,
    MIN(rating) AS min_rating,
    MAX(rating) AS max_rating,
    COUNT(*) AS count_messages
FROM Message
''')
for row in cursor.fetchall():
    print(row)

# 9. INNER JOIN
print("\n6) INNER JOIN: отзывы с названиями продуктов")
cursor.execute('''
SELECT
    m.id,
    p.name AS product_name,
    m.message_text,
    m.rating,
    m.status
FROM Message m
INNER JOIN Products p ON m.product_id = p.id
ORDER BY m.rating DESC
''')
for row in cursor.fetchall():
    print(row)

# 10. LEFT JOIN
print("\n7) LEFT JOIN: все продукты и отзывы к ним")
cursor.execute('''
SELECT
    p.id,
    p.name,
    m.message_text,
    m.rating
FROM Products p
LEFT JOIN Message m ON p.id = m.product_id
ORDER BY p.id
LIMIT 15
''')
for row in cursor.fetchall():
    print(row)

# 11. RIGHT JOIN
# В SQLite нет настоящего RIGHT JOIN, поэтому делаем его аналог через LEFT JOIN,
# поменяв таблицы местами.
print("\n8) RIGHT JOIN: аналог через LEFT JOIN")
cursor.execute('''
SELECT
    p.name AS product_name,
    m.message_text,
    m.rating
FROM Message m
LEFT JOIN Products p ON m.product_id = p.id
ORDER BY m.id
''')
for row in cursor.fetchall():
    print(row)

# 12. WHERE + LIKE
print("\n9) WHERE + LIKE: отзывы, где есть слово 'товар'")
cursor.execute('''
SELECT *
FROM Message
WHERE message_text LIKE '%товар%'
''')
for row in cursor.fetchall():
    print(row)

# 13. NOT LIKE
print("\n10) NOT LIKE: отзывы, где нет слова 'товар'")
cursor.execute('''
SELECT *
FROM Message
WHERE message_text NOT LIKE '%товар%'
''')
for row in cursor.fetchall():
    print(row)

# 14. AND
print("\n11) AND: активные отзывы с рейтингом 5")
cursor.execute('''
SELECT *
FROM Message
WHERE status = 'active' AND rating = 5
''')
for row in cursor.fetchall():
    print(row)

# 15. OR
print("\n12) OR: отзывы со статусом inactive или moderated")
cursor.execute('''
SELECT *
FROM Message
WHERE status = 'inactive' OR status = 'moderated'
''')
for row in cursor.fetchall():
    print(row)

# 16. NOT
print("\n13) NOT: отзывы, которые не active")
cursor.execute('''
SELECT *
FROM Message
WHERE NOT status = 'active'
''')
for row in cursor.fetchall():
    print(row)

# 17. BETWEEN
print("\n14) BETWEEN: отзывы с рейтингом от 3 до 5")
cursor.execute('''
SELECT *
FROM Message
WHERE rating BETWEEN 3 AND 5
''')
for row in cursor.fetchall():
    print(row)

# 18. UPDATE
print("\n15) UPDATE: меняем статус отзывов с рейтингом 3 и ниже на moderated")
cursor.execute('''
UPDATE Message
SET status = 'moderated'
WHERE rating <= 3
''')

conn.commit()

cursor.execute('''
SELECT *
FROM Message
ORDER BY id
''')
for row in cursor.fetchall():
    print(row)

# 19. DELETE
print("\n16) DELETE: удаляем неактивные отзывы")
cursor.execute('''
DELETE FROM Message
WHERE status = 'inactive'
''')

conn.commit()

cursor.execute('''
SELECT *
FROM Message
ORDER BY id
''')
for row in cursor.fetchall():
    print(row)

# 20. DROP
print("\n17) DROP TABLE: удаляем таблицу Message")
cursor.execute('DROP TABLE IF EXISTS Message')

conn.commit()
conn.close()

print("\nЛабораторная работа №2 выполнена успешно!")

import sqlite3

connection = sqlite3.connect("db/parse_db.sqlite")

cursor = connection.cursor()

regions = {
"2":"Санкт-Петербург",
"3":"Екатеринбург",
"237":"Сочи",
"1427":"Дербент"}

skills = {
    "1": "sql",
    "2": "redis",
    "3": "css",
    "4": "html",
    "5": "php"
}

vacancy = {
    "1": "python",
    "2": "java",
    "3": "c#",
    "4": "rust",
    "5": "go"
}
for key, val in regions.items():
    cursor.execute(f"INSERT INTO 'regions' ('id', 'name') VALUES ('{key}', '{val}')")

for key, val in skills.items():
    cursor.execute(f"INSERT INTO  skills' ('id', 'name') VALUES ('{key}', '{val}')")

for key, val in vacancy.items():
    cursor.execute(f"INSERT INTO 'vacancy' ('id', 'name') VALUES ('{key}', '{val}')")

cursor.fetchall()
cursor.execute("SELECT * FROM regions")
cursor.execute("SELECT * FROM skills")
cursor.execute("SELECT * FROM vacancy")

print(cursor.fetchall())


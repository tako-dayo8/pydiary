import sqlite3 , os

db_path = f"{os.path.dirname(__file__)}/../database.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# table一覧を取得
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(f" - {table[0]}")

# 各テーブルのカラム情報を取得
for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"\nColumns in {table_name}:")
    for column in columns:
        print(f" - {column[1]} ({column[2]})")

# 各テーブルのデータを取得
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    print(f"\nData in {table_name}:")
    for row in rows:
        print(f" - {row}")

# データベース接続を閉じる
connection.close()
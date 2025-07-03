import sqlite3
import os

db_path = f"{os.path.dirname(__file__)}/database.db"

class DatabaseManager:
    """
    データベースを管理するクラスです
    sqlite3を使用します

    テーブル設計はdb.mdを参照してください。
    """

    def __init__(self):

        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

        setting_sql = """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL
        )
        """

        diary_sql = """
        CREATE TABLE IF NOT EXISTS diaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            activity_log TEXT NOT NULL,
            comment TEXT,
            todo TEXT
        )
        """

        self.cursor.execute(setting_sql)
        self.cursor.execute(diary_sql)
        self.connection.commit()
        self.connection.close()
        
    def new_cursor(self):
        """
        新しいデータベース接続を返します。
        """
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        return self.connection.cursor()
    
    def close(self):
        """
        データベース接続を閉じます。
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
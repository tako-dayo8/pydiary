from dataclasses import dataclass

from db import db

@dataclass
class Diary:
    id: int
    created_at: str
    updated_at: str
    activity_log: str
    comment: str
    todo: str
    ai_comment: str

def get_diary_by_custom_sql(sql : str) -> list[Diary] | None:
    with db.new_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows:
            return [Diary(*row) for row in rows]
        else:
            return None


def get_diary_by_id(id : int) -> Diary | None:
    with db.new_connection() as conn:
        cursor = conn.cursor()
        sql = """
        SELECT id, created_at, updated_at, activity_log, comment, todo, ai_comment
        FROM diaries
        WHERE id = ?
        """
        cursor.execute(sql , (id))
        row = cursor.fetchone()
        if row:
            return Diary(*row)
        else:
            return None


def get_all_diarys() -> list[Diary] | None:
    with db.new_connection() as conn:
        cursor = conn.cursor()
        sql = """
        SELECT id, created_at, updated_at, activity_log, comment, todo, ai_comment
        FROM diaries
        ORDER BY id DESC
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows:
            return [Diary(*row) for row in rows]
        else:
            return None
        

def get_latest_diary() -> Diary | None:
    with db.new_connection() as conn:
        cursor = conn.cursor()
        sql = """
        SELECT id, created_at, updated_at, activity_log, comment, todo, ai_comment
        FROM diaries
        ORDER BY id DESC
        LIMIT 1
        """
        cursor.execute(sql)
        row = cursor.fetchone()
        if row:
            return Diary(*row)
        else:
            return None
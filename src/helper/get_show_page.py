import flet as ft

from db import db
from enum import IntEnum

class showPage(IntEnum):
    HISTORY = 0
    SAVE = 1

def get_show_page() -> showPage:
    # 現在の閲覧ページをデータベースから取得
    with db.new_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT value FROM settings WHERE key = 'show_page'")

        show_page = cursor.fetchone()

    if show_page is None:
        # デフォルトでHISTORYページを設定・保存
        with db.new_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO settings (key, value)
                VALUES ('show_page', ?)
                """,
                (showPage.HISTORY,),
            )
            conn.commit()

        return showPage.HISTORY
    else:
        return showPage(int(show_page[0]))
import flet as ft

from db import db

from helper.get_diary import get_all_diarys
from helper.logger import Logger , LogLevel

def remove_diary(e : ft.ControlEvent):
    """
    日記を削除する関数
    """
    page: ft.Page = e.page

    control: ft.Control = e.control
    
    # ListTileからタイトルとサブタイトルを取得
    list_tile: ft.ListTile = control.parent.parent.controls[0]
    # print(list_tile)
    title = list_tile.title.value
    Logger.log(LogLevel.INFO ,title)
    subtitle = list_tile.subtitle.value
    Logger.log(LogLevel.INFO , subtitle)

    # カードをページから削除
    page.controls[3].content.controls.remove(control.parent.parent.parent.parent)

    # DBから削除
    with db.new_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            """
            DELETE FROM diaries
            WHERE activity_log = ? AND comment = ?
            """,
            (title, subtitle)
        )

        conn.commit()

    diarys = get_all_diarys()

    # もし日記が一つもなくなったら
    if not diarys:
        # "まだ日記がありません。"のテキストを追加
        page.controls[3].content.controls.append(ft.Text("まだ日記がありません。"))

        # diariesテーブルのidをリセット
        with db.new_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(
                """
                UPDATE sqlite_sequence SET seq = 0 WHERE name = 'diaries'
                """
            )

            conn.commit()

    page.open(ft.SnackBar(
        ft.Text("日記を削除しました！"),
        bgcolor=ft.Colors.GREEN_500,
    ))

    page.update()
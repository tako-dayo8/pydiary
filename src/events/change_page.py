import flet as ft

from db import db
from helper.get_diary import get_all_diarys , get_latest_diary
from helper.get_show_page import showPage

from components.diary_card import create_diary_card
from components.diary_save_field import save_botton , activity_log_field , comment_field , todo_field

from helper.logger import Logger , LogLevel


def change_page(e : ft.ControlEvent):
    """
    ページを切り替える関数
    """

    page: ft.Page = e.page

    Logger.log(LogLevel.INFO , e.control.selected_index)
    if e.control.selected_index == 0:
        # 履歴ページに切り替え
        page.controls[3].content = ft.ListView(
            [
            ft.Column(
                    [
                        ft.Text("AIからの最新コメント", size=16, weight="bold"),
                        ft.Text(value=get_latest_diary().ai_comment, size=14) if get_latest_diary() else ft.Text("AIコメントはここに表示されます。", size=14),
                    ],
                    spacing=10,
            ),
            *([
                create_diary_card(diary.activity_log, diary.comment)
                for diary in get_all_diarys()
            ] if get_all_diarys() else [
                ft.Text("まだ日記がありません。")
            ]),
            ],
            expand=True,
            spacing=20,
        )

        page.floating_action_button = None

        with db.new_connection() as conn:
            cursor = conn.cursor()
                
            cursor.execute(
                    """
                    INSERT INTO settings (key, value)
                    VALUES (?, ?)
                    ON CONFLICT(key) DO UPDATE SET value=excluded.value
                    """,
                    ("show_page", showPage.HISTORY)
            )

            conn.commit()

    else:
        # 記録ページに切り替え
        page.controls[3].content = ft.Column(
            [
                activity_log_field,
                comment_field,
                todo_field,
            ],
            expand=True,
            spacing=20,
        )

        page.floating_action_button = save_botton


        with db.new_connection() as conn:
            cursor = conn.cursor()
                
            cursor.execute(
                    """
                    INSERT INTO settings (key, value)
                    VALUES (?, ?)
                    ON CONFLICT(key) DO UPDATE SET value=excluded.value
                    """,
                    ("show_page", showPage.SAVE)
            )

            conn.commit()
    
    # ページを更新して内容を反映
    page.update()
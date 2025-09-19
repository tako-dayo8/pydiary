import flet as ft
import datetime


from db import db
from gemini import generate_ai_comment_str

from components.diary_save_field import activity_log_field , comment_field , todo_field

from helper.logger import Logger , LogLevel

# test
# from time import sleep


def save_diary(e : ft.ControlEvent):
    """
    日記の内容を保存する関数
    """

    page: ft.Page
    page = e.page

    # ローディングダイアログを作成
    loading_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("保存中..."),
        content=ft.Column([
            ft.ProgressBar(width=400),
            ft.Text("AIコメントを生成しています...")
        ], height=100, alignment=ft.MainAxisAlignment.CENTER),
    )

    # ローディング表示
    page.open(loading_dialog)

    activity_log = activity_log_field.value
    comment = comment_field.value
    todo = todo_field.value
    ai_comment = generate_ai_comment_str(activity_log, comment, todo)

    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_at = created_at  # 保存時点の日時を使用

    # 入力チェック
    if not activity_log:
        # ローディング終了
        page.close(loading_dialog)
        
        page.open(ft.SnackBar(
            ft.Text("今日やったことは必須です！"),
            bgcolor=ft.Colors.RED_500,
        ))
        page.update()
        return
    
    Logger.log_dump(LogLevel.INFO , "=== Saving Diary ===")
    Logger.log_dump(LogLevel.INFO , f"Activity Log: {activity_log}")
    Logger.log_dump(LogLevel.INFO , f"Comment: {comment}")    
    Logger.log_dump(LogLevel.INFO , f"TODO: {todo}")
    Logger.log_dump(LogLevel.INFO , f"AI Comment: {ai_comment}")
    Logger.log_dump(LogLevel.INFO , f"Created At: {created_at}")
    Logger.log_dump(LogLevel.INFO , f"Updated At: {updated_at}")
    
    try:
        # データベースに保存
        with db.new_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO diaries (activity_log, comment, todo, created_at, updated_at , ai_comment)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (activity_log, comment, todo, created_at, updated_at , ai_comment)
            )

            conn.commit()

        # 保存後にフィールドをクリア
        activity_log_field.value = ""
        comment_field.value = ""
        todo_field.value = ""

        # test
        # sleep(5)

        # ローディング終了
        page.close(loading_dialog)

        page.open(ft.SnackBar(
            ft.Text("日記を保存しました！"),
            bgcolor=ft.Colors.GREEN_500,
        ))

        # ページを更新して内容を反映
        page.update()
    except Exception as e:
        Logger.log_dump(LogLevel.ERROR , f"Error saving diaries: {e}")

        # ローディング終了
        page.close(loading_dialog)

        page.open(ft.SnackBar(
            ft.Text("日記の保存に失敗しました。"),
            bgcolor=ft.Colors.RED_500,
        ))

        # ページを更新してエラーメッセージを反映
        page.update()
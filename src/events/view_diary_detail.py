import flet as ft

from components.diary_save_field import activity_log_field, comment_field, todo_field

from helper.logger import Logger, LogLevel
from helper.get_diary import get_diary_by_custom_sql, Diary

def edit_diary(e : ft.ControlEvent , dialog: ft.AlertDialog, diary: Diary):
    page: ft.Page = e.page

    page.close(dialog)

    # 新しいフィールドを作成（既存のフィールドを直接使用しない）
    edit_activity_log_field = ft.TextField(
        label="今日やったこと",
        multiline=True,
        min_lines=3,
        max_lines=5,
        value=diary.activity_log
    )
    
    edit_comment_field = ft.TextField(
        label="コメント",
        multiline=True,
        min_lines=2,
        max_lines=3,
        value=diary.comment if diary.comment else ""
    )
    
    edit_todo_field = ft.TextField(
        label="TODO",
        multiline=True,
        min_lines=2,
        max_lines=3,
        value=diary.todo if diary.todo else ""
    )

    ai_comment = diary.ai_comment if diary.ai_comment else "なし"

    edit_diary_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("日記の編集"),
        content=ft.Column([  # ft.Columnでラップ
            edit_activity_log_field,
            edit_comment_field,
            edit_todo_field,
            ft.Text("AIコメント（編集不可）:", weight="bold"),
            ft.Text(ai_comment),
        ],
        height=400,
        width=500,
        scroll=ft.ScrollMode.AUTO,
        spacing=10),
        actions=[
            # ft.TextButton("保存", on_click=lambda e: save_edited_diary(e, edit_diary_dialog, diary, edit_activity_log_field, edit_comment_field, edit_todo_field)),
            ft.TextButton("閉じる", on_click=lambda e: page.close(edit_diary_dialog))
        ],
    )

    page.open(edit_diary_dialog)

    page.update()
    return

def view_diary_detail(e : ft.ControlEvent):

    page: ft.Page = e.page
    control: ft.Control = e.control

    list_title = control.parent.parent.controls[0]

    title = list_title.title.value
    subtitle = list_title.subtitle.value

    Logger.log(LogLevel.INFO , f"Title: {title}, Subtitle: {subtitle}")


    sql = f"""
    SELECT id, created_at, updated_at, activity_log, comment, todo, ai_comment
    FROM diaries
    WHERE activity_log = '{title}' AND comment = '{subtitle}'
    """

    diarys = get_diary_by_custom_sql(sql)

    if not diarys:
        page.open(ft.SnackBar(
            ft.Text("日記の詳細を取得できませんでした。"),
            bgcolor=ft.Colors.RED_500,
        ))
        page.update()
        return
    
    diary = diarys[0]

    detail_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("日記の詳細"),
        content=ft.Column(
            [
                ft.Text(f"作成日時: {diary.created_at}"),
                ft.Text(f"更新日時: {diary.updated_at}"),
                ft.Divider(),
                ft.Text("今日やったこと:", weight="bold"),
                ft.Text(diary.activity_log),
                ft.Divider(),
                ft.Text("コメント:", weight="bold"),
                ft.Text(diary.comment if diary.comment else "なし"),
                ft.Divider(),
                ft.Text("TODO:", weight="bold"),
                ft.Text(diary.todo if diary.todo else "なし"),
                ft.Divider(),
                ft.Text("AIからのコメント:", weight="bold"),
                ft.Text(diary.ai_comment if diary.ai_comment else "なし"),
            ],
            scroll="auto",
            height=400,
            width=500,
            spacing=10,
        ),  
        actions=[
            ft.TextButton("編集" , on_click=lambda e: edit_diary(e , detail_dialog , diary)),
            ft.TextButton("閉じる", on_click=lambda e: page.close(detail_dialog))
        ],
    )

    page.open(detail_dialog)
    page.update()
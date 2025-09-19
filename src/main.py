import flet as ft

from gemini import generate_ai_comment

# helper
from helper.get_theme import get_theme
from helper.get_show_page import get_show_page , showPage
from helper.get_diary import  get_all_diarys , get_latest_diary

# events
from events.change_theme import chenge_theme
from events.change_page import change_page
from events.save_diary import save_diary

# components
from components.theme_mode_toggle import theme_mode_toggle
from components.diary_save_field import activity_log_field , comment_field , todo_field , save_botton
from components.diary_card import create_diary_card


def main(page: ft.Page):
    global theme_mode_toggle , activity_log_field , comment_field , todo_field # グローバル変数として宣言

    # ページの初期設定
    page.title = "PyDiary"
    # スクロールを可能にする
    page.scroll = ft.ScrollMode.AUTO
    # ページのテーマモードをデータベースから取得
    page.theme_mode = get_theme()
    # デフォルトの大きさを設定
    page.window.width = 550
    page.window.height = 650


    pages = [
        # 履歴ページ
        ft.ListView(
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
        ),
        # 記録ページ
        ft.Column(
            [
                activity_log_field,
                comment_field,
                todo_field,
            ],
            expand=True,
            spacing=20,
        )
    ]

    # アイコンボタンのクリックイベントに関数を割り当て
    theme_mode_toggle.on_click = chenge_theme

    # フローティングアクションボタンのクリックイベントに関数を割り当て
    save_botton.on_click = save_diary

    # フローティングアクションボタンをページに追加
    if get_show_page() == showPage.HISTORY:
        page.floating_action_button = None
    else:
        page.floating_action_button = save_botton


    page.add(
        ft.AppBar(
            title=ft.Text("PyDiary"),
            actions=[
                theme_mode_toggle
            ]
        ),
        ft.Text("Welcome to PyDiary!"),
        ft.Row(
            [
                ft.CupertinoSlidingSegmentedButton(
                    selected_index=get_show_page(),
                    thumb_color=ft.Colors.BLUE_400,
                    on_change=change_page,
                    controls=[
                        ft.Text("履歴"),
                        ft.Text("記録"),
                    ],
                ),
            ],
            width=550,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Container(
            content=pages[get_show_page()],
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
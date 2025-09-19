import flet as ft

from db import db

from components.diary_save_field import activity_log_field , comment_field , todo_field
from components.theme_mode_toggle import theme_mode_toggle

def chenge_theme(e : ft.ControlEvent):
        """
        ページのテーマモードを切り替える関数
        """
        
        page: ft.Page

        page = e.page

        # ページのテーマモードを切り替える
        if page.theme_mode == ft.ThemeMode.DARK:
            # テーマモードをライトに変更
            page.theme_mode = ft.ThemeMode.LIGHT

            # フローティングアクションボタンのアイコンを変更
            if page.floating_action_button:
                page.floating_action_button.bgcolor= ft.Colors.LIME_300

            # テキストフィールドのボーダーカラーを変更
            activity_log_field.border_color = ft.Colors.BLACK
            comment_field.border_color = ft.Colors.BLACK
            todo_field.border_color = ft.Colors.BLACK
        else:
            # テーマモードをダークに変更
            page.theme_mode = ft.ThemeMode.DARK

            # フローティングアクションボタンのアイコンを変更
            if page.floating_action_button:
                page.floating_action_button.bgcolor = ft.Colors.BLUE_600

            # テキストフィールドのボーダーカラーを変更
            activity_log_field.border_color = ft.Colors.BLUE_300
            comment_field.border_color = ft.Colors.BLUE_300
            todo_field.border_color = ft.Colors.BLUE_300

        # アイコンを切り替える
        theme_mode_toggle.icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.LIGHT_MODE
        
        # データベースにテーマ設定を保存
        with db.new_connection() as conn:
            cursor = conn.cursor()
                
            cursor.execute(
                    """
                    INSERT INTO settings (key, value)
                    VALUES (?, ?)
                    ON CONFLICT(key) DO UPDATE SET value=excluded.value
                    """,
                    ("theme_mode", page.theme_mode.value)
            )

            conn.commit()

        # ページを更新してテーマの変更を反映
        page.update()
import datetime , winreg , platform

import flet as ft


from db import DatabaseManager

db = DatabaseManager()

def main(page: ft.Page):

    def get_theme():
        """
        現在のテーマモードをデータベースから取得する関数
        データベースに保存されていない場合はデフォルトのダーク
        将来的にosのテーマ設定を取得する機能を追加する予定
        """
        # 現在のテーマモードをデータベースから取得
        cursor = db.new_cursor()
        try:
            cursor.execute("SELECT value FROM settings WHERE key = 'theme_mode'")
            theme_mode = cursor.fetchone()

            if theme_mode is None:
                if platform.system() == "Windows":
                    # Windowsのテーマ設定を取得
                    try:
                        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
                            theme_mode_value = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
                            if theme_mode_value == 0:
                                return ft.ThemeMode.DARK
                            else:
                                return ft.ThemeMode.LIGHT
                    except:
                        # 何かしらのエラーが発生した場合はデフォルトでダークモードを使用
                        return ft.ThemeMode.DARK
                else:
                    # 他のOSではデフォルトでダークモードを使用
                    return ft.ThemeMode.DARK
            else:
                return ft.ThemeMode(theme_mode[0])

        finally:
            db.close()

    # ページの初期設定
    page.title = "PyDiary"
    # ページのテーマモードをデータベースから取得
    page.theme_mode = get_theme()

    def chenge_theme(e):
        # ページのテーマモードを切り替える
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT

            # フローティングアクションボタンのアイコンを変更
            page.floating_action_button.bgcolor = ft.Colors.LIME_300

            # テキストフィールドのボーダーカラーを変更
            activity_log_field.border_color = ft.Colors.BLACK
            comment_field.border_color = ft.Colors.BLACK
            todo_field.border_color = ft.Colors.BLACK
        else:
            page.theme_mode = ft.ThemeMode.DARK

            # フローティングアクションボタンのアイコンを変更
            page.floating_action_button.bgcolor = ft.Colors.BLUE_600

            # テキストフィールドのボーダーカラーを変更
            activity_log_field.border_color = ft.Colors.BLUE_300
            comment_field.border_color = ft.Colors.BLUE_300
            todo_field.border_color = ft.Colors.BLUE_300

        # アイコンを切り替える
        dark_mode_toggle.icon = ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.LIGHT_MODE
        
        # データベースにテーマ設定を保存
        cursor = db.new_cursor()

        try:
            cursor.execute(
                """
                INSERT INTO settings (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
                """,
                ("theme_mode", page.theme_mode.value)
            )

            db.connection.commit()
        finally:
            db.close()
            

        # ページを更新してテーマの変更を反映
        page.update()

    def save_diary(e):
        """
        日記の内容を保存する関数
        """
    
        activity_log = activity_log_field.value
        comment = comment_field.value
        todo = todo_field.value

        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_at = created_at  # 保存時点の日時を使用

        # 入力チェック
        if not activity_log:
            page.open(ft.SnackBar(
                ft.Text("今日やったことは必須です！"),
                bgcolor=ft.Colors.RED_500,
            ))
            page.update()
            return

        print(f"Activity Log: {activity_log}")
        print(f"Comment: {comment}")    
        print(f"TODO: {todo}")
        print(f"Created At: {created_at}")
        print(f"Updated At: {updated_at}")
        
        # データベースに保存
        cursor = db.new_cursor()
        try:
            cursor.execute(
                """
                INSERT INTO diaries (activity_log, comment, todo, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (activity_log, comment, todo, created_at, updated_at)
            )
            db.connection.commit()

            # 保存後にフィールドをクリア
            activity_log_field.value = ""
            comment_field.value = ""
            todo_field.value = ""

            page.open(ft.SnackBar(
                ft.Text("日記を保存しました！"),
                bgcolor=ft.Colors.GREEN_500,
            ))
            page.update()
        except Exception as e:
            print(f"Error saving diaries: {e}")
            page.open(ft.SnackBar(
                ft.Text("日記を保存しました！"),
                bgcolor=ft.Colors.RED_500,
            ))
            page.update()
        finally:
            db.close()

    dark_mode_toggle = ft.IconButton(
        icon=ft.Icons.DARK_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.LIGHT_MODE,
        tooltip="ダークモード切替",
        on_click=chenge_theme,
    )


    hint_text_style = ft.TextStyle(
        color=ft.Colors.GREY_500,
    )

    textfield_border_color = ft.Colors.BLUE_300 if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.BLACK

    activity_log_field = ft.TextField(
        label="今日やったこと", 
        border_color=textfield_border_color,
        hint_text="今日の活動や出来事を記録",
        hint_style=hint_text_style,
        multiline=True, 
    )

    comment_field = ft.TextField(
        label="コメント", 
        border_color=textfield_border_color,
        hint_text="コメントや感想など",
        hint_style=hint_text_style,
        multiline=True, 
    )

    todo_field = ft.TextField(
        label="今後やること、TODO", 
        border_color=textfield_border_color,
        hint_text="TODOや目標など",
        hint_style=hint_text_style,
        multiline=True, 
    )

    # フローティングアクションボタンの設定
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, 
        on_click=save_diary, 
        bgcolor=ft.Colors.LIME_300 if page.theme_mode == ft.ThemeMode.LIGHT else ft.Colors.BLUE_600,
    )
    page.add(
        ft.AppBar(
            title=ft.Text("PyDiary"),
            actions=[
                dark_mode_toggle,
            ]
        ),
        ft.Text("Welcome to PyDiary!"),
        ft.Column(
            [
                activity_log_field,
                comment_field,
                todo_field,
            ],
            expand=True,
            spacing=20,
        ),
    )






if __name__ == "__main__":
    ft.app(target=main)

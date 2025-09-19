import platform
import winreg
import flet as ft

from db import db
from helper.logger import Logger , LogLevel

def get_theme()-> ft.ThemeMode:
        """
        現在のテーマモードをデータベースから取得する関数
        データベースに保存されていない場合はデフォルトのダーク
        将来的にosのテーマ設定を取得する機能を追加する予定
        """
        # 現在のテーマモードをデータベースから取得
        with db.new_connection() as conn:
            cursor = conn.cursor()

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
                except Exception as e:
                    Logger.log_dump(LogLevel.Error , f"Error retrieving Windows theme: {e}")
                    # 何かしらのエラーが発生した場合はデフォルトでダークモードを使用
                    return ft.ThemeMode.DARK
            else:
                # 他のOSではデフォルトでダークモードを使用
                return ft.ThemeMode.DARK
        else:
            return ft.ThemeMode(theme_mode[0])
        

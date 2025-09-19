import flet as ft

from helper.get_theme import get_theme

global theme_mode_toggle

theme_mode_toggle = ft.IconButton(
            icon=ft.Icons.DARK_MODE if get_theme() == ft.ThemeMode.DARK else ft.Icons.LIGHT_MODE,
            tooltip="ダークモード切替",
        )


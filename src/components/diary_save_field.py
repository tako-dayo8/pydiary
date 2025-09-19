import flet as ft

from helper.get_theme import get_theme

global hint_text_style, textfield_border_color ,activity_log_field, comment_field, todo_field, save_button

hint_text_style = ft.TextStyle(
            color=ft.Colors.GREY_500,
        )

textfield_border_color = ft.Colors.BLUE_300 if get_theme() == ft.ThemeMode.DARK else ft.Colors.BLACK

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

save_botton = ft.FloatingActionButton(
            icon=ft.Icons.ADD,  
            bgcolor=ft.Colors.LIME_300 if get_theme() == ft.ThemeMode.LIGHT else ft.Colors.BLUE_600,
        )


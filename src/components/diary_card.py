import flet as ft

from events.remove_diary import remove_diary
from events.view_diary_detail import view_diary_detail

def create_diary_card(title: str, subtitle: str) -> ft.Card:
    """履歴カードを作成する"""
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.NOTES, color=ft.Colors.BLUE ),
                        title=ft.Text(title),
                        subtitle=ft.Text(subtitle),
                    ),
                    ft.Row(
                        [ft.TextButton("詳細" , on_click=view_diary_detail), ft.TextButton("削除" ,  on_click=remove_diary)],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ]
            ),
            width=500,
            padding=10,
        ),
        width=550,
        shadow_color=ft.Colors.ON_SURFACE_VARIANT,
)

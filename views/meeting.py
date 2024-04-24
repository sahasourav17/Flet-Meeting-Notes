from views.navbar import navbar_item
import flet as ft
from flet_route import Params, Basket


def MeetingView(page: ft.Page, params: Params, basket: Basket):
    def handle_add_meeting(e):
        page.go("/add-meeting")

    def show_meeting():
        pass

    def row_with_alignment(align: ft.MainAxisAlignment):
        return ft.Row(
            [
                ft.Text(
                    "Your Meetings",
                    size=30,
                    color=ft.colors.BLACK,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.IconButton(
                    icon=ft.icons.ADD_ROUNDED,
                    icon_color="red400",
                    icon_size=40,
                    tooltip="Add Meeting",
                    adaptive=True,
                    padding=ft.padding.only(top=6),
                    on_click=handle_add_meeting,
                ),
            ],
            alignment=align,
        )

    def card_data(title, datetime):
        return [
            ft.ListTile(
                leading=ft.Icon(ft.icons.CALENDAR_MONTH),
                title=ft.Text(datetime),
                is_three_line=False,
            ),
            ft.ListTile(
                leading=ft.Icon(ft.icons.SUBJECT),
                title=ft.Text(title),
                is_three_line=False,
            ),
            ft.Row(
                [ft.TextButton("View Details")],
                alignment=ft.MainAxisAlignment.END,
            ),
        ]

    def row_with_card(data):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(data),
            )
        )

    controls = [
        row_with_alignment(ft.MainAxisAlignment.SPACE_BETWEEN),
        row_with_card(card_data("Project Kickoff", "March 01, 2024")),
        row_with_card(card_data("Catch Up Meeting", "Feb 29, 2024")),
        row_with_card(card_data("Session", "Feb 26, 2024")),
        navbar_item(page),
    ]
    return ft.View(controls=controls, scroll=ft.ScrollMode.AUTO)

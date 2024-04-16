from views.navbar import navbar_item
import flet as ft
from flet_route import Params,Basket
def HomeView(page: ft.Page, params: Params, basket: Basket ):
    def row_with_alignment(align: ft.MainAxisAlignment):
        return ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                       [
                        ft.IconButton(
                            icon=ft.icons.MIC,
                            icon_color="red400",
                            icon_size=80,
                            tooltip="Start record",
                            on_click=handle_record_route,
                        ),
                      ], 
                      alignment=align
                    ),
                    # bgcolor=ft.colors.AMBER_100,
                ),
            ]
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
                width=480,
            )
        )
 
    
    def handle_record_route(e):
        e.page.go('/record')
    
    controls=[
        row_with_alignment(ft.MainAxisAlignment.CENTER),
        ft.Text(
            "Recent Meetings",
            size=30,
            color=ft.colors.BLACK,
            weight=ft.FontWeight.NORMAL,
        ),
        row_with_card(card_data("Project Kickoff", "March 01, 2024")),
        row_with_card(card_data("Catch Up Meeting", "Feb 29, 2024")),
        row_with_card(card_data("Session", "Feb 26, 2024")),
        navbar_item(page)
    ]
    return ft.View(controls=controls, scroll=ft.ScrollMode.AUTO)
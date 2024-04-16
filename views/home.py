from views.navbar import navbar_item
import flet as ft
from flet_route import Params,Basket
def HomeView(page: ft.Page, params: Params, basket: Basket ):
    def handle_record_route(e):
        e.page.go('/record')
    
    controls = [
            ft.Text("Home", size=30, weight="bold"),
            ft.ElevatedButton("go to record", on_click=handle_record_route),
            navbar_item(page)
        ]
    return ft.View(controls=controls)
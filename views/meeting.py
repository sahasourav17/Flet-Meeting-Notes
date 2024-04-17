from views.navbar import navbar_item
import flet as ft
from flet_route import Params, Basket


def MeetingView(page: ft.Page, params: Params, basket: Basket):
    controls = [ft.Text("Meeting", size=30, weight="bold"), navbar_item(page)]
    return ft.View(controls=controls)

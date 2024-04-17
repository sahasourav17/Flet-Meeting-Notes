import flet as ft
import helper_functions as helper_func
import os
from flet_route import Routing, path
from views.home import HomeView
from views.help import HelpView
from views.meeting import MeetingView
from views.settings import SettingsView
from views.record import RecordView


async def main(page: ft.Page):
    page.window_width = 500

    # Disable animation transition
    theme = ft.Theme()
    page.theme = theme
    page.update()
    # Define app routes
    app_routes = [
        path(url="/", clear=True, view=HomeView),
        path(url="/record", clear=True, view=RecordView),
        path(url="/meetings", clear=True, view=MeetingView),
        path(url="/settings", clear=True, view=SettingsView),
        path(url="/help", clear=True, view=HelpView),
    ]

    Routing(page=page, app_routes=app_routes)

    page.go(page.route)


ft.app(main)

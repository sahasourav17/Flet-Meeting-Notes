import flet as ft


def navbar_item(page: ft.Page):
    def change_page(e, page):
        print(page.route)
        print(e.control.selected_index)

        if e.control.selected_index == 0:
            page.go("/")
            page.update()

        if e.control.selected_index == 1:
            page.go("/meetings")
            page.update()

        if e.control.selected_index == 2:
            page.go("/settings")
            page.update()

        if e.control.selected_index == 3:
            page.go("/help")
            page.update()

        page.update()

    def get_selected_index(route):
        route_mapping = {
            "/": 0,
            "/meetings": 1,
            "/settings": 2,
            "/help": 3,
            "/add-meeting": 1,
        }
        return route_mapping.get(route, 0)

    navigation_bar = ft.NavigationBar(
        selected_index=get_selected_index(page.route),
        on_change=lambda e: change_page(e, page),
        destinations=[
            ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
            ft.NavigationDestination(icon=ft.icons.HANDSHAKE, label="Meeting"),
            ft.NavigationDestination(
                icon=ft.icons.SETTINGS,
                label="Settings",
            ),
            ft.NavigationDestination(
                icon=ft.icons.HELP,
                label="Help",
            ),
        ],
    )

    return navigation_bar

import flet as ft


def navbar_item(page: ft.Page):
  def change_page(e, page):
    print(page.route)
    print(e.control.selected_index)

    if e.control.selected_index == 0:
      page.go("/")
      page.update()

    if e.control.selected_index == 1:
      page.go("/about")
      page.update()

    if e.control.selected_index == 2:
      page.go("/contact")
      page.update()

    if e.control.selected_index == 3:
      page.go("/record")
      page.update()
      
    page.update()

  navigation_bar = ft.NavigationBar(
    on_change=lambda e:change_page(e, page),
    destinations=[
      ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
      ft.NavigationDestination(icon=ft.icons.HANDSHAKE, label="Meeting"),
      ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings",),
      ft.NavigationDestination(icon=ft.icons.HELP, label="Help",),
    ]
  )

  return navigation_bar
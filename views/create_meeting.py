from views.navbar import navbar_item
import flet as ft
from flet_route import Params, Basket
import datetime


def CreateMeetingView(page: ft.Page, params: Params, basket: Basket):

    def meeting_form(page: ft.Page):
        def change_date(e):
            print(f"Date picker changed, value is {date_picker.value}")

        def date_picker_dismissed(e):
            print(f"Date picker dismissed, value is {date_picker.value}")

        date_picker = ft.DatePicker(
            on_change=change_date,
            on_dismiss=date_picker_dismissed,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )

        def change_time(e):
            print(f"Time picker changed, value  is {time_picker.value}")

        def dismissed(e):
            print(f"Time picker dismissed, value is {time_picker.value}")

        time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            on_change=change_time,
            on_dismiss=dismissed,
        )
        
        page.overlay.append(date_picker)
        page.overlay.append(time_picker)

        def handle_cancel_meeting(e):
            e.page.go("/meetings")

        def handle_save_meeting(e):
            print(f"Meeting Title -> {title.value}")
            print(f"Meeting Description -> {description.value}")
            print(f"Participants -> {participants.value}")
            print(f"Date -> {date_picker.value}")
            print(f"Time -> {time_picker.value}")
            e.page.go("/meetings")

        title = ft.TextField(
            label="Meeting Title",
            adaptive=True,
            dense=True,
        )
        description = ft.TextField(
            label="Description",
            multiline=True,
            max_lines=10,
            adaptive=True,
        )
        participants = ft.TextField(
            label="Participants",
            multiline=True,
            adaptive=True,
            dense=True,
        )
        return ft.ResponsiveRow(
            [
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                title,
                                description,
                                participants,
                                ft.ResponsiveRow(
                                    [
                                        ft.ElevatedButton(
                                            "Select date",
                                            icon=ft.icons.CALENDAR_MONTH,
                                            on_click=lambda _: date_picker.pick_date(),
                                        ),
                                        ft.ElevatedButton(
                                            "Select time",
                                            icon=ft.icons.ACCESS_TIME_ROUNDED,
                                            on_click=lambda _: time_picker.pick_time(),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            adaptive=True,
                        ),
                        padding=ft.padding.all(30),
                    ),
                ),
                ft.Row(
                    [
                        ft.FilledTonalButton(
                            "Cancel",
                            icon=ft.icons.CANCEL_OUTLINED,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                bgcolor=ft.colors.RED_400,
                            ),
                            on_click=handle_cancel_meeting,
                        ),
                        ft.FilledTonalButton(
                            "Save",
                            icon=ft.icons.SAVE_OUTLINED,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                bgcolor=ft.colors.BLUE_300,
                            ),
                            on_click=handle_save_meeting,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ]
        )

    controls = [
        ft.Text("Provide meeting information", size=24, weight="bold", no_wrap="wrap"),
        meeting_form(page),
        navbar_item(page),
    ]
    return ft.View(controls=controls, scroll=ft.ScrollMode.AUTO)

from views.navbar import navbar_item
import flet as ft
from flet_route import Params,Basket
import helper_functions as helper_func
import os

# variables
gcs_bucket_name = 'repl-audio-meeting-notes'
audio_file_path = './audio_files/async.wav'

transcribed_text = ft.Text(value="")

def control_buttons_row(align: ft.MainAxisAlignment):
    buttons = [
        ft.IconButton(
            icon=ft.icons.PLAY_CIRCLE,
            icon_color="red400",
            icon_size=20,
            tooltip="Start",
            on_click=handle_start_recording,
        ),
        ft.IconButton(
            icon=ft.icons.STOP_CIRCLE,
            icon_color="red400",
            icon_size=20,
            tooltip="Stop",
            on_click=handle_stop_recording,
        ),
        ft.IconButton(
            icon=ft.icons.SAVE,
            icon_color="red400",
            icon_size=20,
            tooltip="Save",
            on_click=handle_save_recording,
        ),
    ]
    return ft.Column(
        [
            ft.Container(
                content=ft.Row(buttons, alignment=align),
                bgcolor=ft.colors.AMBER_100,
                border_radius= ft.border_radius.only(0, 0, 8, 8)
            ),
        ]
    )

def show_audio_spectrum_with_control():
    return ft.Card(
        content= ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.ALBUM),
                        title=ft.Text("Meeting Notes"),
                        subtitle=ft.Text(
                            "Record your meeting and get summary of the meeting in ease"
                        ),
                    ),
                    control_buttons_row(ft.MainAxisAlignment.CENTER)
                ]
            )
        )
    )
    
def show_transcribed_meeting():
    return ft.Card(
        content= ft.Container(
            transcribed_text,
            padding=8,
            expand=1
        )
    )
    

def RecordView(page: ft.Page, params: Params, basket: Basket ):
    controls = [
            ft.Text("Record", size=30, weight="bold"),
            show_audio_spectrum_with_control(),
            ft.ElevatedButton('Transcribe Meeting', on_click=handle_transcribe_meeting),
            show_transcribed_meeting(),
            navbar_item(page)
        ]
    return ft.View(controls=controls)


async def handle_transcribe_meeting(e):
    long_text = await helper_func.translate_longer_audio_to_text(audio_file_path)
    print(f'long text: {long_text}')
    transcribed_text.value = long_text
    e.page.update()


async def handle_start_recording(_):
    pass

async def handle_stop_recording(_):
    pass

async def handle_save_recording(_):
    pass
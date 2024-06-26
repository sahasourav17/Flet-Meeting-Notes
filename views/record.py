import os
import datetime
import flet as ft
from flet_route import Params, Basket
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import tkinter as tk
from tkinter import filedialog
from views.navbar import navbar_item
import helper_functions as helper_func

# variables
recording = False
recording_thread = None
recording_buffer = []
transcribed_text = ft.Text(value="")
status_text = ft.Text(value="")
recorded_filename = ""


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
            icon=ft.icons.PAUSE_CIRCLE_ROUNDED,
            icon_color="red400",
            icon_size=20,
            tooltip="Pause",
            on_click=handle_pause_recording,
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
                border_radius=ft.border_radius.only(0, 0, 8, 8),
            ),
        ]
    )


def show_audio_spectrum_with_control():
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.ALBUM),
                        title=ft.Text("Meeting Notes"),
                        subtitle=status_text,
                    ),
                    control_buttons_row(ft.MainAxisAlignment.CENTER),
                ]
            )
        )
    )


def handle_edit_modal(e):
    def close_dlg(e):
        dlg_modal.open = False
        e.page.update()

    def handle_save_note(e):
        transcribed_text.value = dlg_modal.content.value
        close_dlg(e)

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Notes"),
        content=ft.TextField(
            value=transcribed_text.value,
            text_size=12,
            multiline=True,
            min_lines=1,
            max_lines=10,
        ),
        actions=[
            ft.TextButton("Save", on_click=handle_save_note),
            ft.TextButton("Cancel", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    e.page.dialog = dlg_modal
    dlg_modal.open = True
    e.page.update()


def show_transcribed_meeting():
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Column(
                        [
                            transcribed_text,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip="Edit",
                                on_click=handle_edit_modal,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=10,
            alignment=ft.alignment.center,
            width="full",
            height=150,
            border=ft.border.all(1, ft.colors.BLACK),
            border_radius=10,
        )
    )


def save_notes_buttons_row(page: ft.Page, align: ft.MainAxisAlignment):
    global transcribed_text, recorded_filename

    def save_note_file(e: ft.FilePickerResultEvent):
        save_location = e.path
        print(f"location of the file: {save_location}")
        if save_location:
            try:
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")

                file_content = f"Meeting Notes\nDate: {current_date}\n\n"
                file_content += transcribed_text.value

                with open(save_location, "w", encoding="utf-8") as file:
                    file.write(file_content)
            except Exception as e:
                print(f"Error: {e}")
        page.update()

    print("format: %s" % format)
    file_picker = ft.FilePicker(on_result=save_note_file)
    page.overlay.append(file_picker)

    buttons = [
        ft.FilledTonalButton(
            content=ft.Text("Save as Docx", size=16),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=lambda _: file_picker.save_file(allowed_extensions=["docx"]),
        ),
        ft.FilledTonalButton(
            content=ft.Text("Save as PDF", size=16),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=lambda _: file_picker.save_file(allowed_extensions=["pdf"]),
        ),
    ]
    return ft.Container(
        content=ft.Column(
            [
                ft.Container(content=ft.Row(buttons, alignment=align)),
            ],
            tight=True,
        ),
        adaptive=True,
        padding=ft.padding.only(top=16),
    )


def RecordView(page: ft.Page, params: Params, basket: Basket):
    global recording, recording_buffer, recording_thread, recorded_filename
    transcribed_text.value = "Transcribed meeting will be appeared here..."
    status_text.value = "Record and Transcribe your meeting instantly"
    recording = False
    recording_buffer = []
    recording_thread = None
    recorded_filename = ""
    controls = [
        ft.Text("Record", size=30, weight="bold"),
        show_audio_spectrum_with_control(),
        ft.ElevatedButton("Transcribe Meeting", on_click=handle_transcribe_meeting),
        show_transcribed_meeting(),
        save_notes_buttons_row(page, ft.MainAxisAlignment.CENTER),
        navbar_item(page),
    ]
    return ft.View(controls=controls)


async def handle_transcribe_meeting(e):
    long_text = await helper_func.translate_longer_audio_to_text(recorded_filename)
    print(f"long text: {long_text}")
    transcribed_text.value = long_text
    e.page.update()


async def handle_start_recording(e):
    global recording, recording_thread
    if not recording:
        recording = True
        status_text.value = "Recording started..."
        e.page.update()
        sd.default.channels = 1
        sd.default.samplerate = 44100
        sd.default.dtype = "int16"
        recording_thread = sd.InputStream(callback=audio_callback)
        recording_thread.start()


def audio_callback(indata, frames, time, status):
    global recording, recording_buffer
    if status:
        print(status)
    if recording:
        recording_buffer.append(indata.copy())


async def handle_pause_recording(e):
    global recording, recording_thread
    recording = False
    status_text.value = "Recording paused."
    e.page.update()


async def handle_stop_recording(e):
    global recording, recording_thread
    recording = False
    status_text.value = "Recording stopped. You can now save the recording."
    recording_thread.stop()
    e.page.update()


async def handle_save_recording(e):
    global recording_buffer, recorded_filename, recording_thread, recording
    if recording_buffer:
        fs = 44100
        recorded_content = np.concatenate(recording_buffer, axis=0)
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        filename = filedialog.asksaveasfilename(
            parent=root,
            defaultextension=".wav",
            filetypes=[
                ("Wave files", "*.wav"),
                ("MP3 files", "*.mp3"),
                ("M4A files", "*.m4a"),
            ],
        )
        if filename:
            write(filename, fs, recorded_content)
            recorded_filename = filename
            print(f"Recording saved to {recorded_filename}")
            status_text.value = f"Recording saved to {recorded_filename}"
        else:
            status_text.value = "Please enter a valid filename."
        recording_buffer = []
        recording = False
        e.page.update()
        root.destroy()

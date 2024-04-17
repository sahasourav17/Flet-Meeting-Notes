import os
import flet as ft
from flet_route import Params,Basket
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import tkinter as tk
from tkinter import filedialog
from views.navbar import navbar_item
import helper_functions as helper_func

# variables
# audio_file_path = './audio_files/ee.wav'
recording = False
recording_thread = None
recording_buffer = []
transcribed_text = ft.Text(value="")
status_text = ft.Text(value="")
recorded_filename=""

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
                        subtitle=status_text,
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
    global recording, recording_buffer, recording_thread, recorded_filename
    transcribed_text.value = ''
    status_text.value = 'Record and Transcribe your meeting instantly'
    recording = False
    recording_buffer = []
    recording_thread = None
    recorded_filename = ''
    controls = [
            ft.Text("Record", size=30, weight="bold"),
            show_audio_spectrum_with_control(),
            ft.ElevatedButton('Transcribe Meeting', on_click=handle_transcribe_meeting),
            show_transcribed_meeting(),
            navbar_item(page)
        ]
    return ft.View(controls=controls)


async def handle_transcribe_meeting(e):
    long_text = await helper_func.translate_longer_audio_to_text(recorded_filename)
    print(f'long text: {long_text}')
    transcribed_text.value = long_text
    e.page.update()


async def handle_start_recording(e):
    global recording, recording_thread
    if not recording:
        recording = True
        status_text.value = 'Recording started...'
        e.page.update()
        sd.default.channels = 1
        sd.default.samplerate = 44100
        sd.default.dtype = 'int16'
        recording_thread = sd.InputStream(callback=audio_callback)
        recording_thread.start()
def audio_callback(indata, frames, time, status):
    global recording, recording_buffer
    if status:
        print(status)
    if recording:
        recording_buffer.append(indata.copy())
        
async def handle_pause_recording(e):
    global recording,recording_thread
    recording = False
    status_text.value = "Recording paused."
    e.page.update()

async def handle_stop_recording(e):
    global recording
    recording = False
    status_text.value = "Recording stopped. You can now save the recording."
    recording_thread.stop()
    e.page.update()

async def handle_save_recording(e):
    global recording_buffer,recorded_filename,recording_thread, recording
    if recording_buffer:
        fs = 44100
        recorded_content = np.concatenate(recording_buffer, axis=0)
        root = tk.Tk() 
        root.withdraw()
        root.attributes('-topmost', True)
        filename = filedialog.asksaveasfilename(
            parent=root,
            defaultextension=".wav", 
            filetypes=[("Wave files", "*.wav"), ("MP3 files", "*.mp3"), ("M4A files", "*.m4a")]
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
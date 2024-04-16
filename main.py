import flet as ft
import helper_functions as helper_func
import os
from flet_route import Routing, path
from flet_route import Params, Basket
from views.navbar import navbar_item
from views.record import RecordView
from views.home import HomeView



url = "https://github.com/mdn/webaudio-examples/blob/main/audio-analyser/viper.mp3?raw=true"
audio_file_path = 'audio_files/async.wav'
gcs_bucket_name = 'repl-audio-meeting-notes'

# async def main(page: ft.Page):
#     async def volume_down(_):
#         audio1.volume -= 0.1
#         await audio1.update_async()

#     async def volume_up(_):
#         audio1.volume += 0.1
#         await audio1.update_async()


#     async def play(_):
#         await audio1.play_async()

#     async def pause(_):
#         await audio1.pause_async()

#     async def resume(_):
#         await audio1.resume_async()

#     async def get_duration(_):
#         print("Current position:", await audio1.get_duration_async())
        
#     async def navigate_to_record(_):
#         page.go("/record")
#         page.update()
        
#     async def upload_to_gcs(_):
#         print('Setting google cloud creds into environment variables...')
#         helper_func.load_gc_creds()

#         temp_audio_file_path = audio_file_path
        
#         if not os.path.exists(temp_audio_file_path):
#                 print(f"The file {temp_audio_file_path} does not exist.")
#                 return None
            
#         # Convert audio file to wav if necessary
#         if audio_file_path.endswith('.mp3') or audio_file_path.endswith('.m4a'):
#             file_format = audio_file_path.split('.')[-1]
#             print(f'file format: {file_format}')
            

#         # Upload audio file to GCS
#         print(f'Uploading {temp_audio_file_path} to GCS...')
#         dest_audio_file_path = audio_file_path.split('/')[-1].split('.')[0] + '.wav'
#         print(f'Uploading {audio_file_path} to GCS as {dest_audio_file_path}')

#         gcs_uri = await helper_func.upload_blob(bucket_name=gcs_bucket_name,
#                                 source_file_name=temp_audio_file_path,
#                                 destination_blob_name=dest_audio_file_path)
        
#         print(f'Uploaded {temp_audio_file_path} to GCS as {dest_audio_file_path}')
#         print(f'gcs uri: {gcs_uri}')

#     audio1 = ft.Audio(
#         src=url,
#         autoplay=False,
#         volume=1,
#         balance=0,
#         on_loaded=lambda _: print("Loaded"),
#         on_duration_changed=lambda e: print("Duration changed:", e.data),
#         on_position_changed=lambda e: print("Position changed:", e.data),
#         on_state_changed=lambda e: print("State changed:", e.data),
#         on_seek_complete=lambda _: print("Seek complete"),
#     )
#     page.overlay.append(audio1)
#     await page.add_async(
#         ft.ElevatedButton("Play", on_click=play),
#         ft.ElevatedButton("Pause", on_click=pause),
#         ft.ElevatedButton("Resume", on_click=resume),
        
#         ft.Row(
#             [
#                 ft.ElevatedButton("Volume down", on_click=volume_down),
#                 ft.ElevatedButton("Volume up", on_click=volume_up),
#             ]
#         ),
#         ft.ElevatedButton(
#             "Get current position",
#             on_click=get_duration,
#         ),
#         ft.ElevatedButton('upload to GCS', on_click=upload_to_gcs),
#         ft.ElevatedButton('go to record page', on_click=navigate_to_record),
#     )
   
   
   

async def main(page: ft.Page):
    page.window_width = 500

    # Disable animation transition
    theme = ft.Theme()
    page.theme = theme
    page.update()
    
    # await page.add_async(
    #     ft.ElevatedButton("Play"),
    # )
    

    # Define app routes
    app_routes = [
        path(
            url="/",
            clear=True,
            view=HomeView
        ),
        path(
            url="/record",
            clear=True,
            view=RecordView
        ),
    ]

    Routing(
        page=page,
        app_routes=app_routes
    )

    page.go(page.route) 
    
# def record_route(page: ft.Page, params: Params, basket: Basket ):
#     controls = [
#             ft.Text("Record", size=30, weight="bold"),
#             navbar_item(page)
#         ]
#     return ft.View(controls=controls)
    
# def home_route(page: ft.Page,params: Params, basket: Basket):
#     controls = [
#             ft.Text("homepage", size=30, weight="bold"),
#             navbar_item(page)
#         ]
#     return ft.View(controls=controls)

ft.app(main)

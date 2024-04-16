import os
import json
import subprocess
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from google.cloud import storage
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import translate_v2 as translate

load_dotenv()

gcs_bucket_name = os.environ.get('GCS_BUCKET_NAME')

def load_gc_creds():
  google_creds_json = os.environ.get('GOOGLE_CLOUD_TRANSLATE_API_KEY_JSON')
  if google_creds_json is None:
    raise ValueError("The GOOGLE_CLOUD_TRANSLATE_API_KEY is not set.")
  google_creds_dict = json.loads(google_creds_json)
  with open('tmp/google_creds.json', 'w') as creds_file:
    json.dump(google_creds_dict, creds_file)
  os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'tmp/google_creds.json'

async def upload_blob(bucket_name, source_file_name, destination_blob_name):
  """Uploads a file to the bucket."""
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)
  blob.upload_from_filename(source_file_name)
  return f'gs://{bucket_name}/{destination_blob_name}'


def convert_to_wav(self, file_path, format):
    print(f'Converting {file_path} from {format} format to wav format...')
    try:
        audio = AudioSegment.from_file(file_path, format)
        temp_file = "audio_files/temp_audio.wav"
        audio.export(temp_file, format="wav")
        print(f'Converted {temp_file} to wav format.')
        return temp_file
    except CouldntDecodeError as e:
        print(f"An error occurred while decoding the audio file: {file_path}")
        print(str(e))
        # For further debugging, use ffprobe to get the stderr output
        try:
            result = subprocess.run(
                ["ffprobe", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
        except Exception as e:
            print(f"An error occurred while running ffprobe: {e}")
        return False
      
      

async def transcribe_gcs(gcs_uri, language_code='en-US'):
  client = speech.SpeechClient()

  alternative_language_codes = ['en-US', 'en-GB', 'en-IN', 'bn-IN']
  # if gcs_uri
  audio = speech.RecognitionAudio(uri=gcs_uri)
  config = speech.RecognitionConfig(
      encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
      sample_rate_hertz=44100,
      language_code=language_code,
      alternative_language_codes=alternative_language_codes,
      enable_automatic_punctuation=True,
      audio_channel_count = 1,
      use_enhanced=True,
      model='latest_long')

  operation = client.long_running_recognize(config=config, audio=audio, timeout=90)

  print("Waiting for operation to complete...")
  response = operation.result(timeout=90)

  # Transcription results
  transcripts = []
  for result in response.results:
    transcripts.append(result.alternatives[0].transcript)
  return transcripts


async def translate_text(text, target_language="en"):
  translate_client = translate.Client()
  translation = translate_client.translate(text,
                                           target_language=target_language)
  return translation['translatedText']


async def translate_longer_audio_to_text(audio_file_path):
  # Set google cloud creds into environment variables
  print('Setting google cloud creds into environment variables...')
  load_gc_creds()

  temp_audio_file_path = audio_file_path
  
  if not os.path.exists(temp_audio_file_path):
        print(f"The file {temp_audio_file_path} does not exist.")
        return None
      
  # Convert audio file to wav if necessary
  if audio_file_path.endswith('.mp3') or audio_file_path.endswith('.m4a'):
    file_format = audio_file_path.split('.')[-1]
    print(f'file format: {file_format}')
    # print(f'audio file path: {file_path}')
    temp_audio_file_path = await convert_to_wav(audio_file_path, file_format)
    

  # Upload audio file to GCS
  print(f'Uploading {temp_audio_file_path} to GCS...')
  dest_audio_file_path = audio_file_path.split('/')[-1].split('.')[0] + '.wav'
  print(f'Uploading {audio_file_path} to GCS as {dest_audio_file_path}')

  gcs_uri = await  upload_blob(bucket_name=gcs_bucket_name,
                        source_file_name=temp_audio_file_path,
                        destination_blob_name=dest_audio_file_path)
  
  print(f'Uploaded {temp_audio_file_path} to GCS as {dest_audio_file_path}')
  print(f'gcs uri: {gcs_uri}')

  # Transcribe audio file to text
  transcription_results = await  transcribe_gcs(gcs_uri, language_code='bn-BD')
  print(f'transcribed_result -> {transcription_results}')

  # Translate the transcription to English
  translations = []
  for text in transcription_results:
    print(f'{text} | ')
    translations.append(await translate_text(text, target_language="en"))
    
  print(f'------------translations------------ {translations}')

  long_text = ''
  for translated_text in translations:
    long_text += translated_text + '. '

  return long_text

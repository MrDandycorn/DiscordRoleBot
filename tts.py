from google.cloud import texttospeech
from google.oauth2 import service_account
from google.cloud import translate_v3beta1 as translate

import io
from credentials import googleProjectID

credentials = service_account.Credentials.from_service_account_file('service.json')
ttsClient = texttospeech.TextToSpeechClient(credentials=credentials)
translateClient = translate.TranslationServiceClient(credentials=credentials)


def detect_language(text):
    location = 'global'
    parent = translateClient.location_path(googleProjectID, location)
    response = translateClient.detect_language(parent=parent, content=text)
    lang_code = response.languages[0].language_code
    return lang_code


def tts(text):
    lang_code = detect_language(text)
    voice_name = get_voice(lang_code)
    synthesis_input = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=lang_code,
        name=voice_name,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = ttsClient.synthesize_speech(synthesis_input, voice, audio_config)
    return response.audio_content


def get_voice(lang_code):
    response = ttsClient.list_voices(language_code=lang_code)
    for voice in response.voices:
        if ('Wavenet' in voice.name) and (voice.ssml_gender == 1):
            return voice.name


def create_mp3(text):
    mp3bytes = tts(text)
    with io.open('output.mp3', 'wb') as out:
        out.write(mp3bytes)

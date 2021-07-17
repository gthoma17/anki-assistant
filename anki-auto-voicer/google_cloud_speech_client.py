import os
from google.cloud import texttospeech


def __set_credentials():
    creds_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    creds_file = os.path.join(creds_folder, "google_creds.secret.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_file


def __audio_config():
    return texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )


def __voice_config(language_code, gender):
    return texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=gender.for_voice()
    )


def __text_to_speech(text, file_name, voice):
    __set_credentials()
    client = texttospeech.TextToSpeechClient()
    audio_config = __audio_config()
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(text=text),
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(file_name, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
    return file_name


def text_to_speech(text, voice_language, voice_gender, file_name=None):
    file_name = file_name if file_name is not None else f"{text}.mp3"
    voice = __voice_config(voice_language, voice_gender)
    return __text_to_speech(text, file_name, voice)

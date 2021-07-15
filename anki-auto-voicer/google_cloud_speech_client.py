import os
from google.cloud import texttospeech

def main():
	text_to_speech("Hello World", "Hello, world")
	
def _set_credentials():
	creds_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	creds_file = os.path.join(creds_folder, "google_creds.secret.json")
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_file



def _audio_config():
	return texttospeech.AudioConfig(
	    audio_encoding=texttospeech.AudioEncoding.MP3
	)

def _voice_config():
	return texttospeech.VoiceSelectionParams(
	    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
	)

def text_to_speech(text, file_name, voice=_voice_config()): 
	_set_credentials()
	client = texttospeech.TextToSpeechClient()
	response = client.synthesize_speech(
	    input=texttospeech.SynthesisInput(text=text), 
	    voice=voice, 
	    audio_config=_audio_config()
	)

	# The response's audio_content is binary.
	with open(f"{file_name}.mp3", "wb") as out:
	    # Write the response to the output file.
	    out.write(response.audio_content)
	    print(f'Audio content written to file "{file_name}.mp3"')

if __name__ == '__main__':
	main()
import os

from google_cloud_speech_client import text_to_speech
from operations.helpers import get_spoken_text_from_card, replace_card_text


def perform(deck, args):
    for note_index in range(0, len(deck["notes"])):
        note = deck["notes"][note_index]

        spoken_text = get_spoken_text_from_card(note, args.unspoken_separator, args.face)
        audio_path = text_to_speech(
            spoken_text,
            args.language,
            args.gender,
            file_name=f"{args.output_folder}/media/{spoken_text}.mp3"
        )
        deck = _add_audio_to_face_of_note(audio_path, note_index, args, deck)
    return deck





def _add_audio_to_face_of_note(audio_path, note_index, args, deck):
    note_text = deck["notes"][note_index]["fields"][args.face.field_index()]
    file_name = os.path.basename(audio_path)
    sound_reference = f"[sound:{file_name}]"

    if "[sound:" not in note_text:
        replace_card_text(args, deck, note_index, f'{note_text}{sound_reference}')
        deck["media_files"].append(file_name)
        print(f"Added {file_name} to the {str(args.face)} of the card for {note_text}")
    else:
        print(f"Skipping, this card already has a sound: {note_text}")

    return deck

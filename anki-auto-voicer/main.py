import sys, json, os, argparse, enum
from google_cloud_speech_client import text_to_speech
from google.cloud.texttospeech import SsmlVoiceGender


class EnumWithStr(enum.Enum):
    def __str__(self):
        return self.value


class Gender(EnumWithStr):
    neutral = 'neutral'
    female = 'female'
    male = 'male'

    def for_voice(self):
        return SsmlVoiceGender[str(self.value).upper()]


class Face(EnumWithStr):
    front = "front"
    back = "back"

    def field_index(self):
        face_to_index = {
            "front": 0,
            "back": 1
        }
        return face_to_index[self.value]


class Operation(EnumWithStr):
    add = 'add'
    remove = 'remove'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_folder", help="The Anki deck folder", type=str)
    parser.add_argument('--language', '-l',
                        help="language code (any BCP-47 compliant language code should work, but only en-US and ja-JP have been tested)",
                        type=str,
                        default='en-US'
                        )
    parser.add_argument('--gender', '-g',
                        help="gender for the voice to speak with (don't read this as an author's opinion on gender -- this is an API limitation ;-))",
                        type=Gender,
                        choices=list(Gender),
                        default=Gender.neutral)
    parser.add_argument('--face', '-f',
                        help="Which face of the card should we apply the operation to (default front)",
                        type=Face,
                        choices=list(Face),
                        default=Face.front)
    parser.add_argument('--unspoken_seperator', '-s',
                        help="A substring afterwhich text should be ignored and not sent to the cloud for text-to-speech (useful for hints or notes)",
                        type=str,
                        default="<br />")
    parser.add_argument('--operation', '-o',
                        help="What operation the script should perform (adding or removing)",
                        type=Operation,
                        choices=list(Operation),
                        default=Operation.add)

    return parser.parse_args()

def remove_audio_from_face_of_note(note_index, face, deck):
    note_text = deck["notes"][note_index]["fields"][face.field_index()]
    start_index = note_text.find("[sound:")
    end_index = note_text.find("]", start_index)

    if start_index != -1 and end_index != -1:
        new_note_text = f"{note_text[0:start_index]}{note_text[end_index:-1]}"
        deck["notes"][note_index]["fields"][face.field_index()] = new_note_text
        print(f"Removed sound from the {str(face)} of the card for {note_text}")
    else:
        print(f"Skipping, this card already has no sound: {note_text}")

    return deck

def add_audio_to_face_of_note(audio_path, note_index, face, deck):
    note_text = deck["notes"][note_index]["fields"][face.field_index()]
    file_name = os.path.basename(audio_path)
    sound_reference = f"[sound:{file_name}]"

    if "[sound:" not in note_text:
        deck["notes"][note_index]["fields"][face.field_index()] = f'{note_text}{sound_reference}'
        deck["media_files"].append(file_name)
        print(f"Added {file_name} to the {str(face)} of the card for {note_text}")
    else:
        print(f"Skipping, this card already has a sound: {note_text}")

    return deck


def get_spoken_text_from_card(card, seperator):
    if seperator is None:
        return card['fields'][0]
    else:
        return card['fields'][0].split(seperator)[0]


def main():
    args = get_args()
    with open(f"{args.output_folder}/deck.json", 'r') as deck_file:
        deck = json.load(deck_file)

    for note_index in range(0, len(deck["notes"])):
        note = deck["notes"][note_index]

        if args.operation == Operation.add:
            spoken_text = get_spoken_text_from_card(note, args.unspoken_seperator)
            audio_path = text_to_speech(
                spoken_text,
                args.language,
                args.gender,
                file_name=f"{args.output_folder}/media/{spoken_text}.mp3"
            )
            deck = add_audio_to_face_of_note(audio_path, note_index, args.face, deck)

        elif args.operation == Operation.remove:
            deck = remove_audio_from_face_of_note(note_index, args.face, deck)

        with open(f"{args.output_folder}/deck.json", 'w') as deck_file:
            json.dump(deck, deck_file)


if __name__ == '__main__':
    main()

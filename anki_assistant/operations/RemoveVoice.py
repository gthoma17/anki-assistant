from operations.helpers import replace_card_text, remove_sound_references_from_string

def perform(deck, args):
    for note_index in range(0, len(deck["notes"])):
        deck = _remove_audio_from_face_of_note(note_index, args, deck)


def _remove_audio_from_face_of_note(note_index, args, deck):
    note_text = deck["notes"][note_index]["fields"][args.face.field_index()]
    new_note_text = remove_sound_references_from_string(note_text)
    replace_card_text(args, deck, note_index, new_note_text)
    print(f"Removed sound from the card for {new_note_text}")

    return deck

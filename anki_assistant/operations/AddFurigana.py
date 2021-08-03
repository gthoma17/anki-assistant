from operations.helpers import get_raw_text_from_card, replace_card_text


def perform(deck, args):
    for note_index in range(0, len(deck["notes"])):
        card_text = get_raw_text_from_card(deck["notes"][note_index], args)

        # Get the furigana to add
        furigana_to_add = []
        for character_index, character in enumerate(card_text):
            if _is_kanji(character):
                furigana = _get_furigana(card_text, character, character_index)
                kanji_with_ruby = f"<ruby>{character}<rt>{furigana}</rt></ruby>"
                furigana_to_add.append({
                    "character": character,
                    "index": character_index,
                    "kanji_with_ruby": kanji_with_ruby
                })

        # add them back to front
        furigana_to_add.reverse()
        for furigana in furigana_to_add:
            card_text = get_raw_text_from_card(deck["notes"][note_index], args)
            new_card_text = card_text[0:furigana["index"]] + \
                            furigana["kanji_with_ruby"] + \
                            card_text[furigana["index"] + 1:-1]
            replace_card_text(args, deck, note_index, new_card_text)


def _is_kanji(character):
    if 0x4E00 <= ord(character) <= 0x9FFF:  # main blocks
        return True
    elif 0x3400 <= ord(character) <= 0x4DBF:  # extended block A
        return True
    elif 0x20000 <= ord(character) <= 0x2A6DF:  # extended block B
        return True
    elif 0x2A700 <= ord(character) <= 0x2B73F:  # extended block C
        return True
    else:
        return False


def _get_furigana(card_text, character, index):
    furigana = input(f"What is the furigana for {character} in the following sentence\n"
                     f"{card_text[0:index]}「{character}」{card_text[index + 1:-1]}\n"
                     f">>> ")
    return furigana


def _do_thing(note_index, args, deck):
    card_text = get_raw_text_from_card(deck["notes"][note_index], args)

    furigana_to_add = []
    for character_index, character in enumerate(card_text):
        if _is_kanji(character):
            furigana = _get_furigana(card_text, character, character_index)
            kanji_with_ruby = f"<ruby>{character}<rt>{furigana}</rt></ruby>"
            furigana_to_add.append({
                "character": character,
                "index": character_index,
                "kanji_with_ruby": kanji_with_ruby
            })
    furigana_to_add.reverse()
    for furigana in furigana_to_add:
        card_text = get_raw_text_from_card(deck["notes"][note_index], args)
        new_card_text = card_text[0:furigana["index"]] + \
                        furigana["kanji_with_ruby"] + \
                        card_text[furigana["index"] + 1:-1]
        replace_card_text(args, deck, note_index, new_card_text)

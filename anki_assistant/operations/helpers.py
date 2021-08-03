def remove_substring_by_delimiters(super_string, first_delimiter, second_delimiter):
    while first_delimiter in super_string:
        substring_start = super_string.find(first_delimiter)
        substring_end = super_string.find(second_delimiter, substring_start) + len(second_delimiter)
        super_string = super_string[0:substring_start] + super_string[substring_end:-1]
    return super_string


def remove_rubies_from_string(card_text):
    card_text = remove_substring_by_delimiters(card_text, "<rt>", "</rt>")
    card_text = card_text.replace("<ruby>", "")
    card_text = card_text.replace("</ruby>", "")
    return card_text


def remove_sound_references_from_string(card_text):
    return remove_substring_by_delimiters(card_text, "[sound:", "]")


def get_spoken_text_from_card(card, args):
    card_text = card['fields'][args.face.field_index()]

    if args.unspoken_separator is not None:
        card_text = card_text.split(args.unspoken_separator)[0]

    card_text = remove_sound_references_from_string(card_text)
    card_text = remove_rubies_from_string(card_text)
    card_text = card_text.replace("&nbsp;", "")

    return card_text


def get_raw_text_from_card(card, args):
    return card['fields'][args.face.field_index()]


def replace_card_text(args, deck, note_index, new_text):
    deck["notes"][note_index]["fields"][args.face.field_index()] = new_text

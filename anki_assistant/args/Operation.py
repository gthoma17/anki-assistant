from operations import AddVoice, RemoveVoice, AddFurigana
from args.Argument import Argument


class Operation(Argument):
    add_speech = 'add_speech'
    remove_speech = 'remove_speech'
    add_furigana = 'add_furigana'

    def get_method(self):
        names_to_methods = {
            'add_speech': AddVoice.perform,
            'remove_speech': RemoveVoice.perform,
            'add_furigana': AddFurigana.perform
        }
        return names_to_methods[self.value]

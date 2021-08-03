from args.Argument import Argument
from google.cloud.texttospeech_v1 import SsmlVoiceGender


class Gender(Argument):
    neutral = 'neutral'
    female = 'female'
    male = 'male'

    def for_voice(self):
        return SsmlVoiceGender[str(self.value).upper()]

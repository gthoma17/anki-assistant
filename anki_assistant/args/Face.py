from args.Argument import Argument


class Face(Argument):
    front = "front"
    back = "back"

    def field_index(self):
        face_to_index = {
            "front": 0,
            "back": 1
        }
        return face_to_index[self.value]

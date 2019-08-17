from .annotation import Annotation

class Text(Annotation):

    def __init__(self, msg, position):

        super(Text, self).__init__()

        self.msg = msg
        self.position = position

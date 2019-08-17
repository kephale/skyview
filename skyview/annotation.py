from multiprocessing import Value

_next_id = Value('I', 0)

class Annotation:

    def __init__(self):

        with _next_id.get_lock():

            self.id = _next_id.value
            _next_id.value += 1

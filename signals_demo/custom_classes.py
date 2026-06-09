class Rectangle:
    """
    A Rectangle class that yields its dimensions (length first, then width)
    in the form of dictionaries when iterated over.
    """
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}

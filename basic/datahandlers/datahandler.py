class DataHandler:
    def __init__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

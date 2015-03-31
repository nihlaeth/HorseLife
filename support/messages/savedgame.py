from message import Message


class SavedGame(Message):
    def __init__(self, file_name):
        self.file_name = file_name

    def __str__(self):
        return self.file_name

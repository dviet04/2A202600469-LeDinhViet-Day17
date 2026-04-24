# ShortTermMemory: manages recent conversation buffer

class ShortTermMemory:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > self.window_size * 2:
            self.messages = self.messages[-self.window_size * 2:]

    def get_messages(self):
        return self.messages[-self.window_size * 2:]

from shared.singleton import Singleton

@Singleton
class Settings(object):
    def __init__(self):
        self.width = 800
        self.height = 480
class SystemManager:
    def __init__(self):
        pass

    def show(self):
        raise NotImplementedError

    def create(self):
        raise NotImplementedError

    def add(self, system):
        raise NotImplementedError

    def remove(self, system):
        raise NotImplementedError

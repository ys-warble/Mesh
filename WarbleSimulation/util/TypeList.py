class TypeList(list):
    def __init__(self, type):
        super().__init__()
        self.type = type

    def append(self, new_item):
        if not isinstance(object, self.type):
            raise TypeError('item is not of type %s' % self.type)
        self.append(new_item)

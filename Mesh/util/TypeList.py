class TypeList(list):
    def __init__(self, type):
        super().__init__()
        self.type = type

    def append(self, new_item):
        if not isinstance(new_item, self.type):
            raise TypeError('item is not of type %s' % self.type)
        super(TypeList, self).append(new_item)

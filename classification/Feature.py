class Feature:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return 'Feature[' + self.name + ', ' + str(self.value) + ']'

    def __repr__(self):
        return self.__str__()

class Input:
    def __init__(self, path):
        self.path = path

    def parse(self):
        """Parse the file given the path and return a list of strings containing each line"""
        f = open(self.path)
        text = f.read()
        return text.split("\n")

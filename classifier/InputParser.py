class InputParser:
    def __init__(self, path, train):
        self.path = path
        self.train = train

    def parse(self):
        f = open(self.path)
        text = f.read()
        if self.train:
            split_text = [path[19:].split(" ") for path in text.split("\n") if path]
            repo_ids = [t[0] for t in split_text]
            labels = [t[1] for t in split_text]
            return repo_ids, labels
        else:
            return [path[19:] for path in text.split("\n") if path]


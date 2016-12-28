class InputParser:
    def __init__(self, text, train):
        self.text = text
        self.train = train

    def parse(self):
        if self.train:
            split_text = [path[19:].split(" ") for path in self.text.split("\n") if path]
            repo_ids = [t[0] for t in split_text]
            labels = [t[1] for t in split_text]
            return repo_ids, labels
        else:
            return [path[19:] for path in self.text.split("\n") if path], []

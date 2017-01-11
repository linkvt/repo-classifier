class InputParser:
    def __init__(self, text, train):
        self.text = text
        self.train = train

    def parse(self):
        lines = [line.rstrip() for line in self.text.split('\n') if line]
        if self.train:
            del lines[0]
            split_text = [line.split(",") for line in lines]
            repo_ids = [t[0] for t in split_text]
            labels = [t[1] for t in split_text]
            return repo_ids, labels
        else:
            return lines, []

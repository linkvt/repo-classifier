class InputParser:
    def __init__(self, text, train):
        self.text = text
        self.train = train

    def parse(self):
        lines = [line.rstrip() for line in self.text.split('\n') if line]
        if self.train:
            separator = " "
            # Input with commas
            if len(lines[0].split(",")) == 2:
                separator = ","
                del lines[0]
            split_text = [line.split(separator) for line in lines]
            urls = [t[0].rstrip('/') for t in split_text]
            labels = [t[1] for t in split_text]
            return urls, labels
        else:
            return lines, []

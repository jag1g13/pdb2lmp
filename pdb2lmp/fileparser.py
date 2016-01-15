
class FileParser:
    def __init__(self, filename):
        self.filename = filename
        self.section = None
        self.curr_line = 0
        self.find_prev = None

        with open(filename) as f:
            self.lines = f.readlines()

    def getline(self, required=0):
        while True:
            if self.curr_line >= len(self.lines):
                return None

            line = self.lines[self.curr_line].strip()
            self.curr_line += 1

            if line == "":
                continue
            if line[0] in [";", "#"]:
                continue
            if line[0] == "[":
                self.section = line.strip("[ ]")
                continue

            break

        toks = line.split()
        while len(toks) < required:
            toks.append(None)
        return toks

    def findsection(self, section):
        self.rewind()

        while self.section != section:
            if self.getline() is None:
                return False

        return True

    def getlinefromsection(self, section):
        if section != self.find_prev:
            self.rewind()
        self.find_prev = section

        while True:
            line = self.getline()
            if line is None:
                break
            if self.section == section:
                return line

        return None

    def nextsection(self):
        while self.curr_line < len(self.lines):
            line = self.lines[self.curr_line].strip()
            self.curr_line += 1
            if line is not "" and line[0] == "[":
                self.section = line.strip("[ ]")
                return self.section
        return None

    def rewind(self):
        self.curr_line = 0

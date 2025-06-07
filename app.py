

class Parser:
    def __init__(self, filename):
        with open(filename, "r") as file:
            arr = []
            for line in file:
                if line.strip().startswith("/"):
                    continue
                if not line.strip():
                    continue
                arr.append(line.strip())
            self.lines = arr
    def print_lines(self):
        for line in self.lines:
            print(line)

obj = Parser("test.asm")
obj.print_lines()
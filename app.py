

class Parser:
    def __init__(self):
        with open("test.asm", "r") as file:
            for line in file:
                print((line.strip()))

obj = Parser()
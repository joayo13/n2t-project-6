

class Parser:
    def __init__(self, filename):
        with open(filename, "r") as file:
            # open file and extract all needed lines from file
            arr = []
            for line in file:
                # remove comment lines
                if line.strip().startswith("/"):
                    continue
                # remove blank lines
                if not line.strip():
                    continue
                arr.append(line.strip())
            self.lines = arr
            # initialize variables needed to step through lines
            self.current_command: str = None
            self.command_counter: int = 0
    
    def has_more_commands(self):
        if self.command_counter >= len(self.lines):
            return False
        return True
    
    def advance(self):
        if self.has_more_commands():
            self.current_command = self.lines[self.command_counter]
            self.command_counter += 1
        

    def print_lines(self):
        for line in self.lines:
            self.advance()
            print(self.dest())
    
    def command_type(self):
        if self.current_command.startswith("@"):
            return "COMMAND_A"
        elif self.current_command.startswith("("):
            return "COMMAND_L"
        else:
            return "COMMAND_C"

    def symbol(self):
        if self.command_type() == "COMMAND_A":
            return self.current_command.strip("@")
        elif self.command_type() == "COMMAND_L":
            return self.current_command.strip("()")
    def dest(self):
        if self.command_type() == "COMMAND_C":
            if "=" in self.current_command:
                return self.current_command.split("=")[0]
    def comp(self): 
        if self.command_type() == "COMMAND_C":
            if "=" in self.current_command:
                return self.current_command.split("=")[1]
    def jump(self):
        if self.command_type() == "COMMAND_C":
            if ";" in self.current_command:
                return self.current_command.split(";")[1]

parsed = Parser("test.asm")


class Code:
    def __init__(self):
        self.dest_bin = "0b"
        self.comp_bin = "0b"
        self.jump_bin = "0b"
    def comp(self):
        match parsed.comp():
            case "0":
                self.comp_bin += "0101010"
            case "1":
                self.comp_bin += "0111111"
            case "-1":
                self.comp_bin += "0111010"
            case "D":
                self.comp_bin += "0001100"
            case "A":
                self.comp_bin += "0110000"
            case "!D":
                self.comp_bin += "0001101"
            case "!A":
                self.comp_bin += "0110001"
            case "-D":
                self.comp_bin += "0001111"
            case "-A":
                self.comp_bin += "0110011"
            case "D+1":
                self.comp_bin += "0011111"
            case "A+1":
                self.comp_bin += "0110111"
            case "D-1":
                self.comp_bin += "0001110"
            case "A-1":
                self.comp_bin += "0110010"
            case "D+A":
                self.comp_bin += "0000010"
            case "D-A":
                self.comp_bin += "0010011"
            case "A-D":
                self.comp_bin += "0000111"
            case "D&A":
                self.comp_bin += "0000000"
            case "D|A":
                self.comp_bin += "0010101"
            case "M":
                self.comp_bin += "1110000"
            case "!M":
                self.comp_bin += "1110001"
            case "-M":
                self.comp_bin += "1110011"
            case "M+1":
                self.comp_bin += "1110111"
            case "M-1":
                self.comp_bin += "1110010"
            case "D+M":
                self.comp_bin += "1000010"
            case "D-M":
                self.comp_bin += "1010011"
            case "M-D":
                self.comp_bin += "1000111"
            case "D&M":
                self.comp_bin += "1000000"
            case "D|M":
                self.comp_bin += "1010101"
            case _:
                raise ValueError("Invalid comp mnemonic")
parsed.advance()
parsed.advance()
coded = Code()
coded.dest()
print(coded.dest_bin)

                
            
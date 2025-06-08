

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
    def dest(self):
        match parsed.dest():
            case None:
                self.dest_bin += "000"
            case "M":
                self.dest_bin += "001" 
            case "D":
                self.dest_bin += "010" 
            case "MD":
                self.dest_bin += "011" 
            case "A":
                self.dest_bin += "100" 
            case "AM":
                self.dest_bin += "101" 
            case "AD":
                self.dest_bin += "110" 
            case "AMD":
                self.dest_bin += "111" 
coded = Code()
coded.dest()
print(coded.dest_bin)

                
            
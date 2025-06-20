

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
        
    def is_constant(self):
        if self.command_type() == "COMMAND_A":
            return self.symbol().isnumeric()
        
    def dest(self):
        if self.command_type() == "COMMAND_C":
            if "=" in self.current_command:
                return self.current_command.split("=")[0]
    def comp(self): 
        if self.command_type() == "COMMAND_C":
            if "=" in self.current_command:
                return self.current_command.split("=")[1]
            elif ";" in self.current_command:
                return self.current_command.split(";")[0]
    def jump(self):
        if self.command_type() == "COMMAND_C":
            if ";" in self.current_command:
                return self.current_command.split(";")[1]

DEST_TABLE = {
    None:  "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111"
}

COMP_TABLE = {
    # a=0
    "0"  : "0101010",
    "1"  : "0111111",
    "-1" : "0111010",
    "D"  : "0001100",
    "A"  : "0110000",
    "!D" : "0001101",
    "!A" : "0110001",
    "-D" : "0001111",
    "-A" : "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    # a=1
    "M"  : "1110000",
    "!M" : "1110001",
    "-M" : "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

JUMP_TABLE = {
    None:  "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

class Code:
    def __init__(self, command_type):
        if command_type == "COMMAND_C":
            self.bin = "111"
        else:
            self.bin = "0"
    def dest(self, mnemonic):
        try:
            self.bin += DEST_TABLE[mnemonic]
        except KeyError:
            raise ValueError(f"Invalid dest mnemonic: {mnemonic}")
    def comp(self, mnemonic):
        try:
            self.bin += COMP_TABLE[mnemonic]
        except KeyError:
            raise ValueError(f"Invalid comp mnemonic: {mnemonic}")
    def jump(self, mnemonic):
        try:
            self.bin += JUMP_TABLE[mnemonic]
        except KeyError:
            raise ValueError(f"Invalid jump mnemonic: {mnemonic}")

# test symbolless asm
class SymbolTable:
    def __init__(self):
        self.table = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7, 
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576,
        }
    def add_entry(self, name, address):
        self.table[name] = address
    
    def contains(self, name):
        if name in self.table:
            return True
        return False
    def get_address(self, name):
        return self.table[name] 

parsed = Parser("test.asm")
symbol_table = SymbolTable()

with open("out.hack", "w") as outfile:
    rom_address = 0
    ram_address = 16
    
    for line in parsed.lines:

        parsed.advance()

        if parsed.command_type() == "COMMAND_A" or parsed.command_type() == "COMMAND_C":
            rom_address += 1
        
        elif parsed.command_type() == "COMMAND_L":
            if not symbol_table.contains(parsed.symbol()):
                symbol_table.add_entry(parsed.symbol(), rom_address)

    parsed.command_counter = 0

    for line in parsed.lines:
        
        parsed.advance()

        if parsed.is_constant():
            extracted_symbol = parsed.symbol()
            outfile.write(format(int(extracted_symbol), '016b') + "\n")
        
        elif parsed.command_type() == "COMMAND_A":
            # if its not a constant, its a variable assignment and we'll add it to the symbol table and/or write its saved ram_address
            if not symbol_table.contains(parsed.symbol()):
                symbol_table.add_entry(parsed.symbol(), ram_address)
                ram_address += 1
            outfile.write(format(int(symbol_table.table[parsed.symbol()]), '016b') + "\n")

        elif parsed.command_type() == "COMMAND_C":
            coded = Code(parsed.command_type())
            coded.comp(parsed.comp())
            coded.dest(parsed.dest())
            coded.jump(parsed.jump())
            outfile.write(coded.bin + "\n")
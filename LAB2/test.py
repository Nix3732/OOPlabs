import enum
from typing import Dict, Tuple, List
from dataclasses import dataclass


COLORING = "\033[{}m{}"
PLACING = "\033[{};{}H{}"


class Color(enum.Enum):
    TRANSPARENT = 0
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    DEFAULT = 39


@dataclass
class SymbolTemplate:           
    char: str
    lines: List[str]
    width: int


class Printer:
    templates: Dict[str, SymbolTemplate] = {}          
    
    @classmethod
    def load_font(cls, filename: str):              
        with open(filename, 'r', encoding='utf-8') as f:
            current_char = None
            current_lines = []
            
            for line in f:
                line = line.rstrip('\n')
                if not line and current_char is None:
                    continue
                
                if line.startswith('CHAR:'):            
                    if current_char is not None:
                        width = max(len(l) for l in current_lines) if current_lines else 0
                        cls.templates[current_char] = SymbolTemplate(current_char, current_lines, width)         
                    current_char = line[5:].strip().upper()
                    current_lines = []
                else:
                    current_lines.append(line)
            
            if current_char is not None:
                width = max(len(l) for l in current_lines) if current_lines else 0
                cls.templates[current_char] = SymbolTemplate(current_char, current_lines, width)           
    
    @classmethod
    def move_cursor(cls, x: int, y: int):          
        print(f"\033[{y};{x}H", end='')
    
    @classmethod
    def set_color(cls, color: Color):             
        print(f"\033[{color.value}m", end='')
    
    @classmethod
    def reset_console(cls):                
        print('\033[49m', end='')
    
    @classmethod
    def clear_screen(cls):
        print("\033[2J", end='')
        print("\033[H", end='')
    
    @classmethod
    def print_text(cls, text: str, color: Color = Color.DEFAULT, 
                   position: Tuple[int, int] = (1, 1), symbol: str = '*'):           

        x, y = position
        height = 5
        
        for line_num in range(height):
            cls.move_cursor(x, y + line_num)
            cls.set_color(color)
            
            current_x = x
            for char in text.upper():
                if char == ' ':                
                    current_x += 3                 
                    continue
                    
                if char in cls.templates:
                    template = cls.templates[char]
                    if line_num < len(template.lines):
                        line = template.lines[line_num]
                        printed_line = ''.join(symbol if c != ' ' else ' ' for c in line)         
                        print(f"\033[{y + line_num};{current_x}H{printed_line}", end='')
                    current_x += template.width + 1
                else:
                    print(f"\033[{y + line_num};{current_x}H{symbol * 5}", end='')
                    current_x += template.width + 1
        
        cls.reset_console()
    
    def __init__(self, color: Color = Color.DEFAULT, 
                 position: Tuple[int, int] = (1, 1), symbol: str = '*'):
        self.color = color
        self.position = position
        self.symbol = symbol
    
    def __enter__(self):
        print(COLORING.format(self.color.value, ''), end="")        
        return self
    
    def __exit__(self, *args):
        print(COLORING.format(Color.TRANSPARENT.value, ''), end="")       
    
    def print(self, text: str, symbol: str = None):                    
        use_symbol = symbol if symbol is not None else self.symbol
        Printer.print_text(text, self.color, self.position, use_symbol)
        
        if not text:
            return
            
        total_width = 0
        for char in text.upper():
            if char == ' ':                   
                total_width += 3
            else:
                total_width += 6
        
        self.position = (self.position[0] + total_width, self.position[1])



if __name__ == "__main__":
    Printer.clear_screen()
    Printer.load_font('font.txt')
    
    Printer.print_text("EGOR", Color.RED, (50, 15), '#')
    Printer.print_text("POSTOK", Color.BLUE, (1, 16), '@')
    
    with Printer(Color.GREEN, (50, 20), '+') as p:
        p.print("LO  VM")
        p.print("            ABC")

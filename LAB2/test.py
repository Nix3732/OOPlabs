import enum
from typing import Dict, Tuple, List
from dataclasses import dataclass


COLORING = "\033[{}m\033[m{}"

class Color(enum.Enum): #цвета для консоли
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
class SymbolTemplate:           #класс для хранения шаблонов символа
    char: str
    lines: List[str]
    width: int

class Printer:
    _templates: Dict[str, SymbolTemplate] = {}          #словарь шрифта
    
    @classmethod
    def load_font(cls, filename: str):              #функция загрузки шрифта
        with open(filename, 'r', encoding='utf-8') as f:
            current_char = None
            current_lines = []
            
            for line in f:
                line = line.rstrip('\n')
                if not line and current_char is None:
                    continue
                
                if line.startswith('CHAR:'):            #ищем слово CHAR
                    if current_char is not None:
                        width = max(len(l) for l in current_lines) if current_lines else 0
                        cls._templates[current_char] = SymbolTemplate(current_char, current_lines, width)           #добовляем в словарь
                    current_char = line[5:].strip().upper()
                    current_lines = []
                else:
                    current_lines.append(line)
            
            if current_char is not None:
                width = max(len(l) for l in current_lines) if current_lines else 0
                cls._templates[current_char] = SymbolTemplate(current_char, current_lines, width)           #сохранияем последний символ
    
    @classmethod
    def _move_cursor(cls, x: int, y: int):          #перемещение курсора, с помощью ANSI последовательности
        print(f"\033[{y};{x}H", end='')
    
    @classmethod
    def _set_color(cls, color: Color):              #устонавливаем цвет
        print(f"\033[{color.value}m", end='')
    
    @classmethod
    def _reset_console(cls):                #сбрасываем консоль
        print("\033[0m", end='')
    
    @classmethod
    def print_text(cls, text: str, color: Color = Color.DEFAULT, 
                 position: Tuple[int, int] = (1, 1), symbol: str = '*'):            #вывод текста
        x, y = position
        height = 5
        
        for line_num in range(height):
            cls._move_cursor(x, y + line_num)
            cls._set_color(color)
            
            current_x = x
            for char in text.upper():
                if char == ' ':                 #обработка пробела
                    current_x += 3                  #ширина пробела (3 символа)
                    continue
                    
                if char in cls._templates:
                    template = cls._templates[char]
                    if line_num < len(template.lines):
                        line = template.lines[line_num]
                        printed_line = ''.join(symbol if c != ' ' else ' ' for c in line)           #замена символа на заданный
                        print(f"\033[{y + line_num};{current_x}H{printed_line}", end='')
                    current_x += template.width + 1
                else:
                    print(f"\033[{y + line_num};{current_x}H{symbol * 5}", end='')
                    current_x += template.width + 1
        
        cls._reset_console()
    
    def __init__(self, color: Color = Color.DEFAULT, 
                position: Tuple[int, int] = (1, 1), symbol: str = '*'):
        self._color = color
        self._position = position
        self._symbol = symbol
    
    def __enter__(self):
        print(COLORING.format(self._color.value, ''), end="")         #установка цвета
        return self
    
    def __exit__(self, *args):
        print(COLORING.format(Color.TRANSPARENT.value, ''), end="")       #сброс цвета
    
    def print(self, text: str, symbol: str = None):                     #вывод текста
        use_symbol = symbol if symbol is not None else self._symbol
        Printer.print_text(text, self._color, self._position, use_symbol)
        
        if not text:
            return
            
        total_width = 0
        for char in text.upper():
            if char == ' ':                     #пробел
                total_width += 3
            else:
                total_width += 6
        
        self._position = (self._position[0] + total_width, self._position[1])


if __name__ == "__main__":
    for _ in range(30):
        print()

    Printer.load_font('font.txt')
    
    Printer.print_text("EGOR", Color.RED, (20, 5), '#')
    Printer.print_text("POSTOK", Color.BLUE, (1, 12), '@')
    
    with Printer(Color.GREEN, (50, 20), '+') as p:
        p.print("LO VМ")
        p.print("ABC")
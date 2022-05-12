class Token:
    def __init__(self, text: str, index: int, line: int, col: int, filename: str) -> None:
        self.text = text
        self.index = index
        self.line = line
        self.col = col
        self.filename = filename

    def __str__(self):
        return self.text

class IdToken(Token):
    def __str__(self):
        return f'id: {self.text}'

class SymbolToken(Token):
    def __str__(self):
        return f'sym: {self.text}'

class IntToken(Token):
    def __str__(self):
        return f'int: {self.text}'

class FloatToken(Token):
    def __str__(self):
        return f'float: {self.text}'
    
class StringToken(Token):
    def __str__(self):
        return f'string: {self.text}'


class Lexer:
    def __init__(self, code, filename):
        self.code = code + ' '
        self.filename = filename
        self.index = 0
        self.line = 0
        self.tokens = []
        
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_'
        self.numbers = '0123456789'
        self.whitespace = ' \t\v\n'
        self.symbols = ['=']

    def lex(self):
        self.index = 0
        self.line = 0
        self.col = 0
        self.tokens = []
        
        while self.index < len(self.code):
            character = self.code[self.index]

            if character in self.alphabet:
                self.tokens.append(self.get_next_word())
                
            elif character in self.numbers:
                self.tokens.append(self.get_next_number())

            elif character == '"':
                self.tokens.append(self.get_next_string())

            elif character == "'":
                self.tokens.append(self.get_next_char())
                
            elif character == '\n':
                self.line += 1
                self.index += 1
                self.col = 0
            
            elif character in self.whitespace:
                self.index += 1

            else:
                self.tokens.append(self.get_next_symbol())
            
        return self.tokens

    def get_next_word(self):
        if self.code[self.index] not in self.alphabet: raise "Not a word"
        
        acc = ''
        while self.code[self.index] in self.alphabet + self.numbers:
            acc += self.code[self.index]
            self.index += 1
            self.col += 1

        return IdToken(acc, self.index - len(acc), self.line, self.col, self.filename)

    def get_next_symbol(self):
        if self.code[self.index] in self.alphabet + self.numbers + self.whitespace: raise "Not a symbol"

        acc = ''
        while self.code[self.index] not in self.alphabet + self.numbers + self.whitespace:
            acc += self.code[self.index]
            self.index += 1
            self.col += 1

        if acc in self.symbols: return SymbolToken(acc, self.index - len(acc), self.line, self.col, self.filename)
        else: return IdToken(acc, self.index - len(acc), self.line, self.col, self.filename)

    def get_next_number(self):
        if self.code[self.index] not in self.numbers: raise "Not a number"

        acc = ''
        while self.code[self.index] in self.numbers + '.':
            acc += self.code[self.index]
            self.index += 1
            self.col += 1

        if '.' in acc: return FloatToken(acc, self.index - len(acc), self.line, self.col, self.filename)
        else: return IntToken(acc, self.index - len(acc), self.line, self.col, self.filename)

    def get_next_string(self):
        if self.code[self.index] != '"': raise "Not a string"

        acc = ''
        self.index += 1
        while self.code[self.index] != '"':
            acc += self.code[self.index]
            self.index += 1
            self.col += 1
            
            if self.code[self.index] == '\n': raise "Unmatched quote"

        self.index += 1
        self.col += 1

        return StringToken(acc, self.index - len(acc) - 2, self.line, self.col, self.filename)

class Interpreter:
    def __init__(self, code):
        self.code = code

    def parse(self):
        return Lexer(self.code, 'main.dl').lex()
    
    def interpret(self):
        pass

def main():
    with open('main.dl', 'r') as f:
        code = f.read()
    
    interpreter = Interpreter(code)
    parsed = interpreter.parse()
    for token in parsed:
        print(token)

if __name__ == '__main__': main()

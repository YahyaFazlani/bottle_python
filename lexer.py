from enum import Enum, auto
from typing import List
from position import Position
from error_handling import InvalidStringError, InvalidSymbolError, InvalidNumberError

class TokenType(Enum):
    EOF = auto()
    IDENTIFIER = auto()

    #* DATA TYPE
    DT_INT = auto()
    DT_DECIMAL = auto()
    DT_CHAR = auto()
    DT_STR = auto()
    DT_BOOL = auto()
    DT_LIST = auto()

    #* KEYWORD
    KW_PRINT = auto()
    KW_FUNC = auto()
    KW_IMPORT = auto()
    KW_CLASS = auto()
    KW_WHILE = auto()
    KW_FOR = auto()
    KW_IF = auto()
    
    #* OPERATOR
    OP_ADDITION = auto() # +
    OP_SUBTRACTION = auto() # -
    OP_MULTIPLICATION = auto() #\ *
    OP_DIVISION = auto() # /
    OP_ASSIGNMENT = auto() # = 
    OP_AND = auto() # and
    OP_OR = auto() # or
    OP_NOT = auto() # not
    OP_EQUAL = auto() # ==
    OP_NOT_EQUAL = auto() #\ !=
    OP_LT = auto() # <
    OP_LE = auto() # <=
    OP_GT = auto() # >
    OP_GE = auto() # >=
    
    LPARAN = auto() # (
    RPARAN = auto() # )
    LSQBRACKET = auto() # [
    RSQBRACKET = auto() # ]
    LCURLYBRACKET = auto() # {
    RCURLYBRACKET = auto() # }
    SEMICOLON = auto()

    #* ERROR
    ERR_INVALID_NUM = auto()
    ERR_INVALID_STR = auto()
    ERR_INVALID_SYMBOL = auto()

class Lexeme:
    def __init__(self, type: TokenType, val, pos_start=None, pos_end=None) -> None:
        self.type = type
        self.val = val
        self._pos_start = pos_start 
        self.pos_end = pos_end

    @property
    def pos_start(self):
        return self._pos_start
    
    @pos_start.setter
    def pos_start(self, val):
        self._pos_start = val.copy()
        if not self.pos_end:
            self.pos_end = val.copy()
            self.pos_end.next()

    def __repr__(self) -> str:
        if not self.val: return f"{self.type.name}"
        return f"{self.type.name}:{self.val}"
    
class Lexer:
    def __init__(self, fn, code: str):
        self.code = code
        self.pos = Position(-1, 0, -1, fn, code)
        self.current_char = ''
        self.tokens: List[Lexeme] = []
        self.next_char()

    def next_char(self):
        self.pos.next(self.current_char)
        self.current_char = self.code[self.pos.idx] if self.pos.idx < len(self.code) else "EOF"

    def gettok(self):
        SYMBOL_CHARS = ["+", "-", "*", "/", "=", "!", ">", "<", "(", ")", "[", "]", "{", "}", ";"]
        lexeme = Lexeme(TokenType.EOF, "")

        # Ignore whitespace
        while self.current_char == " ":
            self.next_char()
        
        # Handle EOF
        if self.current_char == "EOF":
            lexeme.val = "EOF"
            lexeme.type = TokenType.EOF
            lexeme.pos_start = self.pos


        # Check if string
        elif self.current_char == "\"" or self.current_char == "'":
            is_string_end = False
            lexeme.pos_start = self.pos.copy()

            # Keep the loop running till string, line or file doesn't end
            while not is_string_end:
                lexeme.val += self.current_char

                self.next_char()

                # Valid String
                if self.current_char == lexeme.val[0]:
                    lexeme.val += self.current_char
                    is_string_end = True
                    lexeme.type = TokenType.DT_STR

                # Invalid String
                elif self.current_char == "\n" or self.current_char == "\r" or self.current_char == "EOF":
                    return None, InvalidStringError(lexeme.pos_start, self.pos, f"Expected {lexeme.val[0]}")
                
            lexeme.pos_end = self.pos
            self.next_char() # Go to next character after string ends

        # Check for keywords
        elif self.current_char.isalpha():
            while self.current_char != "EOF" and self.current_char.isalnum():
                lexeme.val += self.current_char
                self.next_char()

            if lexeme.val == "func":
                lexeme.type = TokenType.KW_FUNC
            elif lexeme.val == "import":
                lexeme.type = TokenType.KW_IMPORT
            elif lexeme.val == "print":
                lexeme.type = TokenType.KW_PRINT
            elif lexeme.val == "for":
                lexeme.type = TokenType.KW_FOR
            elif lexeme.val == "while":
                lexeme.type = TokenType.KW_WHILE
            elif lexeme.val == "class":
                lexeme.type = TokenType.KW_CLASS
            elif lexeme.val == "if":
                lexeme.type = TokenType.KW_IF
            elif lexeme.val == "and":
                lexeme.type = TokenType.OP_AND
            elif lexeme.val == "or":
                lexeme.type = TokenType.OP_OR
            elif lexeme.val == "not":
                lexeme.type = TokenType.OP_NOT
            else:
                lexeme.type = TokenType.IDENTIFIER

        # Check if number
        elif self.current_char.isdigit():
            lexeme.pos_start = self.pos.copy()
            no_of_points = 0

            while (self.current_char.isdigit() or self.current_char == "."):
                if self.current_char == ".":
                    no_of_points += 1

                lexeme.val += self.current_char
                self.next_char()

                if (no_of_points > 1):
                    return None, InvalidNumberError(lexeme.pos_start, self.pos, f"More than 1 decimal point found")
            
            # Check type of number
            if no_of_points == 0:
                lexeme.type = TokenType.DT_INT
                lexeme.val = int(lexeme.val)
            elif no_of_points == 1:
                lexeme.type = TokenType.DT_DECIMAL
                lexeme.val = float(lexeme.val)
            lexeme.pos_end = self.pos

        # Check for symbols such as brackets and operators
        elif self.current_char in SYMBOL_CHARS:
            lexeme.pos_start = self.pos.copy()
            # is_bracket checks is a flag to check for parenthesis and appropriately end the loop
            is_paren = False

            # if the current character is a closing (right) parenthesis then this is the last character in the lexeme
            # if the next character is a opening (left) parenthesis then lexeme value has ended and the opening parenthesis is caught in the next lexeme
            while self.current_char in SYMBOL_CHARS and not is_paren:
                if self.current_char == ")":
                    is_paren = True

                lexeme.val += self.current_char
                self.next_char()

                if self.current_char == "(":
                    is_paren = True
            
            lexeme.pos_end = self.pos

            if (lexeme.val == "+"):
                lexeme.type = TokenType.OP_ADDITION
            elif (lexeme.val == "-"):
                lexeme.type = TokenType.OP_SUBTRACTION
            elif (lexeme.val == "*"):
                lexeme.type = TokenType.OP_MULTIPLICATION
            elif (lexeme.val == "/"):
                lexeme.type = TokenType.OP_DIVISION
            elif (lexeme.val == "="):
                lexeme.type = TokenType.OP_ASSIGNMENT
            elif (lexeme.val == "=="):
                lexeme.type = TokenType.OP_EQUAL
            elif (lexeme.val == "!="):
                lexeme.type = TokenType.OP_NOT_EQUAL
            elif (lexeme.val == ">"):
                lexeme.type = TokenType.OP_GT
            elif (lexeme.val == ">="):
                lexeme.type = TokenType.OP_GE
            elif (lexeme.val == "<"):
                lexeme.type = TokenType.OP_LT
            elif (lexeme.val == "<="):
                lexeme.type = TokenType.OP_LE
            elif (lexeme.val == "("):
                lexeme.type = TokenType.LPARAN
            elif (lexeme.val == ")"):
                lexeme.type = TokenType.RPARAN
            elif (lexeme.val == "["):
                lexeme.type = TokenType.LSQBRACKET
            elif (lexeme.val == "]"):
                lexeme.type = TokenType.RSQBRACKET
            elif (lexeme.val == "{"):
                lexeme.type = TokenType.LCURLYBRACKET
            elif (lexeme.val == "}"):
                lexeme.type = TokenType.RCURLYBRACKET
            elif (lexeme.val == ";"):
                lexeme.type = TokenType.SEMICOLON
            else:
                return None, InvalidSymbolError(lexeme.pos_start, lexeme.pos_end, "'" + lexeme.val + "'")

        # Ignore comments and return next token
        elif self.current_char == "#":
            while self.current_char != "EOF" or self.current_char == "\n" or self.current_char == "\r":
                self.next_char()
            
            return self.gettok()
        
        return lexeme, None
    
    def tokenize(self):
        while True:
            token, error = self.gettok()

            if error:
                return [], error

            self.tokens.append(token)

            if token.type == TokenType.EOF:
                break

        return self.tokens, None
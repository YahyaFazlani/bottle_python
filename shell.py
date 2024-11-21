from lexer import Lexer
from parser_ import Parser
from interpreter import Interpreter

class Shell:
    def __init__(self, fn) -> None:
        self.fn = fn
    
    def execute(self, code):
        lexer = Lexer(self.fn, code)
        tokens, error = lexer.tokenize()
        if error: return None, error

        parser = Parser(tokens)
        ast = parser.parse_bin_expr()
        if ast.error: return None, error

        interpreter = Interpreter()
        res = interpreter.visit(ast.node)

        return res.val, None
    
    def run_shell(self):
        while True:
            code = input("bottle >> ")
            result, error = self.execute(code)

            if error: print(error.as_string())
            else: print(result)

shell = Shell("<stdin>")
shell.run_shell()
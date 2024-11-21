from lexer import *
from error_handling import InvalidSyntaxError

#* Nodes
class NumberNode:
    def __init__(self, token: Lexeme) -> None:
        self.token = token

        self.pos_start = token.pos_start
        self.pos_end = token.pos_end

    def __repr__(self) -> str:
        return f"{self.token}"
  
class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"
    
# op_tok is the sign
# node is the magnitude
class UnaryOpNode:
    def __init__(self, sign, node):
        self.op_tok = sign
        self.node = node

    def __repr__(self) -> str:
        return f"({self.op_tok}, {self.node})"

#* Parser Components
class ParseResult:
    def __init__(self) -> None:
        self.error = None
        self.node = None

    # if res is a ParseResult instance then set it's error to new instance error
    # if res is not ParseResult but is a node then return res directly
    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
    
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok: Lexeme
        self.next_token()

    def next_token(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

        return self.current_tok

    def parse_bin_expr(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TokenType.EOF:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '+', '-', '*', '/'"))

        return res

    # Return current token as a NumberNode if it is a factor (integer or decimal) otherwise None
    # Also goes to the next token if current token is number
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TokenType.OP_ADDITION, TokenType.OP_SUBTRACTION):
            res.register(self.next_token())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (TokenType.DT_INT, TokenType.DT_DECIMAL):
            res.register(self.next_token())
            return res.success(NumberNode(tok))
        
        elif tok.type == TokenType.LPARAN:
            res.register(self.next_token())
            expr = res.register(self.expr())
            if res.error: return res

            if self.current_tok.type == TokenType.RPARAN:
                res.register(self.next_token())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))
        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected Integer or Decimal"))

    def term(self):
        res = ParseResult()
        left = res.register(self.factor())
        if res.error: return res

        while self.current_tok.type in (TokenType.OP_MULTIPLICATION, TokenType.OP_DIVISION):
            op_tok = self.current_tok
            res.register(self.next_token())
            right = res.register(self.factor())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        
        return res.success(left)

    def expr(self):
        res = ParseResult()
        left = res.register(self.term())

        while self.current_tok.type in (TokenType.OP_ADDITION, TokenType.OP_SUBTRACTION):
            op_tok = self.current_tok
            res.register(self.next_token())
            right = res.register(self.term())
            left = BinOpNode(left, op_tok, right)
        
        return res.success(left)

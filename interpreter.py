from parser_ import NumberNode, BinOpNode, UnaryOpNode
from lexer import TokenType

class RTResult:
    def __init__(self) -> None:
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self
    
    def failure(self, error):
        self.error = error
        return self


class Interpreter:
    def visit(self, node):
        visit_method_name = f"visit_{type(node).__name__}"
        visit_method = getattr(self, visit_method_name, self.no_visit)

        return visit_method(node)
    
    def no_visit(self, node):
        raise Exception(f"No method as visit_visit_{type(node).__name__}")
    
    def visit_NumberNode(self, node: NumberNode):
        return Number(node.token.val).set_pos(node.pos_start, node.pos_end)
    
    def visit_BinOpNode(self, node: BinOpNode):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if node.op_tok.type == TokenType.OP_ADDITION:
            result = left.add(right)
        elif node.op_tok.type == TokenType.OP_SUBTRACTION:
            result = left.subtract(right)
        elif node.op_tok.type == TokenType.OP_MULTIPLICATION:
            result = left.multiply(right)
        elif node.op_tok.type == TokenType.OP_DIVISION:
            result = left.divide(right)

        return result

    def visit_UnaryOpNode(self, node: UnaryOpNode):
        number = self.visit(node.node)

        if node.op_tok.type == TokenType.OP_SUBTRACTION:
            number = number.multiply(Number(-1))

        return number

class Number:
    def __init__(self, val) -> None:
        self.val = val
        self.set_pos()
    
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end

        return self

    def add(self, other):
        if isinstance(other, Number):
            return Number(self.val + other.val)
        
    def subtract(self, other):
        if isinstance(other, Number):
            return Number(self.val - other.val)
        
    def multiply(self, other):
        if isinstance(other, Number):
            return Number(self.val * other.val)
        
    def divide(self, other):
        if isinstance(other, Number):
            return Number(self.val / other.val) 
  
        

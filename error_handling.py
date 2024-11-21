from position import Position

class Error:
	def __init__(self, pos_start: Position, pos_end: Position, error_name: str, details: str) -> None:
		self.pos_start = pos_start
		self.pos_end = pos_end
		self.error_name = error_name
		self.details = details

	def as_string(self) -> str:
		res = f"{self.error_name}: {self.details}"
		res += f"\nFile {self.pos_start.fn}: line {self.pos_start.ln+1}"
		return res


class InvalidSymbolError(Error):
	def __init__(self, pos_start: Position, pos_end: Position, details: str) -> None:
		super().__init__(pos_start, pos_end, "Invalid Symbol", details)

class InvalidNumberError(Error):
	def __init__(self, pos_start: Position, pos_end: Position, details: str) -> None:
		super().__init__(pos_start, pos_end, "Invalid Number", details)
		
class InvalidStringError(Error):
	def __init__(self, pos_start: Position, pos_end: Position, details: str) -> None:
		super().__init__(pos_start, pos_end, "Invalid String", details)

class InvalidSyntaxError(Error):
	def __init__(self, pos_start: Position, pos_end: Position, details: str) -> None:
		super().__init__(pos_start, pos_end, "Invalid Syntax", details)

class RunTimeError(Error):
	def __init__(self, pos_start: Position, pos_end: Position, details: str) -> None:
		super().__init__(pos_start, pos_end, "Runtime Error", details)
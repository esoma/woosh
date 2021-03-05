
from typing import Any, Generator, Protocol, Union


def tokenize(
    source: Union[bytes, FileLike],
    /, *,
    continue_on_error: bool = False
) -> Generator[Token, None, None]: ...


class Token:

    def __init__(
        self,
        type: Type,
        value: str,
        start_line: int, start_column: int,
        end_line: int, end_column: int,
        /
    ) -> None: ...

    @property
    def type(self) -> Type: ...
    
    @property
    def value(self) -> str: ...
    
    @property
    def start_line(self) -> int: ...
    
    @property
    def start_column(self) -> int: ...
    
    @property
    def end_line(self) -> int: ...
    
    @property
    def end_column(self) -> int: ...
    
    
class Type:

    def __init__(self, name: str, value: int, /) -> None: ...
    
    @property
    def name(self) -> str: ...
    
    @property
    def value(self) -> int: ...
    

COMMENT: Token
DEDENT: Token
ENCODING: Token
EOF: Token
ERROR: Token
INDENT: Token
NAME: Token
NEWLINE: Token
NUMBER: Token
OP: Token
STRING: Token


class FileLike(Protocol):
    
    def tell(self) -> Any: ...
    
    def seek(self, offset: Any) -> Any: ...
    
    def readline(self, byte_count: int) -> bytes: ...

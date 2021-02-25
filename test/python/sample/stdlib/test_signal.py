
# python
import io
import pathlib
# pytest
import pytest
# woosh
import woosh

def tokenize_file_like(source):
    return list(woosh.tokenize(io.BytesIO(source)))

def tokenize_bytes(source):
    return list(woosh.tokenize(source))

SAMPLE_DIR = pathlib.Path(__file__).parent.absolute() / '../../' / '../../' / 'sample'

@pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
def test(tokenize):
    with open(SAMPLE_DIR / 'stdlib/signal.py', 'rb') as f:
        tokens = tokenize(f.read())
    for token, expected in zip(tokens, EXPECTED):
        assert token == expected

EXPECTED = [
woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
woosh.Token(woosh.NAME, 'import', 1, 0, 1, 6),
woosh.Token(woosh.NAME, '_signal', 1, 7, 1, 14),
woosh.Token(woosh.NEWLINE, '\r\n', 1, 14, 2, 0),
woosh.Token(woosh.NAME, 'from', 2, 0, 2, 4),
woosh.Token(woosh.NAME, '_signal', 2, 5, 2, 12),
woosh.Token(woosh.NAME, 'import', 2, 13, 2, 19),
woosh.Token(woosh.OP, '*', 2, 20, 2, 21),
woosh.Token(woosh.NEWLINE, '\r\n', 2, 21, 3, 0),
woosh.Token(woosh.NAME, 'from', 3, 0, 3, 4),
woosh.Token(woosh.NAME, 'functools', 3, 5, 3, 14),
woosh.Token(woosh.NAME, 'import', 3, 15, 3, 21),
woosh.Token(woosh.NAME, 'wraps', 3, 22, 3, 27),
woosh.Token(woosh.NAME, 'as', 3, 28, 3, 30),
woosh.Token(woosh.NAME, '_wraps', 3, 31, 3, 37),
woosh.Token(woosh.NEWLINE, '\r\n', 3, 37, 4, 0),
woosh.Token(woosh.NAME, 'from', 4, 0, 4, 4),
woosh.Token(woosh.NAME, 'enum', 4, 5, 4, 9),
woosh.Token(woosh.NAME, 'import', 4, 10, 4, 16),
woosh.Token(woosh.NAME, 'IntEnum', 4, 17, 4, 24),
woosh.Token(woosh.NAME, 'as', 4, 25, 4, 27),
woosh.Token(woosh.NAME, '_IntEnum', 4, 28, 4, 36),
woosh.Token(woosh.NEWLINE, '\r\n', 4, 36, 5, 0),
woosh.Token(woosh.NAME, '_globals', 6, 0, 6, 8),
woosh.Token(woosh.OP, '=', 6, 9, 6, 10),
woosh.Token(woosh.NAME, 'globals', 6, 11, 6, 18),
woosh.Token(woosh.OP, '(', 6, 18, 6, 19),
woosh.Token(woosh.OP, ')', 6, 19, 6, 20),
woosh.Token(woosh.NEWLINE, '\r\n', 6, 20, 7, 0),
woosh.Token(woosh.NAME, '_IntEnum', 8, 0, 8, 8),
woosh.Token(woosh.OP, '.', 8, 8, 8, 9),
woosh.Token(woosh.NAME, '_convert_', 8, 9, 8, 18),
woosh.Token(woosh.OP, '(', 8, 18, 8, 19),
woosh.Token(woosh.STRING, "'Signals'", 9, 8, 9, 17),
woosh.Token(woosh.OP, ',', 9, 17, 9, 18),
woosh.Token(woosh.NAME, '__name__', 9, 19, 9, 27),
woosh.Token(woosh.OP, ',', 9, 27, 9, 28),
woosh.Token(woosh.NAME, 'lambda', 10, 8, 10, 14),
woosh.Token(woosh.NAME, 'name', 10, 15, 10, 19),
woosh.Token(woosh.OP, ':', 10, 19, 10, 20),
woosh.Token(woosh.NAME, 'name', 11, 12, 11, 16),
woosh.Token(woosh.OP, '.', 11, 16, 11, 17),
woosh.Token(woosh.NAME, 'isupper', 11, 17, 11, 24),
woosh.Token(woosh.OP, '(', 11, 24, 11, 25),
woosh.Token(woosh.OP, ')', 11, 25, 11, 26),
woosh.Token(woosh.NAME, 'and', 12, 12, 12, 15),
woosh.Token(woosh.OP, '(', 12, 16, 12, 17),
woosh.Token(woosh.NAME, 'name', 12, 17, 12, 21),
woosh.Token(woosh.OP, '.', 12, 21, 12, 22),
woosh.Token(woosh.NAME, 'startswith', 12, 22, 12, 32),
woosh.Token(woosh.OP, '(', 12, 32, 12, 33),
woosh.Token(woosh.STRING, "'SIG'", 12, 33, 12, 38),
woosh.Token(woosh.OP, ')', 12, 38, 12, 39),
woosh.Token(woosh.NAME, 'and', 12, 40, 12, 43),
woosh.Token(woosh.NAME, 'not', 12, 44, 12, 47),
woosh.Token(woosh.NAME, 'name', 12, 48, 12, 52),
woosh.Token(woosh.OP, '.', 12, 52, 12, 53),
woosh.Token(woosh.NAME, 'startswith', 12, 53, 12, 63),
woosh.Token(woosh.OP, '(', 12, 63, 12, 64),
woosh.Token(woosh.STRING, "'SIG_'", 12, 64, 12, 70),
woosh.Token(woosh.OP, ')', 12, 70, 12, 71),
woosh.Token(woosh.OP, ')', 12, 71, 12, 72),
woosh.Token(woosh.NAME, 'or', 13, 12, 13, 14),
woosh.Token(woosh.NAME, 'name', 13, 15, 13, 19),
woosh.Token(woosh.OP, '.', 13, 19, 13, 20),
woosh.Token(woosh.NAME, 'startswith', 13, 20, 13, 30),
woosh.Token(woosh.OP, '(', 13, 30, 13, 31),
woosh.Token(woosh.STRING, "'CTRL_'", 13, 31, 13, 38),
woosh.Token(woosh.OP, ')', 13, 38, 13, 39),
woosh.Token(woosh.OP, ')', 13, 39, 13, 40),
woosh.Token(woosh.NEWLINE, '\r\n', 13, 40, 14, 0),
woosh.Token(woosh.NAME, '_IntEnum', 15, 0, 15, 8),
woosh.Token(woosh.OP, '.', 15, 8, 15, 9),
woosh.Token(woosh.NAME, '_convert_', 15, 9, 15, 18),
woosh.Token(woosh.OP, '(', 15, 18, 15, 19),
woosh.Token(woosh.STRING, "'Handlers'", 16, 8, 16, 18),
woosh.Token(woosh.OP, ',', 16, 18, 16, 19),
woosh.Token(woosh.NAME, '__name__', 16, 20, 16, 28),
woosh.Token(woosh.OP, ',', 16, 28, 16, 29),
woosh.Token(woosh.NAME, 'lambda', 17, 8, 17, 14),
woosh.Token(woosh.NAME, 'name', 17, 15, 17, 19),
woosh.Token(woosh.OP, ':', 17, 19, 17, 20),
woosh.Token(woosh.NAME, 'name', 17, 21, 17, 25),
woosh.Token(woosh.NAME, 'in', 17, 26, 17, 28),
woosh.Token(woosh.OP, '(', 17, 29, 17, 30),
woosh.Token(woosh.STRING, "'SIG_DFL'", 17, 30, 17, 39),
woosh.Token(woosh.OP, ',', 17, 39, 17, 40),
woosh.Token(woosh.STRING, "'SIG_IGN'", 17, 41, 17, 50),
woosh.Token(woosh.OP, ')', 17, 50, 17, 51),
woosh.Token(woosh.OP, ')', 17, 51, 17, 52),
woosh.Token(woosh.NEWLINE, '\r\n', 17, 52, 18, 0),
woosh.Token(woosh.NAME, 'if', 19, 0, 19, 2),
woosh.Token(woosh.STRING, "'pthread_sigmask'", 19, 3, 19, 20),
woosh.Token(woosh.NAME, 'in', 19, 21, 19, 23),
woosh.Token(woosh.NAME, '_globals', 19, 24, 19, 32),
woosh.Token(woosh.OP, ':', 19, 32, 19, 33),
woosh.Token(woosh.NEWLINE, '\r\n', 19, 33, 20, 0),
woosh.Token(woosh.INDENT, '    ', 20, 0, 20, 4),
woosh.Token(woosh.NAME, '_IntEnum', 20, 4, 20, 12),
woosh.Token(woosh.OP, '.', 20, 12, 20, 13),
woosh.Token(woosh.NAME, '_convert_', 20, 13, 20, 22),
woosh.Token(woosh.OP, '(', 20, 22, 20, 23),
woosh.Token(woosh.STRING, "'Sigmasks'", 21, 12, 21, 22),
woosh.Token(woosh.OP, ',', 21, 22, 21, 23),
woosh.Token(woosh.NAME, '__name__', 21, 24, 21, 32),
woosh.Token(woosh.OP, ',', 21, 32, 21, 33),
woosh.Token(woosh.NAME, 'lambda', 22, 12, 22, 18),
woosh.Token(woosh.NAME, 'name', 22, 19, 22, 23),
woosh.Token(woosh.OP, ':', 22, 23, 22, 24),
woosh.Token(woosh.NAME, 'name', 22, 25, 22, 29),
woosh.Token(woosh.NAME, 'in', 22, 30, 22, 32),
woosh.Token(woosh.OP, '(', 22, 33, 22, 34),
woosh.Token(woosh.STRING, "'SIG_BLOCK'", 22, 34, 22, 45),
woosh.Token(woosh.OP, ',', 22, 45, 22, 46),
woosh.Token(woosh.STRING, "'SIG_UNBLOCK'", 22, 47, 22, 60),
woosh.Token(woosh.OP, ',', 22, 60, 22, 61),
woosh.Token(woosh.STRING, "'SIG_SETMASK'", 22, 62, 22, 75),
woosh.Token(woosh.OP, ')', 22, 75, 22, 76),
woosh.Token(woosh.OP, ')', 22, 76, 22, 77),
woosh.Token(woosh.NEWLINE, '\r\n', 22, 77, 23, 0),
woosh.Token(woosh.DEDENT, '', 25, 0, 25, 0),
woosh.Token(woosh.NAME, 'def', 25, 0, 25, 3),
woosh.Token(woosh.NAME, '_int_to_enum', 25, 4, 25, 16),
woosh.Token(woosh.OP, '(', 25, 16, 25, 17),
woosh.Token(woosh.NAME, 'value', 25, 17, 25, 22),
woosh.Token(woosh.OP, ',', 25, 22, 25, 23),
woosh.Token(woosh.NAME, 'enum_klass', 25, 24, 25, 34),
woosh.Token(woosh.OP, ')', 25, 34, 25, 35),
woosh.Token(woosh.OP, ':', 25, 35, 25, 36),
woosh.Token(woosh.NEWLINE, '\r\n', 25, 36, 26, 0),
woosh.Token(woosh.INDENT, '    ', 26, 0, 26, 4),
woosh.Token(woosh.STRING, '"""Convert a numeric value to an IntEnum member.\r\n    If it\'s not a known member, return the numeric value itself.\r\n    """', 26, 4, 28, 7),
woosh.Token(woosh.NEWLINE, '\r\n', 28, 7, 29, 0),
woosh.Token(woosh.NAME, 'try', 29, 4, 29, 7),
woosh.Token(woosh.OP, ':', 29, 7, 29, 8),
woosh.Token(woosh.NEWLINE, '\r\n', 29, 8, 30, 0),
woosh.Token(woosh.INDENT, '        ', 30, 0, 30, 8),
woosh.Token(woosh.NAME, 'return', 30, 8, 30, 14),
woosh.Token(woosh.NAME, 'enum_klass', 30, 15, 30, 25),
woosh.Token(woosh.OP, '(', 30, 25, 30, 26),
woosh.Token(woosh.NAME, 'value', 30, 26, 30, 31),
woosh.Token(woosh.OP, ')', 30, 31, 30, 32),
woosh.Token(woosh.NEWLINE, '\r\n', 30, 32, 31, 0),
woosh.Token(woosh.DEDENT, '    ', 31, 0, 31, 4),
woosh.Token(woosh.NAME, 'except', 31, 4, 31, 10),
woosh.Token(woosh.NAME, 'ValueError', 31, 11, 31, 21),
woosh.Token(woosh.OP, ':', 31, 21, 31, 22),
woosh.Token(woosh.NEWLINE, '\r\n', 31, 22, 32, 0),
woosh.Token(woosh.INDENT, '        ', 32, 0, 32, 8),
woosh.Token(woosh.NAME, 'return', 32, 8, 32, 14),
woosh.Token(woosh.NAME, 'value', 32, 15, 32, 20),
woosh.Token(woosh.NEWLINE, '\r\n', 32, 20, 33, 0),
woosh.Token(woosh.DEDENT, '', 35, 0, 35, 0),
woosh.Token(woosh.DEDENT, '', 35, 0, 35, 0),
woosh.Token(woosh.NAME, 'def', 35, 0, 35, 3),
woosh.Token(woosh.NAME, '_enum_to_int', 35, 4, 35, 16),
woosh.Token(woosh.OP, '(', 35, 16, 35, 17),
woosh.Token(woosh.NAME, 'value', 35, 17, 35, 22),
woosh.Token(woosh.OP, ')', 35, 22, 35, 23),
woosh.Token(woosh.OP, ':', 35, 23, 35, 24),
woosh.Token(woosh.NEWLINE, '\r\n', 35, 24, 36, 0),
woosh.Token(woosh.INDENT, '    ', 36, 0, 36, 4),
woosh.Token(woosh.STRING, '"""Convert an IntEnum member to a numeric value.\r\n    If it\'s not an IntEnum member return the value itself.\r\n    """', 36, 4, 38, 7),
woosh.Token(woosh.NEWLINE, '\r\n', 38, 7, 39, 0),
woosh.Token(woosh.NAME, 'try', 39, 4, 39, 7),
woosh.Token(woosh.OP, ':', 39, 7, 39, 8),
woosh.Token(woosh.NEWLINE, '\r\n', 39, 8, 40, 0),
woosh.Token(woosh.INDENT, '        ', 40, 0, 40, 8),
woosh.Token(woosh.NAME, 'return', 40, 8, 40, 14),
woosh.Token(woosh.NAME, 'int', 40, 15, 40, 18),
woosh.Token(woosh.OP, '(', 40, 18, 40, 19),
woosh.Token(woosh.NAME, 'value', 40, 19, 40, 24),
woosh.Token(woosh.OP, ')', 40, 24, 40, 25),
woosh.Token(woosh.NEWLINE, '\r\n', 40, 25, 41, 0),
woosh.Token(woosh.DEDENT, '    ', 41, 0, 41, 4),
woosh.Token(woosh.NAME, 'except', 41, 4, 41, 10),
woosh.Token(woosh.OP, '(', 41, 11, 41, 12),
woosh.Token(woosh.NAME, 'ValueError', 41, 12, 41, 22),
woosh.Token(woosh.OP, ',', 41, 22, 41, 23),
woosh.Token(woosh.NAME, 'TypeError', 41, 24, 41, 33),
woosh.Token(woosh.OP, ')', 41, 33, 41, 34),
woosh.Token(woosh.OP, ':', 41, 34, 41, 35),
woosh.Token(woosh.NEWLINE, '\r\n', 41, 35, 42, 0),
woosh.Token(woosh.INDENT, '        ', 42, 0, 42, 8),
woosh.Token(woosh.NAME, 'return', 42, 8, 42, 14),
woosh.Token(woosh.NAME, 'value', 42, 15, 42, 20),
woosh.Token(woosh.NEWLINE, '\r\n', 42, 20, 43, 0),
woosh.Token(woosh.DEDENT, '', 45, 0, 45, 0),
woosh.Token(woosh.DEDENT, '', 45, 0, 45, 0),
woosh.Token(woosh.OP, '@', 45, 0, 45, 1),
woosh.Token(woosh.NAME, '_wraps', 45, 1, 45, 7),
woosh.Token(woosh.OP, '(', 45, 7, 45, 8),
woosh.Token(woosh.NAME, '_signal', 45, 8, 45, 15),
woosh.Token(woosh.OP, '.', 45, 15, 45, 16),
woosh.Token(woosh.NAME, 'signal', 45, 16, 45, 22),
woosh.Token(woosh.OP, ')', 45, 22, 45, 23),
woosh.Token(woosh.NEWLINE, '\r\n', 45, 23, 46, 0),
woosh.Token(woosh.NAME, 'def', 46, 0, 46, 3),
woosh.Token(woosh.NAME, 'signal', 46, 4, 46, 10),
woosh.Token(woosh.OP, '(', 46, 10, 46, 11),
woosh.Token(woosh.NAME, 'signalnum', 46, 11, 46, 20),
woosh.Token(woosh.OP, ',', 46, 20, 46, 21),
woosh.Token(woosh.NAME, 'handler', 46, 22, 46, 29),
woosh.Token(woosh.OP, ')', 46, 29, 46, 30),
woosh.Token(woosh.OP, ':', 46, 30, 46, 31),
woosh.Token(woosh.NEWLINE, '\r\n', 46, 31, 47, 0),
woosh.Token(woosh.INDENT, '    ', 47, 0, 47, 4),
woosh.Token(woosh.NAME, 'handler', 47, 4, 47, 11),
woosh.Token(woosh.OP, '=', 47, 12, 47, 13),
woosh.Token(woosh.NAME, '_signal', 47, 14, 47, 21),
woosh.Token(woosh.OP, '.', 47, 21, 47, 22),
woosh.Token(woosh.NAME, 'signal', 47, 22, 47, 28),
woosh.Token(woosh.OP, '(', 47, 28, 47, 29),
woosh.Token(woosh.NAME, '_enum_to_int', 47, 29, 47, 41),
woosh.Token(woosh.OP, '(', 47, 41, 47, 42),
woosh.Token(woosh.NAME, 'signalnum', 47, 42, 47, 51),
woosh.Token(woosh.OP, ')', 47, 51, 47, 52),
woosh.Token(woosh.OP, ',', 47, 52, 47, 53),
woosh.Token(woosh.NAME, '_enum_to_int', 47, 54, 47, 66),
woosh.Token(woosh.OP, '(', 47, 66, 47, 67),
woosh.Token(woosh.NAME, 'handler', 47, 67, 47, 74),
woosh.Token(woosh.OP, ')', 47, 74, 47, 75),
woosh.Token(woosh.OP, ')', 47, 75, 47, 76),
woosh.Token(woosh.NEWLINE, '\r\n', 47, 76, 48, 0),
woosh.Token(woosh.NAME, 'return', 48, 4, 48, 10),
woosh.Token(woosh.NAME, '_int_to_enum', 48, 11, 48, 23),
woosh.Token(woosh.OP, '(', 48, 23, 48, 24),
woosh.Token(woosh.NAME, 'handler', 48, 24, 48, 31),
woosh.Token(woosh.OP, ',', 48, 31, 48, 32),
woosh.Token(woosh.NAME, 'Handlers', 48, 33, 48, 41),
woosh.Token(woosh.OP, ')', 48, 41, 48, 42),
woosh.Token(woosh.NEWLINE, '\r\n', 48, 42, 49, 0),
woosh.Token(woosh.DEDENT, '', 51, 0, 51, 0),
woosh.Token(woosh.OP, '@', 51, 0, 51, 1),
woosh.Token(woosh.NAME, '_wraps', 51, 1, 51, 7),
woosh.Token(woosh.OP, '(', 51, 7, 51, 8),
woosh.Token(woosh.NAME, '_signal', 51, 8, 51, 15),
woosh.Token(woosh.OP, '.', 51, 15, 51, 16),
woosh.Token(woosh.NAME, 'getsignal', 51, 16, 51, 25),
woosh.Token(woosh.OP, ')', 51, 25, 51, 26),
woosh.Token(woosh.NEWLINE, '\r\n', 51, 26, 52, 0),
woosh.Token(woosh.NAME, 'def', 52, 0, 52, 3),
woosh.Token(woosh.NAME, 'getsignal', 52, 4, 52, 13),
woosh.Token(woosh.OP, '(', 52, 13, 52, 14),
woosh.Token(woosh.NAME, 'signalnum', 52, 14, 52, 23),
woosh.Token(woosh.OP, ')', 52, 23, 52, 24),
woosh.Token(woosh.OP, ':', 52, 24, 52, 25),
woosh.Token(woosh.NEWLINE, '\r\n', 52, 25, 53, 0),
woosh.Token(woosh.INDENT, '    ', 53, 0, 53, 4),
woosh.Token(woosh.NAME, 'handler', 53, 4, 53, 11),
woosh.Token(woosh.OP, '=', 53, 12, 53, 13),
woosh.Token(woosh.NAME, '_signal', 53, 14, 53, 21),
woosh.Token(woosh.OP, '.', 53, 21, 53, 22),
woosh.Token(woosh.NAME, 'getsignal', 53, 22, 53, 31),
woosh.Token(woosh.OP, '(', 53, 31, 53, 32),
woosh.Token(woosh.NAME, 'signalnum', 53, 32, 53, 41),
woosh.Token(woosh.OP, ')', 53, 41, 53, 42),
woosh.Token(woosh.NEWLINE, '\r\n', 53, 42, 54, 0),
woosh.Token(woosh.NAME, 'return', 54, 4, 54, 10),
woosh.Token(woosh.NAME, '_int_to_enum', 54, 11, 54, 23),
woosh.Token(woosh.OP, '(', 54, 23, 54, 24),
woosh.Token(woosh.NAME, 'handler', 54, 24, 54, 31),
woosh.Token(woosh.OP, ',', 54, 31, 54, 32),
woosh.Token(woosh.NAME, 'Handlers', 54, 33, 54, 41),
woosh.Token(woosh.OP, ')', 54, 41, 54, 42),
woosh.Token(woosh.NEWLINE, '\r\n', 54, 42, 55, 0),
woosh.Token(woosh.DEDENT, '', 57, 0, 57, 0),
woosh.Token(woosh.NAME, 'if', 57, 0, 57, 2),
woosh.Token(woosh.STRING, "'pthread_sigmask'", 57, 3, 57, 20),
woosh.Token(woosh.NAME, 'in', 57, 21, 57, 23),
woosh.Token(woosh.NAME, '_globals', 57, 24, 57, 32),
woosh.Token(woosh.OP, ':', 57, 32, 57, 33),
woosh.Token(woosh.NEWLINE, '\r\n', 57, 33, 58, 0),
woosh.Token(woosh.INDENT, '    ', 58, 0, 58, 4),
woosh.Token(woosh.OP, '@', 58, 4, 58, 5),
woosh.Token(woosh.NAME, '_wraps', 58, 5, 58, 11),
woosh.Token(woosh.OP, '(', 58, 11, 58, 12),
woosh.Token(woosh.NAME, '_signal', 58, 12, 58, 19),
woosh.Token(woosh.OP, '.', 58, 19, 58, 20),
woosh.Token(woosh.NAME, 'pthread_sigmask', 58, 20, 58, 35),
woosh.Token(woosh.OP, ')', 58, 35, 58, 36),
woosh.Token(woosh.NEWLINE, '\r\n', 58, 36, 59, 0),
woosh.Token(woosh.NAME, 'def', 59, 4, 59, 7),
woosh.Token(woosh.NAME, 'pthread_sigmask', 59, 8, 59, 23),
woosh.Token(woosh.OP, '(', 59, 23, 59, 24),
woosh.Token(woosh.NAME, 'how', 59, 24, 59, 27),
woosh.Token(woosh.OP, ',', 59, 27, 59, 28),
woosh.Token(woosh.NAME, 'mask', 59, 29, 59, 33),
woosh.Token(woosh.OP, ')', 59, 33, 59, 34),
woosh.Token(woosh.OP, ':', 59, 34, 59, 35),
woosh.Token(woosh.NEWLINE, '\r\n', 59, 35, 60, 0),
woosh.Token(woosh.INDENT, '        ', 60, 0, 60, 8),
woosh.Token(woosh.NAME, 'sigs_set', 60, 8, 60, 16),
woosh.Token(woosh.OP, '=', 60, 17, 60, 18),
woosh.Token(woosh.NAME, '_signal', 60, 19, 60, 26),
woosh.Token(woosh.OP, '.', 60, 26, 60, 27),
woosh.Token(woosh.NAME, 'pthread_sigmask', 60, 27, 60, 42),
woosh.Token(woosh.OP, '(', 60, 42, 60, 43),
woosh.Token(woosh.NAME, 'how', 60, 43, 60, 46),
woosh.Token(woosh.OP, ',', 60, 46, 60, 47),
woosh.Token(woosh.NAME, 'mask', 60, 48, 60, 52),
woosh.Token(woosh.OP, ')', 60, 52, 60, 53),
woosh.Token(woosh.NEWLINE, '\r\n', 60, 53, 61, 0),
woosh.Token(woosh.NAME, 'return', 61, 8, 61, 14),
woosh.Token(woosh.NAME, 'set', 61, 15, 61, 18),
woosh.Token(woosh.OP, '(', 61, 18, 61, 19),
woosh.Token(woosh.NAME, '_int_to_enum', 61, 19, 61, 31),
woosh.Token(woosh.OP, '(', 61, 31, 61, 32),
woosh.Token(woosh.NAME, 'x', 61, 32, 61, 33),
woosh.Token(woosh.OP, ',', 61, 33, 61, 34),
woosh.Token(woosh.NAME, 'Signals', 61, 35, 61, 42),
woosh.Token(woosh.OP, ')', 61, 42, 61, 43),
woosh.Token(woosh.NAME, 'for', 61, 44, 61, 47),
woosh.Token(woosh.NAME, 'x', 61, 48, 61, 49),
woosh.Token(woosh.NAME, 'in', 61, 50, 61, 52),
woosh.Token(woosh.NAME, 'sigs_set', 61, 53, 61, 61),
woosh.Token(woosh.OP, ')', 61, 61, 61, 62),
woosh.Token(woosh.NEWLINE, '\r\n', 61, 62, 62, 0),
woosh.Token(woosh.DEDENT, '    ', 62, 0, 62, 4),
woosh.Token(woosh.NAME, 'pthread_sigmask', 62, 4, 62, 19),
woosh.Token(woosh.OP, '.', 62, 19, 62, 20),
woosh.Token(woosh.NAME, '__doc__', 62, 20, 62, 27),
woosh.Token(woosh.OP, '=', 62, 28, 62, 29),
woosh.Token(woosh.NAME, '_signal', 62, 30, 62, 37),
woosh.Token(woosh.OP, '.', 62, 37, 62, 38),
woosh.Token(woosh.NAME, 'pthread_sigmask', 62, 38, 62, 53),
woosh.Token(woosh.OP, '.', 62, 53, 62, 54),
woosh.Token(woosh.NAME, '__doc__', 62, 54, 62, 61),
woosh.Token(woosh.NEWLINE, '\r\n', 62, 61, 63, 0),
woosh.Token(woosh.DEDENT, '', 65, 0, 65, 0),
woosh.Token(woosh.NAME, 'if', 65, 0, 65, 2),
woosh.Token(woosh.STRING, "'sigpending'", 65, 3, 65, 15),
woosh.Token(woosh.NAME, 'in', 65, 16, 65, 18),
woosh.Token(woosh.NAME, '_globals', 65, 19, 65, 27),
woosh.Token(woosh.OP, ':', 65, 27, 65, 28),
woosh.Token(woosh.NEWLINE, '\r\n', 65, 28, 66, 0),
woosh.Token(woosh.INDENT, '    ', 66, 0, 66, 4),
woosh.Token(woosh.OP, '@', 66, 4, 66, 5),
woosh.Token(woosh.NAME, '_wraps', 66, 5, 66, 11),
woosh.Token(woosh.OP, '(', 66, 11, 66, 12),
woosh.Token(woosh.NAME, '_signal', 66, 12, 66, 19),
woosh.Token(woosh.OP, '.', 66, 19, 66, 20),
woosh.Token(woosh.NAME, 'sigpending', 66, 20, 66, 30),
woosh.Token(woosh.OP, ')', 66, 30, 66, 31),
woosh.Token(woosh.NEWLINE, '\r\n', 66, 31, 67, 0),
woosh.Token(woosh.NAME, 'def', 67, 4, 67, 7),
woosh.Token(woosh.NAME, 'sigpending', 67, 8, 67, 18),
woosh.Token(woosh.OP, '(', 67, 18, 67, 19),
woosh.Token(woosh.OP, ')', 67, 19, 67, 20),
woosh.Token(woosh.OP, ':', 67, 20, 67, 21),
woosh.Token(woosh.NEWLINE, '\r\n', 67, 21, 68, 0),
woosh.Token(woosh.INDENT, '        ', 68, 0, 68, 8),
woosh.Token(woosh.NAME, 'return', 68, 8, 68, 14),
woosh.Token(woosh.OP, '{', 68, 15, 68, 16),
woosh.Token(woosh.NAME, '_int_to_enum', 68, 16, 68, 28),
woosh.Token(woosh.OP, '(', 68, 28, 68, 29),
woosh.Token(woosh.NAME, 'x', 68, 29, 68, 30),
woosh.Token(woosh.OP, ',', 68, 30, 68, 31),
woosh.Token(woosh.NAME, 'Signals', 68, 32, 68, 39),
woosh.Token(woosh.OP, ')', 68, 39, 68, 40),
woosh.Token(woosh.NAME, 'for', 68, 41, 68, 44),
woosh.Token(woosh.NAME, 'x', 68, 45, 68, 46),
woosh.Token(woosh.NAME, 'in', 68, 47, 68, 49),
woosh.Token(woosh.NAME, '_signal', 68, 50, 68, 57),
woosh.Token(woosh.OP, '.', 68, 57, 68, 58),
woosh.Token(woosh.NAME, 'sigpending', 68, 58, 68, 68),
woosh.Token(woosh.OP, '(', 68, 68, 68, 69),
woosh.Token(woosh.OP, ')', 68, 69, 68, 70),
woosh.Token(woosh.OP, '}', 68, 70, 68, 71),
woosh.Token(woosh.NEWLINE, '\r\n', 68, 71, 69, 0),
woosh.Token(woosh.DEDENT, '', 71, 0, 71, 0),
woosh.Token(woosh.DEDENT, '', 71, 0, 71, 0),
woosh.Token(woosh.NAME, 'if', 71, 0, 71, 2),
woosh.Token(woosh.STRING, "'sigwait'", 71, 3, 71, 12),
woosh.Token(woosh.NAME, 'in', 71, 13, 71, 15),
woosh.Token(woosh.NAME, '_globals', 71, 16, 71, 24),
woosh.Token(woosh.OP, ':', 71, 24, 71, 25),
woosh.Token(woosh.NEWLINE, '\r\n', 71, 25, 72, 0),
woosh.Token(woosh.INDENT, '    ', 72, 0, 72, 4),
woosh.Token(woosh.OP, '@', 72, 4, 72, 5),
woosh.Token(woosh.NAME, '_wraps', 72, 5, 72, 11),
woosh.Token(woosh.OP, '(', 72, 11, 72, 12),
woosh.Token(woosh.NAME, '_signal', 72, 12, 72, 19),
woosh.Token(woosh.OP, '.', 72, 19, 72, 20),
woosh.Token(woosh.NAME, 'sigwait', 72, 20, 72, 27),
woosh.Token(woosh.OP, ')', 72, 27, 72, 28),
woosh.Token(woosh.NEWLINE, '\r\n', 72, 28, 73, 0),
woosh.Token(woosh.NAME, 'def', 73, 4, 73, 7),
woosh.Token(woosh.NAME, 'sigwait', 73, 8, 73, 15),
woosh.Token(woosh.OP, '(', 73, 15, 73, 16),
woosh.Token(woosh.NAME, 'sigset', 73, 16, 73, 22),
woosh.Token(woosh.OP, ')', 73, 22, 73, 23),
woosh.Token(woosh.OP, ':', 73, 23, 73, 24),
woosh.Token(woosh.NEWLINE, '\r\n', 73, 24, 74, 0),
woosh.Token(woosh.INDENT, '        ', 74, 0, 74, 8),
woosh.Token(woosh.NAME, 'retsig', 74, 8, 74, 14),
woosh.Token(woosh.OP, '=', 74, 15, 74, 16),
woosh.Token(woosh.NAME, '_signal', 74, 17, 74, 24),
woosh.Token(woosh.OP, '.', 74, 24, 74, 25),
woosh.Token(woosh.NAME, 'sigwait', 74, 25, 74, 32),
woosh.Token(woosh.OP, '(', 74, 32, 74, 33),
woosh.Token(woosh.NAME, 'sigset', 74, 33, 74, 39),
woosh.Token(woosh.OP, ')', 74, 39, 74, 40),
woosh.Token(woosh.NEWLINE, '\r\n', 74, 40, 75, 0),
woosh.Token(woosh.NAME, 'return', 75, 8, 75, 14),
woosh.Token(woosh.NAME, '_int_to_enum', 75, 15, 75, 27),
woosh.Token(woosh.OP, '(', 75, 27, 75, 28),
woosh.Token(woosh.NAME, 'retsig', 75, 28, 75, 34),
woosh.Token(woosh.OP, ',', 75, 34, 75, 35),
woosh.Token(woosh.NAME, 'Signals', 75, 36, 75, 43),
woosh.Token(woosh.OP, ')', 75, 43, 75, 44),
woosh.Token(woosh.NEWLINE, '\r\n', 75, 44, 76, 0),
woosh.Token(woosh.DEDENT, '    ', 76, 0, 76, 4),
woosh.Token(woosh.NAME, 'sigwait', 76, 4, 76, 11),
woosh.Token(woosh.OP, '.', 76, 11, 76, 12),
woosh.Token(woosh.NAME, '__doc__', 76, 12, 76, 19),
woosh.Token(woosh.OP, '=', 76, 20, 76, 21),
woosh.Token(woosh.NAME, '_signal', 76, 22, 76, 29),
woosh.Token(woosh.OP, '.', 76, 29, 76, 30),
woosh.Token(woosh.NAME, 'sigwait', 76, 30, 76, 37),
woosh.Token(woosh.NEWLINE, '\r\n', 76, 37, 77, 0),
woosh.Token(woosh.DEDENT, '', 79, 0, 79, 0),
woosh.Token(woosh.NAME, 'if', 79, 0, 79, 2),
woosh.Token(woosh.STRING, "'valid_signals'", 79, 3, 79, 18),
woosh.Token(woosh.NAME, 'in', 79, 19, 79, 21),
woosh.Token(woosh.NAME, '_globals', 79, 22, 79, 30),
woosh.Token(woosh.OP, ':', 79, 30, 79, 31),
woosh.Token(woosh.NEWLINE, '\r\n', 79, 31, 80, 0),
woosh.Token(woosh.INDENT, '    ', 80, 0, 80, 4),
woosh.Token(woosh.OP, '@', 80, 4, 80, 5),
woosh.Token(woosh.NAME, '_wraps', 80, 5, 80, 11),
woosh.Token(woosh.OP, '(', 80, 11, 80, 12),
woosh.Token(woosh.NAME, '_signal', 80, 12, 80, 19),
woosh.Token(woosh.OP, '.', 80, 19, 80, 20),
woosh.Token(woosh.NAME, 'valid_signals', 80, 20, 80, 33),
woosh.Token(woosh.OP, ')', 80, 33, 80, 34),
woosh.Token(woosh.NEWLINE, '\r\n', 80, 34, 81, 0),
woosh.Token(woosh.NAME, 'def', 81, 4, 81, 7),
woosh.Token(woosh.NAME, 'valid_signals', 81, 8, 81, 21),
woosh.Token(woosh.OP, '(', 81, 21, 81, 22),
woosh.Token(woosh.OP, ')', 81, 22, 81, 23),
woosh.Token(woosh.OP, ':', 81, 23, 81, 24),
woosh.Token(woosh.NEWLINE, '\r\n', 81, 24, 82, 0),
woosh.Token(woosh.INDENT, '        ', 82, 0, 82, 8),
woosh.Token(woosh.NAME, 'return', 82, 8, 82, 14),
woosh.Token(woosh.OP, '{', 82, 15, 82, 16),
woosh.Token(woosh.NAME, '_int_to_enum', 82, 16, 82, 28),
woosh.Token(woosh.OP, '(', 82, 28, 82, 29),
woosh.Token(woosh.NAME, 'x', 82, 29, 82, 30),
woosh.Token(woosh.OP, ',', 82, 30, 82, 31),
woosh.Token(woosh.NAME, 'Signals', 82, 32, 82, 39),
woosh.Token(woosh.OP, ')', 82, 39, 82, 40),
woosh.Token(woosh.NAME, 'for', 82, 41, 82, 44),
woosh.Token(woosh.NAME, 'x', 82, 45, 82, 46),
woosh.Token(woosh.NAME, 'in', 82, 47, 82, 49),
woosh.Token(woosh.NAME, '_signal', 82, 50, 82, 57),
woosh.Token(woosh.OP, '.', 82, 57, 82, 58),
woosh.Token(woosh.NAME, 'valid_signals', 82, 58, 82, 71),
woosh.Token(woosh.OP, '(', 82, 71, 82, 72),
woosh.Token(woosh.OP, ')', 82, 72, 82, 73),
woosh.Token(woosh.OP, '}', 82, 73, 82, 74),
woosh.Token(woosh.NEWLINE, '\r\n', 82, 74, 83, 0),
woosh.Token(woosh.DEDENT, '', 85, 0, 85, 0),
woosh.Token(woosh.DEDENT, '', 85, 0, 85, 0),
woosh.Token(woosh.NAME, 'del', 85, 0, 85, 3),
woosh.Token(woosh.NAME, '_globals', 85, 4, 85, 12),
woosh.Token(woosh.OP, ',', 85, 12, 85, 13),
woosh.Token(woosh.NAME, '_wraps', 85, 14, 85, 20),
woosh.Token(woosh.NEWLINE, '\r\n', 85, 20, 86, 0),
woosh.Token(woosh.EOF, '', 86, 0, 86, 0),
]

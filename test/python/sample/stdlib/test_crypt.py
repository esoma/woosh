
# this file was generated using test/python/sample/generate.py

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
    with open(SAMPLE_DIR / 'stdlib/crypt.py', 'rb') as f:
        tokens = tokenize(f.read())
    for token, expected in zip(tokens, EXPECTED):
        assert token == expected

EXPECTED = [
woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
woosh.Token(woosh.STRING, '"""Wrapper to the POSIX crypt library call and associated functionality."""', 1, 0, 1, 75),
woosh.Token(woosh.NEWLINE, '\r\n', 1, 75, 2, 0),
woosh.Token(woosh.NAME, 'import', 3, 0, 3, 6),
woosh.Token(woosh.NAME, 'sys', 3, 7, 3, 10),
woosh.Token(woosh.NAME, 'as', 3, 11, 3, 13),
woosh.Token(woosh.NAME, '_sys', 3, 14, 3, 18),
woosh.Token(woosh.NEWLINE, '\r\n', 3, 18, 4, 0),
woosh.Token(woosh.NAME, 'try', 5, 0, 5, 3),
woosh.Token(woosh.OP, ':', 5, 3, 5, 4),
woosh.Token(woosh.NEWLINE, '\r\n', 5, 4, 6, 0),
woosh.Token(woosh.INDENT, '    ', 6, 0, 6, 4),
woosh.Token(woosh.NAME, 'import', 6, 4, 6, 10),
woosh.Token(woosh.NAME, '_crypt', 6, 11, 6, 17),
woosh.Token(woosh.NEWLINE, '\r\n', 6, 17, 7, 0),
woosh.Token(woosh.DEDENT, '', 7, 0, 7, 0),
woosh.Token(woosh.NAME, 'except', 7, 0, 7, 6),
woosh.Token(woosh.NAME, 'ModuleNotFoundError', 7, 7, 7, 26),
woosh.Token(woosh.OP, ':', 7, 26, 7, 27),
woosh.Token(woosh.NEWLINE, '\r\n', 7, 27, 8, 0),
woosh.Token(woosh.INDENT, '    ', 8, 0, 8, 4),
woosh.Token(woosh.NAME, 'if', 8, 4, 8, 6),
woosh.Token(woosh.NAME, '_sys', 8, 7, 8, 11),
woosh.Token(woosh.OP, '.', 8, 11, 8, 12),
woosh.Token(woosh.NAME, 'platform', 8, 12, 8, 20),
woosh.Token(woosh.OP, '==', 8, 21, 8, 23),
woosh.Token(woosh.STRING, "'win32'", 8, 24, 8, 31),
woosh.Token(woosh.OP, ':', 8, 31, 8, 32),
woosh.Token(woosh.NEWLINE, '\r\n', 8, 32, 9, 0),
woosh.Token(woosh.INDENT, '        ', 9, 0, 9, 8),
woosh.Token(woosh.NAME, 'raise', 9, 8, 9, 13),
woosh.Token(woosh.NAME, 'ImportError', 9, 14, 9, 25),
woosh.Token(woosh.OP, '(', 9, 25, 9, 26),
woosh.Token(woosh.STRING, '"The crypt module is not supported on Windows"', 9, 26, 9, 72),
woosh.Token(woosh.OP, ')', 9, 72, 9, 73),
woosh.Token(woosh.NEWLINE, '\r\n', 9, 73, 10, 0),
woosh.Token(woosh.DEDENT, '    ', 10, 0, 10, 4),
woosh.Token(woosh.NAME, 'else', 10, 4, 10, 8),
woosh.Token(woosh.OP, ':', 10, 8, 10, 9),
woosh.Token(woosh.NEWLINE, '\r\n', 10, 9, 11, 0),
woosh.Token(woosh.INDENT, '        ', 11, 0, 11, 8),
woosh.Token(woosh.NAME, 'raise', 11, 8, 11, 13),
woosh.Token(woosh.NAME, 'ImportError', 11, 14, 11, 25),
woosh.Token(woosh.OP, '(', 11, 25, 11, 26),
woosh.Token(woosh.STRING, '"The required _crypt module was not built as part of CPython"', 11, 26, 11, 87),
woosh.Token(woosh.OP, ')', 11, 87, 11, 88),
woosh.Token(woosh.NEWLINE, '\r\n', 11, 88, 12, 0),
woosh.Token(woosh.DEDENT, '', 13, 0, 13, 0),
woosh.Token(woosh.DEDENT, '', 13, 0, 13, 0),
woosh.Token(woosh.NAME, 'import', 13, 0, 13, 6),
woosh.Token(woosh.NAME, 'errno', 13, 7, 13, 12),
woosh.Token(woosh.NEWLINE, '\r\n', 13, 12, 14, 0),
woosh.Token(woosh.NAME, 'import', 14, 0, 14, 6),
woosh.Token(woosh.NAME, 'string', 14, 7, 14, 13),
woosh.Token(woosh.NAME, 'as', 14, 14, 14, 16),
woosh.Token(woosh.NAME, '_string', 14, 17, 14, 24),
woosh.Token(woosh.NEWLINE, '\r\n', 14, 24, 15, 0),
woosh.Token(woosh.NAME, 'from', 15, 0, 15, 4),
woosh.Token(woosh.NAME, 'random', 15, 5, 15, 11),
woosh.Token(woosh.NAME, 'import', 15, 12, 15, 18),
woosh.Token(woosh.NAME, 'SystemRandom', 15, 19, 15, 31),
woosh.Token(woosh.NAME, 'as', 15, 32, 15, 34),
woosh.Token(woosh.NAME, '_SystemRandom', 15, 35, 15, 48),
woosh.Token(woosh.NEWLINE, '\r\n', 15, 48, 16, 0),
woosh.Token(woosh.NAME, 'from', 16, 0, 16, 4),
woosh.Token(woosh.NAME, 'collections', 16, 5, 16, 16),
woosh.Token(woosh.NAME, 'import', 16, 17, 16, 23),
woosh.Token(woosh.NAME, 'namedtuple', 16, 24, 16, 34),
woosh.Token(woosh.NAME, 'as', 16, 35, 16, 37),
woosh.Token(woosh.NAME, '_namedtuple', 16, 38, 16, 49),
woosh.Token(woosh.NEWLINE, '\r\n', 16, 49, 17, 0),
woosh.Token(woosh.NAME, '_saltchars', 19, 0, 19, 10),
woosh.Token(woosh.OP, '=', 19, 11, 19, 12),
woosh.Token(woosh.NAME, '_string', 19, 13, 19, 20),
woosh.Token(woosh.OP, '.', 19, 20, 19, 21),
woosh.Token(woosh.NAME, 'ascii_letters', 19, 21, 19, 34),
woosh.Token(woosh.OP, '+', 19, 35, 19, 36),
woosh.Token(woosh.NAME, '_string', 19, 37, 19, 44),
woosh.Token(woosh.OP, '.', 19, 44, 19, 45),
woosh.Token(woosh.NAME, 'digits', 19, 45, 19, 51),
woosh.Token(woosh.OP, '+', 19, 52, 19, 53),
woosh.Token(woosh.STRING, "'./'", 19, 54, 19, 58),
woosh.Token(woosh.NEWLINE, '\r\n', 19, 58, 20, 0),
woosh.Token(woosh.NAME, '_sr', 20, 0, 20, 3),
woosh.Token(woosh.OP, '=', 20, 4, 20, 5),
woosh.Token(woosh.NAME, '_SystemRandom', 20, 6, 20, 19),
woosh.Token(woosh.OP, '(', 20, 19, 20, 20),
woosh.Token(woosh.OP, ')', 20, 20, 20, 21),
woosh.Token(woosh.NEWLINE, '\r\n', 20, 21, 21, 0),
woosh.Token(woosh.NAME, 'class', 23, 0, 23, 5),
woosh.Token(woosh.NAME, '_Method', 23, 6, 23, 13),
woosh.Token(woosh.OP, '(', 23, 13, 23, 14),
woosh.Token(woosh.NAME, '_namedtuple', 23, 14, 23, 25),
woosh.Token(woosh.OP, '(', 23, 25, 23, 26),
woosh.Token(woosh.STRING, "'_Method'", 23, 26, 23, 35),
woosh.Token(woosh.OP, ',', 23, 35, 23, 36),
woosh.Token(woosh.STRING, "'name ident salt_chars total_size'", 23, 37, 23, 71),
woosh.Token(woosh.OP, ')', 23, 71, 23, 72),
woosh.Token(woosh.OP, ')', 23, 72, 23, 73),
woosh.Token(woosh.OP, ':', 23, 73, 23, 74),
woosh.Token(woosh.NEWLINE, '\r\n', 23, 74, 24, 0),
woosh.Token(woosh.INDENT, '    ', 25, 0, 25, 4),
woosh.Token(woosh.STRING, '"""Class representing a salt method per the Modular Crypt Format or the\r\n    legacy 2-character crypt method."""', 25, 4, 26, 39),
woosh.Token(woosh.NEWLINE, '\r\n', 26, 39, 27, 0),
woosh.Token(woosh.NAME, 'def', 28, 4, 28, 7),
woosh.Token(woosh.NAME, '__repr__', 28, 8, 28, 16),
woosh.Token(woosh.OP, '(', 28, 16, 28, 17),
woosh.Token(woosh.NAME, 'self', 28, 17, 28, 21),
woosh.Token(woosh.OP, ')', 28, 21, 28, 22),
woosh.Token(woosh.OP, ':', 28, 22, 28, 23),
woosh.Token(woosh.NEWLINE, '\r\n', 28, 23, 29, 0),
woosh.Token(woosh.INDENT, '        ', 29, 0, 29, 8),
woosh.Token(woosh.NAME, 'return', 29, 8, 29, 14),
woosh.Token(woosh.STRING, "'<crypt.METHOD_{}>'", 29, 15, 29, 34),
woosh.Token(woosh.OP, '.', 29, 34, 29, 35),
woosh.Token(woosh.NAME, 'format', 29, 35, 29, 41),
woosh.Token(woosh.OP, '(', 29, 41, 29, 42),
woosh.Token(woosh.NAME, 'self', 29, 42, 29, 46),
woosh.Token(woosh.OP, '.', 29, 46, 29, 47),
woosh.Token(woosh.NAME, 'name', 29, 47, 29, 51),
woosh.Token(woosh.OP, ')', 29, 51, 29, 52),
woosh.Token(woosh.NEWLINE, '\r\n', 29, 52, 30, 0),
woosh.Token(woosh.DEDENT, '', 32, 0, 32, 0),
woosh.Token(woosh.DEDENT, '', 32, 0, 32, 0),
woosh.Token(woosh.NAME, 'def', 32, 0, 32, 3),
woosh.Token(woosh.NAME, 'mksalt', 32, 4, 32, 10),
woosh.Token(woosh.OP, '(', 32, 10, 32, 11),
woosh.Token(woosh.NAME, 'method', 32, 11, 32, 17),
woosh.Token(woosh.OP, '=', 32, 17, 32, 18),
woosh.Token(woosh.NAME, 'None', 32, 18, 32, 22),
woosh.Token(woosh.OP, ',', 32, 22, 32, 23),
woosh.Token(woosh.OP, '*', 32, 24, 32, 25),
woosh.Token(woosh.OP, ',', 32, 25, 32, 26),
woosh.Token(woosh.NAME, 'rounds', 32, 27, 32, 33),
woosh.Token(woosh.OP, '=', 32, 33, 32, 34),
woosh.Token(woosh.NAME, 'None', 32, 34, 32, 38),
woosh.Token(woosh.OP, ')', 32, 38, 32, 39),
woosh.Token(woosh.OP, ':', 32, 39, 32, 40),
woosh.Token(woosh.NEWLINE, '\r\n', 32, 40, 33, 0),
woosh.Token(woosh.INDENT, '    ', 33, 0, 33, 4),
woosh.Token(woosh.STRING, '"""Generate a salt for the specified method.\r\n\r\n    If not specified, the strongest available method will be used.\r\n\r\n    """', 33, 4, 37, 7),
woosh.Token(woosh.NEWLINE, '\r\n', 37, 7, 38, 0),
woosh.Token(woosh.NAME, 'if', 38, 4, 38, 6),
woosh.Token(woosh.NAME, 'method', 38, 7, 38, 13),
woosh.Token(woosh.NAME, 'is', 38, 14, 38, 16),
woosh.Token(woosh.NAME, 'None', 38, 17, 38, 21),
woosh.Token(woosh.OP, ':', 38, 21, 38, 22),
woosh.Token(woosh.NEWLINE, '\r\n', 38, 22, 39, 0),
woosh.Token(woosh.INDENT, '        ', 39, 0, 39, 8),
woosh.Token(woosh.NAME, 'method', 39, 8, 39, 14),
woosh.Token(woosh.OP, '=', 39, 15, 39, 16),
woosh.Token(woosh.NAME, 'methods', 39, 17, 39, 24),
woosh.Token(woosh.OP, '[', 39, 24, 39, 25),
woosh.Token(woosh.NUMBER, '0', 39, 25, 39, 26),
woosh.Token(woosh.OP, ']', 39, 26, 39, 27),
woosh.Token(woosh.NEWLINE, '\r\n', 39, 27, 40, 0),
woosh.Token(woosh.DEDENT, '    ', 40, 0, 40, 4),
woosh.Token(woosh.NAME, 'if', 40, 4, 40, 6),
woosh.Token(woosh.NAME, 'rounds', 40, 7, 40, 13),
woosh.Token(woosh.NAME, 'is', 40, 14, 40, 16),
woosh.Token(woosh.NAME, 'not', 40, 17, 40, 20),
woosh.Token(woosh.NAME, 'None', 40, 21, 40, 25),
woosh.Token(woosh.NAME, 'and', 40, 26, 40, 29),
woosh.Token(woosh.NAME, 'not', 40, 30, 40, 33),
woosh.Token(woosh.NAME, 'isinstance', 40, 34, 40, 44),
woosh.Token(woosh.OP, '(', 40, 44, 40, 45),
woosh.Token(woosh.NAME, 'rounds', 40, 45, 40, 51),
woosh.Token(woosh.OP, ',', 40, 51, 40, 52),
woosh.Token(woosh.NAME, 'int', 40, 53, 40, 56),
woosh.Token(woosh.OP, ')', 40, 56, 40, 57),
woosh.Token(woosh.OP, ':', 40, 57, 40, 58),
woosh.Token(woosh.NEWLINE, '\r\n', 40, 58, 41, 0),
woosh.Token(woosh.INDENT, '        ', 41, 0, 41, 8),
woosh.Token(woosh.NAME, 'raise', 41, 8, 41, 13),
woosh.Token(woosh.NAME, 'TypeError', 41, 14, 41, 23),
woosh.Token(woosh.OP, '(', 41, 23, 41, 24),
woosh.Token(woosh.STRING, "f'{rounds.__class__.__name__} object cannot be '", 41, 24, 41, 72),
woosh.Token(woosh.STRING, "f'interpreted as an integer'", 42, 24, 42, 52),
woosh.Token(woosh.OP, ')', 42, 52, 42, 53),
woosh.Token(woosh.NEWLINE, '\r\n', 42, 53, 43, 0),
woosh.Token(woosh.DEDENT, '    ', 43, 0, 43, 4),
woosh.Token(woosh.NAME, 'if', 43, 4, 43, 6),
woosh.Token(woosh.NAME, 'not', 43, 7, 43, 10),
woosh.Token(woosh.NAME, 'method', 43, 11, 43, 17),
woosh.Token(woosh.OP, '.', 43, 17, 43, 18),
woosh.Token(woosh.NAME, 'ident', 43, 18, 43, 23),
woosh.Token(woosh.OP, ':', 43, 23, 43, 24),
woosh.Token(woosh.COMMENT, '# traditional', 43, 26, 43, 39),
woosh.Token(woosh.NEWLINE, '\r\n', 43, 39, 44, 0),
woosh.Token(woosh.INDENT, '        ', 44, 0, 44, 8),
woosh.Token(woosh.NAME, 's', 44, 8, 44, 9),
woosh.Token(woosh.OP, '=', 44, 10, 44, 11),
woosh.Token(woosh.STRING, "''", 44, 12, 44, 14),
woosh.Token(woosh.NEWLINE, '\r\n', 44, 14, 45, 0),
woosh.Token(woosh.DEDENT, '    ', 45, 0, 45, 4),
woosh.Token(woosh.NAME, 'else', 45, 4, 45, 8),
woosh.Token(woosh.OP, ':', 45, 8, 45, 9),
woosh.Token(woosh.COMMENT, '# modular', 45, 11, 45, 20),
woosh.Token(woosh.NEWLINE, '\r\n', 45, 20, 46, 0),
woosh.Token(woosh.INDENT, '        ', 46, 0, 46, 8),
woosh.Token(woosh.NAME, 's', 46, 8, 46, 9),
woosh.Token(woosh.OP, '=', 46, 10, 46, 11),
woosh.Token(woosh.STRING, "f'${method.ident}$'", 46, 12, 46, 31),
woosh.Token(woosh.NEWLINE, '\r\n', 46, 31, 47, 0),
woosh.Token(woosh.DEDENT, '    ', 48, 0, 48, 4),
woosh.Token(woosh.NAME, 'if', 48, 4, 48, 6),
woosh.Token(woosh.NAME, 'method', 48, 7, 48, 13),
woosh.Token(woosh.OP, '.', 48, 13, 48, 14),
woosh.Token(woosh.NAME, 'ident', 48, 14, 48, 19),
woosh.Token(woosh.NAME, 'and', 48, 20, 48, 23),
woosh.Token(woosh.NAME, 'method', 48, 24, 48, 30),
woosh.Token(woosh.OP, '.', 48, 30, 48, 31),
woosh.Token(woosh.NAME, 'ident', 48, 31, 48, 36),
woosh.Token(woosh.OP, '[', 48, 36, 48, 37),
woosh.Token(woosh.NUMBER, '0', 48, 37, 48, 38),
woosh.Token(woosh.OP, ']', 48, 38, 48, 39),
woosh.Token(woosh.OP, '==', 48, 40, 48, 42),
woosh.Token(woosh.STRING, "'2'", 48, 43, 48, 46),
woosh.Token(woosh.OP, ':', 48, 46, 48, 47),
woosh.Token(woosh.COMMENT, '# Blowfish variants', 48, 49, 48, 68),
woosh.Token(woosh.NEWLINE, '\r\n', 48, 68, 49, 0),
woosh.Token(woosh.INDENT, '        ', 49, 0, 49, 8),
woosh.Token(woosh.NAME, 'if', 49, 8, 49, 10),
woosh.Token(woosh.NAME, 'rounds', 49, 11, 49, 17),
woosh.Token(woosh.NAME, 'is', 49, 18, 49, 20),
woosh.Token(woosh.NAME, 'None', 49, 21, 49, 25),
woosh.Token(woosh.OP, ':', 49, 25, 49, 26),
woosh.Token(woosh.NEWLINE, '\r\n', 49, 26, 50, 0),
woosh.Token(woosh.INDENT, '            ', 50, 0, 50, 12),
woosh.Token(woosh.NAME, 'log_rounds', 50, 12, 50, 22),
woosh.Token(woosh.OP, '=', 50, 23, 50, 24),
woosh.Token(woosh.NUMBER, '12', 50, 25, 50, 27),
woosh.Token(woosh.NEWLINE, '\r\n', 50, 27, 51, 0),
woosh.Token(woosh.DEDENT, '        ', 51, 0, 51, 8),
woosh.Token(woosh.NAME, 'else', 51, 8, 51, 12),
woosh.Token(woosh.OP, ':', 51, 12, 51, 13),
woosh.Token(woosh.NEWLINE, '\r\n', 51, 13, 52, 0),
woosh.Token(woosh.INDENT, '            ', 52, 0, 52, 12),
woosh.Token(woosh.NAME, 'log_rounds', 52, 12, 52, 22),
woosh.Token(woosh.OP, '=', 52, 23, 52, 24),
woosh.Token(woosh.NAME, 'int', 52, 25, 52, 28),
woosh.Token(woosh.OP, '.', 52, 28, 52, 29),
woosh.Token(woosh.NAME, 'bit_length', 52, 29, 52, 39),
woosh.Token(woosh.OP, '(', 52, 39, 52, 40),
woosh.Token(woosh.NAME, 'rounds', 52, 40, 52, 46),
woosh.Token(woosh.OP, '-', 52, 46, 52, 47),
woosh.Token(woosh.NUMBER, '1', 52, 47, 52, 48),
woosh.Token(woosh.OP, ')', 52, 48, 52, 49),
woosh.Token(woosh.NEWLINE, '\r\n', 52, 49, 53, 0),
woosh.Token(woosh.NAME, 'if', 53, 12, 53, 14),
woosh.Token(woosh.NAME, 'rounds', 53, 15, 53, 21),
woosh.Token(woosh.OP, '!=', 53, 22, 53, 24),
woosh.Token(woosh.NUMBER, '1', 53, 25, 53, 26),
woosh.Token(woosh.OP, '<<', 53, 27, 53, 29),
woosh.Token(woosh.NAME, 'log_rounds', 53, 30, 53, 40),
woosh.Token(woosh.OP, ':', 53, 40, 53, 41),
woosh.Token(woosh.NEWLINE, '\r\n', 53, 41, 54, 0),
woosh.Token(woosh.INDENT, '                ', 54, 0, 54, 16),
woosh.Token(woosh.NAME, 'raise', 54, 16, 54, 21),
woosh.Token(woosh.NAME, 'ValueError', 54, 22, 54, 32),
woosh.Token(woosh.OP, '(', 54, 32, 54, 33),
woosh.Token(woosh.STRING, "'rounds must be a power of 2'", 54, 33, 54, 62),
woosh.Token(woosh.OP, ')', 54, 62, 54, 63),
woosh.Token(woosh.NEWLINE, '\r\n', 54, 63, 55, 0),
woosh.Token(woosh.DEDENT, '            ', 55, 0, 55, 12),
woosh.Token(woosh.NAME, 'if', 55, 12, 55, 14),
woosh.Token(woosh.NAME, 'not', 55, 15, 55, 18),
woosh.Token(woosh.NUMBER, '4', 55, 19, 55, 20),
woosh.Token(woosh.OP, '<=', 55, 21, 55, 23),
woosh.Token(woosh.NAME, 'log_rounds', 55, 24, 55, 34),
woosh.Token(woosh.OP, '<=', 55, 35, 55, 37),
woosh.Token(woosh.NUMBER, '31', 55, 38, 55, 40),
woosh.Token(woosh.OP, ':', 55, 40, 55, 41),
woosh.Token(woosh.NEWLINE, '\r\n', 55, 41, 56, 0),
woosh.Token(woosh.INDENT, '                ', 56, 0, 56, 16),
woosh.Token(woosh.NAME, 'raise', 56, 16, 56, 21),
woosh.Token(woosh.NAME, 'ValueError', 56, 22, 56, 32),
woosh.Token(woosh.OP, '(', 56, 32, 56, 33),
woosh.Token(woosh.STRING, "'rounds out of the range 2**4 to 2**31'", 56, 33, 56, 72),
woosh.Token(woosh.OP, ')', 56, 72, 56, 73),
woosh.Token(woosh.NEWLINE, '\r\n', 56, 73, 57, 0),
woosh.Token(woosh.DEDENT, '        ', 57, 0, 57, 8),
woosh.Token(woosh.DEDENT, '', 57, 8, 57, 8),
woosh.Token(woosh.NAME, 's', 57, 8, 57, 9),
woosh.Token(woosh.OP, '+=', 57, 10, 57, 12),
woosh.Token(woosh.STRING, "f'{log_rounds:02d}$'", 57, 13, 57, 33),
woosh.Token(woosh.NEWLINE, '\r\n', 57, 33, 58, 0),
woosh.Token(woosh.DEDENT, '    ', 58, 0, 58, 4),
woosh.Token(woosh.NAME, 'elif', 58, 4, 58, 8),
woosh.Token(woosh.NAME, 'method', 58, 9, 58, 15),
woosh.Token(woosh.OP, '.', 58, 15, 58, 16),
woosh.Token(woosh.NAME, 'ident', 58, 16, 58, 21),
woosh.Token(woosh.NAME, 'in', 58, 22, 58, 24),
woosh.Token(woosh.OP, '(', 58, 25, 58, 26),
woosh.Token(woosh.STRING, "'5'", 58, 26, 58, 29),
woosh.Token(woosh.OP, ',', 58, 29, 58, 30),
woosh.Token(woosh.STRING, "'6'", 58, 31, 58, 34),
woosh.Token(woosh.OP, ')', 58, 34, 58, 35),
woosh.Token(woosh.OP, ':', 58, 35, 58, 36),
woosh.Token(woosh.COMMENT, '# SHA-2', 58, 38, 58, 45),
woosh.Token(woosh.NEWLINE, '\r\n', 58, 45, 59, 0),
woosh.Token(woosh.INDENT, '        ', 59, 0, 59, 8),
woosh.Token(woosh.NAME, 'if', 59, 8, 59, 10),
woosh.Token(woosh.NAME, 'rounds', 59, 11, 59, 17),
woosh.Token(woosh.NAME, 'is', 59, 18, 59, 20),
woosh.Token(woosh.NAME, 'not', 59, 21, 59, 24),
woosh.Token(woosh.NAME, 'None', 59, 25, 59, 29),
woosh.Token(woosh.OP, ':', 59, 29, 59, 30),
woosh.Token(woosh.NEWLINE, '\r\n', 59, 30, 60, 0),
woosh.Token(woosh.INDENT, '            ', 60, 0, 60, 12),
woosh.Token(woosh.NAME, 'if', 60, 12, 60, 14),
woosh.Token(woosh.NAME, 'not', 60, 15, 60, 18),
woosh.Token(woosh.NUMBER, '1000', 60, 19, 60, 23),
woosh.Token(woosh.OP, '<=', 60, 24, 60, 26),
woosh.Token(woosh.NAME, 'rounds', 60, 27, 60, 33),
woosh.Token(woosh.OP, '<=', 60, 34, 60, 36),
woosh.Token(woosh.NUMBER, '999_999_999', 60, 37, 60, 48),
woosh.Token(woosh.OP, ':', 60, 48, 60, 49),
woosh.Token(woosh.NEWLINE, '\r\n', 60, 49, 61, 0),
woosh.Token(woosh.INDENT, '                ', 61, 0, 61, 16),
woosh.Token(woosh.NAME, 'raise', 61, 16, 61, 21),
woosh.Token(woosh.NAME, 'ValueError', 61, 22, 61, 32),
woosh.Token(woosh.OP, '(', 61, 32, 61, 33),
woosh.Token(woosh.STRING, "'rounds out of the range 1000 to 999_999_999'", 61, 33, 61, 78),
woosh.Token(woosh.OP, ')', 61, 78, 61, 79),
woosh.Token(woosh.NEWLINE, '\r\n', 61, 79, 62, 0),
woosh.Token(woosh.DEDENT, '            ', 62, 0, 62, 12),
woosh.Token(woosh.NAME, 's', 62, 12, 62, 13),
woosh.Token(woosh.OP, '+=', 62, 14, 62, 16),
woosh.Token(woosh.STRING, "f'rounds={rounds}$'", 62, 17, 62, 36),
woosh.Token(woosh.NEWLINE, '\r\n', 62, 36, 63, 0),
woosh.Token(woosh.DEDENT, '    ', 63, 0, 63, 4),
woosh.Token(woosh.DEDENT, '', 63, 4, 63, 4),
woosh.Token(woosh.NAME, 'elif', 63, 4, 63, 8),
woosh.Token(woosh.NAME, 'rounds', 63, 9, 63, 15),
woosh.Token(woosh.NAME, 'is', 63, 16, 63, 18),
woosh.Token(woosh.NAME, 'not', 63, 19, 63, 22),
woosh.Token(woosh.NAME, 'None', 63, 23, 63, 27),
woosh.Token(woosh.OP, ':', 63, 27, 63, 28),
woosh.Token(woosh.NEWLINE, '\r\n', 63, 28, 64, 0),
woosh.Token(woosh.INDENT, '        ', 64, 0, 64, 8),
woosh.Token(woosh.NAME, 'raise', 64, 8, 64, 13),
woosh.Token(woosh.NAME, 'ValueError', 64, 14, 64, 24),
woosh.Token(woosh.OP, '(', 64, 24, 64, 25),
woosh.Token(woosh.STRING, 'f"{method} doesn\'t support the rounds argument"', 64, 25, 64, 72),
woosh.Token(woosh.OP, ')', 64, 72, 64, 73),
woosh.Token(woosh.NEWLINE, '\r\n', 64, 73, 65, 0),
woosh.Token(woosh.DEDENT, '    ', 66, 0, 66, 4),
woosh.Token(woosh.NAME, 's', 66, 4, 66, 5),
woosh.Token(woosh.OP, '+=', 66, 6, 66, 8),
woosh.Token(woosh.STRING, "''", 66, 9, 66, 11),
woosh.Token(woosh.OP, '.', 66, 11, 66, 12),
woosh.Token(woosh.NAME, 'join', 66, 12, 66, 16),
woosh.Token(woosh.OP, '(', 66, 16, 66, 17),
woosh.Token(woosh.NAME, '_sr', 66, 17, 66, 20),
woosh.Token(woosh.OP, '.', 66, 20, 66, 21),
woosh.Token(woosh.NAME, 'choice', 66, 21, 66, 27),
woosh.Token(woosh.OP, '(', 66, 27, 66, 28),
woosh.Token(woosh.NAME, '_saltchars', 66, 28, 66, 38),
woosh.Token(woosh.OP, ')', 66, 38, 66, 39),
woosh.Token(woosh.NAME, 'for', 66, 40, 66, 43),
woosh.Token(woosh.NAME, 'char', 66, 44, 66, 48),
woosh.Token(woosh.NAME, 'in', 66, 49, 66, 51),
woosh.Token(woosh.NAME, 'range', 66, 52, 66, 57),
woosh.Token(woosh.OP, '(', 66, 57, 66, 58),
woosh.Token(woosh.NAME, 'method', 66, 58, 66, 64),
woosh.Token(woosh.OP, '.', 66, 64, 66, 65),
woosh.Token(woosh.NAME, 'salt_chars', 66, 65, 66, 75),
woosh.Token(woosh.OP, ')', 66, 75, 66, 76),
woosh.Token(woosh.OP, ')', 66, 76, 66, 77),
woosh.Token(woosh.NEWLINE, '\r\n', 66, 77, 67, 0),
woosh.Token(woosh.NAME, 'return', 67, 4, 67, 10),
woosh.Token(woosh.NAME, 's', 67, 11, 67, 12),
woosh.Token(woosh.NEWLINE, '\r\n', 67, 12, 68, 0),
woosh.Token(woosh.DEDENT, '', 70, 0, 70, 0),
woosh.Token(woosh.NAME, 'def', 70, 0, 70, 3),
woosh.Token(woosh.NAME, 'crypt', 70, 4, 70, 9),
woosh.Token(woosh.OP, '(', 70, 9, 70, 10),
woosh.Token(woosh.NAME, 'word', 70, 10, 70, 14),
woosh.Token(woosh.OP, ',', 70, 14, 70, 15),
woosh.Token(woosh.NAME, 'salt', 70, 16, 70, 20),
woosh.Token(woosh.OP, '=', 70, 20, 70, 21),
woosh.Token(woosh.NAME, 'None', 70, 21, 70, 25),
woosh.Token(woosh.OP, ')', 70, 25, 70, 26),
woosh.Token(woosh.OP, ':', 70, 26, 70, 27),
woosh.Token(woosh.NEWLINE, '\r\n', 70, 27, 71, 0),
woosh.Token(woosh.INDENT, '    ', 71, 0, 71, 4),
woosh.Token(woosh.STRING, '"""Return a string representing the one-way hash of a password, with a salt\r\n    prepended.\r\n\r\n    If ``salt`` is not specified or is ``None``, the strongest\r\n    available method will be selected and a salt generated.  Otherwise,\r\n    ``salt`` may be one of the ``crypt.METHOD_*`` values, or a string as\r\n    returned by ``crypt.mksalt()``.\r\n\r\n    """', 71, 4, 79, 7),
woosh.Token(woosh.NEWLINE, '\r\n', 79, 7, 80, 0),
woosh.Token(woosh.NAME, 'if', 80, 4, 80, 6),
woosh.Token(woosh.NAME, 'salt', 80, 7, 80, 11),
woosh.Token(woosh.NAME, 'is', 80, 12, 80, 14),
woosh.Token(woosh.NAME, 'None', 80, 15, 80, 19),
woosh.Token(woosh.NAME, 'or', 80, 20, 80, 22),
woosh.Token(woosh.NAME, 'isinstance', 80, 23, 80, 33),
woosh.Token(woosh.OP, '(', 80, 33, 80, 34),
woosh.Token(woosh.NAME, 'salt', 80, 34, 80, 38),
woosh.Token(woosh.OP, ',', 80, 38, 80, 39),
woosh.Token(woosh.NAME, '_Method', 80, 40, 80, 47),
woosh.Token(woosh.OP, ')', 80, 47, 80, 48),
woosh.Token(woosh.OP, ':', 80, 48, 80, 49),
woosh.Token(woosh.NEWLINE, '\r\n', 80, 49, 81, 0),
woosh.Token(woosh.INDENT, '        ', 81, 0, 81, 8),
woosh.Token(woosh.NAME, 'salt', 81, 8, 81, 12),
woosh.Token(woosh.OP, '=', 81, 13, 81, 14),
woosh.Token(woosh.NAME, 'mksalt', 81, 15, 81, 21),
woosh.Token(woosh.OP, '(', 81, 21, 81, 22),
woosh.Token(woosh.NAME, 'salt', 81, 22, 81, 26),
woosh.Token(woosh.OP, ')', 81, 26, 81, 27),
woosh.Token(woosh.NEWLINE, '\r\n', 81, 27, 82, 0),
woosh.Token(woosh.DEDENT, '    ', 82, 0, 82, 4),
woosh.Token(woosh.NAME, 'return', 82, 4, 82, 10),
woosh.Token(woosh.NAME, '_crypt', 82, 11, 82, 17),
woosh.Token(woosh.OP, '.', 82, 17, 82, 18),
woosh.Token(woosh.NAME, 'crypt', 82, 18, 82, 23),
woosh.Token(woosh.OP, '(', 82, 23, 82, 24),
woosh.Token(woosh.NAME, 'word', 82, 24, 82, 28),
woosh.Token(woosh.OP, ',', 82, 28, 82, 29),
woosh.Token(woosh.NAME, 'salt', 82, 30, 82, 34),
woosh.Token(woosh.OP, ')', 82, 34, 82, 35),
woosh.Token(woosh.NEWLINE, '\r\n', 82, 35, 83, 0),
woosh.Token(woosh.COMMENT, '#  available salting/crypto methods', 85, 0, 85, 35),
woosh.Token(woosh.DEDENT, '', 86, 0, 86, 0),
woosh.Token(woosh.NAME, 'methods', 86, 0, 86, 7),
woosh.Token(woosh.OP, '=', 86, 8, 86, 9),
woosh.Token(woosh.OP, '[', 86, 10, 86, 11),
woosh.Token(woosh.OP, ']', 86, 11, 86, 12),
woosh.Token(woosh.NEWLINE, '\r\n', 86, 12, 87, 0),
woosh.Token(woosh.NAME, 'def', 88, 0, 88, 3),
woosh.Token(woosh.NAME, '_add_method', 88, 4, 88, 15),
woosh.Token(woosh.OP, '(', 88, 15, 88, 16),
woosh.Token(woosh.NAME, 'name', 88, 16, 88, 20),
woosh.Token(woosh.OP, ',', 88, 20, 88, 21),
woosh.Token(woosh.OP, '*', 88, 22, 88, 23),
woosh.Token(woosh.NAME, 'args', 88, 23, 88, 27),
woosh.Token(woosh.OP, ',', 88, 27, 88, 28),
woosh.Token(woosh.NAME, 'rounds', 88, 29, 88, 35),
woosh.Token(woosh.OP, '=', 88, 35, 88, 36),
woosh.Token(woosh.NAME, 'None', 88, 36, 88, 40),
woosh.Token(woosh.OP, ')', 88, 40, 88, 41),
woosh.Token(woosh.OP, ':', 88, 41, 88, 42),
woosh.Token(woosh.NEWLINE, '\r\n', 88, 42, 89, 0),
woosh.Token(woosh.INDENT, '    ', 89, 0, 89, 4),
woosh.Token(woosh.NAME, 'method', 89, 4, 89, 10),
woosh.Token(woosh.OP, '=', 89, 11, 89, 12),
woosh.Token(woosh.NAME, '_Method', 89, 13, 89, 20),
woosh.Token(woosh.OP, '(', 89, 20, 89, 21),
woosh.Token(woosh.NAME, 'name', 89, 21, 89, 25),
woosh.Token(woosh.OP, ',', 89, 25, 89, 26),
woosh.Token(woosh.OP, '*', 89, 27, 89, 28),
woosh.Token(woosh.NAME, 'args', 89, 28, 89, 32),
woosh.Token(woosh.OP, ')', 89, 32, 89, 33),
woosh.Token(woosh.NEWLINE, '\r\n', 89, 33, 90, 0),
woosh.Token(woosh.NAME, 'globals', 90, 4, 90, 11),
woosh.Token(woosh.OP, '(', 90, 11, 90, 12),
woosh.Token(woosh.OP, ')', 90, 12, 90, 13),
woosh.Token(woosh.OP, '[', 90, 13, 90, 14),
woosh.Token(woosh.STRING, "'METHOD_'", 90, 14, 90, 23),
woosh.Token(woosh.OP, '+', 90, 24, 90, 25),
woosh.Token(woosh.NAME, 'name', 90, 26, 90, 30),
woosh.Token(woosh.OP, ']', 90, 30, 90, 31),
woosh.Token(woosh.OP, '=', 90, 32, 90, 33),
woosh.Token(woosh.NAME, 'method', 90, 34, 90, 40),
woosh.Token(woosh.NEWLINE, '\r\n', 90, 40, 91, 0),
woosh.Token(woosh.NAME, 'salt', 91, 4, 91, 8),
woosh.Token(woosh.OP, '=', 91, 9, 91, 10),
woosh.Token(woosh.NAME, 'mksalt', 91, 11, 91, 17),
woosh.Token(woosh.OP, '(', 91, 17, 91, 18),
woosh.Token(woosh.NAME, 'method', 91, 18, 91, 24),
woosh.Token(woosh.OP, ',', 91, 24, 91, 25),
woosh.Token(woosh.NAME, 'rounds', 91, 26, 91, 32),
woosh.Token(woosh.OP, '=', 91, 32, 91, 33),
woosh.Token(woosh.NAME, 'rounds', 91, 33, 91, 39),
woosh.Token(woosh.OP, ')', 91, 39, 91, 40),
woosh.Token(woosh.NEWLINE, '\r\n', 91, 40, 92, 0),
woosh.Token(woosh.NAME, 'result', 92, 4, 92, 10),
woosh.Token(woosh.OP, '=', 92, 11, 92, 12),
woosh.Token(woosh.NAME, 'None', 92, 13, 92, 17),
woosh.Token(woosh.NEWLINE, '\r\n', 92, 17, 93, 0),
woosh.Token(woosh.NAME, 'try', 93, 4, 93, 7),
woosh.Token(woosh.OP, ':', 93, 7, 93, 8),
woosh.Token(woosh.NEWLINE, '\r\n', 93, 8, 94, 0),
woosh.Token(woosh.INDENT, '        ', 94, 0, 94, 8),
woosh.Token(woosh.NAME, 'result', 94, 8, 94, 14),
woosh.Token(woosh.OP, '=', 94, 15, 94, 16),
woosh.Token(woosh.NAME, 'crypt', 94, 17, 94, 22),
woosh.Token(woosh.OP, '(', 94, 22, 94, 23),
woosh.Token(woosh.STRING, "''", 94, 23, 94, 25),
woosh.Token(woosh.OP, ',', 94, 25, 94, 26),
woosh.Token(woosh.NAME, 'salt', 94, 27, 94, 31),
woosh.Token(woosh.OP, ')', 94, 31, 94, 32),
woosh.Token(woosh.NEWLINE, '\r\n', 94, 32, 95, 0),
woosh.Token(woosh.DEDENT, '    ', 95, 0, 95, 4),
woosh.Token(woosh.NAME, 'except', 95, 4, 95, 10),
woosh.Token(woosh.NAME, 'OSError', 95, 11, 95, 18),
woosh.Token(woosh.NAME, 'as', 95, 19, 95, 21),
woosh.Token(woosh.NAME, 'e', 95, 22, 95, 23),
woosh.Token(woosh.OP, ':', 95, 23, 95, 24),
woosh.Token(woosh.NEWLINE, '\r\n', 95, 24, 96, 0),
woosh.Token(woosh.COMMENT, '# Not all libc libraries support all encryption methods.', 96, 8, 96, 64),
woosh.Token(woosh.INDENT, '        ', 97, 0, 97, 8),
woosh.Token(woosh.NAME, 'if', 97, 8, 97, 10),
woosh.Token(woosh.NAME, 'e', 97, 11, 97, 12),
woosh.Token(woosh.OP, '.', 97, 12, 97, 13),
woosh.Token(woosh.NAME, 'errno', 97, 13, 97, 18),
woosh.Token(woosh.OP, '==', 97, 19, 97, 21),
woosh.Token(woosh.NAME, 'errno', 97, 22, 97, 27),
woosh.Token(woosh.OP, '.', 97, 27, 97, 28),
woosh.Token(woosh.NAME, 'EINVAL', 97, 28, 97, 34),
woosh.Token(woosh.OP, ':', 97, 34, 97, 35),
woosh.Token(woosh.NEWLINE, '\r\n', 97, 35, 98, 0),
woosh.Token(woosh.INDENT, '            ', 98, 0, 98, 12),
woosh.Token(woosh.NAME, 'return', 98, 12, 98, 18),
woosh.Token(woosh.NAME, 'False', 98, 19, 98, 24),
woosh.Token(woosh.NEWLINE, '\r\n', 98, 24, 99, 0),
woosh.Token(woosh.DEDENT, '        ', 99, 0, 99, 8),
woosh.Token(woosh.NAME, 'raise', 99, 8, 99, 13),
woosh.Token(woosh.NEWLINE, '\r\n', 99, 13, 100, 0),
woosh.Token(woosh.DEDENT, '    ', 100, 0, 100, 4),
woosh.Token(woosh.NAME, 'if', 100, 4, 100, 6),
woosh.Token(woosh.NAME, 'result', 100, 7, 100, 13),
woosh.Token(woosh.NAME, 'and', 100, 14, 100, 17),
woosh.Token(woosh.NAME, 'len', 100, 18, 100, 21),
woosh.Token(woosh.OP, '(', 100, 21, 100, 22),
woosh.Token(woosh.NAME, 'result', 100, 22, 100, 28),
woosh.Token(woosh.OP, ')', 100, 28, 100, 29),
woosh.Token(woosh.OP, '==', 100, 30, 100, 32),
woosh.Token(woosh.NAME, 'method', 100, 33, 100, 39),
woosh.Token(woosh.OP, '.', 100, 39, 100, 40),
woosh.Token(woosh.NAME, 'total_size', 100, 40, 100, 50),
woosh.Token(woosh.OP, ':', 100, 50, 100, 51),
woosh.Token(woosh.NEWLINE, '\r\n', 100, 51, 101, 0),
woosh.Token(woosh.INDENT, '        ', 101, 0, 101, 8),
woosh.Token(woosh.NAME, 'methods', 101, 8, 101, 15),
woosh.Token(woosh.OP, '.', 101, 15, 101, 16),
woosh.Token(woosh.NAME, 'append', 101, 16, 101, 22),
woosh.Token(woosh.OP, '(', 101, 22, 101, 23),
woosh.Token(woosh.NAME, 'method', 101, 23, 101, 29),
woosh.Token(woosh.OP, ')', 101, 29, 101, 30),
woosh.Token(woosh.NEWLINE, '\r\n', 101, 30, 102, 0),
woosh.Token(woosh.NAME, 'return', 102, 8, 102, 14),
woosh.Token(woosh.NAME, 'True', 102, 15, 102, 19),
woosh.Token(woosh.NEWLINE, '\r\n', 102, 19, 103, 0),
woosh.Token(woosh.DEDENT, '    ', 103, 0, 103, 4),
woosh.Token(woosh.NAME, 'return', 103, 4, 103, 10),
woosh.Token(woosh.NAME, 'False', 103, 11, 103, 16),
woosh.Token(woosh.NEWLINE, '\r\n', 103, 16, 104, 0),
woosh.Token(woosh.DEDENT, '', 105, 0, 105, 0),
woosh.Token(woosh.NAME, '_add_method', 105, 0, 105, 11),
woosh.Token(woosh.OP, '(', 105, 11, 105, 12),
woosh.Token(woosh.STRING, "'SHA512'", 105, 12, 105, 20),
woosh.Token(woosh.OP, ',', 105, 20, 105, 21),
woosh.Token(woosh.STRING, "'6'", 105, 22, 105, 25),
woosh.Token(woosh.OP, ',', 105, 25, 105, 26),
woosh.Token(woosh.NUMBER, '16', 105, 27, 105, 29),
woosh.Token(woosh.OP, ',', 105, 29, 105, 30),
woosh.Token(woosh.NUMBER, '106', 105, 31, 105, 34),
woosh.Token(woosh.OP, ')', 105, 34, 105, 35),
woosh.Token(woosh.NEWLINE, '\r\n', 105, 35, 106, 0),
woosh.Token(woosh.NAME, '_add_method', 106, 0, 106, 11),
woosh.Token(woosh.OP, '(', 106, 11, 106, 12),
woosh.Token(woosh.STRING, "'SHA256'", 106, 12, 106, 20),
woosh.Token(woosh.OP, ',', 106, 20, 106, 21),
woosh.Token(woosh.STRING, "'5'", 106, 22, 106, 25),
woosh.Token(woosh.OP, ',', 106, 25, 106, 26),
woosh.Token(woosh.NUMBER, '16', 106, 27, 106, 29),
woosh.Token(woosh.OP, ',', 106, 29, 106, 30),
woosh.Token(woosh.NUMBER, '63', 106, 31, 106, 33),
woosh.Token(woosh.OP, ')', 106, 33, 106, 34),
woosh.Token(woosh.NEWLINE, '\r\n', 106, 34, 107, 0),
woosh.Token(woosh.COMMENT, '# Choose the strongest supported version of Blowfish hashing.', 108, 0, 108, 61),
woosh.Token(woosh.COMMENT, "# Early versions have flaws.  Version 'a' fixes flaws of", 109, 0, 109, 56),
woosh.Token(woosh.COMMENT, "# the initial implementation, 'b' fixes flaws of 'a'.", 110, 0, 110, 53),
woosh.Token(woosh.COMMENT, "# 'y' is the same as 'b', for compatibility", 111, 0, 111, 43),
woosh.Token(woosh.COMMENT, '# with openwall crypt_blowfish.', 112, 0, 112, 31),
woosh.Token(woosh.NAME, 'for', 113, 0, 113, 3),
woosh.Token(woosh.NAME, '_v', 113, 4, 113, 6),
woosh.Token(woosh.NAME, 'in', 113, 7, 113, 9),
woosh.Token(woosh.STRING, "'b'", 113, 10, 113, 13),
woosh.Token(woosh.OP, ',', 113, 13, 113, 14),
woosh.Token(woosh.STRING, "'y'", 113, 15, 113, 18),
woosh.Token(woosh.OP, ',', 113, 18, 113, 19),
woosh.Token(woosh.STRING, "'a'", 113, 20, 113, 23),
woosh.Token(woosh.OP, ',', 113, 23, 113, 24),
woosh.Token(woosh.STRING, "''", 113, 25, 113, 27),
woosh.Token(woosh.OP, ':', 113, 27, 113, 28),
woosh.Token(woosh.NEWLINE, '\r\n', 113, 28, 114, 0),
woosh.Token(woosh.INDENT, '    ', 114, 0, 114, 4),
woosh.Token(woosh.NAME, 'if', 114, 4, 114, 6),
woosh.Token(woosh.NAME, '_add_method', 114, 7, 114, 18),
woosh.Token(woosh.OP, '(', 114, 18, 114, 19),
woosh.Token(woosh.STRING, "'BLOWFISH'", 114, 19, 114, 29),
woosh.Token(woosh.OP, ',', 114, 29, 114, 30),
woosh.Token(woosh.STRING, "'2'", 114, 31, 114, 34),
woosh.Token(woosh.OP, '+', 114, 35, 114, 36),
woosh.Token(woosh.NAME, '_v', 114, 37, 114, 39),
woosh.Token(woosh.OP, ',', 114, 39, 114, 40),
woosh.Token(woosh.NUMBER, '22', 114, 41, 114, 43),
woosh.Token(woosh.OP, ',', 114, 43, 114, 44),
woosh.Token(woosh.NUMBER, '59', 114, 45, 114, 47),
woosh.Token(woosh.OP, '+', 114, 48, 114, 49),
woosh.Token(woosh.NAME, 'len', 114, 50, 114, 53),
woosh.Token(woosh.OP, '(', 114, 53, 114, 54),
woosh.Token(woosh.NAME, '_v', 114, 54, 114, 56),
woosh.Token(woosh.OP, ')', 114, 56, 114, 57),
woosh.Token(woosh.OP, ',', 114, 57, 114, 58),
woosh.Token(woosh.NAME, 'rounds', 114, 59, 114, 65),
woosh.Token(woosh.OP, '=', 114, 65, 114, 66),
woosh.Token(woosh.NUMBER, '1', 114, 66, 114, 67),
woosh.Token(woosh.OP, '<<', 114, 67, 114, 69),
woosh.Token(woosh.NUMBER, '4', 114, 69, 114, 70),
woosh.Token(woosh.OP, ')', 114, 70, 114, 71),
woosh.Token(woosh.OP, ':', 114, 71, 114, 72),
woosh.Token(woosh.NEWLINE, '\r\n', 114, 72, 115, 0),
woosh.Token(woosh.INDENT, '        ', 115, 0, 115, 8),
woosh.Token(woosh.NAME, 'break', 115, 8, 115, 13),
woosh.Token(woosh.NEWLINE, '\r\n', 115, 13, 116, 0),
woosh.Token(woosh.DEDENT, '', 117, 0, 117, 0),
woosh.Token(woosh.DEDENT, '', 117, 0, 117, 0),
woosh.Token(woosh.NAME, '_add_method', 117, 0, 117, 11),
woosh.Token(woosh.OP, '(', 117, 11, 117, 12),
woosh.Token(woosh.STRING, "'MD5'", 117, 12, 117, 17),
woosh.Token(woosh.OP, ',', 117, 17, 117, 18),
woosh.Token(woosh.STRING, "'1'", 117, 19, 117, 22),
woosh.Token(woosh.OP, ',', 117, 22, 117, 23),
woosh.Token(woosh.NUMBER, '8', 117, 24, 117, 25),
woosh.Token(woosh.OP, ',', 117, 25, 117, 26),
woosh.Token(woosh.NUMBER, '34', 117, 27, 117, 29),
woosh.Token(woosh.OP, ')', 117, 29, 117, 30),
woosh.Token(woosh.NEWLINE, '\r\n', 117, 30, 118, 0),
woosh.Token(woosh.NAME, '_add_method', 118, 0, 118, 11),
woosh.Token(woosh.OP, '(', 118, 11, 118, 12),
woosh.Token(woosh.STRING, "'CRYPT'", 118, 12, 118, 19),
woosh.Token(woosh.OP, ',', 118, 19, 118, 20),
woosh.Token(woosh.NAME, 'None', 118, 21, 118, 25),
woosh.Token(woosh.OP, ',', 118, 25, 118, 26),
woosh.Token(woosh.NUMBER, '2', 118, 27, 118, 28),
woosh.Token(woosh.OP, ',', 118, 28, 118, 29),
woosh.Token(woosh.NUMBER, '13', 118, 30, 118, 32),
woosh.Token(woosh.OP, ')', 118, 32, 118, 33),
woosh.Token(woosh.NEWLINE, '\r\n', 118, 33, 119, 0),
woosh.Token(woosh.NAME, 'del', 120, 0, 120, 3),
woosh.Token(woosh.NAME, '_v', 120, 4, 120, 6),
woosh.Token(woosh.OP, ',', 120, 6, 120, 7),
woosh.Token(woosh.NAME, '_add_method', 120, 8, 120, 19),
woosh.Token(woosh.NEWLINE, '\r\n', 120, 19, 121, 0),
woosh.Token(woosh.EOF, '', 121, 0, 121, 0),
]

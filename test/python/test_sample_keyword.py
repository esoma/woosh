
# python
import pathlib
# woosh
import woosh

SAMPLE_DIR = pathlib.Path(__file__).parent.absolute() / '../../sample/'
def test():
    with open(SAMPLE_DIR / 'keyword.py', 'rb') as f:
        tokens = list(woosh.tokenize(f))
    assert tokens == EXPECTED

EXPECTED = [
    woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
    woosh.Token(woosh.STRING, '"""Keywords (from "Grammar/python.gram")\r\n\r\nThis file is automatically generated; please don\'t muck it up!\r\n\r\nTo update the symbols in this file, \'cd\' to the top directory of\r\nthe python source tree and run:\r\n\r\n    PYTHONPATH=Tools/peg_generator python3 -m pegen.keywordgen \\\r\n        Grammar/python.gram \\\r\n        Grammar/Tokens \\\r\n        Lib/keyword.py\r\n\r\nAlternatively, you can run \'make regen-keyword\'.\r\n"""', 1, 0, 14, 3),
    woosh.Token(woosh.NEWLINE, '\r\n', 14, 3, 15, 0),
    woosh.Token(woosh.NAME, '__all__', 16, 0, 16, 7),
    woosh.Token(woosh.OP, '=', 16, 8, 16, 9),
    woosh.Token(woosh.OP, '[', 16, 10, 16, 11),
    woosh.Token(woosh.STRING, '"iskeyword"', 16, 11, 16, 22),
    woosh.Token(woosh.OP, ',', 16, 22, 16, 23),
    woosh.Token(woosh.STRING, '"issoftkeyword"', 16, 24, 16, 39),
    woosh.Token(woosh.OP, ',', 16, 39, 16, 40),
    woosh.Token(woosh.STRING, '"kwlist"', 16, 41, 16, 49),
    woosh.Token(woosh.OP, ',', 16, 49, 16, 50),
    woosh.Token(woosh.STRING, '"softkwlist"', 16, 51, 16, 63),
    woosh.Token(woosh.OP, ']', 16, 63, 16, 64),
    woosh.Token(woosh.NEWLINE, '\r\n', 16, 64, 17, 0),
    woosh.Token(woosh.NAME, 'kwlist', 18, 0, 18, 6),
    woosh.Token(woosh.OP, '=', 18, 7, 18, 8),
    woosh.Token(woosh.OP, '[', 18, 9, 18, 10),
    woosh.Token(woosh.STRING, "'False'", 19, 4, 19, 11),
    woosh.Token(woosh.OP, ',', 19, 11, 19, 12),
    woosh.Token(woosh.STRING, "'None'", 20, 4, 20, 10),
    woosh.Token(woosh.OP, ',', 20, 10, 20, 11),
    woosh.Token(woosh.STRING, "'True'", 21, 4, 21, 10),
    woosh.Token(woosh.OP, ',', 21, 10, 21, 11),
    woosh.Token(woosh.STRING, "'and'", 22, 4, 22, 9),
    woosh.Token(woosh.OP, ',', 22, 9, 22, 10),
    woosh.Token(woosh.STRING, "'as'", 23, 4, 23, 8),
    woosh.Token(woosh.OP, ',', 23, 8, 23, 9),
    woosh.Token(woosh.STRING, "'assert'", 24, 4, 24, 12),
    woosh.Token(woosh.OP, ',', 24, 12, 24, 13),
    woosh.Token(woosh.STRING, "'async'", 25, 4, 25, 11),
    woosh.Token(woosh.OP, ',', 25, 11, 25, 12),
    woosh.Token(woosh.STRING, "'await'", 26, 4, 26, 11),
    woosh.Token(woosh.OP, ',', 26, 11, 26, 12),
    woosh.Token(woosh.STRING, "'break'", 27, 4, 27, 11),
    woosh.Token(woosh.OP, ',', 27, 11, 27, 12),
    woosh.Token(woosh.STRING, "'class'", 28, 4, 28, 11),
    woosh.Token(woosh.OP, ',', 28, 11, 28, 12),
    woosh.Token(woosh.STRING, "'continue'", 29, 4, 29, 14),
    woosh.Token(woosh.OP, ',', 29, 14, 29, 15),
    woosh.Token(woosh.STRING, "'def'", 30, 4, 30, 9),
    woosh.Token(woosh.OP, ',', 30, 9, 30, 10),
    woosh.Token(woosh.STRING, "'del'", 31, 4, 31, 9),
    woosh.Token(woosh.OP, ',', 31, 9, 31, 10),
    woosh.Token(woosh.STRING, "'elif'", 32, 4, 32, 10),
    woosh.Token(woosh.OP, ',', 32, 10, 32, 11),
    woosh.Token(woosh.STRING, "'else'", 33, 4, 33, 10),
    woosh.Token(woosh.OP, ',', 33, 10, 33, 11),
    woosh.Token(woosh.STRING, "'except'", 34, 4, 34, 12),
    woosh.Token(woosh.OP, ',', 34, 12, 34, 13),
    woosh.Token(woosh.STRING, "'finally'", 35, 4, 35, 13),
    woosh.Token(woosh.OP, ',', 35, 13, 35, 14),
    woosh.Token(woosh.STRING, "'for'", 36, 4, 36, 9),
    woosh.Token(woosh.OP, ',', 36, 9, 36, 10),
    woosh.Token(woosh.STRING, "'from'", 37, 4, 37, 10),
    woosh.Token(woosh.OP, ',', 37, 10, 37, 11),
    woosh.Token(woosh.STRING, "'global'", 38, 4, 38, 12),
    woosh.Token(woosh.OP, ',', 38, 12, 38, 13),
    woosh.Token(woosh.STRING, "'if'", 39, 4, 39, 8),
    woosh.Token(woosh.OP, ',', 39, 8, 39, 9),
    woosh.Token(woosh.STRING, "'import'", 40, 4, 40, 12),
    woosh.Token(woosh.OP, ',', 40, 12, 40, 13),
    woosh.Token(woosh.STRING, "'in'", 41, 4, 41, 8),
    woosh.Token(woosh.OP, ',', 41, 8, 41, 9),
    woosh.Token(woosh.STRING, "'is'", 42, 4, 42, 8),
    woosh.Token(woosh.OP, ',', 42, 8, 42, 9),
    woosh.Token(woosh.STRING, "'lambda'", 43, 4, 43, 12),
    woosh.Token(woosh.OP, ',', 43, 12, 43, 13),
    woosh.Token(woosh.STRING, "'nonlocal'", 44, 4, 44, 14),
    woosh.Token(woosh.OP, ',', 44, 14, 44, 15),
    woosh.Token(woosh.STRING, "'not'", 45, 4, 45, 9),
    woosh.Token(woosh.OP, ',', 45, 9, 45, 10),
    woosh.Token(woosh.STRING, "'or'", 46, 4, 46, 8),
    woosh.Token(woosh.OP, ',', 46, 8, 46, 9),
    woosh.Token(woosh.STRING, "'pass'", 47, 4, 47, 10),
    woosh.Token(woosh.OP, ',', 47, 10, 47, 11),
    woosh.Token(woosh.STRING, "'raise'", 48, 4, 48, 11),
    woosh.Token(woosh.OP, ',', 48, 11, 48, 12),
    woosh.Token(woosh.STRING, "'return'", 49, 4, 49, 12),
    woosh.Token(woosh.OP, ',', 49, 12, 49, 13),
    woosh.Token(woosh.STRING, "'try'", 50, 4, 50, 9),
    woosh.Token(woosh.OP, ',', 50, 9, 50, 10),
    woosh.Token(woosh.STRING, "'while'", 51, 4, 51, 11),
    woosh.Token(woosh.OP, ',', 51, 11, 51, 12),
    woosh.Token(woosh.STRING, "'with'", 52, 4, 52, 10),
    woosh.Token(woosh.OP, ',', 52, 10, 52, 11),
    woosh.Token(woosh.STRING, "'yield'", 53, 4, 53, 11),
    woosh.Token(woosh.OP, ']', 54, 0, 54, 1),
    woosh.Token(woosh.NEWLINE, '\r\n', 54, 1, 55, 0),
    woosh.Token(woosh.NAME, 'softkwlist', 56, 0, 56, 10),
    woosh.Token(woosh.OP, '=', 56, 11, 56, 12),
    woosh.Token(woosh.OP, '[', 56, 13, 56, 14),
    woosh.Token(woosh.OP, ']', 58, 0, 58, 1),
    woosh.Token(woosh.NEWLINE, '\r\n', 58, 1, 59, 0),
    woosh.Token(woosh.NAME, 'iskeyword', 60, 0, 60, 9),
    woosh.Token(woosh.OP, '=', 60, 10, 60, 11),
    woosh.Token(woosh.NAME, 'frozenset', 60, 12, 60, 21),
    woosh.Token(woosh.OP, '(', 60, 21, 60, 22),
    woosh.Token(woosh.NAME, 'kwlist', 60, 22, 60, 28),
    woosh.Token(woosh.OP, ')', 60, 28, 60, 29),
    woosh.Token(woosh.OP, '.', 60, 29, 60, 30),
    woosh.Token(woosh.NAME, '__contains__', 60, 30, 60, 42),
    woosh.Token(woosh.NEWLINE, '\r\n', 60, 42, 61, 0),
    woosh.Token(woosh.NAME, 'issoftkeyword', 61, 0, 61, 13),
    woosh.Token(woosh.OP, '=', 61, 14, 61, 15),
    woosh.Token(woosh.NAME, 'frozenset', 61, 16, 61, 25),
    woosh.Token(woosh.OP, '(', 61, 25, 61, 26),
    woosh.Token(woosh.NAME, 'softkwlist', 61, 26, 61, 36),
    woosh.Token(woosh.OP, ')', 61, 36, 61, 37),
    woosh.Token(woosh.OP, '.', 61, 37, 61, 38),
    woosh.Token(woosh.NAME, '__contains__', 61, 38, 61, 50),
    woosh.Token(woosh.NEWLINE, '\r\n', 61, 50, 62, 0),
    woosh.Token(woosh.EOF, '', 62, 0, 62, 0),
]


# python
import pathlib
# woosh
import woosh

SAMPLE_DIR = pathlib.Path(__file__).parent.absolute() / '../../' / '../../' / 'sample'
def test():
    with open(SAMPLE_DIR / 'stdlib/token.py', 'rb') as f:
        tokens = list(woosh.tokenize(f))
    for token, expected in zip(tokens, EXPECTED):
        assert token == expected

EXPECTED = [
woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
woosh.Token(woosh.STRING, '"""Token constants."""', 1, 0, 1, 22),
woosh.Token(woosh.NEWLINE, '\r\n', 1, 22, 2, 0),
woosh.Token(woosh.COMMENT, '# Auto-generated by Tools/scripts/generate_token.py', 2, 0, 2, 51),
woosh.Token(woosh.NAME, '__all__', 4, 0, 4, 7),
woosh.Token(woosh.OP, '=', 4, 8, 4, 9),
woosh.Token(woosh.OP, '[', 4, 10, 4, 11),
woosh.Token(woosh.STRING, "'tok_name'", 4, 11, 4, 21),
woosh.Token(woosh.OP, ',', 4, 21, 4, 22),
woosh.Token(woosh.STRING, "'ISTERMINAL'", 4, 23, 4, 35),
woosh.Token(woosh.OP, ',', 4, 35, 4, 36),
woosh.Token(woosh.STRING, "'ISNONTERMINAL'", 4, 37, 4, 52),
woosh.Token(woosh.OP, ',', 4, 52, 4, 53),
woosh.Token(woosh.STRING, "'ISEOF'", 4, 54, 4, 61),
woosh.Token(woosh.OP, ']', 4, 61, 4, 62),
woosh.Token(woosh.NEWLINE, '\r\n', 4, 62, 5, 0),
woosh.Token(woosh.NAME, 'ENDMARKER', 6, 0, 6, 9),
woosh.Token(woosh.OP, '=', 6, 10, 6, 11),
woosh.Token(woosh.NUMBER, '0', 6, 12, 6, 13),
woosh.Token(woosh.NEWLINE, '\r\n', 6, 13, 7, 0),
woosh.Token(woosh.NAME, 'NAME', 7, 0, 7, 4),
woosh.Token(woosh.OP, '=', 7, 5, 7, 6),
woosh.Token(woosh.NUMBER, '1', 7, 7, 7, 8),
woosh.Token(woosh.NEWLINE, '\r\n', 7, 8, 8, 0),
woosh.Token(woosh.NAME, 'NUMBER', 8, 0, 8, 6),
woosh.Token(woosh.OP, '=', 8, 7, 8, 8),
woosh.Token(woosh.NUMBER, '2', 8, 9, 8, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 8, 10, 9, 0),
woosh.Token(woosh.NAME, 'STRING', 9, 0, 9, 6),
woosh.Token(woosh.OP, '=', 9, 7, 9, 8),
woosh.Token(woosh.NUMBER, '3', 9, 9, 9, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 9, 10, 10, 0),
woosh.Token(woosh.NAME, 'NEWLINE', 10, 0, 10, 7),
woosh.Token(woosh.OP, '=', 10, 8, 10, 9),
woosh.Token(woosh.NUMBER, '4', 10, 10, 10, 11),
woosh.Token(woosh.NEWLINE, '\r\n', 10, 11, 11, 0),
woosh.Token(woosh.NAME, 'INDENT', 11, 0, 11, 6),
woosh.Token(woosh.OP, '=', 11, 7, 11, 8),
woosh.Token(woosh.NUMBER, '5', 11, 9, 11, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 11, 10, 12, 0),
woosh.Token(woosh.NAME, 'DEDENT', 12, 0, 12, 6),
woosh.Token(woosh.OP, '=', 12, 7, 12, 8),
woosh.Token(woosh.NUMBER, '6', 12, 9, 12, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 12, 10, 13, 0),
woosh.Token(woosh.NAME, 'LPAR', 13, 0, 13, 4),
woosh.Token(woosh.OP, '=', 13, 5, 13, 6),
woosh.Token(woosh.NUMBER, '7', 13, 7, 13, 8),
woosh.Token(woosh.NEWLINE, '\r\n', 13, 8, 14, 0),
woosh.Token(woosh.NAME, 'RPAR', 14, 0, 14, 4),
woosh.Token(woosh.OP, '=', 14, 5, 14, 6),
woosh.Token(woosh.NUMBER, '8', 14, 7, 14, 8),
woosh.Token(woosh.NEWLINE, '\r\n', 14, 8, 15, 0),
woosh.Token(woosh.NAME, 'LSQB', 15, 0, 15, 4),
woosh.Token(woosh.OP, '=', 15, 5, 15, 6),
woosh.Token(woosh.NUMBER, '9', 15, 7, 15, 8),
woosh.Token(woosh.NEWLINE, '\r\n', 15, 8, 16, 0),
woosh.Token(woosh.NAME, 'RSQB', 16, 0, 16, 4),
woosh.Token(woosh.OP, '=', 16, 5, 16, 6),
woosh.Token(woosh.NUMBER, '10', 16, 7, 16, 9),
woosh.Token(woosh.NEWLINE, '\r\n', 16, 9, 17, 0),
woosh.Token(woosh.NAME, 'COLON', 17, 0, 17, 5),
woosh.Token(woosh.OP, '=', 17, 6, 17, 7),
woosh.Token(woosh.NUMBER, '11', 17, 8, 17, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 17, 10, 18, 0),
woosh.Token(woosh.NAME, 'COMMA', 18, 0, 18, 5),
woosh.Token(woosh.OP, '=', 18, 6, 18, 7),
woosh.Token(woosh.NUMBER, '12', 18, 8, 18, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 18, 10, 19, 0),
woosh.Token(woosh.NAME, 'SEMI', 19, 0, 19, 4),
woosh.Token(woosh.OP, '=', 19, 5, 19, 6),
woosh.Token(woosh.NUMBER, '13', 19, 7, 19, 9),
woosh.Token(woosh.NEWLINE, '\r\n', 19, 9, 20, 0),
woosh.Token(woosh.NAME, 'PLUS', 20, 0, 20, 4),
woosh.Token(woosh.OP, '=', 20, 5, 20, 6),
woosh.Token(woosh.NUMBER, '14', 20, 7, 20, 9),
woosh.Token(woosh.NEWLINE, '\r\n', 20, 9, 21, 0),
woosh.Token(woosh.NAME, 'MINUS', 21, 0, 21, 5),
woosh.Token(woosh.OP, '=', 21, 6, 21, 7),
woosh.Token(woosh.NUMBER, '15', 21, 8, 21, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 21, 10, 22, 0),
woosh.Token(woosh.NAME, 'STAR', 22, 0, 22, 4),
woosh.Token(woosh.OP, '=', 22, 5, 22, 6),
woosh.Token(woosh.NUMBER, '16', 22, 7, 22, 9),
woosh.Token(woosh.NEWLINE, '\r\n', 22, 9, 23, 0),
woosh.Token(woosh.NAME, 'SLASH', 23, 0, 23, 5),
woosh.Token(woosh.OP, '=', 23, 6, 23, 7),
woosh.Token(woosh.NUMBER, '17', 23, 8, 23, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 23, 10, 24, 0),
woosh.Token(woosh.NAME, 'VBAR', 24, 0, 24, 4),
woosh.Token(woosh.OP, '=', 24, 5, 24, 6),
woosh.Token(woosh.NUMBER, '18', 24, 7, 24, 9),
woosh.Token(woosh.NEWLINE, '\r\n', 24, 9, 25, 0),
woosh.Token(woosh.NAME, 'AMPER', 25, 0, 25, 5),
woosh.Token(woosh.OP, '=', 25, 6, 25, 7),
woosh.Token(woosh.NUMBER, '19', 25, 8, 25, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 25, 10, 26, 0),
woosh.Token(woosh.NAME, 'LESS', 26, 0, 26, 4),
woosh.Token(woosh.OP, '=', 26, 5, 26, 6),
woosh.Token(woosh.NUMBER, '20', 26, 7, 26, 9),
woosh.Token(woosh.NEWLINE, '\r\n', 26, 9, 27, 0),
woosh.Token(woosh.NAME, 'GREATER', 27, 0, 27, 7),
woosh.Token(woosh.OP, '=', 27, 8, 27, 9),
woosh.Token(woosh.NUMBER, '21', 27, 10, 27, 12),
woosh.Token(woosh.NEWLINE, '\r\n', 27, 12, 28, 0),
woosh.Token(woosh.NAME, 'EQUAL', 28, 0, 28, 5),
woosh.Token(woosh.OP, '=', 28, 6, 28, 7),
woosh.Token(woosh.NUMBER, '22', 28, 8, 28, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 28, 10, 29, 0),
woosh.Token(woosh.NAME, 'DOT', 29, 0, 29, 3),
woosh.Token(woosh.OP, '=', 29, 4, 29, 5),
woosh.Token(woosh.NUMBER, '23', 29, 6, 29, 8),
woosh.Token(woosh.NEWLINE, '\r\n', 29, 8, 30, 0),
woosh.Token(woosh.NAME, 'PERCENT', 30, 0, 30, 7),
woosh.Token(woosh.OP, '=', 30, 8, 30, 9),
woosh.Token(woosh.NUMBER, '24', 30, 10, 30, 12),
woosh.Token(woosh.NEWLINE, '\r\n', 30, 12, 31, 0),
woosh.Token(woosh.NAME, 'LBRACE', 31, 0, 31, 6),
woosh.Token(woosh.OP, '=', 31, 7, 31, 8),
woosh.Token(woosh.NUMBER, '25', 31, 9, 31, 11),
woosh.Token(woosh.NEWLINE, '\r\n', 31, 11, 32, 0),
woosh.Token(woosh.NAME, 'RBRACE', 32, 0, 32, 6),
woosh.Token(woosh.OP, '=', 32, 7, 32, 8),
woosh.Token(woosh.NUMBER, '26', 32, 9, 32, 11),
woosh.Token(woosh.NEWLINE, '\r\n', 32, 11, 33, 0),
woosh.Token(woosh.NAME, 'EQEQUAL', 33, 0, 33, 7),
woosh.Token(woosh.OP, '=', 33, 8, 33, 9),
woosh.Token(woosh.NUMBER, '27', 33, 10, 33, 12),
woosh.Token(woosh.NEWLINE, '\r\n', 33, 12, 34, 0),
woosh.Token(woosh.NAME, 'NOTEQUAL', 34, 0, 34, 8),
woosh.Token(woosh.OP, '=', 34, 9, 34, 10),
woosh.Token(woosh.NUMBER, '28', 34, 11, 34, 13),
woosh.Token(woosh.NEWLINE, '\r\n', 34, 13, 35, 0),
woosh.Token(woosh.NAME, 'LESSEQUAL', 35, 0, 35, 9),
woosh.Token(woosh.OP, '=', 35, 10, 35, 11),
woosh.Token(woosh.NUMBER, '29', 35, 12, 35, 14),
woosh.Token(woosh.NEWLINE, '\r\n', 35, 14, 36, 0),
woosh.Token(woosh.NAME, 'GREATEREQUAL', 36, 0, 36, 12),
woosh.Token(woosh.OP, '=', 36, 13, 36, 14),
woosh.Token(woosh.NUMBER, '30', 36, 15, 36, 17),
woosh.Token(woosh.NEWLINE, '\r\n', 36, 17, 37, 0),
woosh.Token(woosh.NAME, 'TILDE', 37, 0, 37, 5),
woosh.Token(woosh.OP, '=', 37, 6, 37, 7),
woosh.Token(woosh.NUMBER, '31', 37, 8, 37, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 37, 10, 38, 0),
woosh.Token(woosh.NAME, 'CIRCUMFLEX', 38, 0, 38, 10),
woosh.Token(woosh.OP, '=', 38, 11, 38, 12),
woosh.Token(woosh.NUMBER, '32', 38, 13, 38, 15),
woosh.Token(woosh.NEWLINE, '\r\n', 38, 15, 39, 0),
woosh.Token(woosh.NAME, 'LEFTSHIFT', 39, 0, 39, 9),
woosh.Token(woosh.OP, '=', 39, 10, 39, 11),
woosh.Token(woosh.NUMBER, '33', 39, 12, 39, 14),
woosh.Token(woosh.NEWLINE, '\r\n', 39, 14, 40, 0),
woosh.Token(woosh.NAME, 'RIGHTSHIFT', 40, 0, 40, 10),
woosh.Token(woosh.OP, '=', 40, 11, 40, 12),
woosh.Token(woosh.NUMBER, '34', 40, 13, 40, 15),
woosh.Token(woosh.NEWLINE, '\r\n', 40, 15, 41, 0),
woosh.Token(woosh.NAME, 'DOUBLESTAR', 41, 0, 41, 10),
woosh.Token(woosh.OP, '=', 41, 11, 41, 12),
woosh.Token(woosh.NUMBER, '35', 41, 13, 41, 15),
woosh.Token(woosh.NEWLINE, '\r\n', 41, 15, 42, 0),
woosh.Token(woosh.NAME, 'PLUSEQUAL', 42, 0, 42, 9),
woosh.Token(woosh.OP, '=', 42, 10, 42, 11),
woosh.Token(woosh.NUMBER, '36', 42, 12, 42, 14),
woosh.Token(woosh.NEWLINE, '\r\n', 42, 14, 43, 0),
woosh.Token(woosh.NAME, 'MINEQUAL', 43, 0, 43, 8),
woosh.Token(woosh.OP, '=', 43, 9, 43, 10),
woosh.Token(woosh.NUMBER, '37', 43, 11, 43, 13),
woosh.Token(woosh.NEWLINE, '\r\n', 43, 13, 44, 0),
woosh.Token(woosh.NAME, 'STAREQUAL', 44, 0, 44, 9),
woosh.Token(woosh.OP, '=', 44, 10, 44, 11),
woosh.Token(woosh.NUMBER, '38', 44, 12, 44, 14),
woosh.Token(woosh.NEWLINE, '\r\n', 44, 14, 45, 0),
woosh.Token(woosh.NAME, 'SLASHEQUAL', 45, 0, 45, 10),
woosh.Token(woosh.OP, '=', 45, 11, 45, 12),
woosh.Token(woosh.NUMBER, '39', 45, 13, 45, 15),
woosh.Token(woosh.NEWLINE, '\r\n', 45, 15, 46, 0),
woosh.Token(woosh.NAME, 'PERCENTEQUAL', 46, 0, 46, 12),
woosh.Token(woosh.OP, '=', 46, 13, 46, 14),
woosh.Token(woosh.NUMBER, '40', 46, 15, 46, 17),
woosh.Token(woosh.NEWLINE, '\r\n', 46, 17, 47, 0),
woosh.Token(woosh.NAME, 'AMPEREQUAL', 47, 0, 47, 10),
woosh.Token(woosh.OP, '=', 47, 11, 47, 12),
woosh.Token(woosh.NUMBER, '41', 47, 13, 47, 15),
woosh.Token(woosh.NEWLINE, '\r\n', 47, 15, 48, 0),
woosh.Token(woosh.NAME, 'VBAREQUAL', 48, 0, 48, 9),
woosh.Token(woosh.OP, '=', 48, 10, 48, 11),
woosh.Token(woosh.NUMBER, '42', 48, 12, 48, 14),
woosh.Token(woosh.NEWLINE, '\r\n', 48, 14, 49, 0),
woosh.Token(woosh.NAME, 'CIRCUMFLEXEQUAL', 49, 0, 49, 15),
woosh.Token(woosh.OP, '=', 49, 16, 49, 17),
woosh.Token(woosh.NUMBER, '43', 49, 18, 49, 20),
woosh.Token(woosh.NEWLINE, '\r\n', 49, 20, 50, 0),
woosh.Token(woosh.NAME, 'LEFTSHIFTEQUAL', 50, 0, 50, 14),
woosh.Token(woosh.OP, '=', 50, 15, 50, 16),
woosh.Token(woosh.NUMBER, '44', 50, 17, 50, 19),
woosh.Token(woosh.NEWLINE, '\r\n', 50, 19, 51, 0),
woosh.Token(woosh.NAME, 'RIGHTSHIFTEQUAL', 51, 0, 51, 15),
woosh.Token(woosh.OP, '=', 51, 16, 51, 17),
woosh.Token(woosh.NUMBER, '45', 51, 18, 51, 20),
woosh.Token(woosh.NEWLINE, '\r\n', 51, 20, 52, 0),
woosh.Token(woosh.NAME, 'DOUBLESTAREQUAL', 52, 0, 52, 15),
woosh.Token(woosh.OP, '=', 52, 16, 52, 17),
woosh.Token(woosh.NUMBER, '46', 52, 18, 52, 20),
woosh.Token(woosh.NEWLINE, '\r\n', 52, 20, 53, 0),
woosh.Token(woosh.NAME, 'DOUBLESLASH', 53, 0, 53, 11),
woosh.Token(woosh.OP, '=', 53, 12, 53, 13),
woosh.Token(woosh.NUMBER, '47', 53, 14, 53, 16),
woosh.Token(woosh.NEWLINE, '\r\n', 53, 16, 54, 0),
woosh.Token(woosh.NAME, 'DOUBLESLASHEQUAL', 54, 0, 54, 16),
woosh.Token(woosh.OP, '=', 54, 17, 54, 18),
woosh.Token(woosh.NUMBER, '48', 54, 19, 54, 21),
woosh.Token(woosh.NEWLINE, '\r\n', 54, 21, 55, 0),
woosh.Token(woosh.NAME, 'AT', 55, 0, 55, 2),
woosh.Token(woosh.OP, '=', 55, 3, 55, 4),
woosh.Token(woosh.NUMBER, '49', 55, 5, 55, 7),
woosh.Token(woosh.NEWLINE, '\r\n', 55, 7, 56, 0),
woosh.Token(woosh.NAME, 'ATEQUAL', 56, 0, 56, 7),
woosh.Token(woosh.OP, '=', 56, 8, 56, 9),
woosh.Token(woosh.NUMBER, '50', 56, 10, 56, 12),
woosh.Token(woosh.NEWLINE, '\r\n', 56, 12, 57, 0),
woosh.Token(woosh.NAME, 'RARROW', 57, 0, 57, 6),
woosh.Token(woosh.OP, '=', 57, 7, 57, 8),
woosh.Token(woosh.NUMBER, '51', 57, 9, 57, 11),
woosh.Token(woosh.NEWLINE, '\r\n', 57, 11, 58, 0),
woosh.Token(woosh.NAME, 'ELLIPSIS', 58, 0, 58, 8),
woosh.Token(woosh.OP, '=', 58, 9, 58, 10),
woosh.Token(woosh.NUMBER, '52', 58, 11, 58, 13),
woosh.Token(woosh.NEWLINE, '\r\n', 58, 13, 59, 0),
woosh.Token(woosh.NAME, 'COLONEQUAL', 59, 0, 59, 10),
woosh.Token(woosh.OP, '=', 59, 11, 59, 12),
woosh.Token(woosh.NUMBER, '53', 59, 13, 59, 15),
woosh.Token(woosh.NEWLINE, '\r\n', 59, 15, 60, 0),
woosh.Token(woosh.NAME, 'OP', 60, 0, 60, 2),
woosh.Token(woosh.OP, '=', 60, 3, 60, 4),
woosh.Token(woosh.NUMBER, '54', 60, 5, 60, 7),
woosh.Token(woosh.NEWLINE, '\r\n', 60, 7, 61, 0),
woosh.Token(woosh.NAME, 'AWAIT', 61, 0, 61, 5),
woosh.Token(woosh.OP, '=', 61, 6, 61, 7),
woosh.Token(woosh.NUMBER, '55', 61, 8, 61, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 61, 10, 62, 0),
woosh.Token(woosh.NAME, 'ASYNC', 62, 0, 62, 5),
woosh.Token(woosh.OP, '=', 62, 6, 62, 7),
woosh.Token(woosh.NUMBER, '56', 62, 8, 62, 10),
woosh.Token(woosh.NEWLINE, '\r\n', 62, 10, 63, 0),
woosh.Token(woosh.NAME, 'TYPE_IGNORE', 63, 0, 63, 11),
woosh.Token(woosh.OP, '=', 63, 12, 63, 13),
woosh.Token(woosh.NUMBER, '57', 63, 14, 63, 16),
woosh.Token(woosh.NEWLINE, '\r\n', 63, 16, 64, 0),
woosh.Token(woosh.NAME, 'TYPE_COMMENT', 64, 0, 64, 12),
woosh.Token(woosh.OP, '=', 64, 13, 64, 14),
woosh.Token(woosh.NUMBER, '58', 64, 15, 64, 17),
woosh.Token(woosh.NEWLINE, '\r\n', 64, 17, 65, 0),
woosh.Token(woosh.COMMENT, "# These aren't used by the C tokenizer but are needed for tokenize.py", 65, 0, 65, 69),
woosh.Token(woosh.NAME, 'ERRORTOKEN', 66, 0, 66, 10),
woosh.Token(woosh.OP, '=', 66, 11, 66, 12),
woosh.Token(woosh.NUMBER, '59', 66, 13, 66, 15),
woosh.Token(woosh.NEWLINE, '\r\n', 66, 15, 67, 0),
woosh.Token(woosh.NAME, 'COMMENT', 67, 0, 67, 7),
woosh.Token(woosh.OP, '=', 67, 8, 67, 9),
woosh.Token(woosh.NUMBER, '60', 67, 10, 67, 12),
woosh.Token(woosh.NEWLINE, '\r\n', 67, 12, 68, 0),
woosh.Token(woosh.NAME, 'NL', 68, 0, 68, 2),
woosh.Token(woosh.OP, '=', 68, 3, 68, 4),
woosh.Token(woosh.NUMBER, '61', 68, 5, 68, 7),
woosh.Token(woosh.NEWLINE, '\r\n', 68, 7, 69, 0),
woosh.Token(woosh.NAME, 'ENCODING', 69, 0, 69, 8),
woosh.Token(woosh.OP, '=', 69, 9, 69, 10),
woosh.Token(woosh.NUMBER, '62', 69, 11, 69, 13),
woosh.Token(woosh.NEWLINE, '\r\n', 69, 13, 70, 0),
woosh.Token(woosh.NAME, 'N_TOKENS', 70, 0, 70, 8),
woosh.Token(woosh.OP, '=', 70, 9, 70, 10),
woosh.Token(woosh.NUMBER, '63', 70, 11, 70, 13),
woosh.Token(woosh.NEWLINE, '\r\n', 70, 13, 71, 0),
woosh.Token(woosh.COMMENT, '# Special definitions for cooperation with parser', 71, 0, 71, 49),
woosh.Token(woosh.NAME, 'NT_OFFSET', 72, 0, 72, 9),
woosh.Token(woosh.OP, '=', 72, 10, 72, 11),
woosh.Token(woosh.NUMBER, '256', 72, 12, 72, 15),
woosh.Token(woosh.NEWLINE, '\r\n', 72, 15, 73, 0),
woosh.Token(woosh.NAME, 'tok_name', 74, 0, 74, 8),
woosh.Token(woosh.OP, '=', 74, 9, 74, 10),
woosh.Token(woosh.OP, '{', 74, 11, 74, 12),
woosh.Token(woosh.NAME, 'value', 74, 12, 74, 17),
woosh.Token(woosh.OP, ':', 74, 17, 74, 18),
woosh.Token(woosh.NAME, 'name', 74, 19, 74, 23),
woosh.Token(woosh.NAME, 'for', 75, 12, 75, 15),
woosh.Token(woosh.NAME, 'name', 75, 16, 75, 20),
woosh.Token(woosh.OP, ',', 75, 20, 75, 21),
woosh.Token(woosh.NAME, 'value', 75, 22, 75, 27),
woosh.Token(woosh.NAME, 'in', 75, 28, 75, 30),
woosh.Token(woosh.NAME, 'globals', 75, 31, 75, 38),
woosh.Token(woosh.OP, '(', 75, 38, 75, 39),
woosh.Token(woosh.OP, ')', 75, 39, 75, 40),
woosh.Token(woosh.OP, '.', 75, 40, 75, 41),
woosh.Token(woosh.NAME, 'items', 75, 41, 75, 46),
woosh.Token(woosh.OP, '(', 75, 46, 75, 47),
woosh.Token(woosh.OP, ')', 75, 47, 75, 48),
woosh.Token(woosh.NAME, 'if', 76, 12, 76, 14),
woosh.Token(woosh.NAME, 'isinstance', 76, 15, 76, 25),
woosh.Token(woosh.OP, '(', 76, 25, 76, 26),
woosh.Token(woosh.NAME, 'value', 76, 26, 76, 31),
woosh.Token(woosh.OP, ',', 76, 31, 76, 32),
woosh.Token(woosh.NAME, 'int', 76, 33, 76, 36),
woosh.Token(woosh.OP, ')', 76, 36, 76, 37),
woosh.Token(woosh.NAME, 'and', 76, 38, 76, 41),
woosh.Token(woosh.NAME, 'not', 76, 42, 76, 45),
woosh.Token(woosh.NAME, 'name', 76, 46, 76, 50),
woosh.Token(woosh.OP, '.', 76, 50, 76, 51),
woosh.Token(woosh.NAME, 'startswith', 76, 51, 76, 61),
woosh.Token(woosh.OP, '(', 76, 61, 76, 62),
woosh.Token(woosh.STRING, "'_'", 76, 62, 76, 65),
woosh.Token(woosh.OP, ')', 76, 65, 76, 66),
woosh.Token(woosh.OP, '}', 76, 66, 76, 67),
woosh.Token(woosh.NEWLINE, '\r\n', 76, 67, 77, 0),
woosh.Token(woosh.NAME, '__all__', 77, 0, 77, 7),
woosh.Token(woosh.OP, '.', 77, 7, 77, 8),
woosh.Token(woosh.NAME, 'extend', 77, 8, 77, 14),
woosh.Token(woosh.OP, '(', 77, 14, 77, 15),
woosh.Token(woosh.NAME, 'tok_name', 77, 15, 77, 23),
woosh.Token(woosh.OP, '.', 77, 23, 77, 24),
woosh.Token(woosh.NAME, 'values', 77, 24, 77, 30),
woosh.Token(woosh.OP, '(', 77, 30, 77, 31),
woosh.Token(woosh.OP, ')', 77, 31, 77, 32),
woosh.Token(woosh.OP, ')', 77, 32, 77, 33),
woosh.Token(woosh.NEWLINE, '\r\n', 77, 33, 78, 0),
woosh.Token(woosh.NAME, 'EXACT_TOKEN_TYPES', 79, 0, 79, 17),
woosh.Token(woosh.OP, '=', 79, 18, 79, 19),
woosh.Token(woosh.OP, '{', 79, 20, 79, 21),
woosh.Token(woosh.STRING, "'!='", 80, 4, 80, 8),
woosh.Token(woosh.OP, ':', 80, 8, 80, 9),
woosh.Token(woosh.NAME, 'NOTEQUAL', 80, 10, 80, 18),
woosh.Token(woosh.OP, ',', 80, 18, 80, 19),
woosh.Token(woosh.STRING, "'%'", 81, 4, 81, 7),
woosh.Token(woosh.OP, ':', 81, 7, 81, 8),
woosh.Token(woosh.NAME, 'PERCENT', 81, 9, 81, 16),
woosh.Token(woosh.OP, ',', 81, 16, 81, 17),
woosh.Token(woosh.STRING, "'%='", 82, 4, 82, 8),
woosh.Token(woosh.OP, ':', 82, 8, 82, 9),
woosh.Token(woosh.NAME, 'PERCENTEQUAL', 82, 10, 82, 22),
woosh.Token(woosh.OP, ',', 82, 22, 82, 23),
woosh.Token(woosh.STRING, "'&'", 83, 4, 83, 7),
woosh.Token(woosh.OP, ':', 83, 7, 83, 8),
woosh.Token(woosh.NAME, 'AMPER', 83, 9, 83, 14),
woosh.Token(woosh.OP, ',', 83, 14, 83, 15),
woosh.Token(woosh.STRING, "'&='", 84, 4, 84, 8),
woosh.Token(woosh.OP, ':', 84, 8, 84, 9),
woosh.Token(woosh.NAME, 'AMPEREQUAL', 84, 10, 84, 20),
woosh.Token(woosh.OP, ',', 84, 20, 84, 21),
woosh.Token(woosh.STRING, "'('", 85, 4, 85, 7),
woosh.Token(woosh.OP, ':', 85, 7, 85, 8),
woosh.Token(woosh.NAME, 'LPAR', 85, 9, 85, 13),
woosh.Token(woosh.OP, ',', 85, 13, 85, 14),
woosh.Token(woosh.STRING, "')'", 86, 4, 86, 7),
woosh.Token(woosh.OP, ':', 86, 7, 86, 8),
woosh.Token(woosh.NAME, 'RPAR', 86, 9, 86, 13),
woosh.Token(woosh.OP, ',', 86, 13, 86, 14),
woosh.Token(woosh.STRING, "'*'", 87, 4, 87, 7),
woosh.Token(woosh.OP, ':', 87, 7, 87, 8),
woosh.Token(woosh.NAME, 'STAR', 87, 9, 87, 13),
woosh.Token(woosh.OP, ',', 87, 13, 87, 14),
woosh.Token(woosh.STRING, "'**'", 88, 4, 88, 8),
woosh.Token(woosh.OP, ':', 88, 8, 88, 9),
woosh.Token(woosh.NAME, 'DOUBLESTAR', 88, 10, 88, 20),
woosh.Token(woosh.OP, ',', 88, 20, 88, 21),
woosh.Token(woosh.STRING, "'**='", 89, 4, 89, 9),
woosh.Token(woosh.OP, ':', 89, 9, 89, 10),
woosh.Token(woosh.NAME, 'DOUBLESTAREQUAL', 89, 11, 89, 26),
woosh.Token(woosh.OP, ',', 89, 26, 89, 27),
woosh.Token(woosh.STRING, "'*='", 90, 4, 90, 8),
woosh.Token(woosh.OP, ':', 90, 8, 90, 9),
woosh.Token(woosh.NAME, 'STAREQUAL', 90, 10, 90, 19),
woosh.Token(woosh.OP, ',', 90, 19, 90, 20),
woosh.Token(woosh.STRING, "'+'", 91, 4, 91, 7),
woosh.Token(woosh.OP, ':', 91, 7, 91, 8),
woosh.Token(woosh.NAME, 'PLUS', 91, 9, 91, 13),
woosh.Token(woosh.OP, ',', 91, 13, 91, 14),
woosh.Token(woosh.STRING, "'+='", 92, 4, 92, 8),
woosh.Token(woosh.OP, ':', 92, 8, 92, 9),
woosh.Token(woosh.NAME, 'PLUSEQUAL', 92, 10, 92, 19),
woosh.Token(woosh.OP, ',', 92, 19, 92, 20),
woosh.Token(woosh.STRING, "','", 93, 4, 93, 7),
woosh.Token(woosh.OP, ':', 93, 7, 93, 8),
woosh.Token(woosh.NAME, 'COMMA', 93, 9, 93, 14),
woosh.Token(woosh.OP, ',', 93, 14, 93, 15),
woosh.Token(woosh.STRING, "'-'", 94, 4, 94, 7),
woosh.Token(woosh.OP, ':', 94, 7, 94, 8),
woosh.Token(woosh.NAME, 'MINUS', 94, 9, 94, 14),
woosh.Token(woosh.OP, ',', 94, 14, 94, 15),
woosh.Token(woosh.STRING, "'-='", 95, 4, 95, 8),
woosh.Token(woosh.OP, ':', 95, 8, 95, 9),
woosh.Token(woosh.NAME, 'MINEQUAL', 95, 10, 95, 18),
woosh.Token(woosh.OP, ',', 95, 18, 95, 19),
woosh.Token(woosh.STRING, "'->'", 96, 4, 96, 8),
woosh.Token(woosh.OP, ':', 96, 8, 96, 9),
woosh.Token(woosh.NAME, 'RARROW', 96, 10, 96, 16),
woosh.Token(woosh.OP, ',', 96, 16, 96, 17),
woosh.Token(woosh.STRING, "'.'", 97, 4, 97, 7),
woosh.Token(woosh.OP, ':', 97, 7, 97, 8),
woosh.Token(woosh.NAME, 'DOT', 97, 9, 97, 12),
woosh.Token(woosh.OP, ',', 97, 12, 97, 13),
woosh.Token(woosh.STRING, "'...'", 98, 4, 98, 9),
woosh.Token(woosh.OP, ':', 98, 9, 98, 10),
woosh.Token(woosh.NAME, 'ELLIPSIS', 98, 11, 98, 19),
woosh.Token(woosh.OP, ',', 98, 19, 98, 20),
woosh.Token(woosh.STRING, "'/'", 99, 4, 99, 7),
woosh.Token(woosh.OP, ':', 99, 7, 99, 8),
woosh.Token(woosh.NAME, 'SLASH', 99, 9, 99, 14),
woosh.Token(woosh.OP, ',', 99, 14, 99, 15),
woosh.Token(woosh.STRING, "'//'", 100, 4, 100, 8),
woosh.Token(woosh.OP, ':', 100, 8, 100, 9),
woosh.Token(woosh.NAME, 'DOUBLESLASH', 100, 10, 100, 21),
woosh.Token(woosh.OP, ',', 100, 21, 100, 22),
woosh.Token(woosh.STRING, "'//='", 101, 4, 101, 9),
woosh.Token(woosh.OP, ':', 101, 9, 101, 10),
woosh.Token(woosh.NAME, 'DOUBLESLASHEQUAL', 101, 11, 101, 27),
woosh.Token(woosh.OP, ',', 101, 27, 101, 28),
woosh.Token(woosh.STRING, "'/='", 102, 4, 102, 8),
woosh.Token(woosh.OP, ':', 102, 8, 102, 9),
woosh.Token(woosh.NAME, 'SLASHEQUAL', 102, 10, 102, 20),
woosh.Token(woosh.OP, ',', 102, 20, 102, 21),
woosh.Token(woosh.STRING, "':'", 103, 4, 103, 7),
woosh.Token(woosh.OP, ':', 103, 7, 103, 8),
woosh.Token(woosh.NAME, 'COLON', 103, 9, 103, 14),
woosh.Token(woosh.OP, ',', 103, 14, 103, 15),
woosh.Token(woosh.STRING, "':='", 104, 4, 104, 8),
woosh.Token(woosh.OP, ':', 104, 8, 104, 9),
woosh.Token(woosh.NAME, 'COLONEQUAL', 104, 10, 104, 20),
woosh.Token(woosh.OP, ',', 104, 20, 104, 21),
woosh.Token(woosh.STRING, "';'", 105, 4, 105, 7),
woosh.Token(woosh.OP, ':', 105, 7, 105, 8),
woosh.Token(woosh.NAME, 'SEMI', 105, 9, 105, 13),
woosh.Token(woosh.OP, ',', 105, 13, 105, 14),
woosh.Token(woosh.STRING, "'<'", 106, 4, 106, 7),
woosh.Token(woosh.OP, ':', 106, 7, 106, 8),
woosh.Token(woosh.NAME, 'LESS', 106, 9, 106, 13),
woosh.Token(woosh.OP, ',', 106, 13, 106, 14),
woosh.Token(woosh.STRING, "'<<'", 107, 4, 107, 8),
woosh.Token(woosh.OP, ':', 107, 8, 107, 9),
woosh.Token(woosh.NAME, 'LEFTSHIFT', 107, 10, 107, 19),
woosh.Token(woosh.OP, ',', 107, 19, 107, 20),
woosh.Token(woosh.STRING, "'<<='", 108, 4, 108, 9),
woosh.Token(woosh.OP, ':', 108, 9, 108, 10),
woosh.Token(woosh.NAME, 'LEFTSHIFTEQUAL', 108, 11, 108, 25),
woosh.Token(woosh.OP, ',', 108, 25, 108, 26),
woosh.Token(woosh.STRING, "'<='", 109, 4, 109, 8),
woosh.Token(woosh.OP, ':', 109, 8, 109, 9),
woosh.Token(woosh.NAME, 'LESSEQUAL', 109, 10, 109, 19),
woosh.Token(woosh.OP, ',', 109, 19, 109, 20),
woosh.Token(woosh.STRING, "'='", 110, 4, 110, 7),
woosh.Token(woosh.OP, ':', 110, 7, 110, 8),
woosh.Token(woosh.NAME, 'EQUAL', 110, 9, 110, 14),
woosh.Token(woosh.OP, ',', 110, 14, 110, 15),
woosh.Token(woosh.STRING, "'=='", 111, 4, 111, 8),
woosh.Token(woosh.OP, ':', 111, 8, 111, 9),
woosh.Token(woosh.NAME, 'EQEQUAL', 111, 10, 111, 17),
woosh.Token(woosh.OP, ',', 111, 17, 111, 18),
woosh.Token(woosh.STRING, "'>'", 112, 4, 112, 7),
woosh.Token(woosh.OP, ':', 112, 7, 112, 8),
woosh.Token(woosh.NAME, 'GREATER', 112, 9, 112, 16),
woosh.Token(woosh.OP, ',', 112, 16, 112, 17),
woosh.Token(woosh.STRING, "'>='", 113, 4, 113, 8),
woosh.Token(woosh.OP, ':', 113, 8, 113, 9),
woosh.Token(woosh.NAME, 'GREATEREQUAL', 113, 10, 113, 22),
woosh.Token(woosh.OP, ',', 113, 22, 113, 23),
woosh.Token(woosh.STRING, "'>>'", 114, 4, 114, 8),
woosh.Token(woosh.OP, ':', 114, 8, 114, 9),
woosh.Token(woosh.NAME, 'RIGHTSHIFT', 114, 10, 114, 20),
woosh.Token(woosh.OP, ',', 114, 20, 114, 21),
woosh.Token(woosh.STRING, "'>>='", 115, 4, 115, 9),
woosh.Token(woosh.OP, ':', 115, 9, 115, 10),
woosh.Token(woosh.NAME, 'RIGHTSHIFTEQUAL', 115, 11, 115, 26),
woosh.Token(woosh.OP, ',', 115, 26, 115, 27),
woosh.Token(woosh.STRING, "'@'", 116, 4, 116, 7),
woosh.Token(woosh.OP, ':', 116, 7, 116, 8),
woosh.Token(woosh.NAME, 'AT', 116, 9, 116, 11),
woosh.Token(woosh.OP, ',', 116, 11, 116, 12),
woosh.Token(woosh.STRING, "'@='", 117, 4, 117, 8),
woosh.Token(woosh.OP, ':', 117, 8, 117, 9),
woosh.Token(woosh.NAME, 'ATEQUAL', 117, 10, 117, 17),
woosh.Token(woosh.OP, ',', 117, 17, 117, 18),
woosh.Token(woosh.STRING, "'['", 118, 4, 118, 7),
woosh.Token(woosh.OP, ':', 118, 7, 118, 8),
woosh.Token(woosh.NAME, 'LSQB', 118, 9, 118, 13),
woosh.Token(woosh.OP, ',', 118, 13, 118, 14),
woosh.Token(woosh.STRING, "']'", 119, 4, 119, 7),
woosh.Token(woosh.OP, ':', 119, 7, 119, 8),
woosh.Token(woosh.NAME, 'RSQB', 119, 9, 119, 13),
woosh.Token(woosh.OP, ',', 119, 13, 119, 14),
woosh.Token(woosh.STRING, "'^'", 120, 4, 120, 7),
woosh.Token(woosh.OP, ':', 120, 7, 120, 8),
woosh.Token(woosh.NAME, 'CIRCUMFLEX', 120, 9, 120, 19),
woosh.Token(woosh.OP, ',', 120, 19, 120, 20),
woosh.Token(woosh.STRING, "'^='", 121, 4, 121, 8),
woosh.Token(woosh.OP, ':', 121, 8, 121, 9),
woosh.Token(woosh.NAME, 'CIRCUMFLEXEQUAL', 121, 10, 121, 25),
woosh.Token(woosh.OP, ',', 121, 25, 121, 26),
woosh.Token(woosh.STRING, "'{'", 122, 4, 122, 7),
woosh.Token(woosh.OP, ':', 122, 7, 122, 8),
woosh.Token(woosh.NAME, 'LBRACE', 122, 9, 122, 15),
woosh.Token(woosh.OP, ',', 122, 15, 122, 16),
woosh.Token(woosh.STRING, "'|'", 123, 4, 123, 7),
woosh.Token(woosh.OP, ':', 123, 7, 123, 8),
woosh.Token(woosh.NAME, 'VBAR', 123, 9, 123, 13),
woosh.Token(woosh.OP, ',', 123, 13, 123, 14),
woosh.Token(woosh.STRING, "'|='", 124, 4, 124, 8),
woosh.Token(woosh.OP, ':', 124, 8, 124, 9),
woosh.Token(woosh.NAME, 'VBAREQUAL', 124, 10, 124, 19),
woosh.Token(woosh.OP, ',', 124, 19, 124, 20),
woosh.Token(woosh.STRING, "'}'", 125, 4, 125, 7),
woosh.Token(woosh.OP, ':', 125, 7, 125, 8),
woosh.Token(woosh.NAME, 'RBRACE', 125, 9, 125, 15),
woosh.Token(woosh.OP, ',', 125, 15, 125, 16),
woosh.Token(woosh.STRING, "'~'", 126, 4, 126, 7),
woosh.Token(woosh.OP, ':', 126, 7, 126, 8),
woosh.Token(woosh.NAME, 'TILDE', 126, 9, 126, 14),
woosh.Token(woosh.OP, ',', 126, 14, 126, 15),
woosh.Token(woosh.OP, '}', 127, 0, 127, 1),
woosh.Token(woosh.NEWLINE, '\r\n', 127, 1, 128, 0),
woosh.Token(woosh.NAME, 'def', 129, 0, 129, 3),
woosh.Token(woosh.NAME, 'ISTERMINAL', 129, 4, 129, 14),
woosh.Token(woosh.OP, '(', 129, 14, 129, 15),
woosh.Token(woosh.NAME, 'x', 129, 15, 129, 16),
woosh.Token(woosh.OP, ')', 129, 16, 129, 17),
woosh.Token(woosh.OP, ':', 129, 17, 129, 18),
woosh.Token(woosh.NEWLINE, '\r\n', 129, 18, 130, 0),
woosh.Token(woosh.INDENT, '    ', 130, 0, 130, 4),
woosh.Token(woosh.NAME, 'return', 130, 4, 130, 10),
woosh.Token(woosh.NAME, 'x', 130, 11, 130, 12),
woosh.Token(woosh.OP, '<', 130, 13, 130, 14),
woosh.Token(woosh.NAME, 'NT_OFFSET', 130, 15, 130, 24),
woosh.Token(woosh.NEWLINE, '\r\n', 130, 24, 131, 0),
woosh.Token(woosh.DEDENT, '', 132, 0, 132, 0),
woosh.Token(woosh.NAME, 'def', 132, 0, 132, 3),
woosh.Token(woosh.NAME, 'ISNONTERMINAL', 132, 4, 132, 17),
woosh.Token(woosh.OP, '(', 132, 17, 132, 18),
woosh.Token(woosh.NAME, 'x', 132, 18, 132, 19),
woosh.Token(woosh.OP, ')', 132, 19, 132, 20),
woosh.Token(woosh.OP, ':', 132, 20, 132, 21),
woosh.Token(woosh.NEWLINE, '\r\n', 132, 21, 133, 0),
woosh.Token(woosh.INDENT, '    ', 133, 0, 133, 4),
woosh.Token(woosh.NAME, 'return', 133, 4, 133, 10),
woosh.Token(woosh.NAME, 'x', 133, 11, 133, 12),
woosh.Token(woosh.OP, '>=', 133, 13, 133, 15),
woosh.Token(woosh.NAME, 'NT_OFFSET', 133, 16, 133, 25),
woosh.Token(woosh.NEWLINE, '\r\n', 133, 25, 134, 0),
woosh.Token(woosh.DEDENT, '', 135, 0, 135, 0),
woosh.Token(woosh.NAME, 'def', 135, 0, 135, 3),
woosh.Token(woosh.NAME, 'ISEOF', 135, 4, 135, 9),
woosh.Token(woosh.OP, '(', 135, 9, 135, 10),
woosh.Token(woosh.NAME, 'x', 135, 10, 135, 11),
woosh.Token(woosh.OP, ')', 135, 11, 135, 12),
woosh.Token(woosh.OP, ':', 135, 12, 135, 13),
woosh.Token(woosh.NEWLINE, '\r\n', 135, 13, 136, 0),
woosh.Token(woosh.INDENT, '    ', 136, 0, 136, 4),
woosh.Token(woosh.NAME, 'return', 136, 4, 136, 10),
woosh.Token(woosh.NAME, 'x', 136, 11, 136, 12),
woosh.Token(woosh.OP, '==', 136, 13, 136, 15),
woosh.Token(woosh.NAME, 'ENDMARKER', 136, 16, 136, 25),
woosh.Token(woosh.NEWLINE, '\r\n', 136, 25, 137, 0),
woosh.Token(woosh.DEDENT, '', 137, 0, 137, 0),
woosh.Token(woosh.EOF, '', 137, 0, 137, 0),
]

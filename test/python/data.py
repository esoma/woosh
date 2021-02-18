
# this module contains a collection of valid and invalid tokens or bits of
# source to be used for testing

import ucd

# python
import itertools
from typing import Final

NORMAL_ASCII_CHARACTERS: Final = tuple(
    chr(i) for i in itertools.chain(
        range(ord(' '), ord('~') + 1),
    )
) + ('\t',)

NEWLINES: Final = ('\n', '\r\n')
OPTIONAL_NEWLINES: Final = ('',) + NEWLINES

ONELINE_STRING_QUOTES: Final = ('\'', '"')
MULTILINE_STRING_QUOTES: Final = ('\'\'\'', '"""')
STRING_QUOTES: Final = ONELINE_STRING_QUOTES + MULTILINE_STRING_QUOTES
UNICODE_PREFIXES: Final = (
    '',
    'f', 'F',
    'fr', 'fR', 'Fr', 'FR',
    'r', 'R',
    'rf', 'rF', 'Rf', 'RF',
    'u', 'U',
)
BYTES_PREFIXES: Final = (
    'rb', 'rB', 'Rb', 'RB',
    'b', 'B',
    'br', 'bR', 'Br', 'BR',
)
STRING_PREFIXES: Final = UNICODE_PREFIXES + BYTES_PREFIXES
VALID_STRING_LITERALS_NO_PREFIX: Final = (
    # empty strings
    *(q * 2 for q in STRING_QUOTES),
    # 'hello world'
    *(f'{q}hello world{q}' for q in STRING_QUOTES),
    # '\n'
    *(f'{q}\\n{q}' for q in STRING_QUOTES),
    # '\''
    *(f'{q}\\{q}{q}' for q in ONELINE_STRING_QUOTES),
    # """hello
    # world"""
    *(
        f'{q}hello{newline}world{q}'
        for q, newline in itertools.product(MULTILINE_STRING_QUOTES, NEWLINES)
    ),
    # """ ' """
    *(f'{q} {q[0]} {q}' for q in MULTILINE_STRING_QUOTES),
    # 'line\
    # continuation'
    *(
        f'{q}line\\{newline}continuation{q}'
        for q, newline in itertools.product(STRING_QUOTES, NEWLINES)
    ),
)
VALID_STRING_LITERALS: Final = (
    *(
        f'{prefix}{literal}'
        for prefix, literal in
        itertools.product(STRING_PREFIXES, VALID_STRING_LITERALS_NO_PREFIX)
    ),
    # ucd strings may have ucd literals
    *(
        f'{prefix}{q}ðŸ{q}'
        for prefix, q in
        itertools.product(UNICODE_PREFIXES, STRING_QUOTES)
    )
)
INVALID_STRING_LITERALS: Final = (
    # abrupt end
    # '
    *(
        (f'{q}hello{q}'[:-1], f'{q}hello{q}'[:-1])
        for q in STRING_QUOTES
    ),
    # abrupt continuation end
    # '\
    *((f'{q}\\', f'{q}\\') for q in STRING_QUOTES),
    # non-continued newline in one line string
    # 'hello
    # world'
    *(
        (f'{q}hello{newline}world{q}', f'{q}hello{newline}')
        for q, newline in itertools.product(ONELINE_STRING_QUOTES, NEWLINES)
    ),
    # byte strings may not have ucd literals
    *(
        (f'{prefix}{q}{ucd}{q}', f'{prefix}{q}{ucd}')
        for prefix, ucd, q in
        itertools.product(
            BYTES_PREFIXES,
            ('ðŸ', chr(128)),
            STRING_QUOTES,
        )
    )
)
VALID_NAME_LITERALS: Final = (
    '_',
    # name start characters
    # we only check the min and max in each range since checking every character
    # isn't all that reasonable
    *(
        chr(c)
        for min_max in ucd.XID_START
        for c in min_max
    ),
    # name continue characters
    # we only check the min and max in each range since checking every character
    # isn't all that reasonable
    *(
        f'_{chr(c)}'
        for min_max in ucd.XID_CONTINUE
        for c in min_max
    ),
    # string prefixes without a following quote character are valid names
    *(p for p in STRING_PREFIXES if len(p) > 1),
)

INVALID_NAME_LITERALS: Final = (
    # starting with a non-start ascii characters that aren't "normal" (that is
    # they're not numbers, whitespace, operators, etc.)
    *(
        (chr(c), chr(c))
        for c in range(1, 128)
        if chr(c) not in NORMAL_ASCII_CHARACTERS
        if chr(c) != '\n'
    ),
    # starting with a non-start ucd character
    # we only check the min and max in each range since checking every character
    # isn't all that reasonable
    *(
        (chr(c), chr(c))
        for min, max in ucd.XID_START
        for c in (min - 1, max + 1)
        # we're already checking the ascii characters
        if c >= 128
    ),
)
NAMES_SPLIT_BY_TOKEN: Final = (
    # continueing with a ascii characters that can't continue a name
    *(
        (f'_{chr(c)}', '_')
        for c in range(0, 128)
        if not (c >= ord('a') and c <= ord('z'))
        if not (c >= ord('A') and c <= ord('Z'))
        if not (c >= ord('0') and c <= ord('9'))
        if c != ord('_')
    ),
    # continueing with a non-continue ucd character
    # we only check the min and max in each range since checking every character
    # isn't all that reasonable
    *(
        (f'_{chr(c)}', '_')
        for min, max in ucd.XID_CONTINUE
        for c in (min - 1, max + 1)
        # we're already checking the ascii characters
        if c >= 128
    ),
)

EXPONENT_SIGILS: Final = ('e', 'E')
OPTIONAL_EXPONENT_SIGILS: Final = ('',) + EXPONENT_SIGILS
EXPONENT_SIGNS: Final = ('+', '-')
OPTIONAL_EXPONENT_SIGNS: Final = ('',) + EXPONENT_SIGNS

IMAGINARY_SIGILS: Final = ('j', 'J')
OPTIONAL_IMAGINARY_SIGILS: Final = ('',) + IMAGINARY_SIGILS

BINARY_SIGILS: Final = ('b', 'B')
BINARY_VALUES: Final = tuple(str(i) for i in range(0, 2))
VALID_BINARY_VALUES: Final = (
    *BINARY_VALUES,
    *(f'{b0}{b1}' for b0, b1 in itertools.product(
        BINARY_VALUES,
        BINARY_VALUES
    )),
    *(f'{b0}_{b1}' for b0, b1 in itertools.product(
        BINARY_VALUES,
        BINARY_VALUES
    )),
    *(f'{b0}{b1}_{b0}{b1}' for b0, b1 in itertools.product(
        BINARY_VALUES,
        BINARY_VALUES
    )),
)
VALID_BINARY_LITERALS: Final = tuple(
    f'0{sigil}{value}'
    for sigil, value in itertools.product(BINARY_SIGILS, VALID_BINARY_VALUES)
)
INVALID_BINARY_LITERALS: Final = (
    # `0b`
    #   ^ incomplete
    *(
        (f'0{sigil}', f'0{sigil}')
        for sigil in BINARY_SIGILS
    ),
    # `0b0_`
    #   ^ ends with underscore
    *(
        (f'0{sigil}{binary}_', f'0{sigil}{binary}_')
        for sigil, binary in itertools.product(BINARY_SIGILS, BINARY_VALUES)
    ),
    # `00b0`
    #    ^ starts with two zeroes
    *(
        (f'00{sigil}{binary}', f'00{sigil}')
        for sigil, binary in itertools.product(BINARY_SIGILS, BINARY_VALUES)
    ),
    # `0b0__0`
    #    ^ double underscore
    *(
        (f'0{sigil}{binary}__{binary}', f'0{sigil}{binary}__')
        for sigil, binary in itertools.product(BINARY_SIGILS, BINARY_VALUES)
    ),
)
BINARIES_SPLIT_BY_TOKEN: Final = (
    # 0b0a
    #   ^ end of number
    #    ^ start of something else
    *(
        (f'0{sigil}{binary}{character}0', f'0{sigil}{binary}')
        for binary, sigil, character in itertools.product(
            BINARY_VALUES,
            BINARY_SIGILS,
            (
                chr(c) for c in range(0, 128)
                if chr(c) not in BINARY_VALUES
                if chr(c) != '_'
            )
        )
    ),
)

OCTAL_SIGILS: Final = ('o', 'O')
OCTAL_VALUES: Final = tuple(str(i) for i in range(0, 8))
VALID_OCTAL_VALUES: Final = (
    *OCTAL_VALUES,
    *(f'{o0}{o1}' for o0, o1 in itertools.product(
        OCTAL_VALUES,
        OCTAL_VALUES
    )),
    *(f'{o0}_{o1}' for o0, o1 in itertools.product(
        OCTAL_VALUES,
        OCTAL_VALUES
    )),
    *(f'{o0}{o1}_{o0}{o1}' for o0, o1 in itertools.product(
        OCTAL_VALUES,
        OCTAL_VALUES
    )),
)
VALID_OCTAL_LITERALS: Final = tuple(
    f'0{sigil}{value}'
    for sigil, value in itertools.product(OCTAL_SIGILS, VALID_OCTAL_VALUES)
)
INVALID_OCTAL_LITERALS: Final = (
    # `0o`
    #   ^ incomplete
    *(
        (f'0{sigil}', f'0{sigil}')
        for sigil in OCTAL_SIGILS
    ),
    # `0o0_`
    #   ^ ends with underscore
    *(
        (f'0{sigil}{octal}_', f'0{sigil}{octal}_')
        for sigil, octal in itertools.product(OCTAL_SIGILS, OCTAL_VALUES)
    ),
    # `00o0`
    #    ^ starts with two zeroes
    *(
        (f'00{sigil}{octal}', f'00{sigil}')
        for sigil, octal in itertools.product(OCTAL_SIGILS, OCTAL_VALUES)
    ),
    # `0o0__0`
    #    ^ double underscore
    *(
        (f'0{sigil}{octal}__{octal}', f'0{sigil}{octal}__')
        for sigil, octal in itertools.product(OCTAL_SIGILS, OCTAL_VALUES)
    ),
)
OCTAL_SPLIT_BY_TOKEN: Final = (
    # 0o0a
    #   ^ end of number
    #    ^ start of something else
    *(
        (f'0{sigil}{octal}{character}0', f'0{sigil}{octal}')
        for octal, sigil, character in itertools.product(
            OCTAL_VALUES,
            OCTAL_SIGILS,
            (
                c for c in NORMAL_ASCII_CHARACTERS + NEWLINES
                if c not in OCTAL_VALUES
                if c != '_'
            )
        )
    ),
)

HEX_SIGILS: Final = ('x', 'X')
HEX_VALUES: Final = (
    *(str(i) for i in range(0, 10)),
    *(chr(i) for i in range(ord('a'), ord('f') + 1)),
    *(chr(i) for i in range(ord('A'), ord('F') + 1))
)
VALID_HEX_EXPONENT_VALUES: Final = (
    *HEX_VALUES,
    *(f'0{v}' for v in HEX_VALUES),
    ''.join(HEX_VALUES),
    ''.join(HEX_VALUES[::-1]),
)
VALID_HEX_EXPONENTS: Final = tuple(
    f'{exponent_template}'.format(
        exponent_sign=exponent_sign,
        exponent_number=exponent_number
    )
    for exponent_template, exponent_sign, exponent_number
    in itertools.product(
        tuple(
            f'{exponent_sigil}{{exponent_sign}}{{exponent_number}}'
            for exponent_sigil in EXPONENT_SIGILS
        ),
        OPTIONAL_EXPONENT_SIGNS,
        VALID_HEX_EXPONENT_VALUES
    )
)
VALID_HEX_VALUES: Final = (
    *HEX_VALUES,
    *(f'{h0}{h1}' for h0, h1 in itertools.product(
        HEX_VALUES,
        HEX_VALUES
    )),
    *(f'{h0}_{h1}' for h0, h1 in itertools.product(
        HEX_VALUES,
        HEX_VALUES
    )),
    *(f'{h0}{h1}_{h0}{h1}' for h0, h1 in itertools.product(
        HEX_VALUES,
        HEX_VALUES
    )),
)
VALID_HEX_LITERALS: Final = tuple(
    f'0{sigil}{value}'
    for sigil, value in itertools.product(HEX_SIGILS, VALID_HEX_VALUES)
)
INVALID_HEX_LITERALS: Final = (
    # `0x`
    #   ^ incomplete
    *(
        (f'0{sigil}', f'0{sigil}')
        for sigil in HEX_SIGILS
    ),
    # `0x0_`
    #     ^ ends with underscore
    *(
        (f'0{sigil}{hex}_', f'0{sigil}{hex}_')
        for sigil, hex in itertools.product(HEX_SIGILS, HEX_VALUES)
    ),
    # `00x0`
    #    ^ starts with two zeroes
    *(
        (f'00{sigil}{hex}', f'00{sigil}')
        for sigil, hex in itertools.product(HEX_SIGILS, HEX_VALUES)
    ),
    # `0x0__0`
    #      ^ double underscore
    *(
        (f'0{sigil}{hex}__{hex}', f'0{sigil}{hex}__')
        for sigil, hex in itertools.product(HEX_SIGILS, HEX_VALUES)
    ),
)
HEX_SPLIT_BY_TOKEN: Final = (
    # 0x0a
    #   ^ end of number
    #    ^ start of something else
    *(
        (f'0{sigil}{hex}{character}0', f'0{sigil}{hex}')
        for hex, sigil, character in itertools.product(
            HEX_VALUES,
            HEX_SIGILS,
            (
                c for c in NORMAL_ASCII_CHARACTERS + NEWLINES
                if c not in HEX_VALUES
                if c != '_'
            )
        )
    ),
)

DECIMAL_VALUES: Final = tuple(str(i) for i in range(0, 10))
VALID_EXPONENT_VALUES: Final = (
    *DECIMAL_VALUES,
    *(f'0{v}' for v in DECIMAL_VALUES),
    ''.join(DECIMAL_VALUES),
    ''.join(DECIMAL_VALUES[::-1]),
)
VALID_EXPONENTS: Final = tuple(
    f'{exponent_template}{imaginary_sigil}'.format(
        exponent_sign=exponent_sign,
        exponent_number=exponent_number
    )
    for exponent_template, exponent_sign, exponent_number, imaginary_sigil
    in itertools.product(
        tuple(
            f'{exponent_sigil}{{exponent_sign}}{{exponent_number}}'
            for exponent_sigil in EXPONENT_SIGILS
        ),
        OPTIONAL_EXPONENT_SIGNS,
        VALID_EXPONENT_VALUES,
        OPTIONAL_IMAGINARY_SIGILS,
    )
)
VALID_NON_ZERO_DECIMAL_LITERALS_NO_SIGILS: Final = (
    *(d for d in DECIMAL_VALUES if d != '0'),
    *(f'{d}0' for d in DECIMAL_VALUES if d != '0'),
    *(f'{d}_0' for d in DECIMAL_VALUES if d != '0'),
    *(f'{d}00_00{d}' for d in DECIMAL_VALUES if d != '0'),
)
VALID_ZERO_LITERALS: Final = (
    '0',
    '00',
    '0_0',
    *(f'0{exponent}' for exponent in VALID_EXPONENTS)
)
VALID_NON_ZERO_DECIMAL_LITERALS: Final = (
    *VALID_NON_ZERO_DECIMAL_LITERALS_NO_SIGILS,
    *(
        f'{decimal}{exponent}'
        for decimal, exponent
        in itertools.product(
            VALID_NON_ZERO_DECIMAL_LITERALS_NO_SIGILS,
            VALID_EXPONENTS,
        )
    )
)
INVALID_DECIMAL_LITERALS: Final = (
    # `0_`
    #   ^ ends with underscore
    *(
        (f'{decimal}_', f'{decimal}_')
        for decimal in DECIMAL_VALUES
    ),
    # `01`
    #   ^ starts with zero
    *(
        (f'0{decimal}', f'0{decimal}')
        for decimal in DECIMAL_VALUES
        if decimal != '0'
    ),
    # `0__0`
    #    ^ double underscore
    *(
        (f'{decimal}__{decimal}', f'{decimal}__')
        for decimal in DECIMAL_VALUES
    ),
    # `0_e0`
    #   ^ exponent after underscore
    *(
        (f'{decimal}_{exponent_sigil}{decimal}', f'{decimal}_')
        for decimal, exponent_sigil
        in itertools.product(DECIMAL_VALUES, EXPONENT_SIGILS)
    ),
    # `0e0_`
    #     ^ exponent ends with underscore
    *(
        (
            f'{decimal}{exponent_sigil}{decimal}_',
            f'{decimal}{exponent_sigil}{decimal}_',
        )
        for decimal, exponent_sigil
        in itertools.product(DECIMAL_VALUES, EXPONENT_SIGILS)
    ),
    # `0e0__0`
    #      ^ exponent has double underscore
    *(
        (
            f'{decimal}{exponent_sigil}{decimal}__{decimal}',
            f'{decimal}{exponent_sigil}{decimal}__',
        )
        for decimal, exponent_sigil
        in itertools.product(DECIMAL_VALUES, EXPONENT_SIGILS)
    ),
    # `0ea`
    #    ^ exponent is not a number
    *(
        (
            f'{decimal}{exponent_sigil}{exponent_sign}a',
            f'{decimal}{exponent_sigil}{exponent_sign}a',
        )
        for decimal, exponent_sigil, exponent_sign
        in itertools.product(
            DECIMAL_VALUES,
            EXPONENT_SIGILS,
            OPTIONAL_EXPONENT_SIGNS
        )
    ),
    # `0e++0`
    #     ^ exponent has multiple signs
    *(
        (
            f'{decimal}{exponent_sigil}{exponent_sign}{exponent_sign}{decimal}',
            f'{decimal}{exponent_sigil}{exponent_sign}{exponent_sign}'
        )
        for decimal, exponent_sigil, exponent_sign
        in itertools.product(
            DECIMAL_VALUES,
            EXPONENT_SIGILS,
            EXPONENT_SIGNS
        )
    ),
    # `0_i`
    #   ^ imaginary after underscore
    *(
        (f'{decimal}_{imaginary_sigil}', f'{decimal}_')
        for decimal, imaginary_sigil
        in itertools.product(DECIMAL_VALUES, IMAGINARY_SIGILS)
    ),
)
DECIMALS_SPLIT_BY_TOKEN: Final = (
    # 0a0
    # ^ end of number
    #  ^ start of something else
    *(
        (f'{decimal}{character}0', decimal)
        for decimal, character in itertools.product(
            DECIMAL_VALUES,
            (
                c for c in NORMAL_ASCII_CHARACTERS
                if ord(c) < ord('0') or ord(c) > ord('9')
                if c not in ('.', '_')
            )
        )
        if character not in EXPONENT_SIGILS
        if character not in IMAGINARY_SIGILS
        # 0b0 will not split but 1b0 will
        if decimal != '0' or (
            character not in BINARY_SIGILS and
            character not in OCTAL_SIGILS and
            character not in HEX_SIGILS
        )
    ),
    # 0\n
    # ^ end of number
    #  ^ newline
    *(
        (f'{decimal}{newline}', decimal)
        for decimal, newline in itertools.product(
            DECIMAL_VALUES,
            NEWLINES,
        )
    ),
    # 0e0a0
    #   ^ end of number
    #    ^ start of something else
    *(
        (
            f'{decimal}{sigil}{sign}{decimal}{character}0',
            f'{decimal}{sigil}{sign}{decimal}',
        )
        for decimal, sigil, sign, character in itertools.product(
            DECIMAL_VALUES,
            EXPONENT_SIGILS,
            EXPONENT_SIGNS,
            (
                c for c in NORMAL_ASCII_CHARACTERS
                if ord(c) < ord('0') or ord(c) > ord('9')
                # 0e0_0 is not broken
                if c != '_'
                # 0e0j0 is broken, but after the imaginary, not testing with
                # this part of the fixture
                if c not in IMAGINARY_SIGILS
            )
        )
    ),
    # 0ja
    #  ^ end of number
    #   ^ start of something else
    *(
        (
            f'{decimal}{imaginary_sigil}{character}',
            f'{decimal}{imaginary_sigil}',
        )
        for decimal, imaginary_sigil, character in itertools.product(
            DECIMAL_VALUES,
            IMAGINARY_SIGILS,
            NORMAL_ASCII_CHARACTERS + NEWLINES,
        )
    ),
)

VALID_FLOAT_LITERAL_BASES: Final = (
    '.',
    '0.',
    *(f'{d}.' for d in VALID_NON_ZERO_DECIMAL_LITERALS_NO_SIGILS)
)
VALID_FLOAT_LITERAL_FRACTIONS: Final = (
    '',
    *VALID_NON_ZERO_DECIMAL_LITERALS_NO_SIGILS,
)
VALID_FLOAT_LITERALS_NO_SIGILS: Final = tuple(
    f'{base}{fraction}'
    for base, fraction
    in itertools.product(
        VALID_FLOAT_LITERAL_BASES,
        VALID_FLOAT_LITERAL_FRACTIONS,
    )
    # a plain `.` is not a float
    if base != '.' and fraction
)
VALID_FLOAT_LITERALS: Final = (
    *VALID_FLOAT_LITERALS_NO_SIGILS,
    *(
        f'{base}{exponent}'
        for base, exponent
        in itertools.product(
            VALID_FLOAT_LITERALS_NO_SIGILS,
            VALID_EXPONENTS,
        )
    )
)
INVALID_FLOAT_LITERALS: Final = (
    # `0.0_`
    #   ^ ends with underscore
    *(
        (f'{decimal}.{decimal}_', f'{decimal}.{decimal}_')
        for decimal in DECIMAL_VALUES
    ),
    # `0.0__0`
    #    ^ double underscore
    *(
        (f'{decimal}.{decimal}__{decimal}', f'{decimal}.{decimal}__')
        for decimal in DECIMAL_VALUES
    ),
    # `0.0_e0`
    #   ^ exponent after underscore
    *(
        (
            f'{decimal}.{decimal}_{exponent_sigil}{decimal}',
            f'{decimal}.{decimal}_',
        )
        for decimal, exponent_sigil
        in itertools.product(DECIMAL_VALUES, EXPONENT_SIGILS)
    ),
    # `0.0e0_`
    #     ^ exponent ends with underscore
    *(
        (
            f'{decimal}.{decimal}{exponent_sigil}{decimal}_',
            f'{decimal}.{decimal}{exponent_sigil}{decimal}_',
        )
        for decimal, exponent_sigil
        in itertools.product(DECIMAL_VALUES, EXPONENT_SIGILS)
    ),
    # `0.0e0__0`
    #      ^ exponent has double underscore
    *(
        (
            f'{decimal}.{decimal}{exponent_sigil}{decimal}__{decimal}',
            f'{decimal}.{decimal}{exponent_sigil}{decimal}__',
        )
        for decimal, exponent_sigil
        in itertools.product(DECIMAL_VALUES, EXPONENT_SIGILS)
    ),
    # `0.0ea`
    #    ^ exponent is not a number
    *(
        (
            f'{decimal}.{decimal}{exponent_sigil}{exponent_sign}a',
            f'{decimal}.{decimal}{exponent_sigil}{exponent_sign}a',
        )
        for decimal, exponent_sigil, exponent_sign
        in itertools.product(
            DECIMAL_VALUES,
            EXPONENT_SIGILS,
            OPTIONAL_EXPONENT_SIGNS
        )
    ),
    # `0.0e++0`
    #     ^ exponent has multiple signs
    *(
        (
            f'{decimal}.{decimal}{exponent_sigil}{exponent_sign}{exponent_sign}{decimal}',
            f'{decimal}.{decimal}{exponent_sigil}{exponent_sign}{exponent_sign}'
        )
        for decimal, exponent_sigil, exponent_sign
        in itertools.product(
            DECIMAL_VALUES,
            EXPONENT_SIGILS,
            EXPONENT_SIGNS
        )
    ),
    # `0.0_i`
    #   ^ imaginary after underscore
    *(
        (f'{decimal}.{decimal}_{imaginary_sigil}', f'{decimal}.{decimal}_')
        for decimal, imaginary_sigil
        in itertools.product(DECIMAL_VALUES, IMAGINARY_SIGILS)
    ),
)
FLOATS_SPLIT_BY_TOKEN: Final = (
    # 0.0a0
    # ^ end of number
    #  ^ start of something else
    *(
        (f'{decimal}.{decimal}{character}0', f'{decimal}.{decimal}')
        for decimal, character in itertools.product(
            DECIMAL_VALUES,
            (
                c for c in NORMAL_ASCII_CHARACTERS
                if ord(c) < ord('0') or ord(c) > ord('9')
                if c != '_'
            )
        )
        if character not in EXPONENT_SIGILS
        if character not in IMAGINARY_SIGILS
    ),
    # 0.0\n
    #   ^ end of number
    #    ^ newline
    *(
        (f'{decimal}.{decimal}{newline}', f'{decimal}.{decimal}')
        for decimal, newline in itertools.product(
            DECIMAL_VALUES,
            NEWLINES,
        )
    ),
    # 0.0e0a0
    #     ^ end of number
    #      ^ start of something else
    *(
        (
            f'{decimal}.{decimal}{sigil}{sign}{decimal}{character}0',
            f'{decimal}.{decimal}{sigil}{sign}{decimal}',
        )
        for decimal, sigil, sign, character in itertools.product(
            DECIMAL_VALUES,
            EXPONENT_SIGILS,
            EXPONENT_SIGNS,
            (
                c for c in NORMAL_ASCII_CHARACTERS
                if ord(c) < ord('0') or ord(c) > ord('9')
                # 0.0e0_0 is not broken
                if c != '_'
                # 0.0e0j0 is broken, but after the imaginary, not testing with
                # this part of the fixture
                if c not in IMAGINARY_SIGILS
            )
        )
    ),
    # 0.0ja
    #    ^ end of number
    #     ^ start of something else
    *(
        (
            f'{decimal}.{decimal}{imaginary_sigil}{character}',
            f'{decimal}.{decimal}{imaginary_sigil}',
        )
        for decimal, imaginary_sigil, character in itertools.product(
            DECIMAL_VALUES,
            IMAGINARY_SIGILS,
            NORMAL_ASCII_CHARACTERS + NEWLINES,
        )
    ),
)

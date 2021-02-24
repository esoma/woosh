
# python
import os
import pathlib
import textwrap
# woosh
import woosh

DIR = pathlib.Path(__file__).parent.absolute()
SAMPLE_DIR = DIR / '../../sample/'
SAMPLE_FILES = os.listdir(SAMPLE_DIR)

try:
    os.mkdir(DIR / 'sample')
except FileExistsError:
    pass

for sample_file in SAMPLE_FILES:
    with open(SAMPLE_DIR / sample_file, 'rb') as f:
        tokens = list(woosh.tokenize(f))
    expected = '\n'.join(
        f'            woosh.Token(woosh.{token.type}, {token.value!r}, {token.start_line}, {token.start_column}, {token.end_line}, {token.end_column}),'
        for token in tokens
    )
    template = textwrap.dedent(f"""
        # python
        import pathlib
        # woosh
        import woosh

        SAMPLE_DIR = pathlib.Path(__file__).parent.absolute() / '../../../sample/'
        def test():
            with open(SAMPLE_DIR / '{sample_file}', 'rb') as f:
                tokens = list(woosh.tokenize(f))
            for token, expected in zip(tokens, EXPECTED):
                assert token == expected
                    
        EXPECTED = [\n{expected}
        ]
    """)
    with open(DIR / f'sample/test_{sample_file}', 'wb') as f:
        f.write(template.encode(tokens[0].value))
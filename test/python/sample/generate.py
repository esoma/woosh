
# python
import os
import pathlib
import textwrap
# woosh
import woosh

DIR = pathlib.Path(__file__).parent.absolute()
ROOT = (DIR / '../../../').resolve()
SAMPLE_DIR = ROOT / 'sample'


for directory, _, files in os.walk(SAMPLE_DIR):
    directory = pathlib.Path(directory)
    for sample_file_name in files:
        sample_file = (directory / sample_file_name).resolve()
        rel = len(str(pathlib.PurePosixPath(directory.relative_to(ROOT))).split('/'))
        sample_file_relative_sample = pathlib.PurePosixPath(
            sample_file.relative_to(SAMPLE_DIR)
        )
        if sample_file.suffix != '.py':
            continue
        with open(sample_file, 'rb') as f:
            tokens = list(woosh.tokenize(f))
        expected = '\n'.join(
            f'            woosh.Token(woosh.{token.type}, {token.value!r}, {token.start_line}, {token.start_column}, {token.end_line}, {token.end_column}),'
            for token in tokens
        )
        template = textwrap.dedent(f"""
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

            SAMPLE_DIR = pathlib.Path(__file__).parent.absolute() / '../../' / {'../' * rel!r} / 'sample'
            
            @pytest.mark.parametrize('tokenize', [tokenize_file_like, tokenize_bytes])
            def test(tokenize):
                with open(SAMPLE_DIR / {str(sample_file_relative_sample)!r}, 'rb') as f:
                    tokens = tokenize(f.read())
                for token, expected in zip(tokens, EXPECTED):
                    assert token == expected
                        
            EXPECTED = [\n{expected}
            ]
        """)
        test_file_dir = DIR / sample_file_relative_sample.parent
        test_file_dir.mkdir(parents=True, exist_ok=True)
        with open(test_file_dir / '__init__.py', 'w') as f:
            pass
        test_file = test_file_dir / f'test_{sample_file_relative_sample.name}'
        with open(test_file, 'wb') as f:
            f.write(template.encode(tokens[0].value))

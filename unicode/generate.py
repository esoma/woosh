
# this script generates some files using the unicode character database

# python
import pathlib
import re
import textwrap

WOOSH_DIR = pathlib.Path(__file__).parent.parent.absolute()

id_pattern = re.compile(
    r'^([0-9a-fA-F]+)(\.\.([0-9a-fA-F]+))?\s*;\s*(XID_(Start|Continue))'
)

property_codepoints = {
    "XID_Start": [],
    "XID_Continue": [],
}

with open(WOOSH_DIR / 'unicode/DerivedCoreProperties.txt') as file:
    for line in file:
        if match := id_pattern.match(line):
            min_cp = match.group(1)
            max_cp = match.group(3)
            property = match.group(4)
            if max_cp is None:
                max_cp = min_cp
            min_cp = int(min_cp, 16)
            max_cp = int(max_cp, 16)
            # normalize ranges so that there is always a gap between them
            try:
                last_min_max = property_codepoints[property][-1]
            except IndexError:
                last_min_max = None
            if last_min_max:
                if last_min_max[1] == min_cp - 1:
                    property_codepoints[property][-1] = (last_min_max[0], max_cp)
                    continue
            property_codepoints[property].append((min_cp, max_cp))
            
with open(WOOSH_DIR / 'test/python/ucd.py', 'w') as f:
    f.write(textwrap.dedent('''
        # this file is generated from woosh/unicode/generate.py using
        # properties from the unicode character database
        
    '''))
    for property, codepoints in property_codepoints.items():
        f.write(f'{property.upper()} = (\n')
        for min, max in codepoints:
            f.write(f'    ({min}, {max}),\n')
        f.write(')\n')

with open(WOOSH_DIR / 'src/unicode.h', 'wb') as f:
    f.write(textwrap.dedent('''
        // this file is generated from woosh/unicode/generate.py using
        // properties from the unicode character database
        
        #define PY_SSIZE_T_CLEAN
        #include <Python.h>
    ''').encode('utf-8'))
    for property, codepoints in property_codepoints.items():
        cmps = []
        for min, max in codepoints:
            if min < 128 or max < 128:
                assert min < 128 and max < 128
                continue
            cmps.append(
                f'                // {chr(min)} - {chr(max)}\n'
                f'                ({min} <= c && c <= {max})'
            )
        cmp = '\n' + ' ||\n'.join(cmps)
        f.write(textwrap.dedent(f'''
            int
            is_unicode_{property.lower()}(Py_UCS4 c)
            {{
                // only check unicode characters this way
                assert(c >= 128);
                return ({cmp}
                );
            }}
        ''').encode('utf-8'))

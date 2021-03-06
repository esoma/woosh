
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
    with open(SAMPLE_DIR / 'stdlib/abc.py', 'rb') as f:
        tokens = tokenize(f.read())
    for token, expected in zip(tokens, EXPECTED):
        assert token == expected

EXPECTED = [
woosh.Token(woosh.ENCODING, 'utf-8', 1, 0, 1, 0),
woosh.Token(woosh.COMMENT, '# Copyright 2007 Google, Inc. All Rights Reserved.', 1, 0, 1, 50),
woosh.Token(woosh.COMMENT, '# Licensed to PSF under a Contributor Agreement.', 2, 0, 2, 48),
woosh.Token(woosh.STRING, '"""Abstract Base Classes (ABCs) according to PEP 3119."""', 4, 0, 4, 57),
woosh.Token(woosh.NEWLINE, '\r\n', 4, 57, 5, 0),
woosh.Token(woosh.NAME, 'def', 7, 0, 7, 3),
woosh.Token(woosh.NAME, 'abstractmethod', 7, 4, 7, 18),
woosh.Token(woosh.OP, '(', 7, 18, 7, 19),
woosh.Token(woosh.NAME, 'funcobj', 7, 19, 7, 26),
woosh.Token(woosh.OP, ')', 7, 26, 7, 27),
woosh.Token(woosh.OP, ':', 7, 27, 7, 28),
woosh.Token(woosh.NEWLINE, '\r\n', 7, 28, 8, 0),
woosh.Token(woosh.INDENT, '    ', 8, 0, 8, 4),
woosh.Token(woosh.STRING, '"""A decorator indicating abstract methods.\r\n\r\n    Requires that the metaclass is ABCMeta or derived from it.  A\r\n    class that has a metaclass derived from ABCMeta cannot be\r\n    instantiated unless all of its abstract methods are overridden.\r\n    The abstract methods can be called using any of the normal\r\n    \'super\' call mechanisms.  abstractmethod() may be used to declare\r\n    abstract methods for properties and descriptors.\r\n\r\n    Usage:\r\n\r\n        class C(metaclass=ABCMeta):\r\n            @abstractmethod\r\n            def my_abstract_method(self, ...):\r\n                ...\r\n    """', 8, 4, 23, 7),
woosh.Token(woosh.NEWLINE, '\r\n', 23, 7, 24, 0),
woosh.Token(woosh.NAME, 'funcobj', 24, 4, 24, 11),
woosh.Token(woosh.OP, '.', 24, 11, 24, 12),
woosh.Token(woosh.NAME, '__isabstractmethod__', 24, 12, 24, 32),
woosh.Token(woosh.OP, '=', 24, 33, 24, 34),
woosh.Token(woosh.NAME, 'True', 24, 35, 24, 39),
woosh.Token(woosh.NEWLINE, '\r\n', 24, 39, 25, 0),
woosh.Token(woosh.NAME, 'return', 25, 4, 25, 10),
woosh.Token(woosh.NAME, 'funcobj', 25, 11, 25, 18),
woosh.Token(woosh.NEWLINE, '\r\n', 25, 18, 26, 0),
woosh.Token(woosh.DEDENT, '', 28, 0, 28, 0),
woosh.Token(woosh.NAME, 'class', 28, 0, 28, 5),
woosh.Token(woosh.NAME, 'abstractclassmethod', 28, 6, 28, 25),
woosh.Token(woosh.OP, '(', 28, 25, 28, 26),
woosh.Token(woosh.NAME, 'classmethod', 28, 26, 28, 37),
woosh.Token(woosh.OP, ')', 28, 37, 28, 38),
woosh.Token(woosh.OP, ':', 28, 38, 28, 39),
woosh.Token(woosh.NEWLINE, '\r\n', 28, 39, 29, 0),
woosh.Token(woosh.INDENT, '    ', 29, 0, 29, 4),
woosh.Token(woosh.STRING, '"""A decorator indicating abstract classmethods.\r\n\r\n    Deprecated, use \'classmethod\' with \'abstractmethod\' instead.\r\n    """', 29, 4, 32, 7),
woosh.Token(woosh.NEWLINE, '\r\n', 32, 7, 33, 0),
woosh.Token(woosh.NAME, '__isabstractmethod__', 34, 4, 34, 24),
woosh.Token(woosh.OP, '=', 34, 25, 34, 26),
woosh.Token(woosh.NAME, 'True', 34, 27, 34, 31),
woosh.Token(woosh.NEWLINE, '\r\n', 34, 31, 35, 0),
woosh.Token(woosh.NAME, 'def', 36, 4, 36, 7),
woosh.Token(woosh.NAME, '__init__', 36, 8, 36, 16),
woosh.Token(woosh.OP, '(', 36, 16, 36, 17),
woosh.Token(woosh.NAME, 'self', 36, 17, 36, 21),
woosh.Token(woosh.OP, ',', 36, 21, 36, 22),
woosh.Token(woosh.NAME, 'callable', 36, 23, 36, 31),
woosh.Token(woosh.OP, ')', 36, 31, 36, 32),
woosh.Token(woosh.OP, ':', 36, 32, 36, 33),
woosh.Token(woosh.NEWLINE, '\r\n', 36, 33, 37, 0),
woosh.Token(woosh.INDENT, '        ', 37, 0, 37, 8),
woosh.Token(woosh.NAME, 'callable', 37, 8, 37, 16),
woosh.Token(woosh.OP, '.', 37, 16, 37, 17),
woosh.Token(woosh.NAME, '__isabstractmethod__', 37, 17, 37, 37),
woosh.Token(woosh.OP, '=', 37, 38, 37, 39),
woosh.Token(woosh.NAME, 'True', 37, 40, 37, 44),
woosh.Token(woosh.NEWLINE, '\r\n', 37, 44, 38, 0),
woosh.Token(woosh.NAME, 'super', 38, 8, 38, 13),
woosh.Token(woosh.OP, '(', 38, 13, 38, 14),
woosh.Token(woosh.OP, ')', 38, 14, 38, 15),
woosh.Token(woosh.OP, '.', 38, 15, 38, 16),
woosh.Token(woosh.NAME, '__init__', 38, 16, 38, 24),
woosh.Token(woosh.OP, '(', 38, 24, 38, 25),
woosh.Token(woosh.NAME, 'callable', 38, 25, 38, 33),
woosh.Token(woosh.OP, ')', 38, 33, 38, 34),
woosh.Token(woosh.NEWLINE, '\r\n', 38, 34, 39, 0),
woosh.Token(woosh.DEDENT, '', 41, 0, 41, 0),
woosh.Token(woosh.DEDENT, '', 41, 0, 41, 0),
woosh.Token(woosh.NAME, 'class', 41, 0, 41, 5),
woosh.Token(woosh.NAME, 'abstractstaticmethod', 41, 6, 41, 26),
woosh.Token(woosh.OP, '(', 41, 26, 41, 27),
woosh.Token(woosh.NAME, 'staticmethod', 41, 27, 41, 39),
woosh.Token(woosh.OP, ')', 41, 39, 41, 40),
woosh.Token(woosh.OP, ':', 41, 40, 41, 41),
woosh.Token(woosh.NEWLINE, '\r\n', 41, 41, 42, 0),
woosh.Token(woosh.INDENT, '    ', 42, 0, 42, 4),
woosh.Token(woosh.STRING, '"""A decorator indicating abstract staticmethods.\r\n\r\n    Deprecated, use \'staticmethod\' with \'abstractmethod\' instead.\r\n    """', 42, 4, 45, 7),
woosh.Token(woosh.NEWLINE, '\r\n', 45, 7, 46, 0),
woosh.Token(woosh.NAME, '__isabstractmethod__', 47, 4, 47, 24),
woosh.Token(woosh.OP, '=', 47, 25, 47, 26),
woosh.Token(woosh.NAME, 'True', 47, 27, 47, 31),
woosh.Token(woosh.NEWLINE, '\r\n', 47, 31, 48, 0),
woosh.Token(woosh.NAME, 'def', 49, 4, 49, 7),
woosh.Token(woosh.NAME, '__init__', 49, 8, 49, 16),
woosh.Token(woosh.OP, '(', 49, 16, 49, 17),
woosh.Token(woosh.NAME, 'self', 49, 17, 49, 21),
woosh.Token(woosh.OP, ',', 49, 21, 49, 22),
woosh.Token(woosh.NAME, 'callable', 49, 23, 49, 31),
woosh.Token(woosh.OP, ')', 49, 31, 49, 32),
woosh.Token(woosh.OP, ':', 49, 32, 49, 33),
woosh.Token(woosh.NEWLINE, '\r\n', 49, 33, 50, 0),
woosh.Token(woosh.INDENT, '        ', 50, 0, 50, 8),
woosh.Token(woosh.NAME, 'callable', 50, 8, 50, 16),
woosh.Token(woosh.OP, '.', 50, 16, 50, 17),
woosh.Token(woosh.NAME, '__isabstractmethod__', 50, 17, 50, 37),
woosh.Token(woosh.OP, '=', 50, 38, 50, 39),
woosh.Token(woosh.NAME, 'True', 50, 40, 50, 44),
woosh.Token(woosh.NEWLINE, '\r\n', 50, 44, 51, 0),
woosh.Token(woosh.NAME, 'super', 51, 8, 51, 13),
woosh.Token(woosh.OP, '(', 51, 13, 51, 14),
woosh.Token(woosh.OP, ')', 51, 14, 51, 15),
woosh.Token(woosh.OP, '.', 51, 15, 51, 16),
woosh.Token(woosh.NAME, '__init__', 51, 16, 51, 24),
woosh.Token(woosh.OP, '(', 51, 24, 51, 25),
woosh.Token(woosh.NAME, 'callable', 51, 25, 51, 33),
woosh.Token(woosh.OP, ')', 51, 33, 51, 34),
woosh.Token(woosh.NEWLINE, '\r\n', 51, 34, 52, 0),
woosh.Token(woosh.DEDENT, '', 54, 0, 54, 0),
woosh.Token(woosh.DEDENT, '', 54, 0, 54, 0),
woosh.Token(woosh.NAME, 'class', 54, 0, 54, 5),
woosh.Token(woosh.NAME, 'abstractproperty', 54, 6, 54, 22),
woosh.Token(woosh.OP, '(', 54, 22, 54, 23),
woosh.Token(woosh.NAME, 'property', 54, 23, 54, 31),
woosh.Token(woosh.OP, ')', 54, 31, 54, 32),
woosh.Token(woosh.OP, ':', 54, 32, 54, 33),
woosh.Token(woosh.NEWLINE, '\r\n', 54, 33, 55, 0),
woosh.Token(woosh.INDENT, '    ', 55, 0, 55, 4),
woosh.Token(woosh.STRING, '"""A decorator indicating abstract properties.\r\n\r\n    Deprecated, use \'property\' with \'abstractmethod\' instead.\r\n    """', 55, 4, 58, 7),
woosh.Token(woosh.NEWLINE, '\r\n', 58, 7, 59, 0),
woosh.Token(woosh.NAME, '__isabstractmethod__', 60, 4, 60, 24),
woosh.Token(woosh.OP, '=', 60, 25, 60, 26),
woosh.Token(woosh.NAME, 'True', 60, 27, 60, 31),
woosh.Token(woosh.NEWLINE, '\r\n', 60, 31, 61, 0),
woosh.Token(woosh.DEDENT, '', 63, 0, 63, 0),
woosh.Token(woosh.NAME, 'try', 63, 0, 63, 3),
woosh.Token(woosh.OP, ':', 63, 3, 63, 4),
woosh.Token(woosh.NEWLINE, '\r\n', 63, 4, 64, 0),
woosh.Token(woosh.INDENT, '    ', 64, 0, 64, 4),
woosh.Token(woosh.NAME, 'from', 64, 4, 64, 8),
woosh.Token(woosh.NAME, '_abc', 64, 9, 64, 13),
woosh.Token(woosh.NAME, 'import', 64, 14, 64, 20),
woosh.Token(woosh.OP, '(', 64, 21, 64, 22),
woosh.Token(woosh.NAME, 'get_cache_token', 64, 22, 64, 37),
woosh.Token(woosh.OP, ',', 64, 37, 64, 38),
woosh.Token(woosh.NAME, '_abc_init', 64, 39, 64, 48),
woosh.Token(woosh.OP, ',', 64, 48, 64, 49),
woosh.Token(woosh.NAME, '_abc_register', 64, 50, 64, 63),
woosh.Token(woosh.OP, ',', 64, 63, 64, 64),
woosh.Token(woosh.NAME, '_abc_instancecheck', 65, 22, 65, 40),
woosh.Token(woosh.OP, ',', 65, 40, 65, 41),
woosh.Token(woosh.NAME, '_abc_subclasscheck', 65, 42, 65, 60),
woosh.Token(woosh.OP, ',', 65, 60, 65, 61),
woosh.Token(woosh.NAME, '_get_dump', 65, 62, 65, 71),
woosh.Token(woosh.OP, ',', 65, 71, 65, 72),
woosh.Token(woosh.NAME, '_reset_registry', 66, 22, 66, 37),
woosh.Token(woosh.OP, ',', 66, 37, 66, 38),
woosh.Token(woosh.NAME, '_reset_caches', 66, 39, 66, 52),
woosh.Token(woosh.OP, ')', 66, 52, 66, 53),
woosh.Token(woosh.NEWLINE, '\r\n', 66, 53, 67, 0),
woosh.Token(woosh.DEDENT, '', 67, 0, 67, 0),
woosh.Token(woosh.NAME, 'except', 67, 0, 67, 6),
woosh.Token(woosh.NAME, 'ImportError', 67, 7, 67, 18),
woosh.Token(woosh.OP, ':', 67, 18, 67, 19),
woosh.Token(woosh.NEWLINE, '\r\n', 67, 19, 68, 0),
woosh.Token(woosh.INDENT, '    ', 68, 0, 68, 4),
woosh.Token(woosh.NAME, 'from', 68, 4, 68, 8),
woosh.Token(woosh.NAME, '_py_abc', 68, 9, 68, 16),
woosh.Token(woosh.NAME, 'import', 68, 17, 68, 23),
woosh.Token(woosh.NAME, 'ABCMeta', 68, 24, 68, 31),
woosh.Token(woosh.OP, ',', 68, 31, 68, 32),
woosh.Token(woosh.NAME, 'get_cache_token', 68, 33, 68, 48),
woosh.Token(woosh.NEWLINE, '\r\n', 68, 48, 69, 0),
woosh.Token(woosh.NAME, 'ABCMeta', 69, 4, 69, 11),
woosh.Token(woosh.OP, '.', 69, 11, 69, 12),
woosh.Token(woosh.NAME, '__module__', 69, 12, 69, 22),
woosh.Token(woosh.OP, '=', 69, 23, 69, 24),
woosh.Token(woosh.STRING, "'abc'", 69, 25, 69, 30),
woosh.Token(woosh.NEWLINE, '\r\n', 69, 30, 70, 0),
woosh.Token(woosh.DEDENT, '', 70, 0, 70, 0),
woosh.Token(woosh.NAME, 'else', 70, 0, 70, 4),
woosh.Token(woosh.OP, ':', 70, 4, 70, 5),
woosh.Token(woosh.NEWLINE, '\r\n', 70, 5, 71, 0),
woosh.Token(woosh.INDENT, '    ', 71, 0, 71, 4),
woosh.Token(woosh.NAME, 'class', 71, 4, 71, 9),
woosh.Token(woosh.NAME, 'ABCMeta', 71, 10, 71, 17),
woosh.Token(woosh.OP, '(', 71, 17, 71, 18),
woosh.Token(woosh.NAME, 'type', 71, 18, 71, 22),
woosh.Token(woosh.OP, ')', 71, 22, 71, 23),
woosh.Token(woosh.OP, ':', 71, 23, 71, 24),
woosh.Token(woosh.NEWLINE, '\r\n', 71, 24, 72, 0),
woosh.Token(woosh.INDENT, '        ', 72, 0, 72, 8),
woosh.Token(woosh.STRING, '"""Metaclass for defining Abstract Base Classes (ABCs).\r\n\r\n        Use this metaclass to create an ABC.  An ABC can be subclassed\r\n        directly, and then acts as a mix-in class.  You can also register\r\n        unrelated concrete classes (even built-in classes) and unrelated\r\n        ABCs as \'virtual subclasses\' -- these and their descendants will\r\n        be considered subclasses of the registering ABC by the built-in\r\n        issubclass() function, but the registering ABC won\'t show up in\r\n        their MRO (Method Resolution Order) nor will method\r\n        implementations defined by the registering ABC be callable (not\r\n        even via super()).\r\n        """', 72, 8, 83, 11),
woosh.Token(woosh.NEWLINE, '\r\n', 83, 11, 84, 0),
woosh.Token(woosh.NAME, 'def', 84, 8, 84, 11),
woosh.Token(woosh.NAME, '__new__', 84, 12, 84, 19),
woosh.Token(woosh.OP, '(', 84, 19, 84, 20),
woosh.Token(woosh.NAME, 'mcls', 84, 20, 84, 24),
woosh.Token(woosh.OP, ',', 84, 24, 84, 25),
woosh.Token(woosh.NAME, 'name', 84, 26, 84, 30),
woosh.Token(woosh.OP, ',', 84, 30, 84, 31),
woosh.Token(woosh.NAME, 'bases', 84, 32, 84, 37),
woosh.Token(woosh.OP, ',', 84, 37, 84, 38),
woosh.Token(woosh.NAME, 'namespace', 84, 39, 84, 48),
woosh.Token(woosh.OP, ',', 84, 48, 84, 49),
woosh.Token(woosh.OP, '**', 84, 50, 84, 52),
woosh.Token(woosh.NAME, 'kwargs', 84, 52, 84, 58),
woosh.Token(woosh.OP, ')', 84, 58, 84, 59),
woosh.Token(woosh.OP, ':', 84, 59, 84, 60),
woosh.Token(woosh.NEWLINE, '\r\n', 84, 60, 85, 0),
woosh.Token(woosh.INDENT, '            ', 85, 0, 85, 12),
woosh.Token(woosh.NAME, 'cls', 85, 12, 85, 15),
woosh.Token(woosh.OP, '=', 85, 16, 85, 17),
woosh.Token(woosh.NAME, 'super', 85, 18, 85, 23),
woosh.Token(woosh.OP, '(', 85, 23, 85, 24),
woosh.Token(woosh.OP, ')', 85, 24, 85, 25),
woosh.Token(woosh.OP, '.', 85, 25, 85, 26),
woosh.Token(woosh.NAME, '__new__', 85, 26, 85, 33),
woosh.Token(woosh.OP, '(', 85, 33, 85, 34),
woosh.Token(woosh.NAME, 'mcls', 85, 34, 85, 38),
woosh.Token(woosh.OP, ',', 85, 38, 85, 39),
woosh.Token(woosh.NAME, 'name', 85, 40, 85, 44),
woosh.Token(woosh.OP, ',', 85, 44, 85, 45),
woosh.Token(woosh.NAME, 'bases', 85, 46, 85, 51),
woosh.Token(woosh.OP, ',', 85, 51, 85, 52),
woosh.Token(woosh.NAME, 'namespace', 85, 53, 85, 62),
woosh.Token(woosh.OP, ',', 85, 62, 85, 63),
woosh.Token(woosh.OP, '**', 85, 64, 85, 66),
woosh.Token(woosh.NAME, 'kwargs', 85, 66, 85, 72),
woosh.Token(woosh.OP, ')', 85, 72, 85, 73),
woosh.Token(woosh.NEWLINE, '\r\n', 85, 73, 86, 0),
woosh.Token(woosh.NAME, '_abc_init', 86, 12, 86, 21),
woosh.Token(woosh.OP, '(', 86, 21, 86, 22),
woosh.Token(woosh.NAME, 'cls', 86, 22, 86, 25),
woosh.Token(woosh.OP, ')', 86, 25, 86, 26),
woosh.Token(woosh.NEWLINE, '\r\n', 86, 26, 87, 0),
woosh.Token(woosh.NAME, 'return', 87, 12, 87, 18),
woosh.Token(woosh.NAME, 'cls', 87, 19, 87, 22),
woosh.Token(woosh.NEWLINE, '\r\n', 87, 22, 88, 0),
woosh.Token(woosh.DEDENT, '        ', 89, 0, 89, 8),
woosh.Token(woosh.NAME, 'def', 89, 8, 89, 11),
woosh.Token(woosh.NAME, 'register', 89, 12, 89, 20),
woosh.Token(woosh.OP, '(', 89, 20, 89, 21),
woosh.Token(woosh.NAME, 'cls', 89, 21, 89, 24),
woosh.Token(woosh.OP, ',', 89, 24, 89, 25),
woosh.Token(woosh.NAME, 'subclass', 89, 26, 89, 34),
woosh.Token(woosh.OP, ')', 89, 34, 89, 35),
woosh.Token(woosh.OP, ':', 89, 35, 89, 36),
woosh.Token(woosh.NEWLINE, '\r\n', 89, 36, 90, 0),
woosh.Token(woosh.INDENT, '            ', 90, 0, 90, 12),
woosh.Token(woosh.STRING, '"""Register a virtual subclass of an ABC.\r\n\r\n            Returns the subclass, to allow usage as a class decorator.\r\n            """', 90, 12, 93, 15),
woosh.Token(woosh.NEWLINE, '\r\n', 93, 15, 94, 0),
woosh.Token(woosh.NAME, 'return', 94, 12, 94, 18),
woosh.Token(woosh.NAME, '_abc_register', 94, 19, 94, 32),
woosh.Token(woosh.OP, '(', 94, 32, 94, 33),
woosh.Token(woosh.NAME, 'cls', 94, 33, 94, 36),
woosh.Token(woosh.OP, ',', 94, 36, 94, 37),
woosh.Token(woosh.NAME, 'subclass', 94, 38, 94, 46),
woosh.Token(woosh.OP, ')', 94, 46, 94, 47),
woosh.Token(woosh.NEWLINE, '\r\n', 94, 47, 95, 0),
woosh.Token(woosh.DEDENT, '        ', 96, 0, 96, 8),
woosh.Token(woosh.NAME, 'def', 96, 8, 96, 11),
woosh.Token(woosh.NAME, '__instancecheck__', 96, 12, 96, 29),
woosh.Token(woosh.OP, '(', 96, 29, 96, 30),
woosh.Token(woosh.NAME, 'cls', 96, 30, 96, 33),
woosh.Token(woosh.OP, ',', 96, 33, 96, 34),
woosh.Token(woosh.NAME, 'instance', 96, 35, 96, 43),
woosh.Token(woosh.OP, ')', 96, 43, 96, 44),
woosh.Token(woosh.OP, ':', 96, 44, 96, 45),
woosh.Token(woosh.NEWLINE, '\r\n', 96, 45, 97, 0),
woosh.Token(woosh.INDENT, '            ', 97, 0, 97, 12),
woosh.Token(woosh.STRING, '"""Override for isinstance(instance, cls)."""', 97, 12, 97, 57),
woosh.Token(woosh.NEWLINE, '\r\n', 97, 57, 98, 0),
woosh.Token(woosh.NAME, 'return', 98, 12, 98, 18),
woosh.Token(woosh.NAME, '_abc_instancecheck', 98, 19, 98, 37),
woosh.Token(woosh.OP, '(', 98, 37, 98, 38),
woosh.Token(woosh.NAME, 'cls', 98, 38, 98, 41),
woosh.Token(woosh.OP, ',', 98, 41, 98, 42),
woosh.Token(woosh.NAME, 'instance', 98, 43, 98, 51),
woosh.Token(woosh.OP, ')', 98, 51, 98, 52),
woosh.Token(woosh.NEWLINE, '\r\n', 98, 52, 99, 0),
woosh.Token(woosh.DEDENT, '        ', 100, 0, 100, 8),
woosh.Token(woosh.NAME, 'def', 100, 8, 100, 11),
woosh.Token(woosh.NAME, '__subclasscheck__', 100, 12, 100, 29),
woosh.Token(woosh.OP, '(', 100, 29, 100, 30),
woosh.Token(woosh.NAME, 'cls', 100, 30, 100, 33),
woosh.Token(woosh.OP, ',', 100, 33, 100, 34),
woosh.Token(woosh.NAME, 'subclass', 100, 35, 100, 43),
woosh.Token(woosh.OP, ')', 100, 43, 100, 44),
woosh.Token(woosh.OP, ':', 100, 44, 100, 45),
woosh.Token(woosh.NEWLINE, '\r\n', 100, 45, 101, 0),
woosh.Token(woosh.INDENT, '            ', 101, 0, 101, 12),
woosh.Token(woosh.STRING, '"""Override for issubclass(subclass, cls)."""', 101, 12, 101, 57),
woosh.Token(woosh.NEWLINE, '\r\n', 101, 57, 102, 0),
woosh.Token(woosh.NAME, 'return', 102, 12, 102, 18),
woosh.Token(woosh.NAME, '_abc_subclasscheck', 102, 19, 102, 37),
woosh.Token(woosh.OP, '(', 102, 37, 102, 38),
woosh.Token(woosh.NAME, 'cls', 102, 38, 102, 41),
woosh.Token(woosh.OP, ',', 102, 41, 102, 42),
woosh.Token(woosh.NAME, 'subclass', 102, 43, 102, 51),
woosh.Token(woosh.OP, ')', 102, 51, 102, 52),
woosh.Token(woosh.NEWLINE, '\r\n', 102, 52, 103, 0),
woosh.Token(woosh.DEDENT, '        ', 104, 0, 104, 8),
woosh.Token(woosh.NAME, 'def', 104, 8, 104, 11),
woosh.Token(woosh.NAME, '_dump_registry', 104, 12, 104, 26),
woosh.Token(woosh.OP, '(', 104, 26, 104, 27),
woosh.Token(woosh.NAME, 'cls', 104, 27, 104, 30),
woosh.Token(woosh.OP, ',', 104, 30, 104, 31),
woosh.Token(woosh.NAME, 'file', 104, 32, 104, 36),
woosh.Token(woosh.OP, '=', 104, 36, 104, 37),
woosh.Token(woosh.NAME, 'None', 104, 37, 104, 41),
woosh.Token(woosh.OP, ')', 104, 41, 104, 42),
woosh.Token(woosh.OP, ':', 104, 42, 104, 43),
woosh.Token(woosh.NEWLINE, '\r\n', 104, 43, 105, 0),
woosh.Token(woosh.INDENT, '            ', 105, 0, 105, 12),
woosh.Token(woosh.STRING, '"""Debug helper to print the ABC registry."""', 105, 12, 105, 57),
woosh.Token(woosh.NEWLINE, '\r\n', 105, 57, 106, 0),
woosh.Token(woosh.NAME, 'print', 106, 12, 106, 17),
woosh.Token(woosh.OP, '(', 106, 17, 106, 18),
woosh.Token(woosh.STRING, 'f"Class: {cls.__module__}.{cls.__qualname__}"', 106, 18, 106, 63),
woosh.Token(woosh.OP, ',', 106, 63, 106, 64),
woosh.Token(woosh.NAME, 'file', 106, 65, 106, 69),
woosh.Token(woosh.OP, '=', 106, 69, 106, 70),
woosh.Token(woosh.NAME, 'file', 106, 70, 106, 74),
woosh.Token(woosh.OP, ')', 106, 74, 106, 75),
woosh.Token(woosh.NEWLINE, '\r\n', 106, 75, 107, 0),
woosh.Token(woosh.NAME, 'print', 107, 12, 107, 17),
woosh.Token(woosh.OP, '(', 107, 17, 107, 18),
woosh.Token(woosh.STRING, 'f"Inv. counter: {get_cache_token()}"', 107, 18, 107, 54),
woosh.Token(woosh.OP, ',', 107, 54, 107, 55),
woosh.Token(woosh.NAME, 'file', 107, 56, 107, 60),
woosh.Token(woosh.OP, '=', 107, 60, 107, 61),
woosh.Token(woosh.NAME, 'file', 107, 61, 107, 65),
woosh.Token(woosh.OP, ')', 107, 65, 107, 66),
woosh.Token(woosh.NEWLINE, '\r\n', 107, 66, 108, 0),
woosh.Token(woosh.OP, '(', 108, 12, 108, 13),
woosh.Token(woosh.NAME, '_abc_registry', 108, 13, 108, 26),
woosh.Token(woosh.OP, ',', 108, 26, 108, 27),
woosh.Token(woosh.NAME, '_abc_cache', 108, 28, 108, 38),
woosh.Token(woosh.OP, ',', 108, 38, 108, 39),
woosh.Token(woosh.NAME, '_abc_negative_cache', 108, 40, 108, 59),
woosh.Token(woosh.OP, ',', 108, 59, 108, 60),
woosh.Token(woosh.NAME, '_abc_negative_cache_version', 109, 13, 109, 40),
woosh.Token(woosh.OP, ')', 109, 40, 109, 41),
woosh.Token(woosh.OP, '=', 109, 42, 109, 43),
woosh.Token(woosh.NAME, '_get_dump', 109, 44, 109, 53),
woosh.Token(woosh.OP, '(', 109, 53, 109, 54),
woosh.Token(woosh.NAME, 'cls', 109, 54, 109, 57),
woosh.Token(woosh.OP, ')', 109, 57, 109, 58),
woosh.Token(woosh.NEWLINE, '\r\n', 109, 58, 110, 0),
woosh.Token(woosh.NAME, 'print', 110, 12, 110, 17),
woosh.Token(woosh.OP, '(', 110, 17, 110, 18),
woosh.Token(woosh.STRING, 'f"_abc_registry: {_abc_registry!r}"', 110, 18, 110, 53),
woosh.Token(woosh.OP, ',', 110, 53, 110, 54),
woosh.Token(woosh.NAME, 'file', 110, 55, 110, 59),
woosh.Token(woosh.OP, '=', 110, 59, 110, 60),
woosh.Token(woosh.NAME, 'file', 110, 60, 110, 64),
woosh.Token(woosh.OP, ')', 110, 64, 110, 65),
woosh.Token(woosh.NEWLINE, '\r\n', 110, 65, 111, 0),
woosh.Token(woosh.NAME, 'print', 111, 12, 111, 17),
woosh.Token(woosh.OP, '(', 111, 17, 111, 18),
woosh.Token(woosh.STRING, 'f"_abc_cache: {_abc_cache!r}"', 111, 18, 111, 47),
woosh.Token(woosh.OP, ',', 111, 47, 111, 48),
woosh.Token(woosh.NAME, 'file', 111, 49, 111, 53),
woosh.Token(woosh.OP, '=', 111, 53, 111, 54),
woosh.Token(woosh.NAME, 'file', 111, 54, 111, 58),
woosh.Token(woosh.OP, ')', 111, 58, 111, 59),
woosh.Token(woosh.NEWLINE, '\r\n', 111, 59, 112, 0),
woosh.Token(woosh.NAME, 'print', 112, 12, 112, 17),
woosh.Token(woosh.OP, '(', 112, 17, 112, 18),
woosh.Token(woosh.STRING, 'f"_abc_negative_cache: {_abc_negative_cache!r}"', 112, 18, 112, 65),
woosh.Token(woosh.OP, ',', 112, 65, 112, 66),
woosh.Token(woosh.NAME, 'file', 112, 67, 112, 71),
woosh.Token(woosh.OP, '=', 112, 71, 112, 72),
woosh.Token(woosh.NAME, 'file', 112, 72, 112, 76),
woosh.Token(woosh.OP, ')', 112, 76, 112, 77),
woosh.Token(woosh.NEWLINE, '\r\n', 112, 77, 113, 0),
woosh.Token(woosh.NAME, 'print', 113, 12, 113, 17),
woosh.Token(woosh.OP, '(', 113, 17, 113, 18),
woosh.Token(woosh.STRING, 'f"_abc_negative_cache_version: {_abc_negative_cache_version!r}"', 113, 18, 113, 81),
woosh.Token(woosh.OP, ',', 113, 81, 113, 82),
woosh.Token(woosh.NAME, 'file', 114, 18, 114, 22),
woosh.Token(woosh.OP, '=', 114, 22, 114, 23),
woosh.Token(woosh.NAME, 'file', 114, 23, 114, 27),
woosh.Token(woosh.OP, ')', 114, 27, 114, 28),
woosh.Token(woosh.NEWLINE, '\r\n', 114, 28, 115, 0),
woosh.Token(woosh.DEDENT, '        ', 116, 0, 116, 8),
woosh.Token(woosh.NAME, 'def', 116, 8, 116, 11),
woosh.Token(woosh.NAME, '_abc_registry_clear', 116, 12, 116, 31),
woosh.Token(woosh.OP, '(', 116, 31, 116, 32),
woosh.Token(woosh.NAME, 'cls', 116, 32, 116, 35),
woosh.Token(woosh.OP, ')', 116, 35, 116, 36),
woosh.Token(woosh.OP, ':', 116, 36, 116, 37),
woosh.Token(woosh.NEWLINE, '\r\n', 116, 37, 117, 0),
woosh.Token(woosh.INDENT, '            ', 117, 0, 117, 12),
woosh.Token(woosh.STRING, '"""Clear the registry (for debugging or testing)."""', 117, 12, 117, 64),
woosh.Token(woosh.NEWLINE, '\r\n', 117, 64, 118, 0),
woosh.Token(woosh.NAME, '_reset_registry', 118, 12, 118, 27),
woosh.Token(woosh.OP, '(', 118, 27, 118, 28),
woosh.Token(woosh.NAME, 'cls', 118, 28, 118, 31),
woosh.Token(woosh.OP, ')', 118, 31, 118, 32),
woosh.Token(woosh.NEWLINE, '\r\n', 118, 32, 119, 0),
woosh.Token(woosh.DEDENT, '        ', 120, 0, 120, 8),
woosh.Token(woosh.NAME, 'def', 120, 8, 120, 11),
woosh.Token(woosh.NAME, '_abc_caches_clear', 120, 12, 120, 29),
woosh.Token(woosh.OP, '(', 120, 29, 120, 30),
woosh.Token(woosh.NAME, 'cls', 120, 30, 120, 33),
woosh.Token(woosh.OP, ')', 120, 33, 120, 34),
woosh.Token(woosh.OP, ':', 120, 34, 120, 35),
woosh.Token(woosh.NEWLINE, '\r\n', 120, 35, 121, 0),
woosh.Token(woosh.INDENT, '            ', 121, 0, 121, 12),
woosh.Token(woosh.STRING, '"""Clear the caches (for debugging or testing)."""', 121, 12, 121, 62),
woosh.Token(woosh.NEWLINE, '\r\n', 121, 62, 122, 0),
woosh.Token(woosh.NAME, '_reset_caches', 122, 12, 122, 25),
woosh.Token(woosh.OP, '(', 122, 25, 122, 26),
woosh.Token(woosh.NAME, 'cls', 122, 26, 122, 29),
woosh.Token(woosh.OP, ')', 122, 29, 122, 30),
woosh.Token(woosh.NEWLINE, '\r\n', 122, 30, 123, 0),
woosh.Token(woosh.DEDENT, '', 125, 0, 125, 0),
woosh.Token(woosh.DEDENT, '', 125, 0, 125, 0),
woosh.Token(woosh.DEDENT, '', 125, 0, 125, 0),
woosh.Token(woosh.NAME, 'class', 125, 0, 125, 5),
woosh.Token(woosh.NAME, 'ABC', 125, 6, 125, 9),
woosh.Token(woosh.OP, '(', 125, 9, 125, 10),
woosh.Token(woosh.NAME, 'metaclass', 125, 10, 125, 19),
woosh.Token(woosh.OP, '=', 125, 19, 125, 20),
woosh.Token(woosh.NAME, 'ABCMeta', 125, 20, 125, 27),
woosh.Token(woosh.OP, ')', 125, 27, 125, 28),
woosh.Token(woosh.OP, ':', 125, 28, 125, 29),
woosh.Token(woosh.NEWLINE, '\r\n', 125, 29, 126, 0),
woosh.Token(woosh.INDENT, '    ', 126, 0, 126, 4),
woosh.Token(woosh.STRING, '"""Helper class that provides a standard way to create an ABC using\r\n    inheritance.\r\n    """', 126, 4, 128, 7),
woosh.Token(woosh.NEWLINE, '\r\n', 128, 7, 129, 0),
woosh.Token(woosh.NAME, '__slots__', 129, 4, 129, 13),
woosh.Token(woosh.OP, '=', 129, 14, 129, 15),
woosh.Token(woosh.OP, '(', 129, 16, 129, 17),
woosh.Token(woosh.OP, ')', 129, 17, 129, 18),
woosh.Token(woosh.NEWLINE, '\r\n', 129, 18, 130, 0),
woosh.Token(woosh.DEDENT, '', 130, 0, 130, 0),
woosh.Token(woosh.EOF, '', 130, 0, 130, 0),
]

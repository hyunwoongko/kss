# -*- coding: utf-8 -*-
"""
    hangulize
    ~~~~~~~~~

    Korean Alphabet Transcription.

    :copyright: (c) 2010-2017 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import
import importlib


__version__ = '0.0.9'
__all__ = ['hangulize', 'get_lang', 'supports']


def hangulize(string, code=None):
    """Transcribes a loanword to Hangul.

        >>> print hangulize(u'gloria', 'ita')
        글로리아

    :param string: a loan word
    :param code: a language code as ISO 639-3.
    """
    return get_lang(code).hangulize(string)


def get_lang(code):
    """Returns a language instance from the given code."""
    code_head = code.split('.', 1)[0]
    if len(code_head) < 2 or len(code_head) > 3:
        raise ValueError('%r is an invalid language code' % code)
    def make_lang(code, submods):
        try:
            code = '.'.join([code] + list(submods))
            return import_lang_module(code).__lang__()
        except ImportError:
            raise ValueError('Hangulize does not support %s' % code)
    # split module path
    if '.' in code:
        code = code.split('.')
        submods = code[1:]
        code = code[0]
    else:
        submods = ()
    return make_lang(code, submods)


def import_lang_module(code):
    """Imports a module from the given code."""
    return importlib.import_module(f'kss._modules.hangulization.hangulize.langs.{code}')


def supports(code):
    """Checks if hangulize supports the given language.

        >>> supports('ita')
        True
        >>> supports('kat.narrow')
        True
        >>> supports('kor')
        False
    """
    try:
        import_lang_module(code)
        return True
    except ImportError:
        return False


def supported(code):
    """Deprecated with 0.0.6. Use :func:`hangulize.supports` instead."""
    import warnings
    warnings.warn('supported() has been deprecated, use supports() instead',
                  DeprecationWarning)
    return supports(code)


# include all submodules.
for name in ['.models', '.normalization', '.processing']:
    module = importlib.import_module(name, __name__)
    __all__.extend(module.__all__)
    for attr in module.__all__:
        locals()[attr] = getattr(module, attr)

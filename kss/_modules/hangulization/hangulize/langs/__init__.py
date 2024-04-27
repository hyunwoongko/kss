# -*- coding: utf-8 -*-
"""
    hangulize.langs
    ~~~~~~~~~~~~~~~

    The languages that Hangulize supports.

    :copyright: (c) 2010-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
import os
import re


p = os.path


def list_langs():
    """Returns the supported language code list."""
    ext = p.extsep + 'py'
    init = '__init__' + ext
    def _list_langs(prefix='', path=None):
        path = path or p.dirname(__file__)
        # helpers
        name = lambda x: prefix + re.sub(re.escape(ext) + '$', '', x)
        def is_lang(x):
            if x.startswith(init):
                return False
            x = p.join(path, x)
            return p.isdir(x) and p.isfile(p.join(x, init)) or \
                   p.isfile(x) and x.endswith(ext)
        # find top-level language modules
        langs = [name(x) for x in os.listdir(path) if is_lang(x)]
        # find sub language modules
        for lang in langs:
            _path = p.join(path, lang)
            if p.isdir(_path):
                langs += _list_langs(prefix=lang + '.', path=_path)
        langs.sort()
        return langs
    return _list_langs()


def get_list():
    """Deprecated with 0.0.6. Use :func:`hangulize.langs.list_langs`
    instead.
    """
    import warnings
    warnings.warn('get_list() has been deprecated, use list_langs() instead',
                  DeprecationWarning)
    return list_langs()

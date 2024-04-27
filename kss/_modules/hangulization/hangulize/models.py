# -*- coding: utf-8 -*-
"""
    hangulize.models
    ~~~~~~~~~~~~~~~~

    :copyright: (c) 2010-2017 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from collections import deque
import functools
import re
import sys

from kss._modules.hangulization.hangulize import hangul
from kss._modules.hangulization.hangulize.hangul import join


__all__ = ['SPACE', 'ZWSP', 'EDGE', 'SPECIAL', 'BLANK', 'DONE', 'ENCODING',
           'EMPTY_TUPLE', 'Phoneme', 'Choseong', 'Jungseong', 'Jongseong',
           'Impurity', 'Notation', 'Language', 'Rewrite']


# include Hangul constants.
for name in dir(hangul):
    if name == name.upper():
        locals()[name] = getattr(hangul, name)
        __all__.append(name)


SPACE = ' '
ZWSP = '/'  # zero-width space
EDGE = chr(3)
SPECIAL = chr(6)
BLANK = '(?:%s)' % '|'.join(map(re.escape, (SPACE, ZWSP, EDGE, SPECIAL)))
DONE = chr(0)
ENCODING = getattr(sys.stdout, 'encoding', 'utf-8')
EMPTY_TUPLE = ()


def cached_property(func, name=None):
    if name is None:
        name = func.__name__
    def get(self):
        try:
            return self.__dict__[name]
        except KeyError:
            val = func(self)
            self.__dict__[name] = val
            return val
    functools.update_wrapper(get, func)
    def del_(self):
        self.__dict__.pop(name, None)
    return property(get, None, del_)


class Phoneme(object):
    """This abstract class wraps a Hangul letter."""

    def __init__(self, letter):
        self.letter = letter

    def __repr__(self):
        name = type(self).__name__
        return "<%s '%s'>" % (name, self.letter.encode(ENCODING))


class Choseong(Phoneme):
    """A initial consonant in Hangul::

        >>> Choseong(G)
        <Choseong 'ㄱ'>

    """

    pass


class Jungseong(Phoneme):
    """A vowel in Hangul::

        >>> Jungseong(A)
        <Jungseong 'ㅏ'>

    """

    pass


class Jongseong(Phoneme):
    """A final consonant in Hangul::

        >>> Jongseong(G)
        <Jongseong 'ㄱ'>

    """

    pass


class Impurity(Phoneme):
    """An impurity letter will be kept."""

    pass


class Notation(object):
    """Describes loanword orthography.

    :param rules: the rewrite rules as an ordered key-value list
    """

    def __init__(self, rules):
        self.rules = rules

    def __add__(self, rules):
        if isinstance(rules, Notation):
            rules = rules.rules
        return Notation(self.rules + rules)

    def __radd__(self, lrules):
        if isinstance(lrules, Notation):
            lrules = lrules.rules
        return Notation(lrules + self.rules)

    def __iter__(self):
        if not getattr(self, '_rewrites', None):
            self._rewrites = [Rewrite(*item) for item in self.items()]
        return iter(self._rewrites)

    def items(self, left_edge=False, right_edge=False, lang=None):
        """Yields each notation rules as regex."""
        for one in self.rules:
            pattern = one[0]
            # accept *args
            if len(one) == 2:
                val = one[1]
                if isinstance(val, Phoneme):
                    val = val,
            # accept args(a tuple instance)
            else:
                val = one[1:]
            yield pattern, val

    @property
    def chars(self):
        """The humane characters from the notation keys."""
        chest = []
        for one in self.rules:
            pattern = Rewrite.VARIABLE_PATTERN.sub('', one[0])
            pattern = re.sub(r'[\{\}\@\[\]\^\$]', '', pattern)
            for c in pattern:
                chest.append(c)
        return set(chest)


class Language(object):
    """Wraps a foreign language. The language should have a :class:`Notation`
    instance::

        >>> class Extraterrestrial(Language):
        ...     notation = Notation([
        ...         (u'ㅹ', (Choseong(BB), Jungseong(U), Jongseong(NG))),
        ...         (u'㉠', (Choseong(G),)),
        ...         (u'ㅣ', (Jungseong(I),)),
        ...         (u'ㅋ', (Choseong(K), Jungseong(I), Jongseong(G)))
        ...     ])
        ...
        >>> ext = Extraterrestrial()
        >>> print ext.hangulize(u'ㅹ㉠ㅣㅋㅋㅋ')
        뿡기킥킥킥

    :param logger: a logger

    """

    __tmp__ = ''
    __special__ = '.,;?~"()[]{}'

    vowels = EMPTY_TUPLE
    notation = None

    def __new__(cls):
        if not getattr(cls, '_instances', None):
            cls._instances = {}
        if cls not in cls._instances:
            cls._instances[cls] = object.__new__(cls)
        return cls._instances[cls]

    def __init__(self):
        if not isinstance(self.notation, Notation):
            raise NotImplementedError("notation has to be defined")

    @cached_property
    def _steal_specials(self):
        def keep(match, rewrite):
            """keep special characters."""
            self._specials.append(match.group(0))
            return SPECIAL
        esc = '(%s)' % '|'.join(re.escape(x) for x in
                                self.__special__ + self.__tmp__)
        return Rewrite(esc, keep)

    @cached_property
    def _recover_specials(self):
        def escape(match, rewrite):
            """escape special characters."""
            return (Impurity(self._specials.pop(0)),)
        return Rewrite(SPECIAL, escape)

    @cached_property
    def _remove_tmp(self):
        tmp = '(%s)' % '|'.join(re.escape(x) for x in self.__tmp__)
        return Rewrite(tmp, None)

    @property
    def chars_pattern(self):
        """The regex pattern which is matched the valid characters."""
        return ''.join(re.escape(c) for c in self.notation.chars)

    def split(self, string):
        """Splits words from the string. Each words have only valid characters.
        """
        pattern = '[^%s]+' % self.chars_pattern
        return re.split(pattern, string)

    def transcribe(self, string, logger=None):
        """Returns :class:`Phoneme` instance list from the word."""
        string = re.sub(r'\s+', SPACE, string)
        string = re.sub(r'^|$', EDGE, string)
        self._specials = []
        phonemes = []

        # steal special characters
        string = self._steal_specials(string, phonemes)
        # apply the notation
        for rewrite in self.notation:
            string = rewrite(string, phonemes, lang=self, logger=logger)
        # remove temporary characters
        string = self._remove_tmp(string, phonemes)
        # recover special characters
        string = self._recover_specials(string, phonemes)

        # post processing
        string = re.sub('^' + BLANK, '', string)
        string = re.sub(BLANK + '$', '', string)
        phonemes = phonemes[1:-1]
        string = _hold_spaces(string, phonemes)
        string = _remove_zwsp(string, phonemes)
        string = _pass_unmatched(string, phonemes)

        # flatten
        flat_phonemes = []
        for phs in phonemes:
            if phs:
                flat_phonemes.extend(phs)
        return flat_phonemes

    def normalize(self, string):
        """Before transcribing, normalizes the string. You could specify the
        different normalization for the language with overriding this method.
        """
        return string

    def hangulize(self, string, logger=None):
        """Hangulizes the string::

            >>> from kss._modules.hangulization.hangulize.langs.ja import Japanese
            >>> ja = Japanese()
            >>> ja.hangulize(u'あかちゃん')
            아카찬

        """
        from kss._modules.hangulization.hangulize.processing import complete_syllables
        def stringify(syllable):
            if isinstance(syllable[0], Impurity):
                return syllable[0].letter
            else:
                return join(syllable)
        string = self.normalize(string)
        logger and logger.info(">> '%s'" % string)
        phonemes = self.transcribe(string, logger=logger)
        try:
            syllables = complete_syllables(phonemes)
            result = [stringify(syl) for syl in syllables]
            hangulized = ''.join(result)
        except TypeError:
            hangulized = u''
        logger and logger.info('=> %s' % hangulized)
        return hangulized

    @property
    def iso639_1(self):
        return self.__iso639__.get(1)

    @property
    def iso639_2(self):
        return self.__iso639__.get(2)

    @property
    def iso639_3(self):
        return self.__iso639__.get(3)

    @property
    def code(self):
        return re.sub('^hangulize\.langs\.', '', type(self).__module__)


class Rewrite(object):

    VOWELS_PATTERN = re.compile('@')
    VARIABLE_PATTERN = re.compile('<(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)>')
    LEFT_EDGE_PATTERN = re.compile(r'^(\^?)\^')
    RIGHT_EDGE_PATTERN = re.compile(r'\$(\$?)$')
    LOOKBEHIND_PATTERN = re.compile('^(?P<edge>(?:\^(?:\^)?)?){([^}]+?)}')
    LOOKAHEAD_PATTERN = re.compile('{([^}]+?)}(?P<edge>(?:\$(?:\$)?)?)$')
    def NEGATIVE(regex):
        pattern = regex.pattern.replace('{', '{~')
        return re.compile(pattern)
    NEGATIVE_LOOKBEHIND_PATTERN = NEGATIVE(LOOKBEHIND_PATTERN)
    NEGATIVE_LOOKAHEAD_PATTERN = NEGATIVE(LOOKAHEAD_PATTERN)
    del NEGATIVE

    def __init__(self, pattern, val):
        """Makes a replace function with the given pattern and value."""
        self.pattern, self.val = pattern, val
        self.__regexes__ = {}

    def __call__(self, string, phonemes=None, lang=None, logger=None):
        # allocate needed offsets
        if not phonemes and isinstance(phonemes, list):
            phonemes += [None] * len(string)

        regex = self.compile_pattern(lang)

        # replacement function
        if phonemes:
            deletions = []
        def repl(match):
            val = self.val(match, self) if callable(self.val) else self.val
            repls.append(val)
            start, end = match.span()

            if val:
                is_tuple = isinstance(val, tuple)
                if not is_tuple:
                    if lang:
                        # variable replacement
                        cls = type(self)
                        srcvars = cls.find_actual_variables(self.pattern)
                        dstvars = cls.find_actual_variables(self.val)
                        srcvars, dstvars = list(srcvars), list(dstvars)
                        if len(srcvars) == len(dstvars) == 1:
                            src = getattr(lang, srcvars[0].group('name'))
                            dst = getattr(lang, dstvars[0].group('name'))
                            if len(src) != len(dst):
                                msg = 'the destination variable should ' \
                                      'have the same length with the ' \
                                      'source variable'
                                raise ValueError(msg)
                            dictionary = dict(zip(src, dst))
                            let = dictionary[match.group(0)]
                            val = self.VARIABLE_PATTERN.sub(let, val)
                        # group reference
                        val = re.sub(r'\\(\d+)',
                                     lambda m: match.group(int(m.group(1))),
                                     val)
                    if phonemes:
                        for x in range(len(val) - len(match.group(0))):
                            phonemes.insert(start, None)
                    return val
                elif phonemes and is_tuple:
                    # toss phonemes, and check the matched string
                    phonemes[start] = val
                    return DONE * (end - start)
            else:
                # when val is None, the matched string should remove
                if phonemes:
                    deletions.append((start, end))
                return ''

        if logger:
            prev = string
        repls = []

        # replace the string
        string = regex.sub(repl, string)

        # remove kept deletions
        if phonemes and deletions:
            _phonemes = deque()
            cur = len(phonemes)
            for start, end in reversed(deletions):
                _phonemes.extendleft(reversed(phonemes[end:cur]))
                cur = start
            _phonemes.extendleft(reversed(phonemes[0:cur]))
            phonemes[:] = _phonemes

        if logger:
            # report changes
            if prev != string:
                val = repls.pop()
                args = (string, self.pattern)
                if not val:
                    msg = ".. '%s'\tremove %s" % args
                elif isinstance(val, tuple):
                    val = ''.join(x.letter for x in val)
                    msg = ".. '%s'\thangulize %s -> %s" % (args + (val,))
                else:
                    msg = ".. '%s'\trewrite %s -> %s" % (args + (val,))
                logger.info(msg)

        return string

    def compile_pattern(self, lang=None):
        if lang not in self.__regexes__:
            regex = re.compile(type(self).regexify(self.pattern, lang))
            self.__regexes__[lang] = regex
        return self.__regexes__[lang]

    @classmethod
    def regexify(cls, pattern, lang=None):
        regex = pattern
        if lang:
            regex = cls.regexify_variable(regex, lang)
        regex = cls.regexify_negative_lookaround(regex)
        regex = cls.regexify_lookaround(regex)
        regex = cls.regexify_edge_of_word(regex)
        return regex

    @classmethod
    def regexify_edge_of_word(cls, regex):
        left_edge = r'(?<=\1%s)' % BLANK
        right_edge = r'(?=%s\1)' % BLANK
        regex = cls.LEFT_EDGE_PATTERN.sub(left_edge, regex)
        regex = cls.RIGHT_EDGE_PATTERN.sub(right_edge, regex)
        return regex

    def _make_lookaround(behind_pattern, ahead_pattern,
                         behind_prefix, ahead_prefix):
        @staticmethod
        def meth(regex):
            def lookbehind(match):
                edge = re.sub('\^$', BLANK, match.group('edge'))
                return '(?' + behind_prefix + edge + \
                       '(?:' + match.group(2) + '))'
            def lookahead(match):
                edge = re.sub('^\$', BLANK, match.group('edge'))
                return '(?' + ahead_prefix + \
                       '(?:' + match.group(1) + ')' + edge + ')'
            regex = behind_pattern.sub(lookbehind, regex)
            regex = ahead_pattern.sub(lookahead, regex)
            return regex
        return meth

    _positive = _make_lookaround(LOOKBEHIND_PATTERN,
                                 LOOKAHEAD_PATTERN,
                                 '<=', '=')
    _negative = _make_lookaround(NEGATIVE_LOOKBEHIND_PATTERN,
                                 NEGATIVE_LOOKAHEAD_PATTERN,
                                 '<!', '!')
    regexify_lookaround = _positive
    regexify_negative_lookaround = _negative
    del _make_lookaround, _positive, _negative

    @classmethod
    def regexify_variable(cls, regex, lang):
        def to_variable(match):
            var = getattr(lang, match.group('name'))
            return '(%s)' % '|'.join(re.escape(x) for x in var)
        regex = cls.VOWELS_PATTERN.sub('<vowels>', regex)
        regex = cls.VARIABLE_PATTERN.sub(to_variable, regex)
        return regex

    @classmethod
    def find_actual_variables(cls, pattern):
        # pass when there's no any variable patterns
        if not cls.VOWELS_PATTERN.search(pattern) and \
           not cls.VARIABLE_PATTERN.search(pattern):
            return EMPTY_TUPLE
        try:
            pattern = cls.LOOKBEHIND_PATTERN.sub(DONE, pattern)
            pattern = cls.LOOKAHEAD_PATTERN.sub(DONE, pattern)
            pattern = cls.VOWELS_PATTERN.sub('<>', pattern)
            return cls.VARIABLE_PATTERN.finditer(pattern)
        except TypeError:
            return EMPTY_TUPLE


_remove_zwsp = Rewrite(ZWSP, (Impurity(''),))
_hold_spaces = Rewrite(SPACE, (Impurity(' '),))
_pass_unmatched = Rewrite('[^' + DONE + ']+',
                          lambda m, r: (Impurity(m.group(0)),))

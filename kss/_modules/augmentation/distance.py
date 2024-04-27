import jamo
import numpy as np

hangul_distance_map = {}
hangul_distance_map.update({lead: 0.5 for lead in jamo.JAMO_LEADS})
hangul_distance_map.update({vowel: 0.5 for vowel in jamo.JAMO_VOWELS})
hangul_distance_map.update({tail: 0.25 for tail in jamo.JAMO_TAILS})


def hangul_levenshtein(
    a,
    b,
    normalize=False,
    decompose=True,
    lowercase=False,
    verbose=False,
    insertions_cost_ratio=0.6,
    deletions_cost_ratio=0.4,
):
    """
    In most, Korean people can identify a word even if only the lead consonants of the word are given.
    For example, 'ㄱ' and 'ㅅ' can be identified as '감사' and 'ㅎ' and 'ㅇ' can be identified as '하이'.
    But, if only tail consonants of the word are given, it is very hard to identify the word.
    For example, We can't identify it's '감사' if ['ㅁ', None] is given.

    Let's say we have a source word and two candidate words like the following:

    - source_word = "또또칸"
    - candidate_1 = "똑똑한"
    - candidate_2 = "고소한"

    With original Levenshtein distance, the distance between `source_word` and `candidate_1` is 3
    and the distance between `source_word` and `candidate_2` is also 3. But, with Hangul Levenshtein
    distance, the distance between `source_word` and `candidate_1` can be decreased to 0.7, but the
    distance between `source_word` and `candidate_2` is 1.5. And we all know that '똑똑한' is much
    closer to '또또칸' than '고소한'.
    """
    if isinstance(a, str) is False:
        raise TypeError('First argument is not a string!')
    if isinstance(b, str) is False:
        raise TypeError('Second argument is not a string!')
    if a == '':
        return len(b)
    if b == '':
        return len(a)

    if lowercase:
        a = a.lower()
        b = b.lower()

    if decompose:
        a = jamo.h2j(a)
        b = jamo.h2j(b)

    default_distance = 1

    n = len(a)
    m = len(b)
    lev = np.zeros((n + 1, m + 1))

    for i in range(n + 1):
        lev[i, 0] = i
    for i in range(m + 1):
        lev[0, i] = i

    decay_by_length = 1.0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # 사전에서 글자에 대한 거리 가져오기, 없으면 기본 거리 사용.
            insertion_cost = hangul_distance_map.get(a[i - 1], default_distance) * decay_by_length
            deletion_cost = hangul_distance_map.get(b[j - 1], default_distance) * decay_by_length

            insertion = lev[i - 1, j] + insertion_cost
            deletion = lev[i, j - 1] + deletion_cost

            if a[i - 1] == b[j - 1]:
                substitution = lev[i - 1, j - 1]
            else:
                substitution_cost = insertion_cost * insertions_cost_ratio + deletion_cost * deletions_cost_ratio
                substitution = lev[i - 1, j - 1] + substitution_cost

            lev[i, j] = min(insertion, deletion, substitution)

        # 글자가 길어질수록 거리를 아주 조금씩 감소시킴.
        # 앞글자를 맞추는게 더 중요하기 때문임.
        decay_by_length -= 0.000001

    if verbose:
        print("levenshtein matrix: {}".format(lev))

    if normalize:
        return lev[n, m] / (n + m / 2)
    else:
        return lev[n, m]

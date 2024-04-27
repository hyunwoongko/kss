import sys
from functools import partial
from typing import List, Optional, Tuple, Union

from kss._modules.preprocessing.anonymize import _anonymize
from kss._modules.preprocessing.filter_out import _filter_out
from kss._modules.preprocessing.normalize import _normalize
from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_text, _check_type, _check_num_workers


def preprocess(
    text: Union[str, List[str], Tuple[str]],
    normalization_type: Optional[str] = None,
    allow_doubled_spaces: bool = True,
    allow_html_tags: bool = True,
    allow_html_escape: bool = True,
    allow_halfwidth_hangul: bool = True,
    allow_hangul_jamo: bool = True,
    allow_invisible_chars: bool = True,
    reduce_char_repeats_over: int = sys.maxsize,
    reduce_emoticon_repeats_over: int = sys.maxsize,
    min_length: int = 0,
    max_length: int = sys.maxsize,
    min_mean_words_length: int = 0,
    max_mean_words_length: int = sys.maxsize,
    min_words: int = 0,
    max_words: int = sys.maxsize,
    min_lines: int = 0,
    max_lines: int = sys.maxsize,
    min_paragraphs: int = 0,
    max_paragraphs: int = sys.maxsize,
    min_alphabet_ratio: float = 0,
    max_alphabet_ratio: float = 1,
    min_alphanumeric_ratio: float = 0,
    max_alphanumeric_ratio: float = 1,
    min_number_ratio: float = 0,
    max_number_ratio: float = 1,
    min_punctuation_ratio: float = 0,
    max_punctuation_ratio: float = 1,
    min_symbols_to_words_ratio: float = 0,
    max_symbols_to_words_ratio: float = 0,
    min_lines_started_with_bullets_ratio: float = 0,
    max_lines_started_with_bullets_ratio: float = 1,
    min_whitespace_ratio: float = 0,
    max_whitespace_ratio: float = 1,
    min_parenthesis_ratio: float = 0,
    max_parenthesis_ratio: float = 1,
    min_ellipsis_ratio: float = 0,
    max_ellipsis_ratio: float = 1,
    min_hangul_ratio: float = 0,
    max_hangul_ratio: float = 1,
    max_hangul_incompleted_form_ratio: float = 1,
    max_words_length: int = sys.maxsize,
    max_line_repeats: int = sys.maxsize,
    max_line_by_char_repeats: int = sys.maxsize,
    max_paragraph_repeats: int = sys.maxsize,
    max_paragraph_by_char_repeats: int = sys.maxsize,
    max_repeating_top_ngram_repeats_score: float = sys.maxsize,
    max_repeating_duplicate_ngrams_score: float = sys.maxsize,
    ngram_size_for_repeating_top_ngram_repeats: int = 3,
    ngram_size_for_repeating_duplicate_ngrams: int = 3,
    phone_number_anonymization: bool = True,
    rrn_anonymization: bool = True,
    card_anonymization: bool = True,
    email_anonymization: bool = True,
    bank_account_anonymization: bool = True,
    credit_card_anonymization: bool = True,
    zip_anonymization: bool = True,
    bitcoin_anonymization: bool = True,
    url_anonymization: bool = True,
    ip_v6_anonymization: bool = True,
    ip_v4_anonymization: bool = True,
    phone_number_replacement: str = "<PHONE_NUMBER>",
    rrn_replacement: str = "<RRN>",
    card_replacement: str = "<CARD>",
    email_replacement: str = "<EMAIL>",
    bank_account_replacement: str = "<BANK_ACCOUNT>",
    credit_card_replacement: str = "<CREDIT_CARD>",
    zip_replacement: str = "<ZIP>",
    bitcoin_replacement: str = "<BITCOIN>",
    url_replacement: str = "<URL>",
    ip_v6_replacement: str = "<IPV6>",
    ip_v4_replacement: str = "<IPV4>",
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This preprocesses text with various options.
    This does 1) normalization, 2) filtering out, and 3) anonymization in order.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list of texts
        normalization_type (Optional[str]): normalization type
        allow_doubled_spaces (bool): whether to allow doubled spaces or not
        allow_html_tags (bool): whether to allow HTML tags or not
        allow_html_escape (bool): whether to allow HTML escape or not
        allow_halfwidth_hangul (bool): whether to allow halfwidth Hangul or not
        allow_hangul_jamo (bool): whether to allow Hangul jamo or not
        allow_invisible_chars (bool): whether to allow invisible characters or not
        reduce_char_repeats_over (int): the maximum number of character that can be repeated
        reduce_emoticon_repeats_over (int): the maximum number of emoticon that can be repeated
        min_length (int): minimum length of text
        max_length (int): maximum length of text
        min_mean_words_length (int): minimum mean words length
        max_mean_words_length (int): maximum mean words length
        min_words (int): minimum number of words
        max_words (int): maximum number of words
        min_lines (int): minimum number of lines
        max_lines (int): maximum number of lines
        min_paragraphs (int): minimum number of paragraphs
        max_paragraphs (int): maximum number of paragraphs
        min_alphabet_ratio (float): minimum alphabet ratio
        max_alphabet_ratio (float): maximum alphabet ratio
        min_alphanumeric_ratio (float): minimum alphanumeric ratio
        max_alphanumeric_ratio (float): maximum alphanumeric ratio
        min_number_ratio (float): minimum number ratio
        max_number_ratio (float): maximum number ratio
        min_punctuation_ratio (float): minimum punctuation ratio
        max_punctuation_ratio (float): maximum punctuation ratio
        min_symbols_to_words_ratio (float): minimum symbols to words ratio
        max_symbols_to_words_ratio (float): maximum symbols to words ratio
        min_lines_started_with_bullets_ratio (float): minimum lines started with bullets ratio
        max_lines_started_with_bullets_ratio (float): maximum lines started with bullets ratio
        min_whitespace_ratio (float): minimum whitespace ratio
        max_whitespace_ratio (float): maximum whitespace ratio
        min_parenthesis_ratio (float): minimum parenthesis ratio
        max_parenthesis_ratio (float): maximum parenthesis ratio
        min_ellipsis_ratio (float): minimum ellipsis ratio
        max_ellipsis_ratio (float): maximum ellipsis ratio
        min_hangul_ratio (float): minimum Hangul ratio
        max_hangul_ratio (float): maximum Hangul ratio
        max_hangul_incompleted_form_ratio (float): maximum Hangul non-completed form ratio
        max_words_length (int): maximum words length
        max_line_repeats (int): maximum line repeats
        max_line_by_char_repeats (int): maximum line by char repeats
        max_paragraph_repeats (int): maximum paragraph repeats
        max_paragraph_by_char_repeats (int): maximum paragraph by char repeats
        max_repeating_top_ngram_repeats_score (float): maximum repeating top ngram repeats score
        max_repeating_duplicate_ngrams_score (float): maximum repeating duplicate ngrams score
        ngram_size_for_repeating_top_ngram_repeats (int): ngram size for repeating top ngram repeats
        ngram_size_for_repeating_duplicate_ngrams (int): ngram size for repeating duplicate ngrams
        phone_number_anonymization (bool): whether to anonymize phone number or not
        rrn_anonymization (bool): whether to anonymize RRN or not
        card_anonymization (bool): whether to anonymize card or not
        email_anonymization (bool): whether to anonymize email or not
        bank_account_anonymization (bool): whether to anonymize bank account or not
        credit_card_anonymization (bool): whether to anonymize credit card or not
        zip_anonymization (bool): whether to anonymize zip or not
        bitcoin_anonymization (bool): whether to anonymize bitcoin or not
        url_anonymization (bool): whether to anonymize URL or not
        ip_v6_anonymization (bool): whether to anonymize IPv6 or not
        ip_v4_anonymization (bool): whether to anonymize IPv4 or not
        phone_number_replacement (str): replacement for phone number
        rrn_replacement (str): replacement for RRN
        card_replacement (str): replacement for card
        email_replacement (str): replacement for email
        bank_account_replacement (str): replacement for bank account
        credit_card_replacement (str): replacement for credit card
        zip_replacement (str): replacement for zip
        bitcoin_replacement (str): replacement for bitcoin
        url_replacement (str): replacement for URL
        ip_v6_replacement (str): replacement for IPv6
        ip_v4_replacement (str): replacement for IPv4
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[Tuple[str, Dict[str, Any]], List[Tuple[str, Dict[str, Any]]]]:
            preprocessed text and filtering metadata or list of preprocessed texts and filtering metadata
    """

    text, finish = _check_text(text)

    if finish:
        return text

    if normalization_type is not None:
        normalization_type = _check_type(normalization_type, "normalization_type", str)
    allow_doubled_spaces = _check_type(allow_doubled_spaces, "allow_doubled_spaces", bool)
    allow_html_tags = _check_type(allow_html_tags, "allow_html_tags", bool)
    allow_html_escape = _check_type(allow_html_escape, "allow_html_escape", bool)
    allow_halfwidth_hangul = _check_type(allow_halfwidth_hangul, "allow_halfwidth_hangul", bool)
    allow_hangul_jamo = _check_type(allow_hangul_jamo, "allow_hangul_jamo", bool)
    reduce_char_repeats_over = _check_type(reduce_char_repeats_over, "reduce_char_repeats_over", int)
    reduce_emoticon_repeats_over = _check_type(reduce_emoticon_repeats_over, "reduce_emoticon_repeats_over", int)
    min_length = _check_type(min_length, "min_length", int)
    max_length = _check_type(max_length, "max_length", int)
    min_mean_words_length = _check_type(min_mean_words_length, "min_mean_words_length", int)
    max_mean_words_length = _check_type(max_mean_words_length, "max_mean_words_length", int)
    min_words = _check_type(min_words, "min_words", int)
    max_words = _check_type(max_words, "max_words", int)
    min_lines = _check_type(min_lines, "min_lines", int)
    max_lines = _check_type(max_lines, "max_lines", int)
    min_paragraphs = _check_type(min_paragraphs, "min_paragraphs", int)
    max_paragraphs = _check_type(max_paragraphs, "max_paragraphs", int)
    min_alphabet_ratio = _check_type(min_alphabet_ratio, "min_alphabet_ratio", float)
    max_alphabet_ratio = _check_type(max_alphabet_ratio, "max_alphabet_ratio", float)
    min_alphanumeric_ratio = _check_type(min_alphanumeric_ratio, "min_alphanumeric_ratio", float)
    max_alphanumeric_ratio = _check_type(max_alphanumeric_ratio, "max_alphanumeric_ratio", float)
    min_number_ratio = _check_type(min_number_ratio, "min_number_ratio", float)
    max_number_ratio = _check_type(max_number_ratio, "max_number_ratio", float)
    min_punctuation_ratio = _check_type(min_punctuation_ratio, "min_punctuation_ratio", float)
    max_punctuation_ratio = _check_type(max_punctuation_ratio, "max_punctuation_ratio", float)
    min_symbols_to_words_ratio = _check_type(min_symbols_to_words_ratio, "min_symbols_to_words_ratio", float)
    max_symbols_to_words_ratio = _check_type(max_symbols_to_words_ratio, "max_symbols_to_words_ratio", float)
    min_lines_started_with_bullets_ratio = _check_type(min_lines_started_with_bullets_ratio,
                                                       "min_lines_started_with_bullets_ratio", float)
    max_lines_started_with_bullets_ratio = _check_type(max_lines_started_with_bullets_ratio,
                                                       "max_lines_started_with_bullets_ratio", float)
    min_whitespace_ratio = _check_type(min_whitespace_ratio, "min_whitespace_ratio", float)
    max_whitespace_ratio = _check_type(max_whitespace_ratio, "max_whitespace_ratio", float)
    min_parenthesis_ratio = _check_type(min_parenthesis_ratio, "min_parenthesis_ratio", float)
    max_parenthesis_ratio = _check_type(max_parenthesis_ratio, "max_parenthesis_ratio", float)
    min_ellipsis_ratio = _check_type(min_ellipsis_ratio, "min_ellipsis_ratio", float)
    max_ellipsis_ratio = _check_type(max_ellipsis_ratio, "max_ellipsis_ratio", float)
    min_hangul_ratio = _check_type(min_hangul_ratio, "min_hangul_ratio", float)
    max_hangul_ratio = _check_type(max_hangul_ratio, "max_hangul_ratio", float)
    max_words_length = _check_type(max_words_length, "max_words_length", int)
    max_line_repeats = _check_type(max_line_repeats, "max_line_repeats", int)
    max_line_by_char_repeats = _check_type(max_line_by_char_repeats, "max_line_by_char_repeats", int)
    max_paragraph_repeats = _check_type(max_paragraph_repeats, "max_paragraph_repeats", int)
    max_paragraph_by_char_repeats = _check_type(max_paragraph_by_char_repeats, "max_paragraph_by_char_repeats", int)
    max_repeating_top_ngram_repeats_score = _check_type(max_repeating_top_ngram_repeats_score,
                                                        "max_repeating_top_ngram_repeats_score", float)
    max_repeating_duplicate_ngrams_score = _check_type(max_repeating_duplicate_ngrams_score,
                                                       "max_repeating_duplicate_ngrams_score", float)
    ngram_size_for_repeating_top_ngram_repeats = _check_type(ngram_size_for_repeating_top_ngram_repeats,
                                                             "ngram_size_for_repeating_top_ngram_repeats", int)
    ngram_size_for_repeating_duplicate_ngrams = _check_type(ngram_size_for_repeating_duplicate_ngrams,
                                                            "ngram_size_for_repeating_duplicate_ngrams", int)
    max_hangul_incompleted_form_ratio = _check_type(max_hangul_incompleted_form_ratio,
                                                      "max_hangul_incompleted_form_ratio", float)
    phone_number_anonymization = _check_type(phone_number_anonymization, "phone_number_anonymization", bool)
    rrn_anonymization = _check_type(rrn_anonymization, "rrn_anonymization", bool)
    card_anonymization = _check_type(card_anonymization, "card_anonymization", bool)
    email_anonymization = _check_type(email_anonymization, "email_anonymization", bool)
    bank_account_anonymization = _check_type(bank_account_anonymization, "bank_account_anonymization", bool)
    credit_card_anonymization = _check_type(credit_card_anonymization, "credit_card_anonymization", bool)
    zip_anonymization = _check_type(zip_anonymization, "zip_anonymization", bool)
    bitcoin_anonymization = _check_type(bitcoin_anonymization, "bitcoin_anonymization", bool)
    url_anonymization = _check_type(url_anonymization, "url_anonymization", bool)
    ip_v6_anonymization = _check_type(ip_v6_anonymization, "ip_v6_anonymization", bool)
    ip_v4_anonymization = _check_type(ip_v4_anonymization, "ip_v4_anonymization", bool)
    phone_number_replacement = _check_type(phone_number_replacement, "phone_number_replacement", str)
    rrn_replacement = _check_type(rrn_replacement, "rrn_replacement", str)
    card_replacement = _check_type(card_replacement, "card_replacement", str)
    email_replacement = _check_type(email_replacement, "email_replacement", str)
    bank_account_replacement = _check_type(bank_account_replacement, "bank_account_replacement", str)
    credit_card_replacement = _check_type(credit_card_replacement, "credit_card_replacement", str)
    zip_replacement = _check_type(zip_replacement, "zip_replacement", str)
    bitcoin_replacement = _check_type(bitcoin_replacement, "bitcoin_replacement", str)
    url_replacement = _check_type(url_replacement, "url_replacement", str)
    ip_v6_replacement = _check_type(ip_v6_replacement, "ip_v6_replacement", str)
    ip_v4_replacement = _check_type(ip_v4_replacement, "ip_v4_replacement", str)
    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=partial(
            _preprocess,
            normalization_type=normalization_type,
            allow_doubled_spaces=allow_doubled_spaces,
            allow_html_tags=allow_html_tags,
            allow_html_escape=allow_html_escape,
            allow_halfwidth_hangul=allow_halfwidth_hangul,
            allow_hangul_jamo=allow_hangul_jamo,
            allow_invisible_chars=allow_invisible_chars,
            reduce_char_repeats_over=reduce_char_repeats_over,
            reduce_emoticon_repeats_over=reduce_emoticon_repeats_over,
            min_length=min_length,
            max_length=max_length,
            min_mean_words_length=min_mean_words_length,
            max_mean_words_length=max_mean_words_length,
            min_words=min_words,
            max_words=max_words,
            min_lines=min_lines,
            max_lines=max_lines,
            min_paragraphs=min_paragraphs,
            max_paragraphs=max_paragraphs,
            min_alphabet_ratio=min_alphabet_ratio,
            max_alphabet_ratio=max_alphabet_ratio,
            min_alphanumeric_ratio=min_alphanumeric_ratio,
            max_alphanumeric_ratio=max_alphanumeric_ratio,
            min_number_ratio=min_number_ratio,
            max_number_ratio=max_number_ratio,
            min_punctuation_ratio=min_punctuation_ratio,
            max_punctuation_ratio=max_punctuation_ratio,
            min_symbols_to_words_ratio=min_symbols_to_words_ratio,
            max_symbols_to_words_ratio=max_symbols_to_words_ratio,
            min_lines_started_with_bullets_ratio=min_lines_started_with_bullets_ratio,
            max_lines_started_with_bullets_ratio=max_lines_started_with_bullets_ratio,
            min_whitespace_ratio=min_whitespace_ratio,
            max_whitespace_ratio=max_whitespace_ratio,
            min_parenthesis_ratio=min_parenthesis_ratio,
            max_parenthesis_ratio=max_parenthesis_ratio,
            min_ellipsis_ratio=min_ellipsis_ratio,
            max_ellipsis_ratio=max_ellipsis_ratio,
            min_hangul_ratio=min_hangul_ratio,
            max_hangul_ratio=max_hangul_ratio,
            max_hangul_incompleted_form_ratio=max_hangul_incompleted_form_ratio,
            max_words_length=max_words_length,
            max_line_repeats=max_line_repeats,
            max_line_by_char_repeats=max_line_by_char_repeats,
            max_paragraph_repeats=max_paragraph_repeats,
            max_paragraph_by_char_repeats=max_paragraph_by_char_repeats,
            max_repeating_top_ngram_repeats_score=max_repeating_top_ngram_repeats_score,
            max_repeating_duplicate_ngrams_score=max_repeating_duplicate_ngrams_score,
            ngram_size_for_repeating_top_ngram_repeats=ngram_size_for_repeating_top_ngram_repeats,
            ngram_size_for_repeating_duplicate_ngrams=ngram_size_for_repeating_duplicate_ngrams,
            phone_number_anonymization=phone_number_anonymization,
            rrn_anonymization=rrn_anonymization,
            card_anonymization=card_anonymization,
            email_anonymization=email_anonymization,
            bank_account_anonymization=bank_account_anonymization,
            credit_card_anonymization=credit_card_anonymization,
            zip_anonymization=zip_anonymization,
            bitcoin_anonymization=bitcoin_anonymization,
            url_anonymization=url_anonymization,
            ip_v6_anonymization=ip_v6_anonymization,
            ip_v4_anonymization=ip_v4_anonymization,
            phone_number_replacement=phone_number_replacement,
            rrn_replacement=rrn_replacement,
            card_replacement=card_replacement,
            email_replacement=email_replacement,
            bank_account_replacement=bank_account_replacement,
            credit_card_replacement=credit_card_replacement,
            zip_replacement=zip_replacement,
            bitcoin_replacement=bitcoin_replacement,
            url_replacement=url_replacement,
            ip_v6_replacement=ip_v6_replacement,
            ip_v4_replacement=ip_v4_replacement,
        ),
        inputs=text,
        num_workers=num_workers,
    )


def _preprocess(
    text,
    normalization_type=None,
    allow_doubled_spaces=True,
    allow_html_tags=True,
    allow_html_escape=True,
    allow_halfwidth_hangul=True,
    allow_hangul_jamo=True,
    allow_invisible_chars=True,
    reduce_char_repeats_over=sys.maxsize,
    reduce_emoticon_repeats_over=sys.maxsize,
    min_length=0,
    max_length=sys.maxsize,
    min_mean_words_length=0,
    max_mean_words_length=sys.maxsize,
    min_words=0,
    max_words=sys.maxsize,
    min_lines=0,
    max_lines=sys.maxsize,
    min_paragraphs=0,
    max_paragraphs=sys.maxsize,
    min_alphabet_ratio=0,
    max_alphabet_ratio=1,
    min_alphanumeric_ratio=0,
    max_alphanumeric_ratio=1,
    min_number_ratio=0,
    max_number_ratio=1,
    min_punctuation_ratio=0,
    max_punctuation_ratio=1,
    min_symbols_to_words_ratio=0,
    max_symbols_to_words_ratio=0,
    min_lines_started_with_bullets_ratio=0,
    max_lines_started_with_bullets_ratio=1,
    min_whitespace_ratio=0,
    max_whitespace_ratio=1,
    min_parenthesis_ratio=0,
    max_parenthesis_ratio=1,
    min_ellipsis_ratio=0,
    max_ellipsis_ratio=1,
    min_hangul_ratio=0,
    max_hangul_ratio=1,
    max_hangul_incompleted_form_ratio=1,
    max_words_length=sys.maxsize,
    max_line_repeats=sys.maxsize,
    max_line_by_char_repeats=sys.maxsize,
    max_paragraph_repeats=sys.maxsize,
    max_paragraph_by_char_repeats=sys.maxsize,
    max_repeating_top_ngram_repeats_score=sys.maxsize,
    max_repeating_duplicate_ngrams_score=sys.maxsize,
    ngram_size_for_repeating_top_ngram_repeats=3,
    ngram_size_for_repeating_duplicate_ngrams=3,
    phone_number_anonymization=True,
    rrn_anonymization=True,
    card_anonymization=True,
    email_anonymization=True,
    bank_account_anonymization=True,
    credit_card_anonymization=True,
    zip_anonymization=True,
    bitcoin_anonymization=True,
    url_anonymization=True,
    ip_v6_anonymization=True,
    ip_v4_anonymization=True,
    phone_number_replacement="<PHONE_NUMBER>",
    rrn_replacement="<RRN>",
    card_replacement="<CARD>",
    email_replacement="<EMAIL>",
    bank_account_replacement="<BANK_ACCOUNT>",
    credit_card_replacement="<CREDIT_CARD>",
    zip_replacement="<ZIP>",
    bitcoin_replacement="<BITCOIN>",
    url_replacement="<URL>",
    ip_v6_replacement="<IPV6>",
    ip_v4_replacement="<IPV4>",
):
    # 1. normalize text
    text = _normalize(
        text,
        normalization_type=normalization_type,
        allow_doubled_spaces=allow_doubled_spaces,
        allow_html_tags=allow_html_tags,
        allow_html_escape=allow_html_escape,
        allow_halfwidth_hangul=allow_halfwidth_hangul,
        allow_hangul_jamo=allow_hangul_jamo,
        allow_invisible_chars=allow_invisible_chars,
        reduce_char_repeats_over=reduce_char_repeats_over,
        reduce_emoticon_repeats_over=reduce_emoticon_repeats_over,
    )

    # 2. filter out bad text
    is_filtered_out, filtered_reason = _filter_out(
        text,
        min_length=min_length,
        max_length=max_length,
        min_mean_words_length=min_mean_words_length,
        max_mean_words_length=max_mean_words_length,
        min_words=min_words,
        max_words=max_words,
        min_lines=min_lines,
        max_lines=max_lines,
        min_paragraphs=min_paragraphs,
        max_paragraphs=max_paragraphs,
        min_alphabet_ratio=min_alphabet_ratio,
        max_alphabet_ratio=max_alphabet_ratio,
        min_alphanumeric_ratio=min_alphanumeric_ratio,
        max_alphanumeric_ratio=max_alphanumeric_ratio,
        min_number_ratio=min_number_ratio,
        max_number_ratio=max_number_ratio,
        min_punctuation_ratio=min_punctuation_ratio,
        max_punctuation_ratio=max_punctuation_ratio,
        min_symbols_to_words_ratio=min_symbols_to_words_ratio,
        max_symbols_to_words_ratio=max_symbols_to_words_ratio,
        min_lines_started_with_bullets_ratio=min_lines_started_with_bullets_ratio,
        max_lines_started_with_bullets_ratio=max_lines_started_with_bullets_ratio,
        min_whitespace_ratio=min_whitespace_ratio,
        max_whitespace_ratio=max_whitespace_ratio,
        min_parenthesis_ratio=min_parenthesis_ratio,
        max_parenthesis_ratio=max_parenthesis_ratio,
        min_ellipsis_ratio=min_ellipsis_ratio,
        max_ellipsis_ratio=max_ellipsis_ratio,
        min_hangul_ratio=min_hangul_ratio,
        max_hangul_ratio=max_hangul_ratio,
        max_words_length=max_words_length,
        max_line_repeats=max_line_repeats,
        max_line_by_char_repeats=max_line_by_char_repeats,
        max_paragraph_repeats=max_paragraph_repeats,
        max_paragraph_by_char_repeats=max_paragraph_by_char_repeats,
        max_repeating_top_ngram_repeats_score=max_repeating_top_ngram_repeats_score,
        max_repeating_duplicate_ngrams_score=max_repeating_duplicate_ngrams_score,
        ngram_size_for_repeating_top_ngram_repeats=ngram_size_for_repeating_top_ngram_repeats,
        ngram_size_for_repeating_duplicate_ngrams=ngram_size_for_repeating_duplicate_ngrams,
        max_hangul_incompleted_form_ratio=max_hangul_incompleted_form_ratio,
    )

    if is_filtered_out:
        return None, filtered_reason

    # 3. anonymize text
    text = _anonymize(
        text,
        phone_number_anonymization=phone_number_anonymization,
        rrn_anonymization=rrn_anonymization,
        card_anonymization=card_anonymization,
        email_anonymization=email_anonymization,
        bank_account_anonymization=bank_account_anonymization,
        credit_card_anonymization=credit_card_anonymization,
        zip_anonymization=zip_anonymization,
        bitcoin_anonymization=bitcoin_anonymization,
        url_anonymization=url_anonymization,
        ip_v6_anonymization=ip_v6_anonymization,
        ip_v4_anonymization=ip_v4_anonymization,
        phone_number_replacement=phone_number_replacement,
        rrn_replacement=rrn_replacement,
        card_replacement=card_replacement,
        email_replacement=email_replacement,
        bank_account_replacement=bank_account_replacement,
        credit_card_replacement=credit_card_replacement,
        zip_replacement=zip_replacement,
        bitcoin_replacement=bitcoin_replacement,
        url_replacement=url_replacement,
        ip_v6_replacement=ip_v6_replacement,
        ip_v4_replacement=ip_v4_replacement,
    )

    return text, filtered_reason

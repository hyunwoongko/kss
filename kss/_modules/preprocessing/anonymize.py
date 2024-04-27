# This is copied from dps [https://github.com/EleutherAI/dps]
# And modified by Hyunwoong Ko [https://github.com/hyunwoongko]

import re
from functools import partial
from typing import Tuple, List, Union

from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_type, _check_num_workers, _check_text


PHONE_NUMBER_PATTERN = re.compile(r"([0-9]{2,3}-[0-9]{3,4}-[0-9]{4})|([0-9]{2,3}[0-9]{3,4}[0-9]{4})")

RRN_PATTERN = re.compile(r"([0-9]{6}-[0-9]{7})")

CARD_PATTERN = re.compile(r"([0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4})")

EMAIL_PATTERN = re.compile(
    r"[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+|[a-z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+\.[a-z]"
)

BANK_ACCOUNT_PATTERN = re.compile(
    r"([0-9]\d{13})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # IBK
    + r"([0-9]\d{13})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # KB
    + r"([0-9]\d{12})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2})"  # NH
    + r"([0-9]\d{11})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # SHINHAN
    + r"([0-9]\d{12})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # WOORI
    + r"([0-9]\d{13})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # KEB
    + r"([0-9]\d{11})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # CITI
    + r"([0-9]\d{11})|([0-9]\d{11})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6}\-[0-9,\-])"  # DGB
    + r"([0-9]\d{12})|([0-9]\d{12})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2})"  # BNK
    + r"([0-9]\d{10})|([0-9]\d{10})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # SC
    + r"([0-9]\d{11})|([0-9]\d{10})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,6})"  # KBANK
    + r"([0-9]\d{12})|([0-9]\d{10})|([0-9,\-]{3,6}\-[0-9,\-]{2,6}\-[0-9,\-]{2,7})"  # KAKAO
)

CREDIT_CARD_PATTERN = re.compile(
    r"^(4026|417500|4405|4508|4844|4913|4917)\d+$|"  # VISA Electron
    + r"^(?:50|5[6-9]|6[0-9])\d+$|"  # Maestro
    + r"^(5019|4571)\d+$|"  # Dankort
    + r"^(62|81)\d+$|"  # China UnionPay
    + r"^4[0-9]\d+$|"  # Visa
    + r"^(?:5[1-5]|222[1-9]|22[3-9][0-9]|2[3-6][0-9][0-9]|27[0-1][0-9]|2720)\d+$|"  # MasterCard
    + r"^(34|37)\d+$|"  # American Express
    + r"^6(?:011|22(12[6-9]|1[3-9][0-9]|[2-8][0-9][0-9]|9[01][0-9]|92[0-5])|5|4|2[4-6][0-9]{3}|28[2-8][0-9]{2})\d+$|"  # Discover
    + r"^(35[2-8][0-9])\d+$|"  # JCB
    + r"^(636)\d+$|"  # InterPayment
    + r"^9[0-9]\d+$|"  # KOREAN
    + r"^(220[0-4])\d+$"  # MIR
)

ZIP_PATTERN = re.compile(r"\d{3}-\d{3}")

_base58_alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
_bech32_alphabet = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
BITCOIN_PATTERN = (
    r"( [13] ["
    + _base58_alphabet
    + "]{25,34}"
    + "| bc1 ["
    + _bech32_alphabet
    + "]{8,87})"
)

IPV4_PATTERN = r'(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)(?:\.(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)){3}'
IPV6_PATTERN = r'\[?((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,' \
               r'4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{' \
               r'1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[' \
               r'0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,' \
               r'3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[' \
               r'1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,' \
               r'2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([' \
               r'0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[' \
               r'0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[' \
               r'0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[' \
               r'0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,' \
               r'5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\]?'

ul = '\u00a1-\uffff'  # Unicode letters range
_HOSTNAME_PATTERN = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]{0,61}[a-z' + ul + r'0-9])?'
# Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
_DOMAIN_PATTERN = r'(?:\.(?!-)[a-z' + ul + r'0-9-]{1,63}(?<!-))*'
_TLD_PATTERN = (
    r'\.'  # dot
    r'(?!-)'  # can't start with a dash
    r'(?:[a-z' + ul + '-]{2,63}'  # domain label
                      r'|xn--[a-z0-9]{1,59})'  # or punycode label
                      r'(?<!-)'  # can't end with a dash
                      r'\.?'  # may have a trailing dot
)

_HOST_PATTERN = '(' + _HOSTNAME_PATTERN + _DOMAIN_PATTERN + _TLD_PATTERN + '|localhost)'

URL_PATTERN_1 = re.compile(
    r"""\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"""
)
URL_PATTERN_2 = re.compile(
    r'([a-z0-9.+-]*:?//)?'  # scheme is validated separately
    r'(?:[^\s:@/]+(?::[^\s:@/]*)?@)?'  # user:pass authentication
    r'(?:' + IPV4_PATTERN + '|' + IPV6_PATTERN + '|' + _HOST_PATTERN + ')'
                                                                       r'(?::\d{2,5})?'  # port
                                                                       r'(?:[/?#][^\s]*)?',  # resource path
    re.IGNORECASE
)


def anonymize(
    text: Union[str, List[str], Tuple[str]],
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
):
    """
    This anonymizes sensitive information in the given text.

    Args:
        text (Union[str, List[str], Tuple[str]): single text or list of texts
        phone_number_anonymization (bool): whether to anonymize phone numbers or not
        rrn_anonymization (bool): whether to anonymize resident registration numbers or not
        card_anonymization (bool): whether to anonymize card numbers or not
        email_anonymization (bool): whether to anonymize email addresses or not
        bank_account_anonymization (bool): whether to anonymize bank account numbers or not
        credit_card_anonymization (bool): whether to anonymize credit card numbers or not
        zip_anonymization (bool): whether to anonymize zip codes or not
        bitcoin_anonymization (bool): whether to anonymize bitcoin addresses or not
        url_anonymization (bool): whether to anonymize URLs or not
        ip_v6_anonymization (bool): whether to anonymize IPv6 addresses or not
        ip_v4_anonymization (bool): whether to anonymize IPv4 addresses or not
        phone_number_replacement (str): the replacement string for phone numbers, default is "<PHONE_NUMBER>"
        rrn_replacement (str): the replacement string for resident registration numbers, default is "<RRN>"
        card_replacement (str): the replacement string for card numbers, default is "<CARD>"
        email_replacement (str): the replacement string for email addresses, default is "<EMAIL>"
        bank_account_replacement (str): the replacement string for bank account numbers, default is "<BANK_ACCOUNT>"
        credit_card_replacement (str): the replacement string for credit card numbers, default is "<CREDIT_CARD>"
        zip_replacement (str): the replacement string for zip codes, default is "<ZIP>"
        bitcoin_replacement (str): the replacement string for bitcoin addresses, default is "<BITCOIN>"
        url_replacement (str): the replacement string for URLs, default is "<URL>"
        ip_v6_replacement (str): the replacement string for IPv6 addresses, default is "<IPV6>"
        ip_v4_replacement (str): the replacement string for IPv4 addresses, default is "<IPV4>"
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str], Tuple[str]]: anonymized text or list of anonymized texts

    Examples:
        >>> from kss import Kss
        >>> anonymize = Kss("anonymize")
        >>> text = "제 전화번호는 010-1234-5678, 이메일 주소는 kevin.brain@kakaobrain.com입니다."
        >>> output = anonymize(text)
        >>> print(output)
        "제 전화번호는 <PHONE_NUMBER>, 이메일 주소는 <EMAIL>입니다."
    """
    text, finish = _check_text(text)

    if finish:
        return text

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
            _anonymize,
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


def _anonymize(
    text: Union[str, List[str], Tuple[str]],
    phone_number_anonymization: bool = False,
    rrn_anonymization: bool = False,
    card_anonymization: bool = False,
    email_anonymization: bool = False,
    bank_account_anonymization: bool = False,
    credit_card_anonymization: bool = False,
    zip_anonymization: bool = False,
    bitcoin_anonymization: bool = False,
    url_anonymization: bool = False,
    ip_v6_anonymization: bool = False,
    ip_v4_anonymization: bool = False,
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
):
    text = re.sub(PHONE_NUMBER_PATTERN, phone_number_replacement, text) if phone_number_anonymization else text
    text = re.sub(RRN_PATTERN, rrn_replacement, text) if rrn_anonymization else text
    text = re.sub(CARD_PATTERN, card_replacement, text) if card_anonymization else text
    text = re.sub(EMAIL_PATTERN, email_replacement, text) if email_anonymization else text
    text = re.sub(BANK_ACCOUNT_PATTERN, bank_account_replacement, text) if bank_account_anonymization else text
    text = re.sub(CREDIT_CARD_PATTERN, credit_card_replacement, text) if credit_card_anonymization else text
    text = re.sub(ZIP_PATTERN, zip_replacement, text) if zip_anonymization else text
    text = re.sub(BITCOIN_PATTERN, bitcoin_replacement, text) if bitcoin_anonymization else text
    text = re.sub(URL_PATTERN_1, url_replacement, text) if url_anonymization else text
    text = re.sub(URL_PATTERN_2, url_replacement, text) if url_anonymization else text
    text = re.sub(IPV6_PATTERN, ip_v6_replacement, text) if ip_v6_anonymization else text
    text = re.sub(IPV4_PATTERN, ip_v4_replacement, text) if ip_v4_anonymization else text
    return text

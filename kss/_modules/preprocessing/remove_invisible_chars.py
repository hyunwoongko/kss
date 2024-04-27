from typing import Union, List, Tuple

from kss._utils.multiprocessing import _run_job
from kss._utils.sanity_checks import _check_text, _check_num_workers

UNICODE_TO_REMOVE = {
    0x0000: None,  # Null
    0x0001: None,  # Start of Heading
    0x0002: None,  # Start of Text
    0x0003: None,  # End of Text
    0x0004: None,  # End of Transmission
    0x0005: None,  # Enquiry
    0x0006: None,  # Acknowledge
    0x0007: None,  # Bell
    0x0008: None,  # Backspace
    0x000B: None,  # Vertical Tab
    0x000C: None,  # Form Feed
    0x000D: None,  # Carriage Return
    0x000E: None,  # Shift Out
    0x000F: None,  # Shift In
    0x0010: None,  # Data Link Escape
    0x0011: None,  # Device Control 1
    0x0012: None,  # Device Control 2
    0x0013: None,  # Device Control 3
    0x0014: None,  # Device Control 4
    0x0015: None,  # Negative Acknowledge
    0x0016: None,  # Synchronous Idle
    0x0017: None,  # End of Transmission Block
    0x0018: None,  # Cancel
    0x0019: None,  # End of Medium
    0x001A: None,  # Substitute
    0x001B: None,  # Escape
    0x001C: None,  # File Separator
    0x001D: None,  # Group Separator
    0x001E: None,  # Record Separator
    0x001F: None,  # Unit Separator
    0x007F: None,  # Delete
    0x0080: None,  # Padding Character
    0x0081: None,  # High Octet Preset
    0x0082: None,  # Break Permitted Here
    0x0083: None,  # No Break Here
    0x0084: None,  # Index
    0x0085: None,  # Next Line
    0x0086: None,  # Start of Selected Area
    0x0087: None,  # End of Selected Area
    0x0088: None,  # Character Tabulation Set
    0x0089: None,  # Character Tabulation with Justification
    0x008A: None,  # Line Tabulation Set
    0x008B: None,  # Partial Line Forward
    0x008C: None,  # Partial Line Backward
    0x008D: None,  # Reverse Line Feed
    0x008E: None,  # Single-Shift Two
    0x008F: None,  # Single-Shift Three
    0x0090: None,  # Device Control String
    0x0091: None,  # Private Use 1
    0x0092: None,  # Private Use 2
    0x0093: None,  # Set Transmit State
    0x0094: None,  # Cancel Character
    0x0095: None,  # Message Waiting
    0x0096: None,  # Start of Guarded Area
    0x0097: None,  # End of Guarded Area
    0x0098: None,  # Start of String
    0x0099: None,  # Single Graphic Character Introducer
    0x009A: None,  # Single Character Introducer
    0x009B: None,  # Control Sequence Introducer
    0x009C: None,  # String Terminator
    0x009D: None,  # Operating System Command
    0x009E: None,  # Privacy Message
    0x009F: None,  # Application Program Command
    0x00A0: None,  # No-Break Space
    0x00AD: None,  # Soft Hyphen
    0x115f: None,  # Hangul Choseong Filler
    0x1160: None,  # Hangul Jungseong Filler
    0x200B: None,  # Zero Width Space
    0x200E: None,  # Left-to-Right Mark
    0x200F: None,  # Right-to-Left Mark
    0x202A: None,  # Left-to-Right Embedding
    0x202B: None,  # Right-to-Left Embedding
    0x202C: None,  # Pop Directional Formatting
    0x202D: None,  # Left-to-Right Override
    0x202E: None,  # Right-to-Left Override
    0x202F: None,  # Narrow No-Break Space
    0x2061: None,  # Function Application
    0x2062: None,  # Invisible Times
    0x2063: None,  # Invisible Separator
    0x2064: None,  # Invisible Plus
    0x2066: None,  # Left-to-Right Isolate
    0x2067: None,  # Right-to-Left Isolate
    0x2068: None,  # First Strong Isolate
    0x2069: None,  # Pop Directional Isolate
    0x206A: None,  # Inhibit Symmetric Swapping
    0x206B: None,  # Activate Symmetric Swapping
    0x206E: None,  # National Digit Shapes
    0x206F: None,  # Nominal Digit Shapes
    0x3164: None,  # Hangul Filler
    0xFEFF: None,  # Zero Width No-Break Space
    0xFFA0: None,  # Halfwidth Hangul Filler
    0xFFFC: None,  # Object Replacement Character
    0xFFFE: None,  # Byte Order Mark
    0xFFFF: None,  # Non character
    0x1BCA0: None,  # Shorthand Format Letter Overlap
}
UNICODE_TO_REMOVE.update({char: None for char in range(0xE0000, 0xF8FF + 1)})  # Tag + PUA characters
UNICODE_TO_REMOVE.update({char: None for char in range(0xF0000, 0xFFFFF + 1)})  # PUA characters
UNICODE_TO_REMOVE.update({char: None for char in range(0x100000, 0x10FFFF + 1)})  # PUA characters
UNICODE_TO_REMOVE.update({char: None for char in range(0x1D100, 0x1D1FF + 1)})  # Musical symbols

UNICODE_TO_REPLACE = {
    0x2028: "\n",  # Line Separator
    0x2029: "\n\n",  # Paragraph Separator
    0x2000: " ",  # En Quad
    0x2001: " ",  # Em Quad
    0x2002: " ",  # En Space
    0x2003: " ",  # Em Space
    0x2004: " ",  # Three-Per-Em Space
    0x2005: " ",  # Four-Per-Em Space
    0x2006: " ",  # Six-Per-Em Space
    0x2007: " ",  # Figure Space
    0x2008: " ",  # Punctuation Space
    0x2009: " ",  # Thin Space
    0x200A: " ",  # Hair Space
    0x205F: " ",  # Medium Mathematical Space
    0x3000: " ",  # Ideographic Space
}


# The following characters are also invisible, but they should not be removed or replaced.
# Because they affect the meaning of the text. In this case, we don't need to do anything,
# but I just wrote this for documentation.

# UNICODE_TO_REMAIN = {
#     0x0020: " ",  # Space
#     0x0009: "\t",  # Horizontal Tab
#     0x000A: "\n",  # Line Feed
#     0x034F: "\u034F",  # Combining Grapheme Joiner
#     0x061C: "\u061C",  # Arabic Letter Mark
#     0x1680: "\u1680",  # Ogham Space Mark
#     0x17B4: "\u17B4",  # Khmer Vowel Inherent AQ
#     0x17B5: "\u17B5",  # Khmer Vowel Inherent AA
#     0x180B: "\u180B",  # Mongolian Free Variation Selector One
#     0x180C: "\u180C",  # Mongolian Free Variation Selector Two
#     0x180D: "\u180D",  # Mongolian Free Variation Selector Three
#     0x180E: "\u180E",  # Mongolian Vowel Separator
#     0x2800: "\u2800",  # Braille Pattern Blank
#     0x200C: "\u200C",  # Zero Width Non-Joiner
#     0x200D: "\u200D",  # Zero Width Joiner
#     0x2060: "\u2060",  # Word Joiner
#     0x206C: "\u206C,   # Inhibit Arabic Form Shaping
#     0x206D: "\u206D",  # Activate Arabic Form Shaping
#     0x1307B: "\U0001307B",  # Egyptian Hieroglyph Alef
# }
# UNICODE_TO_REMAIN.update({char: chr(char) for char in range(0x02B0, 0x02FF + 1)})  # Modifier letters
# UNICODE_TO_REMAIN.update({char: chr(char) for char in range(0x0300, 0x036F + 1)})  # Combining Diacritical Marks
# UNICODE_TO_REMAIN.update({char: chr(char) for char in range(0xFE00, 0xFE0F + 1)})  # Variation Selectors
# UNICODE_TO_REMAIN.update({char: chr(char) for char in range(0x1E0100, 0x1E01EF + 1)})  # Variation Selectors


def remove_invisible_chars(
    text: Union[str, List[str], Tuple[str]],
    num_workers: Union[int, str] = "auto",
) -> Union[str, List[str]]:
    """
    This removes invisible characters from text.

    Args:
        text (Union[str, List[str], Tuple[str]]): single text or list of texts
        num_workers (Union[int, str]): the number of multiprocessing workers

    Returns:
        Union[str, List[str]]: text with removed invisible characters or list of texts with removed invisible characters

    Examples:
        >>> from kss import Kss
        >>> remove_invisible_chars = Kss("remove_invisible_chars")
        >>> text = "안녕\u200b하세요"
        >>> remove_invisible_chars(text)
        '안녕하세요'
    """

    text, finish = _check_text(text)

    if finish:
        return text

    num_workers = _check_num_workers(text, num_workers)

    return _run_job(
        func=_remove_invisible_chars,
        inputs=text,
        num_workers=num_workers,
    )


def _remove_invisible_chars(text: str) -> str:
    text = text.translate(UNICODE_TO_REMOVE)
    text = text.translate(UNICODE_TO_REPLACE)
    return text

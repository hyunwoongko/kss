UNICODE_TO_REMOVE = {
    "\u0000": "",  # Null
    "\u0001": "",  # Start of Heading
    "\u0002": "",  # Start of Text
    "\u0003": "",  # End of Text
    "\u0004": "",  # End of Transmission
    "\u0005": "",  # Enquiry
    "\u0006": "",  # Acknowledge
    "\u0007": "",  # Bell
    "\u0008": "",  # Backspace
    "\u0009": "",  # Horizontal Tab
    "\u000B": "",  # Vertical Tab
    "\u000C": "",  # Form Feed
    "\u000D": "",  # Carriage Return
    "\u000E": "",  # Shift Out
    "\u000F": "",  # Shift In
    "\u0010": "",  # Data Link Escape
    "\u0011": "",  # Device Control 1
    "\u0012": "",  # Device Control 2
    "\u0013": "",  # Device Control 3
    "\u0014": "",  # Device Control 4
    "\u0015": "",  # Negative Acknowledge
    "\u0016": "",  # Synchronous Idle
    "\u0017": "",  # End of Transmission Block
    "\u0018": "",  # Cancel
    "\u0019": "",  # End of Medium
    "\u001A": "",  # Substitute
    "\u001B": "",  # Escape
    "\u001C": "",  # File Separator
    "\u001D": "",  # Group Separator
    "\u001E": "",  # Record Separator
    "\u001F": "",  # Unit Separator
    "\u007F": "",  # Delete
    "\u0080": "",  # Padding Character
    "\u0081": "",  # High Octet Preset
    "\u0082": "",  # Break Permitted Here
    "\u0083": "",  # No Break Here
    "\u0084": "",  # Index
    "\u0085": "",  # Next Line
    "\u0086": "",  # Start of Selected Area
    "\u0087": "",  # End of Selected Area
    "\u0088": "",  # Character Tabulation Set
    "\u0089": "",  # Character Tabulation with Justification
    "\u008A": "",  # Line Tabulation Set
    "\u008B": "",  # Partial Line Forward
    "\u008C": "",  # Partial Line Backward
    "\u008D": "",  # Reverse Line Feed
    "\u008E": "",  # Single-Shift Two
    "\u008F": "",  # Single-Shift Three
    "\u0090": "",  # Device Control String
    "\u0091": "",  # Private Use 1
    "\u0092": "",  # Private Use 2
    "\u0093": "",  # Set Transmit State
    "\u0094": "",  # Cancel Character
    "\u0095": "",  # Message Waiting
    "\u0096": "",  # Start of Guarded Area
    "\u0097": "",  # End of Guarded Area
    "\u0098": "",  # Start of String
    "\u0099": "",  # Single Graphic Character Introducer
    "\u009A": "",  # Single Character Introducer
    "\u009B": "",  # Control Sequence Introducer
    "\u009C": "",  # String Terminator
    "\u009D": "",  # Operating System Command
    "\u009E": "",  # Privacy Message
    "\u009F": "",  # Application Program Command
    "\u00A0": "",  # No-Break Space
    "\u00AD": "",  # Soft Hyphen
    "\u061C": "",  # Arabic Letter Mark
    "\u115f": "",  # Hangul Choseong Filler
    "\u1160": "",  # Hangul Jungseong Filler
    "\u1680": "",  # Ogham Space Mark
    "\u17B4": "",  # Khmer Vowel Inherent AQ
    "\u17B5": "",  # Khmer Vowel Inherent AA
    "\u180B": "",  # Mongolian Free Variation Selector One
    "\u180C": "",  # Mongolian Free Variation Selector Two
    "\u180D": "",  # Mongolian Free Variation Selector Three
    "\u180E": "",  # Mongolian Vowel Separator
    "\u2000": "",  # En Quad
    "\u2001": "",  # Em Quad
    "\u2002": "",  # En Space
    "\u2003": "",  # Em Space
    "\u2004": "",  # Three-Per-Em Space
    "\u2005": "",  # Four-Per-Em Space
    "\u2006": "",  # Six-Per-Em Space
    "\u2007": "",  # Figure Space
    "\u2008": "",  # Punctuation Space
    "\u2009": "",  # Thin Space
    "\u200A": "",  # Hair Space
    "\u200B": "",  # Zero Width Space
    "\u200C": "",  # Zero Width Non-Joiner
    "\u200D": "",  # Zero Width Joiner
    "\u200E": "",  # Left-to-Right Mark
    "\u200F": "",  # Right-to-Left Mark
    "\u202A": "",  # Left-to-Right Embedding
    "\u202B": "",  # Right-to-Left Embedding
    "\u202C": "",  # Pop Directional Formatting
    "\u202D": "",  # Left-to-Right Override
    "\u202E": "",  # Right-to-Left Override
    "\u202F": "",  # Narrow No-Break Space
    "\u2060": "",  # Word Joiner
    "\u2061": "",  # Function Application
    "\u2062": "",  # Invisible Times
    "\u2063": "",  # Invisible Separator
    "\u2064": "",  # Invisible Plus
    "\u2066": "",  # Left-to-Right Isolate
    "\u2067": "",  # Right-to-Left Isolate
    "\u2068": "",  # First Strong Isolate
    "\u2069": "",  # Pop Directional Isolate
    "\u206A": "",  # Inhibit Symmetric Swapping
    "\u206B": "",  # Activate Symmetric Swapping
    "\u206C": "",  # Inhibit Arabic Form Shaping
    "\u206D": "",  # Activate Arabic Form Shaping
    "\u206E": "",  # National Digit Shapes
    "\u206F": "",  # Nominal Digit Shapes
    "\u3164": "",  # Hangul Filler
    "\uFEFF": "",  # Zero Width No-Break Space
    "\uFFA0": "",  # Halfwidth Hangul Filler
    "\uFFFC": "",  # Object Replacement Character
    "\uFFFE": "",  # Byte Order Mark
    "\uFFFF": "",  # Non character
    "\U0001307B": "",  # Egyptian Hieroglyph Z015B
    "\U0001BCA0": "",  # Shorthand Format Letter Overlap
}
UNICODE_TO_REMOVE.update({chr(char): "" for char in range(0xE0000, 0xF8FF + 1)})  # Tag + PUA characters
UNICODE_TO_REMOVE.update({chr(char): "" for char in range(0xF0000, 0xFFFFF + 1)})  # PUA characters
UNICODE_TO_REMOVE.update({chr(char): "" for char in range(0x100000, 0x10FFFF + 1)})  # PUA characters
UNICODE_TO_REMOVE.update({chr(char): "" for char in range(0x1D100, 0x1D1FF + 1)})  # Musical symbols

TO_REPLACE = {
    "\u0020": " ",  # Space
    "\u0009": "\t",  # Horizontal Tab
    "\u000A": "\n",  # Line Feed
    "\u034F": "\u034F",  # Combining Grapheme Joiner
    "\u2028": "\n",  # Line Separator
    "\u2029": "\n\n",  # Paragraph Separator
    "\u2000": " ",  # En Quad
    "\u2001": " ",  # Em Quad
    "\u2002": " ",  # En Space
    "\u2003": " ",  # Em Space
    "\u2004": " ",  # Three-Per-Em Space
    "\u2005": " ",  # Four-Per-Em Space
    "\u2006": " ",  # Six-Per-Em Space
    "\u2007": " ",  # Figure Space
    "\u2008": " ",  # Punctuation Space
    "\u2009": " ",  # Thin Space
    "\u200A": " ",  # Hair Space
    "\u205F": " ",  # Medium Mathematical Space
    "\u3000": " ",  # Ideographic Space
    "\u2800": "\u2800",  # Braille Pattern Blank
    "\u200D": "\u200D",  # Zero Width Joiner
}
# TO_REPLACE.update({chr(char): chr(char) for char in range(0x02B0, 0x02FF + 1)})  # Modifier letters
# TO_REPLACE.update({chr(char): chr(char) for char in range(0x0300, 0x036F + 1)})  # Combining Diacritical Marks
# TO_REPLACE.update({chr(char): chr(char) for char in range(0xFE00, 0xFE0F + 1)})  # Variation Selectors
# TO_REPLACE.update({chr(char): chr(char) for char in range(0x1E0100, 0x1E01EF + 1)})  # Variation Selectors

if __name__ == '__main__':
    text = "string\u0000\u0001\u0002\u0003\u0004\u0005\u0006\u0007\u0008\u0009\u000B\u000C\u000D\u000E\u000F\u0010\u0011\u0012\u0013\u0014\u0015\u0016\u0017\u0018\u0019\u001A\u001B\u001C\u001D\u001E\u001F\u007F\u0080\u0081\u0082\u0083\u0084\u0085\u0086\u0087\u0088\u0089\u008A\u008B\u008C\u008D\u008E\u008F\u0090\u0091\u0092\u0093\u0094\u0095\u0096\u0097\u0098\u0099\u009A\u009B\u009C\u009D\u009E\u009F\u00A0\u00AD\u061C\u115f\u1160\u1680\u17B4\u17B5\u180B\u180C\u180D\u180E\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u200B\u200C\u200D\u200E\u200F\u202A\u202B\u202C\u202D\u202E\u202F\u2060\u2061\u2062\u2063\u2064\u2066\u2067\u2068\u2069\u206A\u206B\u206C\u206D\u206E\u206F\u3164\uFEFF\uFFA0\uFFFC\uFFFE\uFFFF\U0001307B\U0001BCA0"
    text += "".join(chr(char) for char in range(0xE0000, 0xF8FF + 1))  # Tag + PUA characters
    text += "".join(chr(char) for char in range(0xF0000, 0xFFFFF + 1))  # PUA characters
    text += "".join(chr(char) for char in range(0x100000, 0x10FFFF + 1))  # PUA characters
    text += "".join(chr(char) for char in range(0x1D100, 0x1D1FF + 1))  # Musical symbols
    text += "\u0020\u0009\u000A\u034F\u2028\u2029\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u205F\u3000\u2800\u200D"
    print(len(text))
    print(text)
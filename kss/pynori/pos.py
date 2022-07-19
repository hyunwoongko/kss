class POS(object):
    """
    Part of speech classification for Korean based on Sejong corpus classification.
    The list of tags and their meanings is available here:
    https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY
    """

    class Type(object):
        MORPHEME = "MORP"  # A simple morpheme
        COMPOUND = "COMP"  # Compound noun
        INFLECT = "INFL"  # Inflected token
        PREANALYSIS = "PREANY"  # Pre-analysis token

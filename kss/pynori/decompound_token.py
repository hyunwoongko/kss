from kss.pynori.token import Token


class DecompoundToken(Token):
    """
    A token that was generated from a compound
    """

    def __init__(self, posTag, surfaceForm, startOffset, endOffset, posType, dictType):

        super().__init__(
            surfaceForm,
            0,
            len(surfaceForm),
            startOffset,
            endOffset,
            posType,
            None,
            posTag,
            dictType,
        )

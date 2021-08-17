from kss.pynori.token import Token


class DictionaryToken(Token):
    """
    Dictionary interface for retrieving morphological data by id
    """

    def __init__(
        self,
        dictType,
        dictionary,
        wordId,
        surfaceForm,
        offset,
        length,
        startOffset,
        endOffset,
        posType,
        morphemes,
        posTag,
    ):
        super().__init__(
            surfaceForm,
            offset,
            length,
            startOffset,
            endOffset,
            posType,
            morphemes,
            posTag,
            dictType,
        )
        self.dictType = dictType  # KoreanTokenizer.Type type
        self.dictionary = dictionary
        self.wordId = wordId

    def getType(self):
        return self.dictType

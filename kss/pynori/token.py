class Token(object):
    """
    Dictionary interface for retrieving morphological data by id
    """

    def __init__(
        self,
        surfaceForm,
        offset,
        length,
        startOffset,
        endOffset,
        posType,
        morphemes,
        posTag,
        dictType,
    ):
        self.surfaceForm = surfaceForm
        self.offset = offset
        self.length = length
        self.startOffset = startOffset
        self.endOffset = endOffset
        self.posType = posType
        self.morphemes = morphemes
        self.posTag = posTag
        self.dictType = dictType
        self.posIncr = 1
        self.posLen = 1

    def getSurfaceForm(self):
        """return surfaceForm"""
        return self.surfaceForm

    def getOffset(self):
        """return offset into surfaceForm"""
        return self.offset

    def getLength(self):
        """return length of surfaceForm"""
        return self.length

    def getSurfaceFormString(self):
        """return surfaceForm as a String"""
        return self.surfaceForm

    def getPOSType(self):
        """Get the {@link POS.Type} of the token."""
        return self.posType

    def setPOSType(self, pos_type):
        self.posType = pos_type

    def getPOSTag(self):
        return self.posTag

    def getDictType(self):
        return self.dictType

    def getLeftPOS(self):
        """Get the left part of speech of the token."""
        raise NotImplementedError("The method not implemented")

    def getRightPOS(self):
        """Get the right part of speech of the token."""
        raise NotImplementedError("The method not implemented")

    def getReading(self):
        """Get the reading of the token."""
        raise NotImplementedError("The method not implemented")

    def getMorphemes(self):
        """Get the {@link Morpheme} decomposition of the token."""
        return self.morphemes

    def getStartOffset(self):
        """Get the start offset of the term in the analyzed text."""
        return self.startOffset

    def getEndOffset(self):
        """Get the end offset of the term in the analyzed text."""
        return self.endOffset

    def setPositionIncrement(self, posIncr):
        self.posIncr = posIncr

    def getPositionIncrement(self):
        return self.posIncr

    def setPositionLength(self, posLen):
        self.posLen = posLen

    def getPositionLength(self):
        return self.posLen

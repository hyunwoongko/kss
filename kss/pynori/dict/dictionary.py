class Dictionary(object):
    class Morpheme(object):
        """A morpheme extracted from a compound token."""

        def __init__(self, posTag, surfaceForm):
            self.posTag = posTag
            self.surfaceForm = surfaceForm

from kss.pynori.korean_posstop_filter import KoreanPOSStopFilter
from kss.pynori.korean_tokenizer import KoreanTokenizer
from kss.pynori.korean_tokenizer import Type
from kss.pynori.post_processing import PostProcessing
from kss.pynori.synonym_graph_filter import SynonymGraphFilter


class KoreanAnalyzer(object):
    """Analyzer for Korean text, composed of Pre-/Post-processors, Filters, and Tokenizers.

    KoreanAnalyzer - Users only need to initialize this object.
    Basic only use tokenizer.
    Advanced constructs pipeline that consists of Pre-/Post-processors, Filters, and Tokenizers.
    The order of the pipeline is important.
    """

    def __init__(
        self,
        path_userdict="/resources/userdict.txt",
        decompound_mode="NONE",
        infl_decompound_mode="NONE",
        output_unknown_unigrams=False,
        discard_punctuation=False,
        pos_filter=False,
        stop_tags=KoreanPOSStopFilter.DEFAULT_STOP_TAGS,
        synonym_filter=False,
        mode_synonym=False,
    ):
        self.post_processor = PostProcessing()
        self.kor_tokenizer = KoreanTokenizer(
            path_userdict,
            decompound_mode,
            infl_decompound_mode,
            output_unknown_unigrams,
            discard_punctuation,
        )
        self.pos_filter = pos_filter
        self.kor_pos_filter = KoreanPOSStopFilter(stop_tags=stop_tags)
        self.synonym_filter = synonym_filter
        self.mode_synonym = mode_synonym
        self.syn_graph_filter = None

        # SynonymGraphFilter 초기화 처리 지연 시간으로 True일 때만 활성.
        if self.synonym_filter:
            self.syn_graph_filter = SynonymGraphFilter(
                kor_tokenizer=self.kor_tokenizer,
                mode_synonym=self.mode_synonym,
            )

    def do_analysis(self, in_string, preprocessed: bool):
        """Analyze text input string and return tokens

        Filtering 순서에 유의. (POS -> SYNONYM)
        """
        if not isinstance(in_string, str):
            raise ValueError(f"the input type must be {type('')}")

        self.kor_tokenizer.set_input(
            in_string,
            preprocessed=preprocessed,
        )

        while self.kor_tokenizer.increment_token():
            pass
        tkn_attr_obj = self.kor_tokenizer.tkn_attr_obj

        if self.pos_filter:
            tkn_attr_obj = self.kor_pos_filter.do_filter(tkn_attr_obj)

        if self.synonym_filter:
            tkn_attr_obj = self.syn_graph_filter.do_filter(tkn_attr_obj)

        MIN_CHAR_LENGTH = 7
        if (
            len(tkn_attr_obj.termAtt) == 1
            and tkn_attr_obj.dictTypeAtt[0] == Type.UNKNOWN
            and len(tkn_attr_obj.termAtt[0]) >= MIN_CHAR_LENGTH
        ):
            tkn_attr_obj = self.post_processor.relax_long_unk(
                tkn_attr_obj, self.kor_tokenizer
            )

        return tkn_attr_obj.__dict__

    def set_option_tokenizer(
        self,
        decompound_mode=None,
        infl_decompound_mode=None,
        output_unknown_unigrams=None,
        discard_punctuation=None,
    ):
        if decompound_mode is not None:
            self.kor_tokenizer.mode = decompound_mode
        if infl_decompound_mode is not None:
            self.kor_tokenizer.infl_mode = infl_decompound_mode
        if output_unknown_unigrams is not None:
            self.kor_tokenizer.output_unknown_unigrams = output_unknown_unigrams
        if discard_punctuation is not None:
            self.kor_tokenizer.discard_punctuation = discard_punctuation

    def set_option_filter(
        self,
        pos_filter=None,
        stop_tags=None,
        synonym_filter=None,
        mode_synonym=None,
    ):
        if pos_filter is not None:
            self.pos_filter = pos_filter
        if stop_tags is not None:
            self.kor_pos_filter.stop_tags = stop_tags
            if synonym_filter is not None or mode_synonym is not None:
                if self.synonym_filter or synonym_filter:
                    self.syn_graph_filter = SynonymGraphFilter(
                        kor_tokenizer=self.kor_tokenizer,
                        mode_synonym=mode_synonym,
                    )
            if mode_synonym is not None:
                self.mode_synonym = mode_synonym
            if synonym_filter is not None:
                self.synonym_filter = synonym_filter

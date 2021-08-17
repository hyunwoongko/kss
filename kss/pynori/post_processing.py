from kss.pynori.token_attribute import TokenAttribute
from kss.pynori.pos import POS
from kss.pynori.korean_tokenizer import Type


class PostProcessing(object):
    @staticmethod
    def _init_unk_token_attribute(ternAtt, offsetAtt):
        unk_x = TokenAttribute()
        unk_x.termAtt = [ternAtt]
        unk_x.offsetAtt = [offsetAtt]
        unk_x.posLengthAtt = [1]
        unk_x.posTypeAtt = [POS.Type.MORPHEME]
        unk_x.posTagAtt = ["UNKNOWN"]
        unk_x.dictTypeAtt = [Type.UNKNOWN]
        return unk_x

    @staticmethod
    def _merge_token_attribute(source, target):
        """source token attribute를
        target token attribute에 append한다.
        """
        for name, _ in target.__dict__.items():
            target.__dict__[name] += source.__dict__[name]
        return target

    def relax_long_unk(self, tkn_attr_obj, kor_tokenizer):
        long_unknown_token = tkn_attr_obj.termAtt[0]

        idx = -1
        for i, ch in enumerate(long_unknown_token):
            if i == 0:
                pch = ch
            if ch != pch:
                idx = i
                break

        if idx == -1:
            return tkn_attr_obj

        front_string = long_unknown_token[:idx]
        rest_string = long_unknown_token[idx:]

        front_tkn_attr = self._init_unk_token_attribute(
            ternAtt=front_string,
            offsetAtt=(0, len(front_string) - 1),
        )

        kor_tokenizer.set_input(rest_string)
        while kor_tokenizer.increment_token():
            pass
        rest_tkn_attr = kor_tokenizer.tkn_attr_obj

        return self._merge_token_attribute(
            source=rest_tkn_attr,
            target=front_tkn_attr,
        )

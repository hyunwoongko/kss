# Korean Sentence Splitter
# Split Korean text into sentences using heuristic algorithm.
#
# Copyright (C) 2021 Hyun-woong Ko <kevin.woong@kakaobrain.com> and Sang-Kil Park <skpark1224@hyundai.com>
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from kss.kss import split_sentences, split_chunks

__ALL__ = [split_sentences, split_chunks]

import math

import pandas as pd

a = pd.read_csv('ai.tsv', sep="\t").values.tolist()
one = [1, '강남역 맛집으로 소문난 강남 토끼정에 다녀왔습니다.', '강남역 맛집으로 소문난 강남 토끼정에 다녀왔습니다.', '강남역 맛집으로 소문난 강남 토끼정에 다녀왔습니다.']


for i in a:
    val = i[3]
    if isinstance(val, str):
        print(val)
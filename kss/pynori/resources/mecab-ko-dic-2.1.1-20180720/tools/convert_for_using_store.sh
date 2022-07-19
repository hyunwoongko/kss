#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# ']' 품사 변경
#
# 보통의 상품 검색에서는 '[', ']'가 특수한 용도로 사용된다.
# 예를 들면 다음과 같다.
# [강조 문장] 상품명
# [흡연자의 필수품] 에어 워셔
# [고화질] 만화책
# 때문에 Symbol.csv의 ']'의 품사를 SF로 변경한다.

old_symbol_file=$DIR/../Symbol.csv.org
symbol_file=$DIR/../Symbol.csv
cp -f $symbol_file $old_symbol_file

sf_line=`grep -E "^\.,[0-9]+,[0-9]+,[-0-9]+,SF," $old_symbol_file`
left_id=`echo $sf_line | cut -d ',' -f 2`
right_id=`echo $sf_line | cut -d ',' -f 3`
sed -i -re "s/(^\],)([0-9]+),([0-9]+),([-0-9]+),SSC(,.*)/\\1$left_id,$right_id,\\4,SF\\5/g" $symbol_file

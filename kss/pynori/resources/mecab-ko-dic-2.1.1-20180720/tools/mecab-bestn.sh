#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR
#mecab -d $DIR/../ -F "%m\t%f[0],%f[1],%phl,%phr,%pb,%pw,%pC,%pc,%pn\n" -N5
echo "#표현층,품사,의미부류,좌문맥ID,우문맥ID,낱말비용,연접비용,누적비용"
echo ""
mecab -d $DIR/../ -F"%m\t%f[0],%f[1],%phl,%phr,%pw,%pC,%pc\n" -N10
#   %m : 표현층
#   %f[0] : 품사
#   %f[1] : 의미부류
#   %phl : 좌문맥ID
#   %phr: 우문맥ID
#   %pw: 낱말 비용
#   %pC: 이전 형태소와의 연접비용
#   %pc: 연접비용 + 낱말 비용(누적)

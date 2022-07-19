#!/bin/sh
# http://xpt.sourceforge.net/techdocs/nix/tool/make/mk07-Commandautogenconfigure/ar01s02.html 참조

rm -f config.cache

if [ -d m4 ]; then
        echo "Looking in m4 directory for macros."
        aclocal -I m4
else
        echo "Looking in current directory for macros."
        aclocal -I .
        fi

autoconf
automake -a
exit

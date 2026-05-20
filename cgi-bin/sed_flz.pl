#!/bin/sh

for flz in *.cgi; do
#  sed -e 's/ffl_2008/ffl_2009/g' $flz > $flz.tmp
  sed -e 's/select player=/select name=/g' $flz > $flz.tmp
  cp $flz.tmp $flz
done


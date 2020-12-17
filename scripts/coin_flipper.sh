#!/bin/bash


for i in {0..2}
do
  SUM=0
  for j in {0..2}
  do
    TEMP=$(echo "$RANDOM % 2" | bc)
    SUM1=$(echo "$SUM + $TEMP" | bc)
    SUM=$SUM1
  done
  if [ $SUM -gt 1 ]; then
    echo "Series $i - True!"
  else
    echo "Series $i - FALSE!"
  fi
done


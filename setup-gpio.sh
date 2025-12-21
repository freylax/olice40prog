#!/bin/bash
# on the rpi5 we have to find out the gpio number
# which corresponds to GPIO24 pin
# we write this to the file gpio24
# save the path
CWD=$(pwd)
# go to the directory where this source file is located
DIR=$(dirname "$0")

sudo cat /sys/kernel/debug/gpio | grep GPIO24 | sed -r 's/ *gpio-([0-9]+).*$/\1/' > $DIR/gpio24
# create the files for communicate with 'gpio24'
cat $DIR/gpio24 > /sys/class/gpio/export





#!/bin/bash
# set gpio24 to in (normal/read) or out (write) mode
DIR=$(dirname "$0")
echo $1 > /sys/class/gpio/gpio$(cat $DIR/gpio24)/direction

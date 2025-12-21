#!/bin/bash
# write the argument image to olimex hx8k flash content
# execute only after setup-gpio.sh has been run once after sysstart
DIR=$(dirname "$0")
$DIR/bitgen.sh $1 $1.image
$DIR/set-gpio-dir.sh out
sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=10000 -w $1.image
$DIR/set-gpio-dir.sh in

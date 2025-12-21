#!/bin/bash

# reads olimex hx8k flash content to file argument
# execute only after setup-gpio.sh
DIR=$(dirname "$0")
$DIR/set-gpio-dir.sh in
sudo flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=10000 -r $1

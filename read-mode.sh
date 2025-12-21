#!/bin/bash
# set to normal (read) mode
echo in > /sys/class/gpio/gpio$(cat gpio24)/direction

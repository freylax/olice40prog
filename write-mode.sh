#!/bin/bash
# prepare for write
echo out > /sys/class/gpio/gpio$(cat gpio24)/direction

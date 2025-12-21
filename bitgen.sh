#!/bin/bash
# $1 = bin file $2 = image file
# pad bitstream till 2MB
dd if=/dev/zero of=$2 bs=2M count=1
dd if=$1 of=$2 conv=notrunc

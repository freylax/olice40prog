#!/usr/bin/env python3

import argparse
import os
import sys
import subprocess
import gpiod

from gpiod.line import Direction


def set_to_dir(chip_path, line_offset, dir):
    # request the line initially as an input
    with gpiod.request_lines(
        chip_path,
        consumer="reconfigure-input-to-output",
        config={line_offset: gpiod.LineSettings(direction=dir)},
    ) as request:
        # read the current line value
        value = request.get_value(line_offset)
        # print("{}={} ({})".format(line_offset, value, dir))


parser = argparse.ArgumentParser(
    prog="spiflash", description="flash a given binary file to olimex ice40hx fpga"
)
parser.add_argument(
    "-b",
    "--binaryfile",
    help="the file to flash, if not present then print the flash name and size",
)
parser.add_argument(
    "-d",
    "--dev",
    help="the spi device to use, default is /dev/spidev0.0",
    default="/dev/spidev0.0",
)
parser.add_argument(
    "-s", "--speed", help="spi speed in Hz, default is 10000", default="10000"
)
parser.add_argument(
    "-f", "--flashsize", help="flashsize, if not given query the chip", type=int
)
parser.add_argument(
    "-i",
    "--imagefile",
    help="imagefile, get the filename contens padded to flashsize. Will be overwritten if exists. If not given append .img to filename and use this.",
)
parser.add_argument(
    "-g",
    "--gpioline",
    help="the gpioline to use, default is /dev/gpiochip0",
    default="/dev/gpiochip0",
)
parser.add_argument(
    "-r",
    "--resetpin",
    help="the gpio pin which drives the fpga reset, default is 24",
    default=24,
    type=int,
)
args = parser.parse_args()
fr_cmd = ["flashrom", "-p", f"linux_spi:dev={args.dev},spispeed={args.speed}"]

filesize = 0
if args.binaryfile:
    # try to open the file
    if not os.access(args.binaryfile, os.R_OK):
        sys.exit(f"could not access:{args.binaryfile}")
    # get the size of the file
    filesize = os.stat(args.binaryfile).st_size
    if filesize == 0:
        sys.exit(f"empty file:{args.binaryfile}")

set_to_dir(args.gpioline, args.resetpin, Direction.OUTPUT)
try:
    # get the flashsize
    flashsize = 0
    if args.flashsize:
        flashsize = args.flashsize
    else:
        try:
            res = subprocess.run(
                fr_cmd + ["--flash-size"], check=True, capture_output=True, text=True
            )
            flashsize = int(res.stdout.splitlines()[-1])
            if flashsize == 0:
                sys.exit("flashsize is zero")
        except subprocess.CalledProcessError as err:
            print(err.stdout)
            print(err.stderr)
            exit(1)
    # check flash and file sizes
    if filesize > flashsize:
        sys.exit(
            f"filesize ({filesize}) is {filesize - flashsize} bytes larger than flashsize ({flashsize})"
        )
    # the image file
    imagefile = None
    if args.imagefile:
        imagefile = args.imagefile
    elif args.binaryfile:
        imagefile = args.binaryfile + ".img"
    if imagefile and args.binaryfile:
        subprocess.run(
            ["dd", "if=/dev/zero", f"of={imagefile}", f"bs={flashsize}", "count=1"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["dd", f"if={args.binaryfile}", "conv=notrunc", f"of={imagefile}"],
            check=True,
            capture_output=True,
        )
        print(
            f"created imagefile {imagefile}\nfilesize={filesize},flashsize={flashsize},used {filesize * 100.0 / flashsize:.2f}% "
        )
    # get the flash name and vendor
    try:
        res = subprocess.run(
            fr_cmd + ["--flash-name"], check=True, capture_output=True, text=True
        )
        _, flash_vendor, _, flash_name = res.stdout.splitlines()[-1].split('"')[:4]
        print(f"vendor={flash_vendor},name={flash_name}")
    except subprocess.CalledProcessError as err:
        print(err.stdout)
        print(err.stderr)
        exit(1)
    
    if args.binaryfile:
        # flash the file
        try:
            res = subprocess.run(
                fr_cmd + ["-w", imagefile], check=True, capture_output=True, text=True
            )
            print(res.stdout.splitlines()[-1])
        except subprocess.CalledProcessError as err:
            print(err.stdout)
            print(err.stderr)
            exit(1)
    else:
        print(f"flashsize={flashsize}")
finally:
    set_to_dir(args.gpioline, args.resetpin, Direction.INPUT)

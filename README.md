# olice40prog
Python script to flash a binary file to ice40 fpga
using spi device of an single board computer.

The ice40 fpga uses an CRESET pin to know if the spi data
is for programming the chip or for normal operation.
The script drives this CRESET pin using a connected GPIO pin,
for example gpio24, the default setting.

## Usage
```
usage: spiflash [-h] [-b BINARYFILE] [-d DEV] [-s SPEED] [-f FLASHSIZE] [-i IMAGEFILE]
                [-g GPIOLINE] [-r RESETPIN]

flash a given binary file to olimex ice40hx fpga

options:
  -h, --help            show this help message and exit
  -b, --binaryfile BINARYFILE
                        the file to flash, if not present then print the flash name and size
  -d, --dev DEV         the spi device to use, default is /dev/spidev0.0
  -s, --speed SPEED     spi speed in Hz, default is 10000
  -f, --flashsize FLASHSIZE
                        flashsize, if not given query the chip
  -i, --imagefile IMAGEFILE
                        imagefile, get the filename contens padded to flashsize. Will be
                        overwritten if exists. If not given append .img to filename and
                        use this.
  -g, --gpioline GPIOLINE
                        the gpioline to use, default is /dev/gpiochip0
  -r, --resetpin RESETPIN
                        the gpio pin which drives the fpga reset, default is 24
```
If using the defaults then just use this to flash:
```
./spiflash.py -b <BINARYFILE>
```

The script uses [flashrom](https://github.com/flashrom/flashrom)
for flashing. A recent version has to be installed:

## Installing a recent flashrom

```
sudo apt remove flashrom
cd ~/prog
git clone https://github.com/flashrom/flashrom
cd flashrom
sudo apt install meson
meson setup builddir
meson compile -C builddir
meson test -C builddir
meson install -C builddir
```

## Example Connection for Olimex ICE40HX8K-EVB and RPI4/5

```
RPI4/5 pinout
 +-----------------------------------+
 | IP                  HDMI   PWR    |
 |                                   |
 |                                   |
 | USB                               | 
 |                                   |
 |         39...................1    |
 | USB     40...................2    |
 +-----------------------------------+


ICE40-EVB programming connector (UEXT) pinout
and uext cable               
                             | 1  3.3V 
 +-----+   +------------+    | 2  GND
 |10 9 |   |SS_B     SCK|    | 3  RxD
 | 8 7 |   |SDO      SDI|    | 4  TxD
 | 6 5     |CRESET CDONE     | 5  CDONE
 | 4 3 |   |TxD      RxD|    | 6  CRESET
 | 2 1 |   |GND     3.3V|    | 7  SDI
 +-----+   +------------+    | 8  SDO
                             | 9  SCK
                             |10  SS_B
                             

| RPI4/5|        | ICE40-EVB |            |
|-------+--------+-----------+------------+
|    17 | 3v3    |         1 | 3v3        |
|    18 | gpio24 |         6 | creset     | 
|    19 | mosi   |         8 | sdo        | 
|    20 | gnd    |         2 | gnd        | 
|    21 | miso   |         7 | sdi        | 
|    22 | gpio25 |         5 | cdone      |  
|    23 | clk    |         9 | sck        |  
|    24 | ce0    |        10 | #cd = ss_b | 
```

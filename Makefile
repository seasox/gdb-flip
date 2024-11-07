flip: test
	gdb -x bitflip.py --batch -ex "bitflip_wrapper ./test test.c 6 x 1"

test: test.c
	cc -g -o test test.c

all: test

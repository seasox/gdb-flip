# GDB-Flip

This is a simple tool to programatically cause bitflips in a target binary.

## Setup

To test your setup, run `make flip`. This should build the `test` binary and flip varaible `x` in `main.c` at bit position `1`. The expected output is:

```
$ make flip
gdb -x bitflip.py --batch -ex "bitflip_wrapper ./test test.c 6 x 1"
Breakpoint 1 at 0x1190: file test.c, line 6.
Comparing x against known value... failed! Expected 20, got 22
[Inferior 1 (process 6511) exited with code 0377]
Breakpoint set at 'test.c:6' to flip bit 1 of 'x'
Flipped bit 1 in 'x'; new value: 2
```

## Usage

Load `bitflip.py` as a GDB module and run the `bitflip_wrapper` with your target binary, file, line, variable, and bit position as arguments:

```
gdb -x bitflip.py --batch -ex "bitflip_wrapper [TARGET_BINARY] [FILE] [LINE] [VARIABLE] [BITPOS]"
```

As an example, consider we want to flip bit `42` in a variable called `current` when the 
execution of `~/sphincsplus/ref/test/fors` hits line `48` in file `utilsx1.c`, the corresponding GDB-Flip call would be:

```
gdb -x bitflip.py --batch -ex "bitflip_wrapper ~/sphincsplus/ref/test/fors utilsx1.c 48 current 42"
```

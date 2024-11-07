# GDB-Flip

This is a simple tool to programatically cause bitflips in a target binary.

## Setup

To test your setup, run `make flip`. This should build the `test` binary and flip varaible `x` in `main.c` at bit position `1`.

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

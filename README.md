# GDB-Flip

This is a simple tool to programmatically cause bitflips in a target binary.

## Setup

To test your setup, run `make flip`. This should build the `test` binary and flip variable `x` in `main.c` at bit position `1`. The expected output is:

```
$ make flip
gdb -x bitflip.py --batch -ex "bitflip_wrapper ./test test.c 6 x 1"
Breakpoint 1 at 0x1190: file test.c, line 6.
Breakpoint set at 'test.c:6' to flip bit 1 of 'x'
Comparing x against known value... failed! Expected 20, got 22
[Inferior 1 (process 37892) exited with code 0377]
Flipped bit 1 in 'x'; new value: 2
```

## Usage

## Interactive use

Start gdb with `bitflip.py` loaded as a module:

```
$ gdb -x bitflip.py
```

Then start the target binary using the `bitflip_wrapper`:

```
bitflip_wrapper [TARGET_BINARY] [FILE] [LINE] [VARIABLE] [BITPOS]
```

As an example, consider we want to flip bit `42` in a variable called `current` when the 
execution of `~/sphincsplus/ref/test/fors` hits line `48` in file `utilsx1.c`, the corresponding GDB-Flip call would be:

```
(gdb) bitflip_wrapper ~/sphincsplus/ref/test/fors utilsx1.c 48 current 42
```

You can also use `bitflip` directly to add multiple bitflip positions in your program execution:

```
(gdb) file ~/sphincsplus/ref/test/fors
(gdb) bitflip utilsx1.c 48 current 42
(gdb) bitflip utilsx1.c 59 current 123
(gdb) run
```

## Non-interactive use

Load `bitflip.py` as a GDB module and run the `bitflip_wrapper` with your target binary, file, line, variable, and bit position as arguments in `batch` mode:

```
$ gdb -x bitflip.py --batch -ex "bitflip_wrapper [TARGET_BINARY] [FILE] [LINE] [VARIABLE] [BITPOS]"
```

As an example, consider we want to flip bit `42` in a variable called `current` when the 
execution of `~/sphincsplus/ref/test/fors` hits line `48` in file `utilsx1.c`, the corresponding GDB-Flip call would be:

```
$ gdb -x bitflip.py --batch -ex "bitflip_wrapper ~/sphincsplus/ref/test/fors utilsx1.c 48 current 42"
```

# LALU

A programmable 16-bit Arithmetic Logic Unit with support for addition and subtraction, built in Logisim. This was made as part of the spring project for Digital Electronics ([course overview](https://docs.google.com/presentation/d/13zvvAOJ44Jc9marU6MsldvEOEcPNYqvOwxIgNdA3xcI/pub?start=true&loop=true&delayms=5000&slide=id.g195ddaefc5_0_0)), a [LASA {CS}](https://lasacs.com) course.

## Features

- 16-bit adder/subtractor
- Four general purpose registers and a program counter (PC) and instruction register (IR)
- Support for writing custom programs via a custom assembly language
- Simple program performance benchmarking via a cycle counter

## Examples

There are example programs in the `programs/` directory. Compile a program to binary format using the provided assembler:

```
cd assembler
nix develop -c python assembler.py path/to/file.txt
```

Load the displayed instructions into the program memory and fill the RAM if necessary.

### Fibonacci

A video demonstrating using LALU to calculate the Fibonacci sequence up to $F_8$:

https://github.com/user-attachments/assets/8a5e6e0f-b0f0-4695-a126-7d562afc3774

`0x15 = 21` and $F_8 = 21$

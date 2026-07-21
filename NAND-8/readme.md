# INTRO
> Since, I have been learning about how computers work, and made several efforts to emulate some basic behaviours of it like atleast the ALU using the NAND gates. Since NAND and NOR gates are universal, theoratically it could make an entire computer.

> And thus here I am, original idea was just a plain 8 bit adder but then i expanded it more and more slowly(even though it took only 3 days). I now think that this new intrest of mine deserves some more nice projects, so I added this to my new repo here i will mostly make emulators.

# PROPERTIES OF THIS EMULATOR
- This emulator has a 8 bit ALU made entirely from NAND Gate only.
- It has 16 registers with single write and dual read in a single clock.
- It has total of 16 operations including 8 of arithmetic and logical and other 8 of I/O and conditions and branching.
- Technically program memory is as much as a python int can hold, but since program arguments will be 8 bit maximum 256 instructions is recommended for it to avoid major bugs.
- To compile the costum ISO it also has a small assembler which directly gives the instructions set as output.
- It  has 256 slots of RAM that can be read and wrote to anytime with a pointer adress, out of this from 243 onward slots are reserved for I/O.
- Memory mapped I/O is used, it has access to many input and output devices such as a 255x255 pixel greyscale display, keyboard, mouse(both input and output), RNG, and time.




# ISO

## Overview

NAND-8 is an 8-bit load/store architecture with:

* 16 general-purpose registers (`R0`-`R15`)
* 256 bytes of RAM
* 16-bit instructions
* Four status flags:

  * **N** - Negative
  * **Z** - Zero
  * **C** - Carry
  * **V** - Overflow

Registers store 8-bit values.

---
# Registers
```
R0
R1
R2
...
upto r15
```
Any register may be used for arithmetic, memory addressing, or temporary storage.
---

# Program Structure

Comments begin with `;` or `#`.

```
# This is a comment
; This is also a comment
```

Labels end with `:`.

```
loop:
```

Jump instructions may target labels only

```
jump loop
jump 25 #wrong
```

---

# Instruction Set

## PASS

Copies one register into another.

```
pass Rd Rs
```

Operation:

```
Rd = Rs
```
>Note: it will update flags
---

## LDI

Loads an immediate value.

```
ldi Rd value
```

Example:

```
ldi r3 42
```
Operation:

```
r3=42
```

---

## ADD

Adds two registers.

```
add Rd Ra Rb
```

Operation:

```
Rd = Ra + Rb
```

Flags updated.

---

## SUB

Subtracts two registers.

```
sub Rd Ra Rb
```

Operation:

```
Rd = Ra - Rb
```

Flags updated.

---

## CMP

Compares two registers.

```
cmp Ra Rb
```

Operation:

```
Ra - Rb
```

The result is discarded.

Only the flags are updated.

---

## NAND

```
nand Rd Ra Rb
```

Bitwise NAND.

>Note: it will update flags
---

## NOR

```
nor Rd Ra Rb
```

Bitwise NOR.

>Note: it will update flags
---

## XOR

```
xor Rd Ra Rb
```

Bitwise XOR.

>Note: it will update flags
---

## SHL

Logical left shift.

```
shl Rd Ra
```

Operation:

```
Rd = Ra << 1
```
>Note: it will update flags
---

## SHR

Logical right shift.

```
shr Rd Ra
```

Operation:

```
Rd = Ra >> 1
```
>Note: it will update flags
---

## STORE

Stores a register into memory.

```
store Ra Rs
```

Operation:

```
MEM[Ra] = Rs
```

The value inside `Ra` is used as the memory address.

Example:

```
ldi r1 20
ldi r2 99

store r1 r2
```

Result:

```
MEM[20] = 99
```

---

## LOAD

Loads from memory.

```
load Rd Ra
```

Operation:

```
Rd = MEM[Ra]
```

Example:

```
ldi r1 20
load r2 r1
```

Result:

```
R2 = MEM[20]
```

---

## DISPLAY

Prints a register.

```
display Ra
```

Example:

```
display r3
```

---

## JUMP

Unconditional jump.

```
jump label
```

Example:

```
jump loop
```

---

## JC

Conditional jump.

```
jc N label
jc Z label
jc C label
jc V label
```

The jump occurs only if the selected flag is set.

Example:

```
cmp r1 r2
jc Z equal
```

---

## HALT

Stops program execution.

```
halt
```

---

# Flags

## Z (Zero)

Set when the result equals zero.

---

## N (Negative)

Set when the result is negative (two's complement).

---

## C (Carry)

Set when an addition generates a carry or a subtraction produces a borrow, depending on the operation.

---

## V (Overflow)

Set when signed arithmetic overflows.

---


# MEMORY MAPPING

| Memory Address | Description | Details | supports read and write?|
|---------------:|-------------|---------|-------------------------|
| 243 | Color | Grayscale value to write to the display | write |
| 244 | X Position | X position of the pixel | write |
| 245 | Y Position | Y position of the pixel | write |
| 246 | RNG | Get a random number between 0 and 255 | read |
| 247 | Z1234567 | Each bit indicates whether the corresponding key is pressed | read|
| 248 | 89QWERTY | Each bit indicates whether the corresponding key is pressed | read |
| 249 | UIOPASDF | Each bit indicates whether the corresponding key is pressed | read |
| 250 | GHJKLZXC | Each bit indicates whether the corresponding key is pressed | read |
| 251 | VBNM,./; | Each bit indicates whether the corresponding key is pressed | read |
| 252 | Arrow / Space / Ctrl / Shift / Alt | Each bit indicates whether the corresponding key is pressed | read |
| 253 | Time | Time since Unix epoch (`mod 256`) | read |
| 254 | Mouse X | Mouse X position(will be in range 0-255 based on cell mouse is at)| both |
| 255 | Mouse Y | Mouse Y position(will be in range 0-255 based on cell mouse is at) | both |

# Examples

>you can check Examples in the sample_asm folder it contains commented assembly code for some usefull programs
> it can be compiled by using (install the )
```
cd NAND-8
python3 CPU.py sample_asm/name_of_program.asm
```
#  KPU16: architechture draft

> **Status:** Draft architecture specification. Subject to change.

## Overview

This project is a custom  CPU architecture intended to be implemented in python. The goal is to create a clean, modern ISA while remaining simple enough to under2tand completely.

> This emulator operates at a high level of abstraction. It does not simulate electrical circuits, gates, or clock-level har1ware. Instead, it executes KPU16 machine code directly while preserving the architectural behavior of the CPU.
## Current Design Decisions

### Architecture

- Harvar1 architecture
- Load/store architecture
- Fixed-width **32-bit instructions**
- Instruction-based I/O (port I/O)

### Register2

- 32 general-purpose register2 (`R0`-`R31`)
- Register index width: **5 bits**
- Register width: **16 bits**
- Register2 store or1inary 16-bit values; instructions decide whether values are interpreted as signed, unsigned, or memory addresses.

### Data Representation
- Native wor1 size: **16 bits**
- Signed integer2 use **two's complement**
- Unsigned values supported naturally by interpretation of instructions

### Memory
- Register2 hold memory addresses.
- Address space is based on 16-bit addresses.
- Memory is intended to be byte-addressable (subject to final confirmation).
- Maximum address space: **64 KiB**.

### Instruction Format

Current planned layout:

| Bits | Purpose |
|------|---------|
| 1-6 | Opcode |
| 7-11 | Argument 1 |
| 12-16 | Argument 2 |
| 17-32 | Additional fields (immediate, offset, register, function bits, etc.) |

The final 16 bits are interpreted differently depending on the instruction format.

### Opcode Space

- Opcode width: **6 bits**
- Maximum instructions(which allow jumping): **65536**

The current expectation is to implement around **40-50** instructions while reserving unused opcodes for future extensions.

## I/O
This CPU will use **instruction-based I/O** rather than memory-mapped I/O.

# Instruction Set Reference

The following section describes every instruction currently supported by the KPU16 ISA.

General syntax:

```asm
instruction operand1 operand2 operand3
```

Register2 are written as `r0` through `r31`.

---

## Arithmetic Instructions

### add

```asm
add r1 r2 r3
```

Adds `r2` and `r3` and stores the result in `r1`.

Example:

```asm
add r1 r2 r3
```

Result:

```text
r1 = r2 + r3
```

---

### sub

```asm
sub r1 r2 r3
```

Subtracts `r3` from `r2`.

```text
r1 = r2 - r3
```

---

### mult

```asm
mult r1 r2 r3
```

Multiplies two register2.

```text
r1 = r2 × r3
```

---

### div

```asm
div r1 r2 r3
```

Divides `r2` by `r3`.

```text
r1 = r2 // r3
```

Division by zero is undefined.

---

### mod

```asm
mod r1 r2 r3
```

Stores the remainder after division.

```text
r1 = r2 mod r3
```

---

### min

```asm
min r1 r2 r3
```

Stores the smaller of two values.

```text
r1 = min(r2, r3)
```

---

### max

```asm
max r1 r2 r3
```

Stores the larger of two values.

```text
r1 = max(r2, r3)
```

---

# Bitwise Instructions

### and

```asm
and r1 r2 r3
```

Performs a bitwise AND.

```text
r1 = r2 AND r3
```

---

### or

```asm
or r1 r2 r3
```

Performs a bitwise OR.

---

### xor

```asm
xor r1 r2 r3
```

Performs a bitwise XOR.

---

### not

```asm
not r1 r2
```

Performs a bitwise NOT.

```text
r1 = NOT r2
```

---

### shl

```asm
shl r1 r2
```

Shifts `r1` left by the number of bits stored in `r2`.

```text
r1 <<= r2
```

---

### shr

```asm
shr r1 r2
```

Logical right shift.

```text
Zeroes are shifted into the upper bits.
```

---

### sar

```asm
sar r1 r2
```

Arithmetic right shift.

```text
The sign bit is preserved.
```

---

### rol

```asm
rol r1 r2
```

Rotates bits left.

---

### ror

```asm
ror r1 r2
```

Rotates bits right.

---

# Data Movement

### mov

```asm
mov r1 r2
```

Copies one register into another.

```text
r1 = r2
```

---

### ldi

```asm
ldi r1 value
```

Loads a 16-bit immediate value.
supports single ascii character2 and number2 for now.
Example

```asm
ldi r1 100
ldi r2 'h' 
```

---

### load

```asm
load r1 r2
```

Loads a value from memory.

```text
r1 = Memory[r2]
```

---

### store

```asm
store r1 r2
```

Stores a register into memory.

```text
Memory[r1] = r2
```

---

# Comparison

### cmp

```asm
cmp r1 r2
```

Performs an internal subtraction

```text
r2 - r1
```

No register is modified.

Only the CPU flags are updated.

---

# Control Flow

### jump

```asm
jump address
```

Unconditionally jumps to the specified instruction.
use labels for better performance

---

### jc

```asm
jc flags address
```

Jumps only if the specified flag condition is satisfied.

- Multiple flags may be supplied.(well assembler cant handle it yet but imma add it soon dw)
flags used are:
Z-if last arithmetic operation resulted in zero
N-if last arithmetic operation resulted in negative
C-if last arithmetic operation resulted in carry
V-if last arithmetic operation resulted in overflow

Examples

```asm
jc z 100
jc z .loop
jc n .done
```

---

### nop

```asm
nop
```

Does nothing.

---

### halt

```asm
halt
```

Immediately stops program execution.

---

# Input / Output

### read

```asm
read r1
```

Reads an integer from the terminal.

---

### display

```asm
display r2
```

Displays the numeric contents of a register.

---

### print

```asm
print r2
```

Prints the ASCII character represented by the register value.

for printng long masseges you can use 
```asm
print 'your text'
```
assembler breaks it into individual character codes, for this reason using r0 in any operation is not recommended
also escape sequesnces not supported yet 
---

### println

```asm
println r2
```
Same as print but with a new line at the end

---

### time

```asm
time r1
```

Stores the current Unix time in milliseconds into r1.
Since time is too big it may be modulos-ed to fit in the range

---

# Mouse

### mousex

```asm
mousex r1
```

Stores the current mouse X coor1inate into r1.

---

### mousey

```asm
mousey r1
```

Stores the current mouse Y coor1inate into r1.

---

### mbutton

```asm
mbutton r1 button
```

Stores the state of a mouse button.

Result:

```text
1 = pressed
0 = released
```

Example

```asm
mbutton r1 1
```
Button codes are

- 1-left button
- 2-right button
- 3-middle button
---

# Keyboard

### key

```asm
key r1 'a'
```

Stores the state of the specified key.

Result:

```text
1 = pressed
0 = released
```

Example

```asm
key r1 'w'
key r2  KEY_SPACE
```
#### Special Key Constants

The following predefined constants may be used with the `key` instruction.

| Constant | Value | Description |
|----------|------:|-------------|
| `KEY_BACKSPACE` | 8 | Backspace key |
| `KEY_TAB` | 9 | Tab key |
| `KEY_ENTER` | 13 | Enter/Return key |
| `KEY_ESCAPE` | 27 | Escape key |
| `KEY_SPACE` | 32 | Space bar |
| `KEY_DELETE` | 127 | Delete key |
| `KEY_UP` | 1000 | Up arrow |
| `KEY_DOWN` | 1001 | Down arrow |
| `KEY_LEFT` | 1002 | Left arrow |
| `KEY_RIGHT` | 1003 | Right arrow |
| `KEY_HOME` | 1004 | Home key |
| `KEY_END` | 1005 | End key |
| `KEY_PAGEUP` | 1006 | Page Up key |
| `KEY_PAGEDOWN` | 1007 | Page Down key |
| `KEY_INSERT` | 1008 | Insert key |
| `KEY_SHIFT` | 1009 | Shift key |
| `KEY_CTRL` | 1010 | Control (Ctrl) key |
| `KEY_ALT` | 1011 | Alt key |
| `KEY_CAPSLOCK` | 1012 | Caps Lock key |
| `KEY_F1` | 1020 | Function key F1 |
| `KEY_F2` | 1021 | Function key F2 |
| `KEY_F3` | 1022 | Function key F3 |
| `KEY_F4` | 1023 | Function key F4 |
| `KEY_F5` | 1024 | Function key F5 |
| `KEY_F6` | 1025 | Function key F6 |
| `KEY_F7` | 1026 | Function key F7 |
| `KEY_F8` | 1027 | Function key F8 |
| `KEY_F9` | 1028 | Function key F9 |
| `KEY_F10` | 1029 | Function key F10 |
| `KEY_F11` | 1030 | Function key F11 |
| `KEY_F12` | 1031 | Function key F12 |
---

# Graphics

### setpixel

```asm
setpixel x y color
```

Sets the pixel at `(x, y)` to the geyscale(0-255) color.

---

### getpixel

```asm
getpixel r1 x y
```

Reads the color of a pixel.

```text
r1 = pixel(x, y)
```

---

### dispflip

```asm
dispflip
```

Updates (flips) the display buffer to the screen.


# Other Language Features

## Comments

Single-line comments begin with `#`.

```asm
ldi r1 10      # Load decimal 10
add r2 r1 r3   # Add two registers
```

Everything following `#` on a line is ignored by the assembler.

---

## Labels

Labels begin with a period (`.`) and represent instruction addresses.

```asm
.loop
    add r1 r1 r2
    jc z .done
    jump .loop

.done
    halt
```

Labels may be used with any instruction that accepts an instruction address.

---

## Global Constants

Constants are declared using the `&` symbol.

Syntax:

```asm
&NAME = value
```

Example:

```asm
&SIZE = 100
&WIDTH = 320
```

Constants are available throughout the program.

---

## Macros

Macros allow reusable blocks of assembly code.

Syntax:

```asm
$macro_name(arg1, arg2)
    ...
}
```

Example:

```asm
$swap(a, b)
    mov r0 {a}
    mov {a} {b}
    mov {b} r0
}

swap(r1, r2)
```

Macro arguments are substituted using `{argument}` placeholders.

Each macro invocation automatically receives unique internal labels, allowing labels to be safely reused inside macros.

refer to [[dotasm/macro.asm]]

---

## Numeric Literals

The assembler currently supports decimal integers.

```asm
ldi r1 42
ldi r2 -5
```

---

## Character Literals

Single ASCII characters may be used wherever an immediate value is expected.

```asm
ldi r1 'A'
key r2 'w'
```

The assembler converts the character to its ASCII value automatically.

---

## String Expansion

`print` and `println` accept string literals.

```asm
print 'Hello'
println 'World'
```

The assembler automatically expands these into multiple instructions.

For example,

```asm
print 'Hi'
```

is assembled approximately as

```asm
ldi r0 'H'
print r0

ldi r0 'i'
print r0
```

`println` additionally emits a newline character (`ASCII 10`) after the string.

Because string expansion temporarily uses **r0**, it is recommended to avoid relying on `r0` during expanded print statements.

---

## Predefined Key Constants

The `key` instruction accepts predefined keyboard constants.

Example:

```asm
key r1 KEY_SPACE
key r2 KEY_UP
```

These are automatically translated into their corresponding key codes.

---

## Register Names

General-purpose registers are named

```text
r0 ... r31
```

The architecture contains 32 registers, each 16 bits wide.

---

## Error Checking

The assembler reports errors for

- Unknown instructions
- Invalid register names
- Registers outside `r0-r31`
- Incorrect macro argument counts
- Invalid ASCII characters
- Invalid jump targets
- Invalid conditional jump arguments

Assembly stops immediately when an error is encountered.




# Words of maker
- this is genuinly one of my most beloved projects of all time, because this time i am not programming a design made by someone one years ago, I am making the design itself. after recently running famous mysic video bad apple on it i am more happier with this projecy. Its not completed yet and is totally open to contributions and recommendations and even sample programms. Guide is above and refer to the programs made previously. - Kumail-exp
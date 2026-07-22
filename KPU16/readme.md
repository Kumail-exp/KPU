#  KPU16: architechture draft

> **Status:** Draft architecture specification. Subject to change.

## Overview

This project is a custom  CPU architecture intended to be implemented in python. The goal is to create a clean, modern ISA while remaining simple enough to understand completely.

>it will not simulate on lower level and wil work with very abstactions just to simulate a machine code running machine
## Current Design Decisions

### Architecture

- Harvard architecture
- Load/store architecture
- Fixed-width **32-bit instructions**
- Little-endian
- Instruction-based I/O (port I/O)

### Registers

- 32 general-purpose registers (`R0`-`R31`)
- Register index width: **5 bits**
- Register width: **16 bits**
- Registers store ordinary 16-bit values; instructions decide whether values are interpreted as signed, unsigned, or memory addresses.

### Data Representation
- Native word size: **16 bits**
- Signed integers use **two's complement**
- Unsigned values supported naturally by interpretation of instructions

### Memory
- Registers hold memory addresses.
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
- Maximum instructions: **64**

The current expectation is to implement around **40-50** instructions while reserving unused opcodes for future extensions.

## I/O

This CPU will use **instruction-based I/O** rather than memory-mapped I/O.

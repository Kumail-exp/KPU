class ALU:
    def __init__(self):
        self.Flags = {
            'z': False,
            'n': False,
            'c': False,
            'v': False
        }

    def execute(self, A: int, B: int, opcode: int):
        MASK = 0xFFFF
        SIGN = 0x8000
        A &= MASK
        B &= MASK
        C = False 
        V = False
        if opcode == 0:  # ADD
            temp = A + B
            output = temp & MASK
            C = temp > MASK
            V = ((A ^ output) & (B ^ output) & SIGN) != 0

        elif opcode == 1:  # SUB
            temp = A - B
            output = temp & MASK
            C = A >= B
            V = ((A ^ B) & (A ^ output) & SIGN) != 0

        elif opcode == 2:  # MUL
            temp = A * B
            output = temp & MASK
            C = temp > MASK

        elif opcode == 3:  # DIV
            output = 0 if B == 0 else A // B

        elif opcode == 4:  # MOD
            output = 0 if B == 0 else A % B

        elif opcode == 5:
            output = A & B

        elif opcode == 6:
            output = A | B

        elif opcode == 7:
            output = A ^ B

        elif opcode == 8:
            output = (~A) & MASK

        elif opcode == 9:
            shift = B & 0xF
            if shift:
                C = ((A << (shift - 1)) & 0x10000) != 0
            output = (A << shift) & MASK

        elif opcode == 10:
            shift = B & 0xF
            if shift:
                C = bool((A >> (shift - 1)) & 1)
            output = A >> shift

        elif opcode == 11:
            shift = B & 0xF
            signed = A if A < 0x8000 else A - 0x10000
            if shift:
                C = bool((A >> (shift - 1)) & 1)
            output = (signed >> shift) & MASK

        elif opcode == 12:
            shift = B & 0xF
            output = ((A << shift) | (A >> (16 - shift))) & MASK if shift else A
            C = bool(output & 1)

        elif opcode == 13:
            shift = B & 0xF
            output = ((A >> shift) | (A << (16 - shift))) & MASK if shift else A
            C = bool((output >> 15) & 1)

        elif opcode == 14:
            output = min(A, B)

        elif opcode == 15:
            output = max(A, B)

        else:
            raise ValueError(f"Unknown opcode {opcode}")

        output &= MASK  
        self.Flags['z'] = output == 0
        self.Flags['n'] = bool(output & SIGN)
        self.Flags['c'] = bool(C)
        self.Flags['v'] = bool(V)
        return output
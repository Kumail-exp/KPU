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
        match opcode:
            case 0:  # ADD
                temp = A + B
                output = temp & MASK
                C = temp > MASK
                V = ((A ^ output) & (B ^ output) & SIGN) != 0

            case 1:  # SUB
                temp = A - B
                output = temp & MASK
                C = A >= B
                V = ((A ^ B) & (A ^ output) & SIGN) != 0

            case 2:  # MUL
                temp = A * B
                output = temp & MASK
                C = temp > MASK

            case 3:  # DIV
                output = 0 if B == 0 else A // B

            case 4:  # MOD
                output = 0 if B == 0 else A % B

            case 5:
                output = A & B

            case 6:
                output = A | B

            case 7:
                output = A ^ B

            case 8:
                output = (~A) & MASK

            case 9:
                shift = B & 0xF
                if shift:
                    C = ((A << (shift - 1)) & 0x10000) != 0
                output = (A << shift) & MASK

            case 10:
                shift = B & 0xF
                if shift:
                    C = bool((A >> (shift - 1)) & 1)
                output = A >> shift

            case 11:
                shift = B & 0xF
                signed = A if A < 0x8000 else A - 0x10000
                if shift:
                    C = bool((A >> (shift - 1)) & 1)
                output = (signed >> shift) & MASK

            case 12:
                shift = B & 0xF
                output = ((A << shift) | (A >> (16 - shift))) & MASK if shift else A
                C = bool(output & 1)

            case 13:
                shift = B & 0xF
                output = ((A >> shift) | (A << (16 - shift))) & MASK if shift else A
                C = bool((output >> 15) & 1)

            case 14:
                output = min(A, B)

            case 15:
                output = max(A, B)

            case _:
                raise ValueError(f"Unknown opcode {opcode}")

        output &= MASK  
        self.Flags['z'] = output == 0
        self.Flags['n'] = bool(output & SIGN)
        self.Flags['c'] = bool(C)
        self.Flags['v'] = bool(V)
        return output
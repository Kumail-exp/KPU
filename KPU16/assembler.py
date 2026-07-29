OPCODES = {
    'add': 0,
    'sub': 1,
    'mult': 2,
    'div': 3,
    'mod': 4,
    'and': 5,
    'or': 6,
    'xor': 7,
    'not': 8,
    'shl': 9,
    'shr': 10,
    'sar': 11,
    'rol': 12,
    'ror': 13,
    'min': 14,
    'max': 15,
    'ldi': 16,
    'jump': 17,
    'jc': 18,
    'display': 19,
    'load': 20,
    'store': 21,
    'cmp': 22,
    'mov': 23,
    'nop': 24,
    'halt': 25,
    'read':26,
    'gettime':27,
    'print':28,
    'println':29,
    'mousex':30,
    'mousey':31
    }
def ascii_val(char: str):
    if len(char) != 1:
        raise ValueError(f'not a single character->\'{char}\'')

    if char.isascii():
        return ord(char)
    else:
        raise ValueError('not a correct ascii')

def reg_adress(addr:str):
    return int(addr[1:])%32
def to_stream(num:int,size=16):
    b=bin(num)[2:]
    binary=[0]*size
    for i in range(len(b)):
        binary[size-len(b)+i]=int(b[i])
    return binary
class Macro:
    def __init__(self, args: list[str], code: str):
        self.args = args
        self.code = code

    def get_asm(self, values: list[str]) -> str:
        mapping = dict(zip(self.args, values))
        return self.code.format(**mapping)
class Assembler:
    def __init__(self,code:str):
        self.code:list[str]=[]
        for i in code.split('\n'):
            self.code.append(i)
        self.labels:dict[str,int]={}
        self.macros={}
    def preprocess(self) -> list[str]:
        nc = []
        i = 0
        # i have to change the loop format from for loop to while becoz udk it seemed simpler

        while i < len(self.code):
            instruction = self.code[i].split('#')[0].strip()

            if not instruction:
                i += 1
                continue

            if instruction.startswith('.'):
                self.labels[instruction[1:]] = len(nc)
                i += 1
                continue

            if instruction.startswith('$'):
                header = instruction[1:]

                name = header[:header.index('(')].strip()
                args = header[header.index('(')+1:header.index(')')]
                args = [a.strip() for a in args.split(',') if a.strip()]
                body = []
                i += 1
                while i < len(self.code):
                    line = self.code[i].split('#')[0].strip()
                    if line == "}":
                        break
                    if line:
                        body.append(line)
                    i += 1
                self.macros[name] = Macro(args, "\n".join(body))
                i += 1
                continue

            nc.append(instruction.lower())
            i += 1

        self.code = nc
        return nc
    def expand(self) -> list[str]:

        expanded = []

        for line in self.code:
            line = line.strip()

            if '(' not in line or not line.endswith(')'):
                expanded.append(line)
                continue

            name = line[:line.index('(')].strip()

            if name not in self.macros:
                expanded.append(line)
                continue

            argstr = line[line.index('(')+1:-1]

            args = []
            if argstr.strip():
                args = [a.strip() for a in argstr.split(',')]

            macro = self.macros[name]

            if len(args) != len(macro.args):
                raise SyntaxError(
                    f"Macro '{name}' expects {len(macro.args)} arguments, got {len(args)}"
                )
                # making ts like a professional language lawl

            expanded.extend(macro.get_asm(args).splitlines())

        self.code = expanded
        return expanded
    def translate(self,line:str)->list[int]:
        tokens=line.split(' ')
        # print(tokens)
        opcode=tokens[0]
        # 3 input ones
        if(opcode in [  'add',
                        'sub',
                        'mult',
                        'div',
                        'mod',
                        'and',
                        'or',
                        'xor',
                        'min',
                        'max',
                        ]):
            return [OPCODES[opcode],reg_adress(tokens[1]),reg_adress(tokens[2])]+to_stream(reg_adress(tokens[3]),5)+[0]*11
        #two input oens
        if (opcode in [
                        'load',
                        'store',
                        'cmp',
                        'mov',
                        'not',
                        'shl',
                        'shr',
                        'sar',
                        'rol',
                        'ror'
                            ]):
            return [OPCODES[opcode],reg_adress(tokens[1]),reg_adress(tokens[2])]+[0]*16
        # specific ones:
        if(opcode=='ldi'):
            if tokens[2][0]=='\'' and tokens[2][-1]=='\'':
                 val=ascii_val(tokens[2][1:-1])
            else:
                 val=int(tokens[2])
            return [OPCODES[opcode],reg_adress(tokens[1]),0]+to_stream(val)
        if(opcode=='jump'):
                    try:
                        if tokens[1].startswith('.'):
                            value=self.labels[tokens[1][1:]] 
                        else:
                            value=int(tokens[1])
                    except Exception as e:
                        print(e)
                        raise ValueError(f'invalid argument to jump->\'{tokens[1]}\'')
                    return [OPCODES[opcode]]+[0]*2+to_stream(value)
        if(opcode=='jc'):
                            flag_code={'z':1,'n':2,'c':3,'v':4}
                            
                            try:
                                if tokens[2][0]=='.':
                                    value=self.labels[tokens[2][1:]] 
                                else:
                                    value=int(tokens[2])
                                fc=flag_code[tokens[1]]
                            except Exception as e:
                                print(e)
                                raise ValueError(f'invalid argument to jump->\'{tokens[2]}\'')
                            return [OPCODES[opcode],fc,0]+to_stream(value)      
        # one argument ones:
        if opcode in ['display','read','gettime','print','println','mousex','mousey']:
             return [OPCODES[opcode],reg_adress(tokens[1]),0]+[0]*16
        # no argumented ones
        if opcode in ['halt','nop']:
             return [OPCODES[opcode],0,0]+[0]*16
        raise ValueError(f"unknown opcode \'{opcode}\'")
    
    def assemble(self,debug_mode=False)->list[list[int]]:
        '''no need for anything this just returns the perfectly done machine code'''
        self.preprocess()
        self.expand()
        # print("\n".join(self.code))
        # since we need to process the labels inside the macros
        self.preprocess()
        # print(self.labels)
        out=[]
        for line in self.code:
            o=self.translate(line)
            if o:
                if debug_mode:
                     print(f'{line}-->{o}')
                out.append(o)
        return out

if __name__=='__main__':
    import sys
    from pathlib import Path

    if len(sys.argv) != 2:
        print("use the correct format")
        sys.exit(1)

    input_file = Path("dotasm") / sys.argv[1]
    out = Path("dotkpu") / input_file.with_suffix(".kpu").name
    with open(input_file) as f:
        source = f.read()
    obj=Assembler(source)
    mc=obj.assemble(0)

    machine_code =str(mc)

    with open(out, "w") as f:
        f.write(machine_code)
    print(f'program assebled succesfully into {out}')
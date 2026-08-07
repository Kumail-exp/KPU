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
    'mousey':31,
    'setpixel':32,
    'getpixel':33,
    'dispflip':34,
    'mbutton'   :35,
    'key':36
    }
KEYS = {
    # Control
    "KEY_BACKSPACE": 8,
    "KEY_TAB": 9,
    "KEY_ENTER": 13,
    "KEY_ESCAPE": 27,
    "KEY_SPACE": 32,
    "KEY_DELETE": 127,

    # Arrows
    "KEY_UP": 1000,
    "KEY_DOWN": 1001,
    "KEY_LEFT": 1002,
    "KEY_RIGHT": 1003,

    # Navigation
    "KEY_HOME": 1004,
    "KEY_END": 1005,
    "KEY_PAGEUP": 1006,
    "KEY_PAGEDOWN": 1007,
    "KEY_INSERT": 1008,

    # Modifiers
    "KEY_SHIFT": 1009,
    "KEY_CTRL": 1010,
    "KEY_ALT": 1011,
    "KEY_CAPSLOCK": 1012,

    # Function keys
    "KEY_F1": 1020,
    "KEY_F2": 1021,
    "KEY_F3": 1022,
    "KEY_F4": 1023,
    "KEY_F5": 1024,
    "KEY_F6": 1025,
    "KEY_F7": 1026,
    "KEY_F8": 1027,
    "KEY_F9": 1028,
    "KEY_F10": 1029,
    "KEY_F11": 1030,
    "KEY_F12": 1031,
}   
def ascii_val(char: str):
    if len(char) != 1:
        raise ValueError(f'not a single character->\'{char}\'')

    if char.isascii():
        return ord(char)
    else:
        raise ValueError('not a correct ascii')

def reg_adress(addr: str):
    if not addr.startswith('r'):
        raise ValueError(f"invalid register '{addr}'")
    try:
        reg = int(addr[1:])
    except ValueError:
        raise ValueError(f"invalid register '{addr}'")
    if not 0 <= reg <= 31:
        raise ValueError(f"register out of range '{addr}' (expected r1-r31)")

    return reg
def to_stream(num: int, size=16):
    #stole this from stack overflow
    num &= (1 << size) - 1
    return [(num >> (size - 1 - i)) & 1 for i in range(size)]
class Macro:
    def __init__(self,name:str,args: list[str], code: str):
        self.name=name
        self.args = args
        self.code = code
        self.calls=0
    def called(self):
        self.calls+=1
        c=[]
        for line in self.code.split('\n'):
            l=[]
            for token in line.split(' '):
                if token.startswith('.'):
                     l.append(f'.{self.name}_{token[1:]}_{self.calls}')
                else:
                     l.append(token)
            c.append(' '.join(l))
        return '\n'.join(c)    
    def get_asm(self, values: list[str]) -> str:
        code=self.called()
        mapping = dict(zip(self.args, values))
        return code.format(**mapping)
class Assembler:
    def __init__(self,code:str):
        self.code:list[str]=[]
        for i in code.split('\n'):
            self.code.append(i)
        self.labels:dict[str,int]={}
        self.macros={}
        self.globals={}
    def preprocess(self,labelise=True,expand_prints=False) -> list[str]:
        nc = []
        i = 0
        # i have to change the loop format from for loop to while becoz udk it seemed simpler

        while i < len(self.code):
            instruction = self.code[i].split('#')[0].strip()

            if not instruction:
                i += 1
                continue
            if labelise:
                if instruction.startswith('.'):
                    self.labels[instruction[1:]] = len(nc)
                    i += 1
                    continue
            if instruction.startswith('&'):
                var=instruction[1:]
                tk=var.split('=')
                self.globals[tk[0].strip()]=tk[1].strip()
                i+=1
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
                self.macros[name] = Macro(name,args, "\n".join(body))
                i += 1
                continue

            # shortcuts
            if expand_prints:
                if instruction.startswith('println'):
                    word = instruction[len('println'):].strip()

                    if word.startswith("'") and word.endswith("'"):
                        word = word[1:-1]

                    for l in word:
                        nc.append(f"ldi r0 {ascii_val(l)}")
                        nc.append("print r0")

                    nc.append("ldi r0 10")
                    nc.append("print r0")
                    i += 1
                    continue

                if instruction.startswith('print'):
                    word = instruction[len('print'):].strip()

                    if word.startswith("'") and word.endswith("'"):
                        word = word[1:-1]

                    for l in word:
                        nc.append(f"ldi r0 {ascii_val(l)}")
                        nc.append("print r0")

                    i += 1
                    continue
            nc.append(instruction)
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
    def translate(self,line:str)->list[list[int]]:
        try:
            tokens=line.split()
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
                            'setpixel',
                            'getpixel'
                            ]):
                return [[OPCODES[opcode],reg_adress(tokens[1]),reg_adress(tokens[2])]+to_stream(reg_adress(tokens[3]),5)+[0]*11]
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
                            'ror',
                            'mbutton'
                                ]):
                return [[OPCODES[opcode],reg_adress(tokens[1]),reg_adress(tokens[2])]+[0]*16]
            # specific ones:
            if(opcode=='ldi' or opcode=='key'):
                if(tokens[2][0]=='&'):
                    if tokens[2][1:] in self.globals:
                        val=int(self.globals[tokens[2][1:]])
                    else:
                        raise ValueError(f'unknown global variable \'{tokens[2][1:]}\'')
                elif tokens[2] in KEYS:
                    val = KEYS[tokens[2].upper()]
                elif tokens[2][0] == "'" and tokens[2][-1] == "'":
                    val = ascii_val(tokens[2][1:-1])
                else:
                    val = int(tokens[2])
                return [[OPCODES[opcode],reg_adress(tokens[1]),0]+to_stream(val)]
            if(opcode=='jump'):
                        try:
                            if tokens[1].startswith('.'):
                                value=self.labels[tokens[1][1:]] 
                            else:
                                value=int(tokens[1])
                        except Exception as e:
                            print(e)
                            raise ValueError(f'invalid argument to jump->\'{tokens[1]}\'')
                        return [[OPCODES[opcode]]+[0]*2+to_stream(value)]
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
                                return [[OPCODES[opcode],fc,0]+to_stream(value)]      
            # one argument ones:
            if opcode in ['display','read','gettime','print','println','mousex','mousey']:
                return [[OPCODES[opcode],reg_adress(tokens[1]),0]+[0]*16]
            # no argumented ones
            if opcode in ['halt','nop','dispflip']:
                return [[OPCODES[opcode],0,0]+[0]*16]
            raise ValueError(f"unknown opcode \'{opcode}\'")
        except Exception as e:
            print(f'error in line->{line}')
            print(e)
            raise
    def assemble(self,debug_mode=False)->list[list[int]]:
        '''no need for anything this just returns the perfectly done machine code'''
        self.preprocess(False,True)
        self.expand()
        # print("\n".join(self.code))
        # since we need to process the labels inside the macros
        self.preprocess()
        # print(self.globals)
        # print(self.labels)
        out=[]
        for line in self.code:
            o=self.translate(line)
            if o:
                if debug_mode:
                     print(f'{line}-->{o}')
                for ins in o:
                    out.append(ins)
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
    mc=obj.assemble(1)


    with open(out, "w") as f:
        for line in mc:
            f.write(f'{line}\n')
    print(f'program assebled succesfully into {out}')
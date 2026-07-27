from ALU import *
import ast
import sys
from pathlib import Path
# some filler functiuons
def to_stream(num:int,size=8):
    b=bin(num)[2:]
    binary=[0]*size
    for i in range(len(b)):
        binary[size-len(b)+i]=int(b[i])
    return binary
def to_num(stream: list[int], size=None, two_complement=False)->int:
    if size is None:
        size = len(stream)  
    value = 0
    if two_complement:
        value -= int(stream[0]) * (1 << (size - 1))
        start = 1
    else:
        start = 0

    for i in range(start, size):
        value += int(stream[i]) * (1 << (size - 1 - i))

    return value


class CPU:
    def __init__(self):
        self.instructions:list[list[int]]=[[]]
        self.pc:int=0
        self.registers:list[int]=[0 for i in range(32)]
        self.memory={}#memory is too large to pre allocate so we allocate it at runtime lwk
        self.alu=ALU()
        self.running=True
    def execute(self,instruction:list[int]):
        # print(instruction)
        # for alu based operations:
        opcode=instruction[0]
        addr1=instruction[1]
        addr2=instruction[2]
        other=instruction[3:]
        addr3=to_num(other[:5])
        if(opcode<16):
            self.registers[addr1]=self.alu.execute(self.registers[addr2],self.registers[addr3],opcode)
        elif opcode==16:
                self.registers[addr1]=to_num(other,size=16,two_complement=True)
        elif opcode== 17:
                return to_num(other,size=16)
        elif opcode== 18:
                flags=['z','n','c','v']
                # it will have an and gate option too if other addr2 has a value then then it will and before doing anything
                if(addr2!=0):
                    # and case
                    if(self.alu.Flags[flags[addr1-1]] and self.alu.Flags[flags[addr2-1]]):
                        return to_num(other,size=16)
                else:
                    if(self.alu.Flags[flags[addr1-1]] ):
                        return to_num(other,size=16)
        elif opcode== 19:
                print(self.registers[addr1])
        elif opcode==20:
            #load
            self.registers[addr1]=self.memory.get(self.registers[addr2],default=0)
        elif opcode==21:
            self.memory[self.registers[addr1]]=self.registers[addr2]
        elif opcode==22:
            #  cmp
            self.alu.execute(self.registers[addr2],self.registers[addr3],opcode=1)
        elif opcode==23:
            #  mov
            self.registers[addr1]=self.registers[addr2]
        elif opcode==24:
            # no op
            pass
        elif opcode==25:
            #  halt
            self.running=False
        elif opcode==26:#input
             self.registers[addr1]=int(input('>'))
        else:
                raise ValueError(f'this opcode {opcode} is not yet defined')
        return self.pc+1
    def give_ins(self,instructions:list[list[int]]):
        self.instructions=instructions
    def run(self):
        self.running=True
        while self.pc<len(self.instructions) and self.pc>=0 and self.running:
            # print(self.pc)
            self.pc=self.execute(self.instructions[self.pc])
        self.instructions=[[]]
            


if __name__=='__main__':

        if len(sys.argv) != 2:
            print("u cant even use a basic program")
            sys.exit(1)

        input_file = Path("dotkpu") / sys.argv[1]
        with open(input_file) as f:
            source = f.read()
        ins = ast.literal_eval(source)
        cpu=CPU()
        cpu.give_ins(ins)
        cpu.run()
    
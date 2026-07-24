from ALU import *
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
    def execute(self,instruction:list[int]):
        # for alu based operations:
        opcode=instruction[0]
        addr1=instruction[1]
        addr2=instruction[2]
        other=instruction[3:]
        addr3=to_num(other[:5])
        if(opcode<16):
            self.registers[addr1]=self.alu.execute(self.registers[addr2],self.registers[addr3],opcode)
            return self.pc+1
        match(opcode):
            case 16:
                self.registers[addr1]=to_num(other,size=16,two_complement=True)
                return self.pc+1
            case 17:
                return to_num(other,size=16)
            case 18:
                return self.pc+1  # iwill do ts later
            case 19:
                print(self.registers[addr1])
                return self.pc+1
    def give_ins(self,instructions:list[list[int]]):
        self.instructions=instructions
    def run(self):
        while self.pc<len(self.instructions) and self.pc>=0:
            # print(self.pc)
            self.pc=self.execute(self.instructions[self.pc])
        self.instructions=[[]]
            


if __name__=='__main__':
    # just a simple adder lol
    ins=[
        [16,1,0]+to_stream(1,16),
        [16,2,0]+to_stream(1,16),
        [19,1,0]+to_stream(0,16),
        [0,1,2]+to_stream(1,5)+[0]*11,
        [17,0,0]+to_stream(2,16),
    ]
    cpu=CPU()
    cpu.give_ins(ins)
    cpu.run()
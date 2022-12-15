import sys
import csv

class Active_Instruction:
        def __init__(self, instruction) -> None:
            self.instruction = instruction
            self.age = 0

class Cpu:

    X = 0

    def __init__(self, instructions=None) -> None:
        self.X = 1
        self.cycle = 1
        self.instructions = instructions
        self.signal_sum = 0
        
    @classmethod
    def addreg(cls, self, V):
        self.X += V
    
    def check_signal(self):
        return self.X * self.cycle
    
    def run(self, program, reset_cycles=True):
        active_instruction = None
        if reset_cycles:
            self.cycle = 1
        while True:
            if self.cycle in [20,60,100,140,180,220]:
                self.signal_sum += self.check_signal()
            if active_instruction == None:
                try:
                    programline = program.pop(0)
                except:
                    #ohjelma loppu
                    return self.signal_sum
                active_instruction = Active_Instruction(self.instructions[programline[0]])
            active_instruction.age += 1 #Oletetaan, ettei käsky voi kestää nollaa sykliä
            if active_instruction.age >= active_instruction.instruction.duration:
                if active_instruction.instruction.action is not None:
                    active_instruction.instruction.action(self, int(programline[1]))  #Ei kovin yleisessä muodossa tämä
                active_instruction = None
            self.cycle += 1

class Instruction:
    def __init__(self, name, duration, action) -> None:
        self.name = name
        self.duration = duration
        self.action = action

def init_instructions():
    instructions = dict()
    instructions['noop']=(Instruction('noop',1,None))
    instructions['addx']=(Instruction('addx',2,Cpu.addreg))
    return(instructions)

def get_program(file):
    inst_list = []
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=" ")
        for row in reader:
            inst_list.append(row)
    return inst_list

def main(argv):
    instructions = init_instructions()
    program = get_program(argv[1])
    cpu = Cpu(instructions)
    print(cpu.run(program))
    

if __name__ == "__main__":
    main(sys.argv)
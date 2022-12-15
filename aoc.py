import sys
import csv

class Active_Instruction:
        def __init__(self, instruction) -> None:
            self.instruction = instruction
            self.age = 0

class Cpu:

    X = 0
    XPIXEL = 40

    def __init__(self, instructions=None) -> None:
        self.X = 1
        self.cycle = 1
        self.instructions = instructions
        self.signal_sum = 0
        self.get_signal = False
        self.draw_image = False
        self.image = ''
        
    @classmethod
    def addreg(cls, self, V):
        self.X += V
    
    def check_signal(self):
        return self.X * self.cycle

    def draw_pixel(self):
        if abs(self.X - (self.cycle-1)%self.XPIXEL) <= 1:
            addchar = '#'
        else:  
            addchar = '.'
        self.image += addchar
        if (self.cycle)%self.XPIXEL == 0:
            self.image += '\n'
    
    def run(self, program, reset_cycles=True):
        active_instruction = None
        if reset_cycles:
            self.cycle = 1
        while True:
            if self.get_signal and self.cycle in [20,60,100,140,180,220]:
                self.signal_sum += self.check_signal()
            if active_instruction == None:
                try:
                    programline = program.pop(0)
                except:
                    #ohjelma loppu
                    if self.get_signal:
                        return self.signal_sum
                    elif self.draw_image:
                        return self.image
                    else:
                        return -1
                active_instruction = Active_Instruction(self.instructions[programline[0]])
            if self.draw_image:
                self.draw_pixel()
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

def max_calories(file):
    calories = [0]
    with open(file, 'r') as f:
        for line in f:
            if line == '\n': calories.append(0)
            else: calories[-1] += int(line)
    #voi tulla ylimääräinen 0-rivi, mutta se ei voi olla suurin
    return max(calories)


def main(argv):
    #aoc.py päivä osa tiedosto
    if argv[1] == '1':
        print(max_calories(argv[3]))
    if argv[1] == '10':
        instructions = init_instructions()
        program = get_program(argv[3])
        cpu = Cpu(instructions)
        if argv[2] == '1':
            cpu.get_signal = True
        elif argv[2] == '2':
            cpu.draw_image = True
        print(cpu.run(program))
    
if __name__ == "__main__":
    main(sys.argv)
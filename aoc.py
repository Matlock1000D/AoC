import sys
import csv
from day7 import *
from day8 import *
from day9 import *
from day11 import *
from day12 import *
from day13 import *
from day14 import *
from day15 import *
from day16 import *
from day17 import *
from day18 import *
from day19 import *
from day20 import *
from day21 import *
from day22 import *

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

def calories(file):
    calories = [0]
    with open(file, 'r') as f:
        for line in f:
            if line == '\n': calories.append(0)
            else: calories[-1] += int(line)
    #voi tulla ylimääräinen 0-rivi, mutta se ei voi olla suurin
    return calories

class Janken:
    def __init__(self, matchesfile, rules = 'selection'):
        self.points = 0
        self.moves = []
        self.rules = rules
        with open(matchesfile, 'r') as f:
            reader = csv.reader(f, delimiter=" ")
            for row in reader:
                self.moves.append(row)

    def get_selectionpoints(self, match: list[str]) -> int:
        move = match[1]
        if self.rules == 'result':
            return ((ord(match[0])+ord(match[1])-1)%3 + 1)
        elif move in ['X','Y','Z']:
            return (ord(move)-87)

    def get_resultpoints(self, match: list[str]) -> int:
        if match[0] not in ['A','B','C'] or match[1] not in ['X','Y','Z']: raise ValueError('Kielletty käsi')
        if self.rules == 'result': return ((ord(match[1])-88)*3)
        else: return(((ord(match[1])-ord(match[0])-1)%3)*3) 
        

    def get_points(self):
        points = 0
        for match in self.moves:    #match[0] = vastustajan liike, match[1] oma
            points += self.get_selectionpoints(match) + self.get_resultpoints(match)
        return points

def get_prio(mistake):
    x = ord(mistake.swapcase())-64
    if mistake.isupper(): x -= 6
    return x

def priorities(file, spec):
    prio_sum = 0
    if spec == '2':
        with open(file, 'r') as f:
            i = iter(f)
            for a,b,c in zip(i,i,i):
                badge = set(a.strip()).intersection(set(b.strip())).intersection(set(c.strip())).pop()
                prio_sum += get_prio(badge)
        return prio_sum
    else:
        with open(file, 'r') as f:
            for line in f:
                splitpoint = int((len(line.strip()))/2)
                comp1 = line[:splitpoint]
                comp2 = line[splitpoint:]
                mistake = set(comp1).intersection(set(comp2)).pop()
                prio_sum += get_prio(mistake)
        return prio_sum

def check_overlap(line:str, spec:str) -> bool:
    assignments = line.split(',')
    limits = []
    for assignment in assignments:
        limits.append(assignment.split('-'))
    if spec == '2':
        if int(limits[0][1]) < int(limits[1][0]) or int(limits[0][0]) > int(limits[1][1]): return False
        else: return True
    else:
        if int(limits[0][0]) <= int(limits[1][0]) and int(limits[0][1]) >= int(limits[1][1]): return True
        if int(limits[0][0]) >= int(limits[1][0]) and int(limits[0][1]) <= int(limits[1][1]): return True
        return False

def overlaps_count(file, spec):
    overlaps = 0
    with open(file, 'r') as f:
        for line in f:
            if check_overlap(line.strip(),spec): overlaps += 1
    return overlaps


def crane(initfile, spec):
    with open(initfile, 'r') as f:
        for i, line in enumerate(f):
            if len(line) < 2: continue
            if i == 0:
                stacks = int(len(line)/4)
                stack_dict = {}
                for x in range(stacks):
                    stack_dict[x]  = []
            if line[1].isupper() or line[1] == ' ':   #tunnistaa laatikkorivit
                for i in range(stacks):
                    box = line[1 + i*4]
                    if box.isalpha(): stack_dict[i].insert(0, box)
            if line[0] == 'm':
                moves = line.strip().split(' ')
                if spec == '2':
                    lifted_crates = []
                    for i in range(int(moves[1])):
                        lifted_crates.append(stack_dict[int(moves[3])-1].pop())
                    lifted_crates.reverse()
                    stack_dict[int(moves[5])-1] += lifted_crates
                else:
                    for i in range(int(moves[1])):
                        stack_dict[int(moves[5])-1].append(stack_dict[int(moves[3])-1].pop())
    tops = []
    for i in range(stacks): tops.append(stack_dict[i].pop())
    return ''.join(tops)

def get_signal(file, spec):
    if spec == '1': a = 4
    else: a = 14
    with open(file, 'r') as f:
        signal = f.read()
    for i in range(a,len(signal)):
        if len(set(signal[i-a:i])) == a: 
            return i
    return -1

def main(argv):
    #aoc.py päivä osa tiedosto
    if argv[1] == '1':
        if argv[2] == '1': print(max(calories(argv[3])))
        if argv[2] == '2': print(sum(sorted(calories(argv[3]), reverse=True)[:3]))
    if argv[1] == '2':
        if argv[2] == '1': 
            janken = Janken(argv[3])
        else: janken = Janken(argv[3],'result')
        print(janken.get_points())
    if argv[1] == '3':
        print(priorities(argv[3],argv[2]))
    if argv[1] == '4':
        print(overlaps_count(argv[3],argv[2]))
    if argv[1] == '5':
        print(crane(argv[3],argv[2]))
    if argv[1] == '6':
        print(get_signal(argv[3],argv[2]))
    if argv[1] == '7':
        dos = Dos()
        dos.read_batch(argv[3])
        sizes = dos.get_all_size()
        if argv[2] == '1':
            savable = 0
            for dir in sizes:
                if sizes[dir] <= 100000: savable += sizes[dir]
            print(savable)
        else:
            limit = 30000000 - (70000000 - sizes['/'])
            goodsizes = []
            for dir in sizes:
                if sizes[dir] >= limit: goodsizes.append(sizes[dir])
            goodsizes.sort()
            print(goodsizes[0])
    if argv[1] == '8':
        print(get_visibility(argv[3],argv[2]))
    if argv[1] == '9':
        print(follow_rope(argv[3],argv[2]))
    if argv[1] == '10':
        instructions = init_instructions()
        program = get_program(argv[3])
        cpu = Cpu(instructions)
        if argv[2] == '1':
            cpu.get_signal = True
        elif argv[2] == '2':
            cpu.draw_image = True
        print(cpu.run(program))
    if argv[1] == '11':
        monkeys = read_monkeyfile(argv[3],argv[2])
        if argv[2] == '1': print(run_monkeygame(monkeys, 20, 3))
        else: print(run_monkeygame(monkeys, 10000, 1))
    if argv[1] == '12':
        print(find_maproute(argv[3],argv[2]))
    if argv[1] == '13':
        print(read_signal(argv[3],argv[2]))
    if argv[1] == '14':
        print(build_cavemap(argv[3],argv[2]))
    if argv[1] == '15':
        print(scanners(argv[3],argv[2]))
    if argv[1] == '16':
        print(maximise_pressure(argv[3],argv[2]))
    if argv[1] == '17':
        print(tetris(argv[3],argv[2]))
    if argv[1] == '18':
        print(get_sides(argv[3],argv[2]))
    if argv[1] == '19':
        print(do_robots(argv[3],argv[2]))
    if argv[1] == '20':
        print(shuffle(argv[3],argv[2]))
    if argv[1] == '21':
        print(monkeycount(argv[3],argv[2]))
    if argv[1] == '22':
        print(monkeymap(argv[3],argv[2]))
    
if __name__ == "__main__":
    main(sys.argv)
    
from itertools import combinations_with_replacement, permutations
from math import prod

#jos vieläkin on liian hidas, ruvetaan välimuistittamaan robottitehtaiden tiloja ja palataan niihin, ei simuloida alusta

class Robotfactory:
    def __init__(self, number:int, blueprint:str) -> None:
        self.number = number
        self.prices = dict()
        self.stores = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
        self.robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
        self.building = None
        blueprintlist = blueprint[:-1].strip().split('.')
        for item in blueprintlist:
            itemlist = item.strip().split(' ')
            i = 4
            materials = dict()
            while i < len(itemlist):
                materials[itemlist[i+1]] = int(itemlist[i])
                i += 3
            self.prices[itemlist[1]] = materials
        self.maxprices = dict()
        for resource in self.stores:
            if resource != 'geode':
                pricelist = []
                for prices in self.prices.values():
                    nextprice = prices.get(resource, None)
                    if nextprice != None: pricelist.append(nextprice)
                self.maxprices[resource] = max(pricelist)
                pass

    def reset(self):
        self.stores = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
        self.robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
        self.building = None

    def build(self):
        if self.building != None:
            self.robots[self.building] += 1
            self.building = None 

    def start_building(self, newrobo):
        for material in self.prices[newrobo]:
            if self.stores[material] < self.prices[newrobo][material]: return False
        for material in self.prices[newrobo]:
            self.stores[material] -= self.prices[newrobo][material]
        self.building = newrobo
        return True

    def get_materials(self):
        for robot in self.robots:
            self.stores[robot] += self.robots[robot]

def has_been_tried(x, tried):
    for item in tried:
        same = True
        for i, y in enumerate(item):
            if y != x[i]:
                same = False
                break
        if same: return True
    return False

def next_robotsequence(robotsequence,prices,length=24):
    robotcodes = {'ore': 1, 'clay': 2,'obsidian': 3, 'geode': 4}
    if len(robotsequence) < 1: 
        robotsequence = []
        return []
    if robotsequence[-1] < 4:
        robotsequence[-1] += 1
        rangeous = length-len(robotsequence)
        for i in range(rangeous):
            robotsequence.append(1)
    else: robotsequence = next_robotsequence(robotsequence[:-1],prices,length).copy()
    #testataan onko sekvenssi toivoton
    ishopeless = False
    hasgeode = False
    while not hasgeode:
        try:
            firstgeode = robotsequence.index(4)
            hasgeode = True
        except ValueError:
            if robotsequence == []: return []
            robotsequence = next_robotsequence(robotsequence[:-1],prices,length).copy()
    hopelessindex = -1
    for material in prices:
        if robotsequence[:firstgeode].count(robotcodes[material]) > prices[material]:
            ishopeless = True
            index = [i for i, n in enumerate(robotsequence) if n == robotcodes[material]][prices[material]]
            if index > hopelessindex: hopelessindex = index
    if ishopeless: robotsequence = next_robotsequence(robotsequence[:hopelessindex],prices,length).copy()
    return robotsequence

def run_factory(robotfactory, spec='1'):
    robotcodes = {1: 'ore', 2: 'clay', 3: 'obsidian', 4: 'geode'}
    reversecode = dict()
    for i in robotcodes.values():
        reversecode[i] = list(robotcodes.keys())[list(robotcodes.values()).index(i)]
    robots = dict()
    robots['ore'] = 1 
    t_max = 24
    if spec == '2': t_max = 32
    maxgeodes = 0
    newrobo = 'ore'
    robotsequence = [newrobo]
    autosequence = []
    bannedrobos = set()
    autopilot = False
    complete = False
    while not complete:
        t = 0
        lastchoice = t
        if autopilot:
            newrobo = autosequence.pop(0)
            robotsequence = [newrobo]
        while t < t_max:
            #if newrobo == 'ore' and t >= t_max-robotfactory.maxprices['ore']-2:
                #liian myöhäistä rakentaa orebottia
            #    newrobo = 'clay'
            #    robotsequence[-1] = 'clay'
            #    robotfactory.lose_materials(t-lastchoice)
            #    t = lastchoice
            if newrobo != 'geode':
                if robotfactory.stores[newrobo] + (t_max-t)*robotfactory.robots[newrobo] >= (t_max-t)*robotfactory.maxprices[newrobo]:
                    bannedrobos.add(newrobo)
                    for i in range(1,5):
                        robot = robotcodes[i]
                        if robot in bannedrobos: continue
                        if robot != 'geode':
                            if robotfactory.stores[robot] + (t_max-t)*robotfactory.robots[robot] >= (t_max-t)*robotfactory.maxprices[robot]:
                                bannedrobos.add(robot)
                                continue
                        newrobo = robot
                        lastchoice = t
                        break
                    continue
            if t<t_max-1:
                if robotfactory.start_building(newrobo) and t<t_max-1:
                    if autopilot:
                        if len(autosequence) > 0: newrobo = autosequence.pop(0)
                        else: autopilot = False
                    if not autopilot:
                        for i in range(1,5):
                            robot = robotcodes[i]
                            if robot in bannedrobos: continue
                            if robot != 'geode':
                                if robotfactory.stores[robot] + (t_max-t)*robotfactory.robots[robot] >= (t_max-t)*robotfactory.maxprices[robot]:
                                    bannedrobos.add(robot)
                                    continue
                            newrobo = robot
                            lastchoice = t
                            break
                    robotsequence.append(newrobo)
            robotfactory.get_materials()
            robotfactory.build()
            t += 1
        if robotfactory.stores['geode'] > maxgeodes: maxgeodes = robotfactory.stores['geode']
        while robotsequence[-1] == 'geode':
            lastrobo = robotsequence.pop()
            if lastrobo != 'geode':
                robotsequence.append(robotcodes[reversecode[lastrobo]+1])
            if lastrobo == 'geode' and len(robotsequence) == 0:
                complete = True
                break
        if not complete: 
            robotsequence[-1] = robotcodes[reversecode[robotsequence[-1]]+1]
            autosequence = robotsequence.copy()
            robotsequence = []
            autopilot = True
            bannedrobos = set()
            robotfactory.reset()
    print(maxgeodes)
    if spec == '1': return robotfactory.number * maxgeodes
    return maxgeodes

def do_robots(file, spec):
    robotfactories = []
    with open(file, 'r') as f:
        for line in f:
            if len(line) < 1: break
            items = line.strip().split(': ')
            bpnumber = int(items[0].split(' ')[-1])
            if spec == '2' and bpnumber > 3: break
            robotfactories.append(Robotfactory(bpnumber,items[1]))
    if spec=='1': return sum(run_factory(robotfactory) for robotfactory in robotfactories)
    else: return prod(run_factory(robotfactory, spec) for robotfactory in robotfactories)

from itertools import combinations_with_replacement, permutations

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

def next_robotsequence(robotsequence,prices):
    robotcodes = {'ore': 1, 'clay': 2,'obsidian': 3, 'geode': 4}
    if len(robotsequence) < 1: 
        robotsequence = []
        return []
    if robotsequence[-1] < 4:
        robotsequence[-1] += 1
        rangeous = 24-len(robotsequence)
        for i in range(rangeous):
            robotsequence.append(1)
    else: robotsequence = next_robotsequence(robotsequence[:-1],prices).copy()
    #testataan onko sekvenssi toivoton
    ishopeless = False
    hasgeode = False
    while not hasgeode:
        try:
            firstgeode = robotsequence.index(4)
            hasgeode = True
        except ValueError:
            if robotsequence == []: return []
            robotsequence = next_robotsequence(robotsequence[:-1],prices).copy()
    hopelessindex = -1
    for material in prices:
        if robotsequence[:firstgeode].count(robotcodes[material]) > prices[material]:
            ishopeless = True
            index = [i for i, n in enumerate(robotsequence) if n == robotcodes[material]][prices[material]]
            if index > hopelessindex: hopelessindex = index
    if ishopeless: robotsequence = next_robotsequence(robotsequence[:hopelessindex],prices).copy()
    return robotsequence


def run_factory(robotfactory):
    robotcodes = {1: 'ore', 2: 'clay', 3: 'obsidian', 4: 'geode'}
    robots = dict()
    robots['ore'] = 1 
    t_max = 24
    tried = []
    maxgeodes = 0
    robotsequence = []
    for i in range(t_max):
        robotsequence.append(1)
    while robotsequence != []:        
        xit = iter(robotsequence)
        newrobo = robotcodes[next(xit)]
        buildorder = [newrobo]
        t = 0
        while t < t_max:
            if robotfactory.start_building(newrobo) and t<t_max-1:
                if newrobo != 'geode':
                    if robotfactory.stores[newrobo] + (t_max-t)*robotfactory.robots[newrobo] >= (t_max-t)*robotfactory.maxprices[newrobo]:
                        #sub-optimaalinen robotti rakennettu, skippaa loput
                        t = t_max-1
                newrobo = robotcodes[next(xit)]
                buildorder.append(newrobo)
            robotfactory.get_materials()
            robotfactory.build()
            t += 1
        if robotfactory.stores['geode'] > maxgeodes: maxgeodes = robotfactory.stores['geode']
        robotsequence = robotsequence[:sum(robotfactory.robots.values())]   #viimeistä robottia ei ehditty rakentaa
        robotsequence = next_robotsequence(robotsequence,robotfactory.maxprices).copy()
        robotfactory.reset()
        if robotsequence == [4]: break
    return robotfactory.number * maxgeodes

def do_robots(file, spec):
    robotfactories = []
    with open(file, 'r') as f:
        for line in f:
            if len(line) < 1: break
            items = line.strip().split(': ')
            bpnumber = int(items[0].split(' ')[-1])
            robotfactories.append(Robotfactory(bpnumber,items[1]))
    return sum(run_factory(robotfactory) for robotfactory in robotfactories)
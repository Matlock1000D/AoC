from operator import attrgetter

class Pathobj:
    def __init__(self, path:list, pressure:int, t:int) -> None:
        self.path = path
        self.pressure = pressure
        self.t = t
    
    def current(self):
        return self.path[-1]
class Valve:
    def __init__(self, name:str, flowrate:int, linkedvalves:list) -> None:
        self.name = name
        self.flowrate = flowrate
        self.linkedvalves = linkedvalves
        self.open = False

    def open_valve(self):
        self.open = True

    def close_valve(self):
        self.open = False

def open_valve(valve:Valve):
    valve.open = True

def find_distances(valvename, valves):  #ei kovin optimoitu tai nätti, mutta saa kelvata
    goodvalves = []
    for valve in valves.values():
        if valve.flowrate > 0: goodvalves.append(valve.name)
    distances = {}
    for valve in goodvalves:
        dist = 1    #aloitetaan yhdestä, koska avaaminen vie yhden sekunnin
        paths = [[valvename]]
        found = False
        while found == False:
            newpaths = []
            for path in paths:
                if path[-1] == valve:
                    found = True
                    break
                for linkedvalve in valves[path[-1]].linkedvalves:
                    if linkedvalve not in path:
                        newpath = path.copy()
                        newpath.append(linkedvalve)
                        newpaths.append(newpath)
            if not found:
                dist += 1
                paths = newpaths
        distances[valve] = dist
    return distances

def find_distances(valvename, valves):  #ei kovin optimoitu tai nätti, mutta saa kelvata
    goodvalves = []
    for valve in valves.values():
        if valve.flowrate > 0: goodvalves.append(valve.name)
    distances = {}
    for valve in goodvalves:
        dist = 1    #aloitetaan yhdestä, koska avaaminen vie yhden sekunnin
        paths = [[valvename]]
        found = False
        while found == False:
            newpaths = []
            for path in paths:
                if path[-1] == valve:
                    found = True
                    break
                for linkedvalve in valves[path[-1]].linkedvalves:
                    if linkedvalve not in path:
                        newpath = path.copy()
                        newpath.append(linkedvalve)
                        newpaths.append(newpath)
            if not found:
                dist += 1
                paths = newpaths
        distances[valve] = dist
    return distances

def maximise_pressure(file, spec):
    valves = {}
    with open(file, 'r') as f:
        for line in f:
            if len(line) < 9: break
            linelist = line.split(' ')
            name = linelist[1]
            flowrate = int(linelist[4].split('=')[1][:-1])  #puolipiste pois
            linkedvalves = linelist[9:]
            for i, value in enumerate(linkedvalves): linkedvalves[i] = value[:-1] #jämämerkit pois lopusta
            valves[name] = Valve(name, flowrate, linkedvalves)
    if spec == '1': max_t = 30
    else: max_t = 26
    t = 0
    #rakennetaan taulukko etäisyyksistä kelvollisille venttiileille
    maxpres = 0
    goodvalves = {'AA':find_distances('AA', valves)}
    for valve in valves.values():
        if valve.flowrate > 0:
            goodvalves[valve.name] = find_distances(valve.name, valves)
    valves['AA'].open_valve()   #avataan, niin algoritmi ei yritä tänne
    paths = [Pathobj(['AA'],0,0)]
    manpaths = set()
    while True:
        newpathobjs = []
        for pathobj in paths:
            for nextvalve in goodvalves[pathobj.current()]:
                time_remaining = max_t - pathobj.t
                if (goodvalves[pathobj.current()][nextvalve] <= time_remaining) and nextvalve not in pathobj.path:    #kuluvan ajan pitää olla pienempi kuin jäljelläoleva aika, koska ei ole järkevää kääntää venttiiliä, ellei se ehdi päästämään kaasua ainakin sekunnin ajan
                    newpath = list(pathobj.path)
                    newpath.append(nextvalve)
                    t = pathobj.t+goodvalves[pathobj.current()][nextvalve]
                    pressure = pathobj.pressure + (max_t-t) * valves[nextvalve].flowrate
                    newpathobjs.append(Pathobj(newpath,pressure,t))
        if len(newpathobjs) == 0: break
        else:
            paths = list(newpathobjs)
            manpaths.update(paths)
    if spec == '1': return(max(x.pressure for x in paths))
    goodpaths = set()
    for pathobj in manpaths:
        pathobj.path.sort()
        goodpaths.add(tuple(pathobj.path))
    goodpressures = {}
    for x in goodpaths:
        goodpressures[x] = max((y for y in manpaths if tuple(y.path) == x), key=attrgetter('pressure')).pressure
    for combination in goodpressures:
        for valve in goodvalves:
            valves[valve].close_valve()
        for valve in combination:
            valves[valve].open_valve()
        elepaths = [Pathobj(['AA'],goodpressures[combination],0)]
        k = 1
        while True:
            newpathobjs = []
            for pathobj in elepaths:
                if len(pathobj.path) == k:
                    for nextvalve in goodvalves[pathobj.current()]:
                        time_remaining = max_t - pathobj.t
                        if (not valves[nextvalve].open) and (goodvalves[pathobj.current()][nextvalve] < time_remaining) and (nextvalve not in pathobj.path):
                            newpath = list(pathobj.path)
                            newpath.append(nextvalve)
                            t = pathobj.t+goodvalves[pathobj.current()][nextvalve]
                            pressure = pathobj.pressure + (max_t-t) * valves[nextvalve].flowrate
                            newpathobjs.append(Pathobj(newpath,pressure,t))
            if len(newpathobjs) == 0: break #elepathsit tälle pathille
            else: 
                elepaths += list(newpathobjs)
                k += 1
        tempmax = max((x for x in elepaths), key=attrgetter('pressure')).pressure
        if maxpres < tempmax: 
            maxpres = tempmax
            maxpath = (combination,elepaths)
    return maxpres
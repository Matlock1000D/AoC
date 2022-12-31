from copy import deepcopy

class Pathobj:
    def __init__(self, path, pressure, t) -> None:
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
    path = ['AA']
    opened = False
    dontopen = False
    maximum = 0
    temp_maximum = 0
    timedir = 1 #1 = eteen, -1 = taakse
    dontgo = ''
    if 1==2:
        while True:
            if timedir == 1:
                current = path[-1] 
                if valves[current].flowrate > 0 and not valves[current].open and not dontopen:
                    valves[current].open_valve()
                    path.append(current)
                    opened = True
                    t += 1
                    temp_maximum += (max_t - t) * valves[current].flowrate
                else:
                    try: last = path[-2]
                    except: last = []
                    if last == current: last = path[-3]
                    if dontgo != '': dontgo_index = valves[current].linkedvalves.index(dontgo)+1
                    else: dontgo_index = 0
                    foundway = False
                    for linkedvalve in valves[current].linkedvalves[dontgo_index:]:    #iteroidaan reittejä, kunnes löytyy sopiva
                        if opened == False and linkedvalve == last: continue    #turha palata ellei ole avattu mitään
                        #liikutaan seuraavaan paikkaan
                        path.append(linkedvalve)
                        opened = False
                        dontopen = False
                        t += 1
                        foundway = True
                        dontgo = ''
                        break
                    if not foundway: timedir = -1
                if t >= max_t-1:
                    if maximum < temp_maximum: maximum = temp_maximum
                    timedir = -1
            if timedir == -1:
                current = path[-1]
                if opened == True:
                    valves[current].close_valve()
                    path.pop()
                    opened = False
                    dontopen = True
                    temp_maximum -= (max_t - t) * valves[current].flowrate
                    t-=1
                    timedir = 1
                else:
                    if t == 0: return maximum
                    path.pop()
                    if t > 1:
                        if path[-1] == path[-2]: opened = True
                        else: opened = False
                    else: opened = False
                    dontgo = current
                    t-=1
                    timedir = 1
    else:
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
                    if (goodvalves[pathobj.current()][nextvalve] < time_remaining) and nextvalve not in pathobj.path:    #kuluvan ajan pitää olla pienempi kuin jäljelläoleva aika, koska ei ole järkevää kääntää venttiiliä, ellei se ehdi päästämään kaasua ainakin sekunnin ajan
                        newpath = pathobj.path.copy()
                        newpath.append(nextvalve)
                        t = pathobj.t+goodvalves[pathobj.current()][nextvalve]
                        pressure = pathobj.pressure + (max_t-t) * valves[nextvalve].flowrate
                        newpathobjs.append(Pathobj(newpath,pressure,t))
            if len(newpathobjs) == 0: break
            else:
                paths = newpathobjs.copy()
                manpaths.update(paths)
        if spec == '1': return(max(x.pressure for x in paths))
        goodpaths = set()
        for pathobj in manpaths:
            pathobj.path.sort()
            goodpaths.add(tuple(pathobj.path))
        goodpressures = {}
        for x in goodpaths:
            goodpressures[x] = max(y.pressure for y in manpaths if tuple(y.path) == x)
        for combination in goodpressures:
            for valve in goodvalves:
                valves[valve].close_valve()
            for valve in combination:
                valves[valve].open_valve()
            elepaths = [Pathobj(['AA'],goodpressures[combination],0)]
            while True:
                newpathobjs = []
                for pathobj in elepaths:
                    for nextvalve in goodvalves[pathobj.current()]:
                        time_remaining = max_t - pathobj.t
                        if (not valves[nextvalve].open) and (goodvalves[pathobj.current()][nextvalve] < time_remaining) and (nextvalve not in pathobj.path):
                            newpath = pathobj.path.copy()
                            newpath.append(nextvalve)
                            t = pathobj.t+goodvalves[pathobj.current()][nextvalve]
                            pressure = pathobj.pressure + (max_t-t) * valves[nextvalve].flowrate
                            newpathobjs.append(Pathobj(newpath,pressure,t))
                if len(newpathobjs) == 0: break #elepathsit tälle pathille
                else: elepaths = newpathobjs.copy()
            tempmax = max(x.pressure for x in elepaths)
            if maxpres < tempmax: 
                maxpres = tempmax
                maxpath = (combination,elepaths)
        return maxpres

#2144
#2397
#2409
#2562
#2577
#2581

    """Liian hidas tämäkin
    else:
        path = ['AA','AA']
        dontopen = [False,False]
        opened = [False,False]
        dontgo = ['','']
        while True:
            if timedir == 1:
                current = path[-2] 
                if valves[current].flowrate > 0 and not valves[current].open and not dontopen[t%2]:
                    valves[current].open_valve()
                    path.append(current)
                    opened[t%2] = True
                    t += 1
                    temp_maximum += (max_t - t)//2 * valves[current].flowrate
                else:
                    try: last = path[-3]
                    except: last = []
                    if t == 1: last == []
                    elif last == current: last = path[-5]
                    if dontgo[t%2] != '': dontgo_index = valves[current].linkedvalves.index(dontgo[t%2])+1
                    else: dontgo_index = 0
                    foundway = False
                    for linkedvalve in valves[current].linkedvalves[dontgo_index:]:    #iteroidaan reittejä, kunnes löytyy sopiva
                        if opened[t%2] == False and linkedvalve == last: continue    #turha palata ellei ole avattu mitään
                        #liikutaan seuraavaan paikkaan
                        path.append(linkedvalve)
                        opened[t%2] = False
                        dontopen[t%2] = False
                        dontgo[t%2] = ''
                        t += 1
                        foundway = True
                        break
                    if not foundway: timedir = -1
                if t >= max_t-2 or sum(1 for x in valves.values() if x.open) >= goodvalves:    #lopussa, jos aika on loppu tai kaikki venttiilit ovat auki
                    if maximum < temp_maximum: maximum = temp_maximum
                    timedir = -1
            if timedir == -1:
                current = path[-1]
                if opened[t%2] == True:
                    valves[current].close_valve()
                    opened[t%2] = False
                    dontopen[t%2] = True
                    path.pop()
                    temp_maximum -= (max_t - t)//2 * valves[current].flowrate
                    t-=1
                    timedir = 1
                else:
                    if t == 0: return maximum
                    path.pop()
                    if t > 2:
                        if path[-1] == path[-3]: opened[t%2] = True
                        else: opened[t%2] = False
                    else: opened[t%2] = False
                    dontgo[t%2] = current
                    t-=1
                    timedir = 1
    """

    """Liian hidasta
    for t in range(max_t):
        newpaths = []
        for path in paths:
            #väännetäänkö hanaa
            if valves[path[-1][0]].flowrate > 0 and path[-1][0] not in path[-1][2]:
                #voidaan vääntää, lisätään uusiin reitteihin versio, jossa hana on auki
                newpath = path.copy()
                newpath.append((path[-1][0],path[-1][1]+valves[path[-1][0]].flowrate,path[-1][2]))
                newpaths.append(newpath)
            #seuraaville hanoille
            for next in valves[path[-1][0]].linkedvalves:
                newpath = path.copy()
                newpath.append((next,path[-1][1],path[-1][2].copy()))
                newpaths.append(newpath)
        #toivottomien reittien eliminointi
        deletables = [] #lista kelvottomien reittiehdokkaiden indekseistä
        for i, newpath in enumerate(newpaths):
            next_valve = newpath[-1][0]
            next_pressure = newpath[-1][1]
            next_opens = newpath[-1][2]
            useless = False
            for oldpath in paths:
                for oldvalves in oldpath:
                    for j, oldvalve in enumerate(oldvalves[2]): #oldvalve tuple, käytyjen paikkojen historia
                        if oldvalve[0] == next_valve and oldvalve[1] >= next_pressure:
                            if True: #next_opens in oldvalve[2]:
                                deletables.append[i]
                                useless = True
                                break
                    if useless: break
        for index in sorted(deletables, reverse=True):
            del newpaths[index]
            

        ##reitit, joissa palataan jo käytyyn paikkaan ilman, että paine on noussut välissä
        #jos on olemassa reitti, jossa on jo käyty samalla hanalla ja 
            #for i, newpath in enumerate(newpaths):
        paths = newpaths.copy()
        #paths tyhjenee, debuggaa
    return paths
    """
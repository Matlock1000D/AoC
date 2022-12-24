#tutki päätöksentekopuuta
#säilytä liikehistoria
#heitä mäkeen haarat, joissa ollaan samassa pisteessä kuin joku aiempi reitti, mutta aikaa on kulunut enemmän eikä painetta ole enempää

#tee venttiililuokka
#nimi, flowrate, linkedvalves-lista

#133 on liian vähän

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


def maximise_pressure(file, spec):
    valves = {}
    #paths = []
    with open(file, 'r') as f:
        for line in f:
            if len(line) < 9: break
            linelist = line.split(' ')
            name = linelist[1]
            flowrate = int(linelist[4].split('=')[1][:-1])  #puolipiste pois
            linkedvalves = linelist[9:]
            for i, value in enumerate(linkedvalves): linkedvalves[i] = value[:-1] #jämämerkit pois lopusta
            valves[name] = Valve(name, flowrate, linkedvalves)

    #path = [('AA',0,[])]    #Nykytila, paine, avonaiset hanat
    #paths.append(path)
    max_t = 30
    t = 0
    path = ['AA']
    opened = False
    dontopen = False
    maximum = 0
    temp_maximum = 0
    timedir = 1 #1 = eteen, -1 = taakse
    dontgo = ''
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
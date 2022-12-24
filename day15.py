class Sensor:
    def __init__(self, pos:tuple, beacon:tuple) -> None:
        self.pos = pos
        self.beacon = beacon
        self.range = abs(pos[0]-beacon[0])+abs(pos[1]-beacon[1])
        pass

def manhattan_dist(pos1:tuple, pos2:tuple):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def scanners(file, spec):
    sensors = []
    targetrow = 2000000
    searcharea = (0,4000000)
    with open(file, 'r') as f:
        for line in f:
            lst_line = line.split(' ')  #sisältää rivinvaihdot
            sens_x = int(lst_line[2][2:-1])
            sens_y = int(lst_line[3][2:-1])
            beacon_x = int(lst_line[8][2:-1])
            beacon_y = int(lst_line[9][2:-1])
            sensor = Sensor((sens_x,sens_y),(beacon_x,beacon_y))
            sensors.append(sensor)
    #”maalataan” mahdottomat paikat rivillä
    if spec == '1': searchrows = range(targetrow,targetrow+1)
    else: searchrows = range(searcharea[0],searcharea[1]+1)
    for y in searchrows:
        if spec == '2': break
        impossibles = set()
        for sensor in sensors:
            yrange = abs(targetrow-sensor.pos[1])
            xrange = sensor.range-yrange
            if xrange >= 0: impossibles.update(range(sensor.pos[0]-xrange,sensor.pos[0]+xrange+1))
            if sensor.beacon[1] == targetrow: impossibles.discard(sensor.beacon[0]) 
        if spec == '1': return len(impossibles)
        if spec == '2':
            for x in searcharea:
                if x not in searcharea: return (x,y)
    x = y = searcharea[0]
    while y <= searcharea[1]:
        while x <= searcharea[1]:
            norange = True
            for sensor in sensors:
                if manhattan_dist((x,y),sensor.pos) <= sensor.range: 
                    norange = False
                    #siirretään x kantaman reunalle, muuten kestää liian kauan
                    yrange = abs(y-sensor.pos[1])
                    xrange = sensor.range-yrange
                    x = sensor.pos[0]+xrange
                    break
            if norange: return 4000000 * x + y
            x += 1
        y += 1
        x = searcharea[0]
    return -1

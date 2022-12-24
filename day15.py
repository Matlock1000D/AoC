class Sensor:
    def __init__(self, pos:tuple, beacon:tuple) -> None:
        self.pos = pos
        self.beacon = beacon
        self.range = abs(pos[0]-beacon[0])+abs(pos[1]-beacon[1])
        pass

def scanners(file, spec):
    sensors = []
    targetrow = 2000000
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
    impossibles = set()
    for sensor in sensors:
        yrange = abs(targetrow-sensor.pos[1])
        xrange = sensor.range-yrange
        if xrange >= 0: impossibles.update(range(sensor.pos[0]-xrange,sensor.pos[0]+xrange+1))
        if sensor.beacon[1] == targetrow: impossibles.discard(sensor.beacon[0]) 
    return len(impossibles)

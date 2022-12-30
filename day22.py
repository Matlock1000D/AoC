import numpy as np

class Edge:
    def __init__(self, leftcorner, dir, connectededge) -> None:
        self.co = leftcorner    #reunan vasen nurkka sivun sisältä katsoen
        self.dir = np.array(dir)          #suunta ulospäin
        self.conedge = connectededge #missä nurkassa kiinni

def get_manhattandist(p1,p2):
    return sum(abs(p1[i]-p2[i]) for i in range(len(p1)))

def dirnum(dirmatrix)->int:
    return 1 -dirmatrix[0] + abs(dirmatrix[1])*(1 - dirmatrix[1]) 

def monkeymap(file, spec):
    linemap = []
    with open(file, 'r') as f:
        for line in f:
            linelist = []
            linelist[:0] = line[:-1]
            if len(linelist) < 1: break
            linemap.append(linelist)
        maxx = max(len(x) for x in linemap)
        for i, line in enumerate(linemap):
            if len(line) < maxx:
                linemap[i] += [' '] * (maxx - len(line))
        maparr = np.transpose(np.array(linemap))    #ärsyttää numpyn käänteinen logiikka
        instructions = f.readline().strip()

    if spec == '3':
        edgesize = 4
        edges = ({0: Edge((8,0),[0,-1],11),
            1:  Edge((11,0),[1,0],4),
            2:  Edge((11,4),[1,0],3),
            3:  Edge((12,8),[0,-1],2),
            4:  Edge((15,8),[1,0],1),
            5:  Edge((15,11),[0,1],10),
            6:  Edge((11,11),[0,1],9),
            7:  Edge((8,11),[-1,0],8),
            8:  Edge((7,7),[0,1],7),
            9:  Edge((3,7),[0,1],6),
            10:  Edge((0,7),[-1,0],5),
            11:  Edge((0,4),[0,-1],0),
            12:  Edge((4,4),[0,-1],13),
            13:  Edge((8,3),[-1,0],12)
            })

    if spec == '2':
        edgesize = 50
        edges = ({0: Edge((50,0),[0,-1],9),
            1:  Edge((100,0),[0,-1],8),
            2:  Edge((149,0),[1,0],5),
            3:  Edge((149,49),[0,1],4),
            4:  Edge((99,50),[1,0],3),
            5:  Edge((99,100),[1,0],2),
            6:  Edge((99,149),[0,1],7),
            7:  Edge((49,150),[1,0],6),
            8:  Edge((49,199),[0,1],1),
            9:  Edge((0,199),[-1,0],0),
            10:  Edge((0,149),[-1,0],13),
            11:  Edge((0,100),[0,-1],12),
            12:  Edge((50,99),[-1,0],11),
            13:  Edge((50,49),[-1,0],10)
            })
    
    #Etsitään aloitusruutu
    startx = linemap[0].index('.')
    start = (startx,0)
    pos = start
    left = np.array([[0,1],[-1,0]])
    right = np.array([[0,-1],[1,0]])
    rotations = {'L': left, 'R':right}
    dir = np.array([1,0])
    
    #etsitään pelialueen rajat
    #oletetaan, ettei ole pelkkiä seiniä sisältäviä rivejä
    linelimits = []
    for line in linemap:
        try:
            startx = line.index('#')
        except: startx = 1000000000
        if line.index('.') < startx: startx = line.index('.')
        try: endx = line[startx:].index(' ')+startx
        except: endx = len(line)
        linelimits.append((startx,endx))
    columnlimits = []
    for i in range(len(linemap[0])):
        col=[]
        for row in linemap:
            col.append(row[i])
        try:
            starty = col.index('#')
        except: starty = 1000000000
        if col.index('.') < starty: starty = col.index('.')
        try: endy = col[starty:].index(' ')+starty
        except: endy = len(col)
        columnlimits.append((starty,endy))

    while len(instructions) > 0:
        for i in range(1,len(instructions)):
            if instructions[0].isnumeric() != instructions[i].isnumeric(): break
            i = i+1
        instruction = ''.join(instructions[:i])
        instructions = instructions[i:]
        #toimi ohjeen mukaan
        ##liike eteenpäin
        if instruction.isnumeric():
            steps = int(instruction)
            for step in range(steps):
                if spec == '1':
                    nextpos = [pos[0]+dir[0],pos[1]+dir[1]]
                    if nextpos [0] < linelimits[pos[1]][0]: nextpos[0]=linelimits[pos[1]][1]-1
                    if nextpos [0] >= linelimits[pos[1]][1]: nextpos[0]=linelimits[pos[1]][0]
                    if nextpos [1] < columnlimits[pos[0]][0]: nextpos[1]=columnlimits[pos[0]][1]-1
                    if nextpos [1] >= columnlimits[pos[0]][1]: nextpos[1]=columnlimits[pos[0]][0]
                    if not maparr[tuple(nextpos)] == '#': pos = nextpos
                    else: break
                else:
                    nextpos = []
                    crossingedge = False
                    for e in edges:
                        if np.array_equal(edges[e].dir, dir):     #reunan yli voidaan astua vain, jos ollaan menossa siitä ”ulospäin”
                            edgeendx = edges[e].co[0] + np.matmul(right,edges[e].dir)[0] * (edgesize-1)
                            if edges[e].co[0] < edgeendx:
                                x1 = edges[e].co[0]
                                x2 = edgeendx
                            else:
                                x1 = edgeendx
                                x2 = edges[e].co[0]
                            edgeendy = edges[e].co[1] + np.matmul(right,edges[e].dir)[1] * (edgesize-1)
                            if edges[e].co[1] < edgeendy:
                                y1 = edges[e].co[1]
                                y2 = edgeendy
                            else:
                                y1 = edgeendy
                                y2 = edges[e].co[1]
                            
                            if pos[0] in range(x1,x2+1) and pos[1] in range(y1,y2+1):
                                crossingedge = True
                                dist = get_manhattandist(edges[e].co,pos)
                                nextedge = edges[e].conedge
                                for j in range(2):
                                    nextpos.append(edges[nextedge].co[j] + np.matmul(right, edges[nextedge].dir)[j]*(edgesize-dist-1))
                                    #demon ekalla kerralla pitäisi päätyä 14,8:aan
                                if not maparr[tuple(nextpos)] == '#':
                                    pos = nextpos
                                    dir = np.matmul(right,np.matmul(right,edges[nextedge].dir))
                                    break
                    if not crossingedge: 
                        nextpos = [pos[0]+dir[0],pos[1]+dir[1]]
                        if not maparr[tuple(nextpos)] == '#': pos = nextpos
                        else: break
            
        if instruction in rotations:
            dir = np.matmul(rotations[instruction],dir)

    return 1000 * (pos[1]+1) + 4 * (pos[0]+1) + dirnum(dir)
    #palauta lopputuloksen 1000 * rivi + 4 * sarake + suunta
    #77379 too low

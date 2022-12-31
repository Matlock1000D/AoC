import numpy as np
from copy import deepcopy

def tupsum(tup1:tuple, tup2:tuple)->tuple:
    return tuple(sum(tup) for tup in zip(*[tup1,tup2]))

def blizzards(file, spec):
    stage = 0
    blizzmap = []
    markers = { '.': 0, '^': 1, '<': 2, 'v': 4, '>': 8}
    dirs = {1: (0,-1), 2: (-1,0), 4: (0,1), 8: (1,0)}
    with open(file, 'r') as f:
        goal = f.readline()
        for i, x in enumerate(goal.strip()[1:-1]):
            if x == '.': 
                startx = i
                break
        for line in f:
            if not (line[1] == '#' and line[2] == '#'):
                blizzline = list(map(lambda x: markers[x], [*line.strip()[1:-1]]))
                blizzmap.append(blizzline)
            else:
                for i, x in enumerate(line.strip()[1:-1]):
                    if x == '.': 
                        goalx = i
                        break
    blizzarr = np.transpose(np.array(blizzmap,int))
    xlen = blizzarr.shape[0]
    ylen = blizzarr.shape[1]

    startpos = (startx,-1)
    goalpos = (goalx,ylen)
    players = set([startpos])

    goalin = False
    t=0
    while not goalin:
        t += 1
        #liikutetaan myrskyjä
        nextmap = deepcopy(blizzarr)
        for i in [1,2,4,8]:
            nit = np.nditer(blizzarr, flags=['multi_index'])
            for k in nit:
                if i & k:
                    nextindex = list(tupsum(nit.multi_index,dirs[i]))
                    nextindex[0] = nextindex[0]%xlen
                    nextindex[1] = nextindex[1]%ylen
                    nextmap[nit.multi_index] -= i
                    nextmap[tuple(nextindex)] += i
        blizzarr = deepcopy(nextmap)

        #kartoitetaan pelaajan liikkeet
        nextplayer = set()
        nextstage = False
        for player in players:
            newmoves = []
            if player[1] == -1 or player[1] == ylen: newmoves.append(player)
            elif blizzarr[player] == 0: newmoves.append(player)
            for target in [(0,1),(1,0),(-1,0),(0,-1)]:
                newpos = tupsum(player,target)
                if newpos == goalpos:
                    if spec == '1' or stage == 2: return t
                    else:
                        stage += 1
                        players = [goalpos]
                        startpos, goalpos = goalpos, startpos
                        nextstage = True
                        break
                if newpos[0] in range(xlen) and newpos[1] in range(ylen):
                    if blizzarr[newpos] == 0: newmoves.append(newpos)
            if nextstage: break
            nextplayer.update(newmoves)
        if nextstage: continue
        players = set(nextplayer)
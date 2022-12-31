import numpy as np

class Elf:
    def __init__(self, pos:tuple) -> None:
        self.pos = pos
        self.target = None
        self.wantmove = False

def offset_coordinate(pos:tuple, offset:tuple)->tuple:
    """(0,0) kuvautuu (1,1):een tyhjän reunatilan saamiseksi"""
    result = []
    for i in range(len(pos)):
        result.append(pos[i]-offset[i]+1)
    return tuple(result)

def tupsum(tup1:tuple, tup2:tuple)->tuple:
    return tuple(sum(tup) for tup in zip(*[tup1,tup2]))


def diffusion(file,spec):
    elves = []
    directions = [[(0,-1),(-1,-1),(1,-1)],[(0,1),(-1,1),(1,1)],[(-1,0),(-1,-1),(-1,1)],[(1,0),(1,-1),(1,1)]]
    if spec == '1': maxrounds = 10
    else: maxrounds = 10000000
    with open(file, 'r') as f:
        for y, line in enumerate(f):
            for x, col in enumerate(line):
                if col == '#': elves.append(Elf((x,y)))

    for r in range(maxrounds):
        min_x = min(elf.pos[0] for elf in elves)
        max_x = max(elf.pos[0] for elf in elves)
        min_y = min(elf.pos[1] for elf in elves)
        max_y = max(elf.pos[1] for elf in elves)

        xlen = max_x-min_x+1+2  #tehdään ylimääräistä niin, että reunoilla on varmasti tilaa
        ylen = max_y-min_y+1+2
        origin = (min_x,min_y)

        elfmap = np.zeros((xlen,ylen),bool)
        for elf in elves:
            elfmap[offset_coordinate(elf.pos,origin)] = True
        
        #katsotaan liikkuuko
        for elf in elves:
            elf.wantmove = False
            elf.target = None
        for elf in elves:
            stopiter = False
            for dx in range(-1,2):
                for dy in range(-1,2):
                    if dx == dy == 0: continue
                    checkpos = tupsum(elf.pos,(dx,dy))
                    if elfmap[offset_coordinate(checkpos,origin)] == True:
                        elf.wantmove = True
                        stopiter = True
                        break
                if stopiter: break

        if spec == '2':
            movers = sum(1 for elf in elves if elf.wantmove)
            if movers == 0: return r+1

        #katsotaan mihin liikkuu
        nextmap = np.zeros(elfmap.shape, int)
        for elf in elves:
            if elf.wantmove:
                canmove = False
                for dir in directions:
                    empty = True
                    for d in dir:                      
                        checkpos = tupsum(elf.pos,d)
                        if elfmap[offset_coordinate(checkpos,origin)]:
                            empty = False
                            break
                    if empty:
                        elf.target = tupsum(elf.pos,dir[0])
                        canmove = True
                        nextmap[offset_coordinate(elf.target,origin)] += 1
                        break
                if not canmove: elf.wantmove = False
        
        #liikutetaan tonttuja
        for elf in elves:
            if elf.wantmove:
                if nextmap[offset_coordinate(elf.target,origin)] < 2:
                    elf.pos = elf.target
                else:
                    pass
        
        #päivitetään säännöt
        directions.append(directions.pop(0))

    #katsotaan lopputulos
    min_x = min(elf.pos[0] for elf in elves)
    max_x = max(elf.pos[0] for elf in elves)
    min_y = min(elf.pos[1] for elf in elves)
    max_y = max(elf.pos[1] for elf in elves)
    xlen = max_x-min_x+1
    ylen = max_y-min_y+1

    return xlen*ylen-len(elves)
    
#4099 too low
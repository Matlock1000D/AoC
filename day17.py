import numpy as np
from itertools import cycle
from math import lcm

#palikan generoinnissa ongelmaa, korjaa
#lienisi fiksumpaa luokkana, mutta ääh
#typeryyksiä shape-synonyymeillä
#demolla get_maxy = 32221, cycleheight = 1514285714157, offset = 0
#1514705882343 liian paljon
#get_maxy = 32315, offset = 771, cycleheight=1514705881535
#1507692307690

class Blocktype:
    def __init__(self, array) -> None:
        self.shape = array

class Block:
    def __init__(self, x:int,y:int, shape) -> None:
        self.x = x
        self.y = y
        self.shape = shape
        self.age = 0

    def __eq__(self, __o: object) -> bool:
        if __o == None: return False
        if self.x == __o.x and self.y == __o.y and self.shape == __o.shape: return True
        return False

class Cache:
    def __init__(self, field, block, cycles, blocks_fallen, height, windphase) -> None:
        self.field = field
        self.block = block
        self.cycles = cycles
        self.blocks_fallen = blocks_fallen
        self.height = height
        self.windphase = windphase
        pass

    def __eq__(self, __o: object) -> bool:
        if np.array_equal(self.field, __o.field) and self.block == __o.block and self.windphase == __o.windphase: return True
        return False

def windaction(field, block, dir:int) -> bool:
    xsize = field.shape[0]
    newx = block.x + dir
    if newx < 0 or newx + block.shape.shape.shape[0] > xsize: return False
    if block.age < 3: return True   #ensimmäisen kolmen liikkeen aikana ei voi törmätä kuin seiniin
    for by in range(block.shape.shape.shape[1]):
        for bx in range(block.shape.shape.shape[0]):
            if block.shape.shape[bx, by] == 1:
                if field[newx+bx, block.y+by]: return False
    return True

def get_maxy(field, lasty)->int: #pitäisi tulla 16176 ulos ensimmäisellä kutsulla, sitten kolmannella 16175
    for y in range(lasty):
        empty = True
        for x in range(field.shape[0]):
            if field[x, lasty-y-1]: 
                empty = False
                break
        if empty: return lasty-y
    raise ValueError

def drop_ok(field, block)->bool:
    if block.age < 3: return True   #ensimmäisen kolmen liikkeen aikana ei voi olla mitään tiellä
    newy = block.y+1
    if newy + block.shape.shape.shape[1]-1 >= field.shape[1]: return False
    for by in range(block.shape.shape.shape[1]):
        for bx in range(block.shape.shape.shape[0]):
            if block.shape.shape[bx, by] == 1:
                if field[block.x+bx, newy+by]: return False
    return True

def wind(windchar)->int:
    if windchar == '<': return -1
    if windchar == '>': return 1
    raise ValueError('Ei-tuettu tuulimerkki')

#määritellään palikkatyypit
def tetris(file, spec):
    blocktypes = []
    blocktypes.append(Blocktype(np.transpose(np.array([[1,1,1,1]]))))
    blocktypes.append(Blocktype(np.array([[0,1,0],[1,1,1],[0,1,0]])))
    blocktypes.append(Blocktype(np.transpose(np.array([[0,0,1],[0,0,1],[1,1,1]]))))
    blocktypes.append(Blocktype(np.transpose(np.array([[1],[1],[1],[1]]))))
    blocktypes.append(Blocktype(np.array([[1,1],[1,1]])))

#määritellään pelikenttä
    XSIZE = 7
    YSIZE = 2022*16  #tätä isompaa kenttää ei voi tarvita ykkösvaiheessa. Kokeillaan, riittääkö kakkosvaiheeseen
    field = np.zeros((XSIZE,YSIZE),dtype=bool)
    offset = 0
    if spec == '1': targetblocks = 2022
    else: targetblocks = 1000000000000

#8087 on alin rivi, 8088 lattia
#Ensimmäisen palikan pitäisi syntyä riville 8084

#luetaan tuulitiedosto
    with open(file, 'r') as f:
        windpattern = f.readline().strip()
#muut alustukset
    block = None
    blocktype_cycle = cycle(blocktypes)
    wind_cycle = cycle(windpattern)
    blocks_fallen = 0
    moves = 0
    cycleheight = 0
    lasty = YSIZE
    cycles = 0
    caches = []
    skip_cycles = True
    while blocks_fallen < targetblocks:

        if block == None:   #luodaan palikka
            blockshape = next(blocktype_cycle)
            y = get_maxy(field,lasty) - 3 - blockshape.shape.shape[1]
            x = 2
            block = Block(x,y,blockshape)


            """    
            if not np.any(field) and blockshape == blocktypes[0]:
                height = YSIZE-get_maxy(field,lasty)+offset
                cycles = targetblocks//blocks_fallen
                cycleheight = height * cycles
                blocks_fallen *= cycles"""

        while block != None:

            #tuuli
            winddir = wind(next(wind_cycle))
            if windaction(field, block, winddir): block.x += winddir
            #putoaminen
            if drop_ok(field, block):
                block.y += 1
                block.age += 1
            else: 
                for by in range(block.shape.shape.shape[1]):
                    for bx in range(block.shape.shape.shape[0]):
                        if block.shape.shape[bx, by] == 1:
                            field[block.x+bx, block.y+by] = True
                blocks_fallen += 1
                #tarkistetaan, onko syntynyt riviä (tai sitten ei, tätä ei tarvita ja tässä on bugi)
                """
                for by in range(block.shape.shape.shape[1]):
                    fullrow = True
                    for bx in range(XSIZE):
                        if not field[bx, by+block.y]: 
                            fullrow = False
                            break
                    if fullrow:
                        shift = YSIZE-block.y-by
                        np.roll(field, shift, 1)    #vieritetään kenttää alaspäin (positiivisen y-akselin suuntaan)
                        field[0:shift] = False  #nollataan yläosasta vastaava määrä rivejä
                        offset += shift         #lisätään offsetia, että tiedetään missä korkeus menee
                        block.y += shift
                        break
                lasty = block.y
                """
                #katsotaan, onko tullut toistoa
                if blocks_fallen%len(blocktypes) == 0 and skip_cycles:
                    windphase = moves%len(windpattern)
                    rely = get_maxy(field,lasty)
                    height = YSIZE-rely+offset 
                    caches.append(Cache(field[:,rely:rely+16], block, cycles, blocks_fallen, height, windphase))
                    if moves > 0:
                        for i, cache in enumerate(caches):       
                            if i < len(caches)-1:
                                if np.array_equal(cache.field,caches[len(caches)-1].field):
                                    heightdiff = caches[len(caches)-1].height - cache.height
                                    blocksdiff = caches[len(caches)-1].blocks_fallen - cache.blocks_fallen
                                    #jäljellä olevat syklit:
                                    cycles_left = (targetblocks-blocks_fallen)//blocksdiff
                                    #oiotaan syklit
                                    cycleheight = heightdiff * cycles_left
                                    blocks_fallen += cycles_left * blocksdiff
                                    skip_cycles = False
                                    break
                block = None
            moves += 1

    return YSIZE-get_maxy(field,lasty)+offset+cycleheight


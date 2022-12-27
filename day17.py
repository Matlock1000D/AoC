import numpy as np
from itertools import cycle

#lienisi fiksumpaa luokkana, mutta ääh
#typeryyksiä shape-synonyymeillä

class Blocktype:
    def __init__(self, array) -> None:
        self.shape = array

class Block:
    def __init__(self, x:int,y:int, shape) -> None:
        self.x = x
        self.y = y
        self.shape = shape

def windaction(field, block, dir:int) -> bool:
    xsize = field.shape[0]
    newx = block.x + dir
    if newx < 0 or newx + block.shape.shape.shape[0] > xsize: return False
    for by in range(block.shape.shape.shape[1]):
        for bx in range(block.shape.shape.shape[0]):
            if block.shape.shape[bx, by] == 1:
                if field[newx+bx, block.y+by]: return False
    return True

def get_maxy(field)->int:
    for y in range(field.shape[1]):
        for x in range(field.shape[0]):
            if field[x, y]: return y
    return y + 1

def drop_ok(field, block)->bool:
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
    YSIZE = 2022*4  #tätä isompaa kenttää ei voi tarvita
    field = np.zeros((XSIZE,YSIZE),dtype=bool)

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
    while blocks_fallen < 2022:
        if block == None:   #luodaan palikka
            blockshape = next(blocktype_cycle)
            y = get_maxy(field) - 3 - blockshape.shape.shape[1]
            x = 2
            block = Block(x,y,blockshape)

        while block != None:
            #tuuli
            winddir = wind(next(wind_cycle))
            if windaction(field, block, winddir): block.x += winddir
            #putoaminen
            if drop_ok(field, block):
                block.y += 1
            else: 
                for by in range(block.shape.shape.shape[1]):
                    for bx in range(block.shape.shape.shape[0]):
                        if block.shape.shape[bx, by] == 1:
                            field[block.x+bx, block.y+by] = True
                blocks_fallen += 1
                block = None
    return YSIZE-get_maxy(field)


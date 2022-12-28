import numpy as np



def count_sides(block):
    it = np.nditer(block, flags=['multi_index'])
    sides = 0
    for b in it:
        if b:
            for i in range(3):
                for x in [-1,1]:
                    co = it.multi_index[i]+x
                    if co < 0 or co >= block.shape[i]:
                        sides += 1
                        continue
                    else:
                        co_index = list(it.multi_index).copy()
                        co_index[i] += x
                        if not block[tuple(co_index)]: sides += 1
    sides = 0
    for x in range(30):
        for y in range(30):
            for z in range(30):
                if block[x,y,z]:
                    for i in range(3):
                        for j in [-1,1]:
                            co = [x,y,z]
                            co[i] = co[i]+j
                            if co[i] < 0 or co[i] >= 30:
                                sides += 1
                                continue
                            else:
                                if not block[tuple(co)]: sides += 1

    return sides

def fill_insides(block):
    emptiness = set()
    emptiness.add((0,0,0))
    newstep = [(0,0,0)]
    while len(newstep) > 0:
        laststep = newstep.copy()
        newstep = set()
        for index in laststep:
            for i in range(3):
                for j in [-1, 1]:
                    newindex = list(index)
                    newindex[i] += j
                    newindex = tuple(newindex)
                    if newindex[i] >= 0 and newindex[i]<30:
                        if not block[newindex] and newindex not in emptiness:
                            newstep.add(newindex)
        emptiness.update(newstep)
    #täytetään sisäosat
    with np.nditer(block, flags=['multi_index'], op_flags=['readwrite']) as it:
        for x in it:
            if not x:
                if it.multi_index not in emptiness:
                    x[...] = True
                        



#Tänne voisi syöttää myös luetun listan, niin ei tarvitse käydä koko matriisia läpi.

def get_sides(file, spec):
    block = np.zeros((30,30,30),dtype=bool)
    with open(file, 'r') as f:
        for line in f:
            if len(line) < 1: break
            readline = line.strip().split(',')
            #Tämä rikkoo jotenkin indeksoinnin, ei jaksa debugata. Tehdään ennemmin ”tarpeeksi iso” matriisi
            """
            for i, co in enumerate(readline):
                co = int(co)
                if block.shape[i] < co: 
                    newshape = list(block.shape)
                    newshape[i] = co
                    newshape = tuple(newshape)
                    np.resize(block, newshape)
            """
            if spec == '1':
                block[int(readline[0]),int(readline[1]),int(readline[2])] = True
            else:
                block[int(readline[0])+1,int(readline[1])+1,int(readline[2])+1] = True
    if spec == '2':
        fill_insides(block)
    return count_sides(block)

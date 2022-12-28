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
    for x in range(50):
        for y in range(50):
            for z in range(50):
                if block[x,y,z]:
                    for i in range(3):
                        for j in [-1,1]:
                            co = [x,y,z]
                            co[i] = co[i]+j
                            if co[i] < 0 or co[i] >= 50:
                                sides += 1
                                continue
                            else:
                                if not block[tuple(co)]: sides += 1

    return sides



#Tänne voisi syöttää myös luetun listan, niin ei tarvitse käydä koko matriisia läpi.

def get_sides(file, spec):
    block = np.zeros((50,50,50),dtype=bool)
    with open(file, 'r') as f:
        for line in f:
            if len(line) < 1: break
            readline = line.strip().split(',')
            """
            for i, co in enumerate(readline):
                co = int(co)
                if block.shape[i] < co: 
                    newshape = list(block.shape)
                    newshape[i] = co
                    newshape = tuple(newshape)
                    np.resize(block, newshape)
            """
            block[int(readline[0]),int(readline[1]),int(readline[2])] = True
    return count_sides(block)

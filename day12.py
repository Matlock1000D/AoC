import numpy as np

def find_maproute(file, spec):
    contours = []
    with open(file, 'r') as f:
        for y, line in enumerate(f):
            numline = []
            for x, char in enumerate(line.strip()):
                if spec == '1' and char == 'S':
                    start = (x,y)
                    char = 'a'
                if char == 'E':
                    if spec == '1': goal = (x,y)
                    else: start = (x,y)
                    char = 'z'
                numline.append(ord(char))
            contours.append(numline)
    np_contours = np.transpose(np.asarray(contours, dtype = int))

    #Etsitään reitti
    visited = [start]
    currents = [start]  #koordinaatteja
    moves = 1
    while True:
        v = len(visited)
        nextcurrents = []
        for current in currents:
            for i in range(2):
                for dir in [-1,1]:
                    if current[i]+dir >= 0 and current[i]+dir < np_contours.shape[i]:
                        next_l = list(current)
                        next_l[i] += dir
                        next_i = tuple(next_l)
                        nextheight = np_contours[next_i]
                        if spec == '1' and nextheight <= np_contours[current]+1 and next_i not in visited:
                            if next_i == goal: return moves
                            nextcurrents.append(next_i)
                            visited.append(next_i)
                        elif spec == '2' and nextheight >= np_contours[current]-1 and next_i not in visited:
                            if np_contours[next_i] == ord('a'): return moves
                            nextcurrents.append(next_i)
                            visited.append(next_i)
        currents = nextcurrents.copy()
        moves += 1
        if len(visited) == v: 
            debug = np.zeros(np_contours.shape)
            for i in visited:
                debug[i] = 1
            np.savetxt('debug.txt',debug.astype(int), fmt='%i', delimiter="")
            np.savetxt('debug2.txt',np_contours.astype(int), fmt='%i', delimiter="")
            return debug
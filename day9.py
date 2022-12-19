import numpy as np

def follow_rope(file, spec):
    head = np.array([0,0])
    tail = np.array([0,0])
    tail_visits = set()
    tail_visits.add((tail[0],tail[1]))
    directions = ({'U': np.array([0,1]),
        'D': np.array([0,-1]),
        'L': np.array([-1,0]),
        'R': np.array([1,0])})    
    with open(file, 'r') as f:
        for line in f:
            move = line.strip().split(' ')
            for i in range(int(move[1])):
                head += directions[move[0]]
                #liikuta häntää
                movement = head-tail
                if (abs(movement[0]) > 1 or abs(movement[1]) > 1):
                    for a in range(2):
                        movement[a] = int(movement[a] / abs(movement[a])) if movement[a] else 0
                    tail += movement    
                    #päivitä vierailtujen paikkojen lista
                    tail_visits.add((tail[0],tail[1]))
    return len(tail_visits)
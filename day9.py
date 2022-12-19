import numpy as np

def follow_rope(file, spec):
    if spec == '1': knot_number = 2
    else: knot_number = 10
    knots = []
    for i in range(knot_number):
        knots.append(np.array([0,0]))
    tail_visits = set()
    tail_visits.add((knots[knot_number-1][0],knots[knot_number-1][1]))
    directions = ({'U': np.array([0,1]),
        'D': np.array([0,-1]),
        'L': np.array([-1,0]),
        'R': np.array([1,0])})    
    with open(file, 'r') as f:
        for line in f:
            move = line.strip().split(' ')
            for i in range(int(move[1])):
                knots[0] += directions[move[0]]
                for j in range(knot_number-1):
                    #liikuta häntää
                    movement = knots[j]-knots[j+1]
                    if (abs(movement[0]) > 1 or abs(movement[1]) > 1):
                        for a in range(2):
                            movement[a] = int(movement[a] / abs(movement[a])) if movement[a] else 0
                        knots[j+1] += movement    
                #päivitä vierailtujen paikkojen lista
                tail_visits.add((knots[knot_number-1][0],knots[knot_number-1][1]))
    return len(tail_visits)
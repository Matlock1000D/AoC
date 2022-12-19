import numpy as np

def check_visibility(tree, it_trees, np_trees):
    index = it_trees.multi_index
    for dir in [-1, 1]:
        checkin = index[0]+dir
        visible = True
        while checkin >= 0 and checkin < np_trees.shape[0]:
            if np_trees[checkin, index[1]] >= tree: 
                visible = False
                break
            checkin += dir
        if visible: return 1
        checkin = index[1]+dir
        visible = True
        while checkin >= 0 and checkin < np_trees.shape[1]:
            if np_trees[index[0], checkin] >= tree: 
                visible = False
                break
            checkin += dir
        if visible: return 1
    return 0

def get_visibility(file, spec):
    trees = []
    with open(file, 'r') as f:
        for line in f:
            if len(line) < 1: continue
            intline = []
            for char in line.strip():
                intline.append(int(char))
            trees.append(intline)
    np_trees = np.asarray(trees, dtype=int)
    visible = 0
    it_trees = np.nditer(np_trees, flags=['multi_index'])
    for tree in it_trees:
        visible += check_visibility(tree, it_trees, np_trees)
    return visible
        



import numpy as np

def check_scenic_score(tree, it_trees, np_trees):
    index = it_trees.multi_index
    score = 1
    for dir in [-1, 1]:
        checkin = index[0]+dir
        trees = 0
        while checkin >= 0 and checkin < np_trees.shape[0]:
            trees += 1
            if np_trees[checkin, index[1]] >= tree: 
                break
            checkin += dir
        score *= trees
        checkin = index[1]+dir
        trees = 0
        while checkin >= 0 and checkin < np_trees.shape[1]:
            trees += 1
            if np_trees[index[0], checkin] >= tree:
                break
            checkin += dir
        score *= trees
    return score

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
    if spec == '1':
        for tree in it_trees:
            visible += check_visibility(tree, it_trees, np_trees)
        return visible
    else:
        top_score = 0
        for tree in it_trees:
            score = check_scenic_score(tree, it_trees, np_trees)
            if top_score < score: top_score = score
        return top_score
        



def shuffle(file, spec):
    if spec == '1': mixes = 1
    else: mixes = 10
    key = 811589153
    codes = []
    with open(file, 'r') as f:
        for i, line in enumerate(f):
            if len(line) == 0: break
            if spec == '1': codes.append((i,int(line.strip())))
            else: codes.append((i,key*int(line.strip())))
    #sekoitetaan
    maxlen = len(codes)
    unmixed = codes.copy()
    for j in range(mixes):       
        for item in unmixed:
            i = codes.index(item)
            moves = item[1]
            newindex = (i + moves)%(maxlen-1)
            codes.insert(newindex, codes.pop(i))
    #etsitään
    for offset, value in enumerate(codes):
        if value[1] == 0: break
    coordinates = []
    for i in range(1,4):
        coindex = (offset+i*1000)%maxlen
        coordinates.append(codes[coindex][1])
    return sum(coordinates)
import numpy as np
from operator import itemgetter

def build_cavemap(file:str, spec:str):
    walllines = []
    with open(file, 'r') as f:
        for line in f:
            walls = line.strip().split(' -> ')
            nodes = []
            for node in walls:
                coordinates = node.split(',')
                for i, coordinate in enumerate(coordinates):
                    coordinates[i] = int(coordinate)
                coordinates = tuple(coordinates)
                nodes.append(coordinates)
            #Tässä kohtaa rivin seinien kulmien koordinaatit ovat (int,int)-monikkojen listana
            walllines.append(nodes)
        #Nyt kun kulmalista on valmis, tiedetään, miten suuri taulukko tarvitaan
        #Ei riitä, jos luolalla on lattia... Kovakoodattu kakkosvaiheessa leveämmäksi
    maxes = []
    for line in walllines:
        linemaxes = []
        for i in range(2):
            linemaxes.append(max(line,key=itemgetter(i))[i])
        linemaxes = tuple(linemaxes)
        maxes.append(linemaxes)
    real_maxes = []
    for i in range(2):
            real_maxes.append(max(maxes,key=itemgetter(i))[i])
    real_maxes[1] = real_maxes[1]+1 #lisätään yksi tyhjä rivi alas
    ### luodaan luolastokartta ###
    for i in range(2): real_maxes[i] += 1
    if spec == '2':
        real_maxes[0] = 1000 
        real_maxes[1] += 1
    cavemap = np.zeros(tuple(real_maxes), dtype=int, order='F')
    if spec == '2': cavemap[:,real_maxes[1]-1] = 1
    for line in walllines:
        for i, node in enumerate(line):
            if i == len(line) - 1: break
            #Tämä ei toimi, jos seinät voivat mennä muuhunkin kuin kardinaalisuuntiin
            if node[0] < line[i+1][0]: smallnodex, bignodex = node[0], line[i+1][0]
            else: smallnodex, bignodex = line[i+1][0], node[0]
            if node[1] < line[i+1][1]: smallnodey, bignodey = node[1], line[i+1][1]
            else: smallnodey, bignodey = line[i+1][1], node[1]
            for x in range(smallnodex, bignodex+1):
                for y in range(smallnodey, bignodey+1): cavemap[x,y] = 1  #Olkoon 1 seinä ja 0 tyhjä (2 hiekkaa, vaikkei oikeastaan tarvitse erotella seinistä)
    np.savetxt('debug.txt',np.transpose(cavemap.astype(int)), fmt='%i', delimiter = '')
    ### pudotetaan hiekkaa ###
    grains = -1
    supergrain = False
    while True:
        grains += 1
        grain = [500,0]
        falling = True
        while falling == True:
            if supergrain: 
                cavemap[*grain] = 9

            if grain[1] == cavemap.shape[1]-1: 
                np.savetxt('debug.txt',np.transpose(cavemap.astype(int)), fmt='%i', delimiter = '')
                if not supergrain: 
                    supergrain = True
                    break
                else: return grains-1
            for dir in [0,-1,1,100]:
                if dir == 100:
                    falling = False
                    cavemap[*grain] = 2
                    if grain == [500,0]: return grains+1
                elif cavemap[grain[0]+dir,grain[1]+1] == 0:
                    grain[0], grain[1] = grain[0]+dir, grain[1] + 1
                    break
            

            
        
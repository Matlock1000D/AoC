def parse_list(lst):
    """purkaa listan kokonaisluvuiksi ja listoiksi"""
    lst[0] = lst[0][1:]         #Pitäisi tässä kohtaa olla kaikkialla hakasulkeita
    lst[-1] = lst[-1][:-1]
    while sum(1 for x in lst if '[' in x):
        brackets = 0
        startelement = -1
        for i, element in enumerate(lst):
            if type(element) == str and '[' in element and startelement == -1:
                startelement = i
            brackets += element.count('[')
            if type(element) == str and ']' in element:
                brackets -= element.count(']')
                if brackets == 0:
                    newlist = lst[startelement:i+1].copy()
                    del lst[startelement:i+1]
                    parse_list(newlist)
                    lst.insert(startelement,newlist)
                    break   #turvallisempaa aloittaa iteraatio alusta, kun listaa on muutettu
    for i, element in enumerate(lst): 
        if type(element)==str:
            if element.isnumeric(): lst[i] = int(element)
            else: del lst[i]

def smaller_first(i:list,j:list)->int:
    if len(i) < len(j): maxi = len(i)
    else: maxi = len(j)
    for k in range(maxi):
        if type(i[k]) == type(j[k]) == int:
            if i[k] < j[k]: return 1
            elif i[k] > j[k]: return 0
        if type(i[k]) == type(j[k]) == list:
            if (i[k] == j[k]): continue
            else: return smaller_first(i[k],j[k])
        if type(i[k]) == int and type(j[k]) == list:
            comparison = smaller_first([i[k]],j[k])
            if comparison >= 0: return comparison
        if type(j[k]) == int and type(i[k]) == list:
            comparison = smaller_first(i[k],[j[k]])
            if comparison >= 0: return comparison
            #jos -1 niin ratkaisematon
    if len(i) == len(j): return -1
    if len(i) < len(j): return 1
    if len(i) > len(j): return 0

def compare_signals(signals):
    corrects = []
    pair = 0    #signaaliparin indeksi
    s = iter(signals)
    for i,j in zip(s,s):
        pair += 1
        if smaller_first(i,j) == 1: corrects.append(pair)
    return sum(corrects)
         

def read_signal(file, spec):
    with open(file, 'r') as f:
        signals = []
        for line in f:
            linelist = line.strip().split(',')
            if len(linelist) == 0 or linelist[0] == '': continue
            parse_list(linelist)
            signals.append(linelist)
    return compare_signals(signals)
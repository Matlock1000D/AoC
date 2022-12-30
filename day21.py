#menisi varmaan jonain näppäränä binääripuusovelluksena

def monkeycount(file, spec):
    monkeys = dict()
    operations = ({'+': (lambda a,b: a+b),
        '-': (lambda a,b: a-b),
        '/': (lambda a,b: a/b),
        '*': (lambda a,b: a*b)})
    flips = {'+': '-', '-': '+', '*': '/', '/': '*'}

    with open(file, 'r') as f:
        for line in f:
            if len(line) == 0: break
            lineitem = line.strip().split(':')
            monkeys[lineitem[0]] = lineitem[1].strip().split(' ')

    #muunnetaan
    if spec == '2':
        route = ['humn']
        transformeddict = dict()
        for monkey in monkeys:
            item = monkeys[monkey]
            if len(item) >= 3:
                if item[0] == 'humn' or item[2] == 'humn':
                    rootindex = item.index('humn')
                    route.append(monkey)
        while route[-1] != 'root':
            searchable = route[-1]
            for monkey in monkeys:
                item = monkeys[monkey]
                if len(item) >= 3:
                    if item[0] == searchable or item[2] == searchable:
                        rootindex = item.index(searchable)
                        route.append(monkey)
        for i, swapper in enumerate(route):
            if i == len(route)-2: break
            swapitem = monkeys[route[i+1]]
            index = swapitem.index(swapper)
            if swapitem[1] == '+':
                if index == 2:
                    swapitem[2] = swapitem[0]
                    index = 0
                swapitem[1] = '-'
            elif swapitem[1] == '/':
                if index == 0: swapitem[1] = '*'
            elif swapitem[1] == '*':
                if index == 2:
                    swapitem[2] = swapitem[0]    #ptqd = lgvd/ljgn
                    index = 0
                swapitem[1] = '/'
            elif swapitem[1] == '-':
                if index == 0: swapitem[1] = '+'
            swapitem[index] = route[i+1]
            monkeys[swapper] = swapitem
        pass
        k = monkeys[route[-2]].index(route[-2])
        j = monkeys['root'].index(route[-2])
        monkeys[route[-2]][k] = monkeys['root'][2-j]
        monkeys.pop('root')

    #iteroidaan
    if spec == '1': target = 'root'
    else: target = 'humn'
    while type(monkeys[target]) == list:
        for monkey in monkeys:
            item = monkeys[monkey]
            if type(item) == list:
                #vielä on parsittavaa
                if len(item) == 1:
                    monkeys[monkey] = int(item[0])
                else:
                    for k in [0,2]:
                        if type(item[k]) == str:
                            if type(monkeys[item[k]]) == int:
                                monkeys[monkey][k] = monkeys[item[k]]
                    if type(monkeys[monkey][0]) == type(monkeys[monkey][2]) == int:
                        monkeys[monkey] = int(operations[item[1]](monkeys[monkey][0],monkeys[monkey][2]))
    return monkeys[target]
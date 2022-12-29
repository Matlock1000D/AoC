def monkeycount(file, spec):
    monkeys = dict()
    operations = ({'+': (lambda a,b: a+b),
        '-': (lambda a,b: a-b),
        '/': (lambda a,b: a/b),
        '*': (lambda a,b: a*b)})

    with open(file, 'r') as f:
        for line in f:
            if len(line) == 0: break
            lineitem = line.strip().split(':')
            monkeys[lineitem[0]] = lineitem[1].strip().split(' ')
    
    #iteroidaan
    while type(monkeys['root']) == list:
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
    return monkeys['root']
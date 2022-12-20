from collections import OrderedDict

class Monkey:
    def __init__(self, items:list, operand, modifier:int, dividend:int, target_true:int, target_false:int) -> None:
        self.items = items
        self.operand = operand
        self.modifier = modifier    #huolestumiskertoimen kerroin/summattava
        self.dividend = dividend    #testin jakaja
        self.target_true = target_true  #apina, jolle heitetään, jos testi on tosi
        self.target_false = target_false #apina, jolle heitetään, jos testi on tosi
        self.inspections = 0

def read_monkeyfile(file, spec):
    monkeys = {}
    operations = {'*': lambda a,b : a*b, '+': lambda a,b: a+b, '**': lambda a,b: a*a}
    with open(file, 'r') as f:
        for line in f:
            input = line.strip().split(' ')
            if len(input) < 2:
                monkeys[monkeynumber] = Monkey(items, operand, modifier, dividend, target_true, target_false)
                items = []
                operand = None
                modifier = dividend = target_false = target_true = monkeynumber = None
            elif input[0] == 'Monkey':
                monkeynumber = int(input[1][:-1])
            elif input[1] == 'items:':
                items = [int(i.replace(',','')) for i in input[2:]]
            elif input[0] == 'Operation:':
                if input[5] == 'old':
                    operand = operations['**']
                    modifier = 1
                else:
                    operand = operations[input[4]]
                    modifier = int(input[5])
            elif input[0] == 'Test:':
                dividend = int(input[3])
            elif input[1] == 'true:':
                target_true = int(input[5])
            elif input[1] == 'false:':
                target_false = int(input[5])

    monkeys[monkeynumber] = Monkey(items, operand, modifier, dividend, target_true, target_false)            
    monkeys = OrderedDict(sorted(monkeys.items()))
    return monkeys

def get_monkey_business(monkeys):
    x = monkeys.values()
    y = []
    for monkey in x:
        y.append(monkey.inspections)
    y.sort(reverse=True)
    return y[0]*y[1]

def run_monkeygame(monkeys, turns, relaxation):
    #haetaan pym
    x = set()
    for m in monkeys:
        x.add(monkeys[m].dividend)
    megadiv = 1
    for y in x: megadiv *= y

    for i in range(turns):
        for monkey_key in monkeys:
            while len(monkeys[monkey_key].items) > 0:
                monkeys[monkey_key].inspections += 1
                item = monkeys[monkey_key].items[0]
                monkeys[monkey_key].items[0] = monkeys[monkey_key].operand(item, monkeys[monkey_key].modifier)
                if relaxation == 1: monkeys[monkey_key].items[0] = monkeys[monkey_key].items[0]%megadiv
                else: monkeys[monkey_key].items[0] = monkeys[monkey_key].items[0]//relaxation
                if monkeys[monkey_key].items[0]%monkeys[monkey_key].dividend == 0:
                    monkeys[monkeys[monkey_key].target_true].items.append(monkeys[monkey_key].items.pop(0))
                else:
                    monkeys[monkeys[monkey_key].target_false].items.append(monkeys[monkey_key].items.pop(0))
    
    return(get_monkey_business(monkeys))
    

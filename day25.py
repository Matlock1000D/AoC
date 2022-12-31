def from_snafu(sf_num:str)->int:
    chars = {'1': 1, '2': 2, '0': 0, '-': -1, '=': -2}
    snf_list = list(map(lambda x: chars[x],[*sf_num]))
    num = 0
    for i, d in enumerate(reversed(snf_list)):
        num += d * 5**i
    return num

def to_snafu(de_num:int)->str:
    chars = {-2: '=', -1: '-', 0: '0', 1: '1', 2: '2'}
    num = []
    i=0
    while de_num//(5**i) > 0:
        num.append((de_num%(5**(i+1)))//(5**i))
        i += 1
    if len(num) == 0: num = 0
    for i, digit in enumerate(num):
        if digit > 2:
            num[i] = -5 + digit
            num[i+1] += 1
    return ''.join(list(map(lambda x:chars[x], reversed(num))))

def snafu(file, spec):
    sum = 0
    with open(file, 'r') as f:
        for line in f:
            if len(line) < 2: break 
            sum += from_snafu(line.strip())
    return to_snafu(sum)
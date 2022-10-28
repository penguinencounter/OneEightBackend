import string
import random

POOL = string.ascii_lowercase + string.digits
print(f'pool ({len(POOL)}): {POOL}')


def fmt_short_num(inp: int):
    i = 0
    shorts = [
        '', 'k', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx', 'Sp', 'Oc', 'No', 'Dc', 'Ud',
        'Dd', 'Td'
    ]
    while inp > 1000:
        try:
            inp = round(inp / 1000, 3)
        except OverflowError:
            inp = inp // 1000
        i += 1
    if i < len(shorts):
        return f'{inp}{shorts[i]}'
    return f'{inp}e+{i*3}'


def new_generator(length: int):
    print(
        f'new generator: length {length}\n    about {fmt_short_num(len(POOL)**length)} combinations'
    )
    stale = []
    a = length

    def get(disallowed: list = None):
        if disallowed is None:
            disallowed = stale
        while 1:
            b = ''
            for _ in range(a):
                b += random.choice(POOL)
            if b not in disallowed:
                stale.append(b)
                return b

    return get

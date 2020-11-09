import math
import copy
import string
import sys
import copy
from collections import defaultdict
import itertools



with open("22/shuffles.txt") as f:
    shuffles = [s for s in f.read().strip().split('\n')]

# Part 1: The age of innocence

deck = list(range(0, 10007))

def dealInc(deck, n):
    newDeck = [-1] * len(deck)
    i = 0
    while len(deck):
        newDeck[i % len(newDeck)] = deck.pop(0)
        i += n
    assert not any(i == -1 for i in newDeck)
    return newDeck

cmds = {
    'deal with increment ': dealInc,
    'deal into new stack': (lambda x: x[::-1]),
    'cut ': (lambda x,n: x[n:] + x[:n])
}

for s in shuffles:
    for cmd,fn in cmds.items():
        if s.startswith(cmd):
            if cmd[-1] == ' ':
                arg = int(s[len(cmd):])
                deck = fn(deck, arg)
            else:
                deck = fn(deck)
            # assert card < m
            break
    else: 
        print("no command found")
        break
print("Part 1 - card 2019 is at: ", deck.index(2019))


#!/usr/bin/python3

import re
import math
from collections import deque

class Pack(object):    
    def __init__(self, packlen):
        with open("22/shuffles.txt", "r") as f:
            self.orders = f.readlines()
        self.packlen = packlen
        self.pack = deque(range(self.packlen))
    
    def get_index(self, card, num_shuffles):
        ORDER_REGEX = [
            (r"deal into new stack", lambda x, n: -x - 1 % self.packlen),
            (r"cut (?P<number>-?[0-9]+)", lambda x, n: (x - n) % self.packlen),
            (r"deal with increment (?P<number>[0-9]+)", lambda x, n: (x * n) % self.packlen),
        ]
    
        index = card
        for i in range(num_shuffles):
            for order in self.orders:
                for regex, func in ORDER_REGEX:
                    r = re.compile(regex)
                    m = r.match(order.strip("\n"))
                    if m:
                        try:
                            num = int(m.group("number"))
                        except IndexError:
                            num = None
                        index = func(index, num)
                        break
                else:
                    print(f"Error: didn't understand order {order}")
                    return
        print(f"found index: {index}")
                           

print("PART 1:")                
p = Pack(10007)
p.get_index(2019, 1)
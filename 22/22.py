#!/usr/bin/python3

import re
import math
from collections import deque

class Pack(object):    
    def __init__(self, packlen):
        with open("22/shuffles.txt", "r") as f:
            self.orders = f.readlines()
        
        self.rev_orders = self.orders[:]
        self.rev_orders.reverse()
        
        self.packlen = packlen
    
    def get_index(self, card):
        ORDER_REGEX = [
            (r"deal into new stack", lambda x, n: (-x - 1) % self.packlen),
            (r"cut (?P<number>-?[0-9]+)", lambda x, n: (x - n) % self.packlen),
            (r"deal with increment (?P<number>[0-9]+)", lambda x, n: (x * n) % self.packlen),
        ]
    
        index = card
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
        
    def get_card(self, index, n_shuffles):
        # inverse operations
        ORDER_REGEX = [
            (r"deal into new stack", lambda n, A, B: (-A%self.packlen, (self.packlen-B-1)%self.packlen)),
            (r"cut (?P<number>-?[0-9]+)", lambda n, A, B: (A, (B + n) % self.packlen)),
            (r"deal with increment (?P<number>[0-9]+)", lambda n, A, B: ((A * pow(n, self.packlen-2, self.packlen))%self.packlen, (B * pow(n, self.packlen-2, self.packlen))%self.packlen)),
        ]
    
        a, b = 1, 0
        for order in self.rev_orders:
            for regex, func in ORDER_REGEX:
                r = re.compile(regex)
                m = r.match(order.strip("\n"))
                if m:
                    try:
                        num = int(m.group("number"))
                    except IndexError:
                        num = None
                    a, b = func(num, a, b)
                    break
            else:
                print(f"Error: didn't understand order {order}")
                return
        
        def find_nth(a, b, n, index):
            # if we perform transformation ax+b n times we get: a^n + b*sum(a^x)0->n-1
            # last term is a geometric series. Formula for this is:
            #     a^n*x + b(a^n - 1)/(a - 1)
            return ((pow(a, n, self.packlen) * index)%self.packlen + (b * (pow(a, n, self.packlen) - 1))%self.packlen * pow(a-1, self.packlen - 2, self.packlen))%self.packlen
            
        card = find_nth(a, b, n_shuffles, index)
             
        print(f"found card: {card}")
        
                           

print("PART 1:")                
p = Pack(10007)
p.get_index(2019)

print("test part 2 (should be 2019):")
p = Pack(10007)
p.get_card(2519, 1) 

print("PART 2:")
p = Pack(119315717514047)
p.get_card(2020, 101741582076661)
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
    
    def _deal_new_stack(self, number):
        assert(number == None)
        newpack = deque()
        for i in range(len(self.pack)):
            newpack.appendleft(self.pack.popleft())
            
        self.pack = newpack
    
    def _deal_increment(self, number):
        # dequeue and make a list
        packlist = [0] * self.packlen
        
        index = 0
        for i in range(self.packlen):
            packlist[index] = self.pack.popleft()
            index += number
            if index >= self.packlen:
                index -= self.packlen
        
        self.pack = deque(packlist)

    def _cut(self, number):
        if number > 0:
            for i in range(number):
                self.pack.append(self.pack.popleft())
        else:
            for i in range(abs(number)):
                self.pack.appendleft(self.pack.pop())
    
    def display(self):
        for card in self.pack:
            print(card, end="")
        
        print()
    
    def get_index(self, card):
        print(f"{card} card index: {self.pack.index(card)}")
        
    def shuffle(self):
        ORDER_REGEX = [
            (r"deal into new stack", self._deal_new_stack, None),
            (r"cut (?P<number>-?[0-9]+)", self._cut, "number"),
            (r"deal with increment (?P<number>[0-9]+)", self._deal_increment, "number"),
        ]
        for order in self.orders:
            for regex, func, group in ORDER_REGEX:
                r = re.compile(regex)
                m = r.match(order.strip("\n"))
                if m:
                    func((int(m.group(group)) if group else None))
                    break
            else:
                print(f"Error: didn't understand order {order}")
                return
                    

print("PART 1:")                
p = Pack(10007)
p.shuffle()
#p.display()
p.get_index(2019)

#!/usr/bin/python3

from subprocess import Popen, PIPE, STDOUT
import itertools
import intcode

class Drone(object):
    def __init__(self):
        self.coords = {}
           
    def _investigate_coord(self, x, y):
        intcomp = intcode.IntComp('19/int_array9.txt')
        
        intcomp.start()
        intcomp.input(x)
        intcomp.input(y)
        output = intcomp.output()
        self.coords[(x,y)] = output
        
        return output
        
    def investigate(self, xmax, ymax):
        self.xmax, self.ymax = xmax, ymax
        total = sum([self._investigate_coord(x, y) for x, y in \
                    itertools.product(range(xmax), range(ymax))])
                    
        print(f"total found! {total}")              
    
    def plot(self):
        for y in range(self.ymax):
            print("".join([("#" if self.coords[(x, y)] == 1 else ".") for x in range(self.xmax)]))
            
d = Drone()
d.investigate(50, 50)
d.plot()


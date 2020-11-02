#!/usr/bin/python3

from subprocess import Popen, PIPE, STDOUT
import itertools
import copy
import intcode

class Drone(object):
    def __init__(self):
        self.coords = {}
           
    def _investigate_coord(self, coord):
        if coord in self.coords:
            return self.coords[coord]
        intcomp = intcode.IntComp('19/int_array9.txt')
        
        intcomp.start()
        intcomp.input(coord[0])
        intcomp.input(coord[1])
        output = intcomp.output()
        self.coords[coord] = output
        
        return output
        
    def find_number(self, xmax, ymax):
        self.xmax, self.ymax = xmax, ymax
        total = sum([self._investigate_coord((x, y)) for x, y in \
                    itertools.product(range(xmax), range(ymax))])
                    
        print(f"total found! {total}")          
    
    def plot(self, coord=None):
        coords = copy.deepcopy(self.coords)
        if coord:
            coords[coord] = "O"

        for y in range(self.ymax):
            print("".join([("#" if coords[(x, y)] == 1 else ("." if coords[(x,y)] == 0 else coords[(x,y)])) for x in range(self.xmax)]))
    
    def _find_xextent(self, coord, min_x_extent):
        while True:
            if self._investigate_coord((coord[0] + min_x_extent, coord[1])) == 0:
                break
            min_x_extent += 1
        
        return min_x_extent
    
    def _find_yextent(self, coord, min_y_extent):
        while True:
            if self._investigate_coord((coord[0], coord[1] + min_y_extent)) == 0:
                break
            min_y_extent += 1
        
        return min_y_extent
    
    def find_coord(self, xy_extent):
        coord = (0,0)
        min_x_extent = 0
        
        while True:
            # find the next start of row 
            while True:
                coord = (coord[0], coord[1] + 1) 
                if self._investigate_coord(coord) == 1:
                    break
                coord = (coord[0] + 1, coord[1])
                min_x_extent = (0 if min_x_extent == 0 else min_x_extent - 1)
                if self._investigate_coord(coord) == 1:
                    break
            
            min_x_extent = self._find_xextent(coord, min_x_extent)
            if min_x_extent >= xy_extent:
                # Go rightwards and investigate y extent
                min_y_extent = 0
                for x in range(0, min_x_extent - xy_extent + 1):
                    rowcoord = (coord[0] + x, coord[1])
                    min_y_extent = self._find_yextent(rowcoord, min_y_extent)
                    if min_y_extent >= xy_extent:
                        self.plot(rowcoord)
                        print(f"finished!! coord: {rowcoord}")
                        return

d = Drone()
d.find_number(50, 50)
#d.plot()
d.find_coord(100)


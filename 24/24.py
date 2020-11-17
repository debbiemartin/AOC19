#!/usr/bin/python3

class BugMap(object):
    """
    Stores bug coords as unique bits in map_size ^2 bit number
    """
    def __init__(self, map_size):
        self.val = 0
        self.map_size = map_size
    
    def set(self, x, y):
        self.val |= (1 << (self.map_size*y + x)) 
            
    def is_set(self, x,y):
        return self.val & (1 << (self.map_size*y + x))
        
    def get_score(self):
        return self.val


class BugSim(object):
    """
    Bug simulator. Iterates the bug map in time intervals and stores past 
    biodiversity scores (unique to each bug map coord comb).
    """
    MAP_SIZE = 5
    
    def __init__(self):
        with open("24/map.txt", 'r') as f:
            lines = f.readlines()
        
        self.map = BugMap(self.MAP_SIZE)

        for y, line in enumerate(lines):
            for x in range(len(line.strip("\n"))):
                if line[x] == "#":
                    self.map.set(x, y)

        self.past_maps = set([self.map.get_score()])
        
    def iterate(self):
        newmap = BugMap(self.MAP_SIZE)
        increments = [1, -1]

        for y in range(self.MAP_SIZE):
            for x in range(self.MAP_SIZE):
                # Count up the number of adjacent bugs
                n_adj = 0
                for x_inc in increments:
                    if x + x_inc < 0 or x + x_inc >= self.MAP_SIZE:
                        continue
                    if self.map.is_set(x + x_inc, y):
                        n_adj += 1

                for y_inc in increments:
                    if y + y_inc < 0 or y + y_inc >= self.MAP_SIZE:
                        continue
                    if self.map.is_set(x, y + y_inc):
                        n_adj += 1
                
                # Process the coord based on number of adjacent bugs
                if (self.map.is_set(x, y) and n_adj == 1) or \
                    (not self.map.is_set(x, y) and (n_adj == 1 or n_adj == 2)):
                    # Set the bug in the new map
                    newmap.set(x, y)
                
        self.map = newmap

    def iterate_until_repeat(self):
        while True:
            self.iterate()
            if self.map.get_score() in self.past_maps:
                print(f"found the repeat! biodiversity index: {self.map.get_score()}")
                self.print()
                break
            self.past_maps.add(self.map.get_score())
        
    def print(self):
        print("Current map:")
        for y in range(self.MAP_SIZE):
            for x in range(self.MAP_SIZE):
                # use bitwise operator to see whether bug is present
                if self.map.is_set(x, y): 
                    print("#", end="")
                else:
                    print(".", end="")
            print() 
            
b = BugSim()
b.print()
b.iterate_until_repeat()
        

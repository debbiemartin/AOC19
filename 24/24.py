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
            
    def is_set(self, coords):
        return self.val & (1 << (self.map_size*coords[1] + coords[0]))
        
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
        
        level0 = BugMap(self.MAP_SIZE)

        for y, line in enumerate(lines):
            for x in range(len(line.strip("\n"))):
                if line[x] == "#":
                    level0.set(x, y)
        
        self.levels = {}
        self.levels[0] = level0
        
    def _iterate_level_and_neighbours(self, levelnum):
        level = (self.levels[levelnum] if levelnum in self.levels else BugMap(self.MAP_SIZE))
        newlevel = BugMap(self.MAP_SIZE)
        
        for y in range(self.MAP_SIZE):
            for x in range(self.MAP_SIZE):
                if x == (self.MAP_SIZE - 1)/2 and y == (self.MAP_SIZE - 1)/2:
                    # This is the centre square - really a smaller level grid
                    continue
                
                # Count up the number of adjacent bugs
                
                n_adj = 0
                neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                
                for neighbour in neighbours:
                    if neighbour[0] == (self.MAP_SIZE - 1)/2 and \
                       neighbour[1] == (self.MAP_SIZE - 1)/2:
                        # Count bugs in higher level if present
                        if (levelnum + 1) in self.levels:
                            if y == (self.MAP_SIZE - 1)/2 + 1:
                                neighbourcoords = [(i, self.MAP_SIZE - 1) for i in range(self.MAP_SIZE)] 
                            elif y == (self.MAP_SIZE - 1)/2 - 1:
                                neighbourcoords = [(i, 0) for i in range(self.MAP_SIZE)]
                            elif x == (self.MAP_SIZE - 1)/2 + 1:
                                neighbourcoords = [(self.MAP_SIZE - 1, i) for i in range(self.MAP_SIZE)]
                            elif x == (self.MAP_SIZE - 1)/2 - 1:
                                neighbourcoords = [(0, i) for i in range(self.MAP_SIZE)]
                            
                            n_adj += sum(1 for neighbourcoord in neighbourcoords if self.levels[levelnum + 1].is_set(neighbourcoord))    
                                
                    elif neighbour[0] < 0 or neighbour[0] >= self.MAP_SIZE or \
                         neighbour[1] < 0 or neighbour[1] >= self.MAP_SIZE:
                        # Count bug in lower level if present
                        if (levelnum - 1) in self.levels:
                            neighbourcoord = []
                            for i in range(2):
                                neighbourcoord.append(int((self.MAP_SIZE - 1)/2) + (1 if neighbour[i] >= self.MAP_SIZE else (-1 if neighbour[i] < 0 else 0)))

                            if self.levels[levelnum - 1].is_set(neighbourcoord):
                                n_adj += 1
    
                    elif level.is_set(neighbour):
                        n_adj += 1

                # Process the coord based on number of adjacent bugs
                if (level.is_set((x, y)) and n_adj == 1) or \
                    (not level.is_set((x, y)) and (n_adj == 1 or n_adj == 2)):
                    # Set the bug in the new map
                    newlevel.set(x, y)
               
        if levelnum in self.levels or newlevel.get_score() != 0:
            # Either the level was added in a previous iteration or in this
            # one. Levels are not removed as outers may be non-zero
            if levelnum == 0:
                self._iterate_level_and_neighbours(1)
                self._iterate_level_and_neighbours(-1)
            elif levelnum > 0: 
                self._iterate_level_and_neighbours(levelnum + 1)
            else:
                self._iterate_level_and_neighbours(levelnum - 1)
                
            self.levels[levelnum] = newlevel
               
    def iterate_and_count(self, num_iterations):
        for n in range(num_iterations):
            self._iterate_level_and_neighbours(0)
        
        count = 0        
        for num, level in self.levels.items():
            if num >= 6 and num <= 8:
                print(f"level {num}:")
                self.print(level)
            for y in range(self.MAP_SIZE):
                for x in range(self.MAP_SIZE):
                    # use bitwise operator to see whether bug is present
                    if level.is_set((x, y)):
                        count += 1
        
        print(f"Calculated bug count: {count}")

    def print(self, map):
        for y in range(self.MAP_SIZE):
            for x in range(self.MAP_SIZE):
                # use bitwise operator to see whether bug is present
                if map.is_set((x, y)): 
                    print("#", end="")
                else:
                    print(".", end="")
            print()
            
b = BugSim()
b.iterate_and_count(200)

        

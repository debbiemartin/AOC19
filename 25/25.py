#!/usr/bin/python3

from collections import deque
import itertools
import sys
sys.path.insert(1, '19/')

import intcode
       
class Droid(object):
    objectblacklist = ("molten lava", "photons", "infinite loop", 
                       "escape pod", "giant electromagnet")
    def __init__(self):
        self.intcomp = intcode.IntComp("25/intcode.txt")
        self.visited = []
        self.objects = {}
        self.dirs_security = []

    def _get_output(self):
        output_str = ""
    
        while not self.intcomp.output_done():
            output = self.intcomp.output()
            if output > 137:
                print(f"Big number received: {output}")
            else:
                print(chr(output), end="")
                output_str += chr(output)
        
        return output_str
        
    def _rev_dir(self, dir):
        dirs = {"north": "south", "south": "north", "east":"west", "west":"east"}
        
        return dirs[dir]
        
    def _parse_output(self, output):
        if "airlock" in output:
            self.airlockoutput = output
        
        # Parse the name 
        lines = output.split("\n")
        for line in lines:
            if line.startswith("=="):
                name = line.strip("== ").strip(" ==\n")
                break
        
        # Parse the directions
        directions = []
        for dir in ("north", "south", "east", "west"):
            if ("- " + dir + "\n") in output:
                directions.append(dir)
                
        # Parse the object
        object = None
        for linenum, line in enumerate(lines):
            if line.startswith("Items here:"):
                object = lines[linenum + 1].strip("- ").strip("\n")
        print(f"got name {name} directions {directions} object {object}")
        
        return name, directions, object
    
    def _instruct_bot(self, instruction):
        instruction += "\n"
        print(f"instructing bot: {instruction}")

        for char in instruction:
            self.intcomp.input(ord(char))
        
    def explore_dir(self, dir, prevdirs):
        print(f"exploring dir {dir}")        
        # Go in the specified direction
        self._instruct_bot(dir)
        name, directions, object = self._parse_output(self._get_output())

        if name not in self.visited:
            self.visited.append(name)
            if (object and object not in self.objectblacklist):
                self.objects[object] = name
                self._instruct_bot(f"take {object}")
                self._get_output()
            print(f"added {name} to visited list")
                        
            if (name == "Security Checkpoint" and 
                (len(self.dirs_security) == 0 or 
                 len(prevdirs) + 1 < len(self.dirs_security))):
                self.dirs_security = prevdirs + [dir]
                # direction to go through the pressure sensitive flooring is
                # the one which ISN'T the reverse of the last dir to get to 
                # security
                for newdir in directions:
                    if newdir != self._rev_dir(dir):
                        self.through_dir = newdir
                        break
                
            if name != "Pressure-Sensitive Floor":
                for newdir in directions:
                    self.explore_dir(newdir, prevdirs + [dir])
        
        # Go in the reverse direction. Don't do anything with the output
        self._instruct_bot(self._rev_dir(dir))
        self._get_output()
    
    def _try_comb(self, objects):
        """
        Must be called from the security checkpoint
        """
        self._instruct_bot("inv")
        output = self._get_output()
               
        # drop any not in objects not in object
        for object in self.objects:
            if object in output and not object in objects:
                self._instruct_bot(f"drop {object}")
                self._get_output()
            elif object in objects and not object in output:
                self._instruct_bot(f"take {object}")
                self._get_output()
        
        self._instruct_bot(self.through_dir)
        output = self._get_output()
        if "Analysis complete" in output:
            return True
        return False
        
    def _try_all_combs(self):
        combs = []
        for r in range(len(self.objects) + 1):
            combs += list(itertools.combinations(self.objects.keys(), r))
        print(f"walking to security: directions are {self.dirs_security}")
        for dir in self.dirs_security:
            self._instruct_bot(dir)
            self._get_output()
       
        for comb in combs:
            if self._try_comb(comb):
                print("found the way through!!")
                break
            
        print("list of the rooms: ")
        print(self.visited)

    def explore_and_solve(self):
        self.intcomp.start()
        
        # Explore - should be back to node 1
        name, directions, object = self._parse_output(self._get_output())
        self.visited.append(name)
        for dir in directions:
            self.explore_dir(dir, list())
        
        self._try_all_combs()
                
        self.intcomp.stop()

droid = Droid()
print("PART 1:")
droid.explore_and_solve()
#!/usr/bin/python3

from subprocess import Popen, PIPE, STDOUT
import random
import pdb
import copy

class InvalidDirectionError(Exception):
    pass
class Droid(object):
    CODE_PLOT = ["#", ".", "O"]
    def __init__(self):
        self.p = Popen(['python3', '-u', './9.py'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        self.current_coord = (0,0)
        self.coords = {(0,0): 1} # empty space at (0,0)

    def _reverse_direction(self, direction):
        # 1->2
        # 2->1
        # 3->4
        # 4->3
        if direction == 1 or direction == 2:
            return (3 - direction)
        else:
            return (7 - direction)

    def _add_direction(self, coord, direction):
        # new coord based on direction:
        #   north (1), south (2), west (3), and east (4)
        if direction == 1 or direction == 2:
            diff = (1 if direction == 1 else -1)
            new_coord = (coord[0], coord[1] + diff)
        elif direction == 3 or direction == 4:
            diff = (1 if direction == 4 else -1)
            new_coord = (coord[0] + diff, coord[1])
        else:
            print(f"invalid direction {direction}")
            raise InvalidDirectionError

        return new_coord

    def _whats_in_direction(self, direction, coord=None):
        # Sees what's in the direction in the coord set - does not move
        if not coord:
            coord = self.current_coord

        new_coord = self._add_direction(coord, direction)
        if new_coord not in self.coords:
            return -1
        else:
            return self.coords[new_coord]

    def _move(self, direction):
        self.p.stdout.readline()
        self.p.stdin.write("{}\n".format(direction).encode('utf-8'))
        self.p.stdin.flush()

        code = int(self.p.stdout.readline().decode('utf-8').strip('\n'))

        new_coord = self._add_direction(self.current_coord, direction)

        # add to coords
        self.coords[new_coord] = code

        # if not wall, move current coord
        if code != 0:
            self.current_coord = new_coord

        return code

    def search_all_map(self):
        """
        Recursive function to search entirety of the map
        """
        for d in range(1, 5):
            if self._whats_in_direction(d) == -1:
                code = self._move(d)
                if code == 2:
                    self.oxygen = self.current_coord

                if code != 0:
                    self.search_all_map()
                    self._move(self._reverse_direction(d))

    def find_shortest_route(self, start=(0,0), comingfrom=None):
        assert(self.oxygen)

        if any(self._whats_in_direction(d, start) == 2 for d in range(1, 5)):
            return 1

        #@@@ could instead walk to the next junction here to save on recursion
        #    depth for only 1x forward direction
        least = 0
        for d in range(1, 5):
            if self._whats_in_direction(d, start) == 1:
                new_coord = self._add_direction(start, d)
                if comingfrom and new_coord == comingfrom:
                    continue
                remaining = self.find_shortest_route(self._add_direction(start, d), start)
                if (remaining != 0 and (least == 0 or remaining < least)):
                    least = remaining

        return (least if least == 0 else least + 1)

    def _oxygen_step(self, coord):
        stepcoords = set(self._add_direction(coord, d) for d in range(1, 5) if self.oxygencoords[self._add_direction(coord, d)] == 1)

        if len(stepcoords) == 0:
            return 0

        for coord in stepcoords:
            self.oxygencoords[coord] = 2

        steps=max(self._oxygen_step(coord) for coord in stepcoords)

        return steps + 1

    def fill_oxygen(self):
        assert(self.oxygen)

        self.oxygencoords = copy.deepcopy(self.coords)

        return self._oxygen_step(self.oxygen)


    def plot(self):
        XMAX = max(coord[0] for coord in self.coords.keys())
        XMIN = min(coord[0] for coord in self.coords.keys())
        YMAX = max(coord[1] for coord in self.coords.keys())
        YMIN = min(coord[1] for coord in self.coords.keys())
        print("--------------------")
        for y in range(YMAX-YMIN, YMIN-1, -1):
            for x in range(XMIN, XMAX+1):
                coord = (x, y)
                if coord == (0,0):
                    print("S", end='')
                elif coord == self.current_coord:
                    print("D", end='')
                elif coord not in self.coords:
                    print(" ", end='')
                else:
                    print(self.CODE_PLOT[self.coords[coord]], end='')
            print("")


droid = Droid()

droid.search_all_map()
droid.plot()

print(f"shortest route to oxygen: {droid.find_shortest_route()}")

print(f"time to oxygenate map: {droid.fill_oxygen()}")

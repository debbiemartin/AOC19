#!/usr/bin/python3
import copy
from collections import deque

class MapWalker(object):
    DIRS=[(1, 0), (0, -1), (0, 1), (-1, 0)]

    def __init__(self):
        with open("18/map.txt", "r") as f:
            lines = f.readlines()

        self.map = list(line.strip("\n") for line in lines)
        self.XMAX = len(self.map[0])
        self.YMAX = len(self.map)
        self.shortest = 0
        self.keycombs = {}

    def _add_dir(self, coord, dir):
        new_coord = tuple(c + d for c, d in zip(coord, dir))
        return new_coord

    def _find_possible_dirs(self, coord, visited, keysfound):
        for dir in self.DIRS:
            x, y = self._add_dir(coord, dir)

            if (x, y) in visited:
                continue

            if x > self.XMAX or y > self.YMAX:
                continue

            asciicode = ord(self.map[y][x])
            if asciicode != 35 and not (asciicode >= 65 and asciicode <= 90 \
               and chr(asciicode + 32) not in keysfound):
                # not a wall or upper case letter
                yield dir

    def _find_reachable_keys(self, coord, keysfound=""):
        keys = {}
        visited = set()
        # do a BFS search for all reachable keys but keep track of num steps
        d = deque([(coord, 0)])
        while len(d) > 0:
            node, steps = d.popleft()
            visited.add(node)
            # handling for if the node is a key
            asciicode = ord(self.map[node[1]][node[0]])
            if asciicode >= 97 and asciicode <= 122 and chr(asciicode) not in keysfound:
                if node not in keys:
                    keys[node] = steps
                continue

            # put all children nodes (not walls or doors) on the queue
            for dir in self._find_possible_dirs(node, visited, keysfound):
                d.append((self._add_dir(node, dir), steps + 1))

        return keys

    def _shortest_from(self, coord, keysfound=""):
        asciicode = ord(self.map[coord[1]][coord[0]])
        assert(asciicode >= 97 and asciicode <= 122)

        # Check whether this key combination has already been tried, if this
        # route is not shorter, abort. This reduces path analysis and makes
        # only function of state
        keysfound = "".join(sorted(keysfound + chr(asciicode)))

        if (keysfound, chr(asciicode)) in self.keycombs:
            return self.keycombs[(keysfound, chr(asciicode))]

        reachable_keys = self._find_reachable_keys(coord, keysfound)

        if len(reachable_keys) == 0:
            return 0

        minsteps = min(keysteps + self._shortest_from(key, keysfound) \
                       for key, keysteps in reachable_keys.items())
        self.keycombs[(keysfound, chr(asciicode))] = minsteps

        return minsteps

    def get_keys(self):
        for y, line in enumerate(self.map):
            if "@" in line:
                x = line.find("@")
                coord = (x, y)
                break

        reachable_keys = self._find_reachable_keys(coord)

        assert(len(reachable_keys) > 0)

        shortest = min(keysteps + self._shortest_from(key) for key, keysteps in reachable_keys.items())

        print(f"shortest solution: {shortest}")

    def plot(self):
        for line in self.map:
            print(line)

bot = MapWalker()
bot.plot()
bot.get_keys()
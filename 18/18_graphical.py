import copy
import networkx as nx
from collections import deque

class MapWalker(object):
    DIRS=[(1, 0), (0, -1), (0, 1), (-1, 0)]

    def __init__(self, part2=False):
        with open("18/map.txt", "r") as f:
            lines = f.readlines()

        self.map = {}
        self.allkeys = ""
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip("\n")):
                self.map[(x, y)] = char
                if self._is_lower(char):
                    self.allkeys = "".join(sorted(self.allkeys + char))

        self.reachable_keys = {}

        for coord, char in self.map.items():
            if char == "@":
                self.botcoords = [coord]
                break
        if part2:
            self._multi_bots()

        self.shortest = 0
        self.keycombs = {}

    def _multi_bots(self):
        coord = self.botcoords[0]
        self.botcoords = set()

        for dir in [(0,0), (0,1), (1,0), (0,-1), (-1,0)]:
            newcoord = self._add_dir(coord, dir)
            self.map[newcoord] = "#"

        for dir in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            newcoord = self._add_dir(coord, dir)
            self.map[newcoord] = "@"
            self.botcoords.add(newcoord)

    def _is_lower(self, char):
        asciicode = ord(char)
        return asciicode >= 97 and asciicode <=122

    def _add_dir(self, coord, dir):
        new_coord = tuple(c + d for c, d in zip(coord, dir))
        return new_coord

    def _find_possible_dirs(self, coord, visited):
        for dir in self.DIRS:
            x, y = self._add_dir(coord, dir)

            if (x, y) in visited:
                continue

            if (x, y) not in self.map:
                continue

            asciicode = ord(self.map[(x, y)])
            if asciicode != 35:
                keyneeded = (chr(asciicode + 32) if (asciicode >= 65 and asciicode <= 90) else "")

                yield (dir, keyneeded)

    def _find_reachable_keys(self, coords, keysfound=""):
        for coord in coords:
            if not coord in self.reachable_keys:
                # Add to the cache via BFS search of all keys from coord. Keep
                # track of num steps
                self.reachable_keys[coord] = []
                visited = set()
                d = deque([(coord, 0, "")])
                while len(d) > 0:
                    node, steps, neededkeys = d.popleft()
                    visited.add(node)
                    # handling for if the node is a key
                    char = self.map[node]
                    if self._is_lower(char):
                        # add to the cache
                        self.reachable_keys[coord].append((node, steps, char, neededkeys))

                    # put all children nodes (not walls or doors) on the queue
                    for (dir, neededkey) in self._find_possible_dirs(node, visited):
                        d.append((self._add_dir(node, dir), steps + 1, neededkeys + neededkey))

        # Get the reachable keys and distances out of the cache
        def updatearr(coords, coord, node, i):
            newcoords = set(coords)
            newcoords.remove(coord)
            newcoords.add(node)
            return newcoords

        for i, coord in enumerate(coords):
            for (node, steps, key, neededkeys) in self.reachable_keys[coord]:
                if key not in keysfound and len(set(neededkeys) - set(keysfound)) == 0:
                    yield (updatearr(coords, coord,node, i), steps, key)


    def get_keys(self):
        G = nx.Graph()
        d = deque([("", frozenset(self.botcoords))])
        G.add_node(("", frozenset(self.botcoords)))
        G.add_node("FINISHLINE")

        # Construct graph
        while len(d) > 0:
            node = d.popleft()
            for (newcoords, dist, char)  in \
                self._find_reachable_keys(node[1], node[0]):
                newnode = ("".join(sorted(node[0] + char)), frozenset(newcoords))
                if newnode not in G:
                    G.add_node(newnode)
                    d.append(newnode)
                G.add_edge(node, newnode, weight=dist)
                if newnode[0] == self.allkeys:
                    G.add_edge(newnode, "FINISHLINE", weight=0)

        print(nx.dijkstra_path_length(G, ("", frozenset(self.botcoords)), "FINISHLINE", "weight"))


print("PART 1:")
bot = MapWalker(False)
bot.get_keys()

print("PART 2:")
bot = MapWalker(True)
bot.get_keys()
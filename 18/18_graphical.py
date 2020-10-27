import copy
import networkx as nx
from collections import deque

class MapWalker(object):
    DIRS=[(1, 0), (0, -1), (0, 1), (-1, 0)]

    def __init__(self):
        with open("18/map.txt", "r") as f:
            lines = f.readlines()

        self.map = list(line.strip("\n") for line in lines)
        self.XMAX = len(self.map[0])
        self.YMAX = len(self.map)
        self.reachable_keys = {}

        self.allkeys = ""
        for l in self.map:
            for char in l:
                if self._is_lower(char):
                    self.allkeys = "".join(sorted(self.allkeys + char))

        print(f"found all keys: {str(self.allkeys)}")
        self.shortest = 0
        self.keycombs = {}

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

            if x > self.XMAX or y > self.YMAX:
                continue

            asciicode = ord(self.map[y][x])
            if asciicode != 35:
                keyneeded = (chr(asciicode + 32) if (asciicode >= 65 and asciicode <= 90) else "")

                yield (dir, keyneeded)

    def _find_reachable_keys(self, coord, keysfound=""):
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
                char = self.map[node[1]][node[0]]
                if self._is_lower(char):
                    # add to the cache
                    self.reachable_keys[coord].append((node, steps, char, neededkeys))

                # put all children nodes (not walls or doors) on the queue
                for (dir, neededkey) in self._find_possible_dirs(node, visited):
                    d.append((self._add_dir(node, dir), steps + 1, neededkeys + neededkey))

            # add all the keys to the cache

        # Get the reachable keys and distances out of the cache
        keys = [(node, steps, key) for (node, steps, key, neededkeys) in \
                self.reachable_keys[coord] if \
                key not in keysfound and len(set(neededkeys) - set(keysfound)) == 0]
        return keys


    def _shortest_from(self, coord):
        G = nx.Graph()
        d = deque([("", coord)])
        G.add_node(("", coord))
        G.add_node("FINISHLINE")

        # Construct graph
        while len(d) > 0:
            node = d.popleft()
            for (keycoord, dist, char)  in \
                self._find_reachable_keys(node[1], node[0]):
                newnode = ("".join(sorted(node[0] + char)), keycoord)
                if newnode not in G:
                    G.add_node(newnode)
                    d.append(newnode)
                G.add_edge(node, newnode, weight=dist)
                if newnode[0] == self.allkeys:
                    G.add_edge(newnode, "FINISHLINE", weight=0)

        print(nx.dijkstra_path_length(G, ("", coord), "FINISHLINE", "weight"))

    def get_keys(self):
        for y, line in enumerate(self.map):
            if "@" in line:
                x = line.find("@")
                coord = (x, y)
                break

        self._shortest_from(coord)

    def plot(self):
        for line in self.map:
            print(line)

bot = MapWalker()
bot.plot()
bot.get_keys()
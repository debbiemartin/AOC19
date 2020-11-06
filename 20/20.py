# Need to use venv for this to get networkx
import copy
import networkx as nx
from collections import deque

class MapWalker(object):
    DIRS=[(1, 0), (0, -1), (0, 1), (-1, 0)]

    def __init__(self):
        with open("20/map.txt", "r") as f:
            lines = f.readlines()

        self.map = {}
        self.portals = {}
        self.reachable_portals_cache = {}
        self.extent = {"xmin":0, "xmax":0, "ymin":0, "ymax":0}
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip("\n")):
                self.map[(x, y)] = char
                if char == ".":
                    if self.extent["xmin"] == 0 or x < self.extent["xmin"]:
                        self.extent["xmin"] = x
                    if self.extent["xmax"] == 0 or x > self.extent["xmax"]:
                        self.extent["xmax"] = x
                    if self.extent["ymin"] == 0 or y < self.extent["ymin"]:
                        self.extent["ymin"] = y
                    if self.extent["ymax"] == 0 or y > self.extent["ymax"]:
                        self.extent["ymax"] = y
                
        for coord in self.map.keys():
            portal = self._is_portal(coord)
            if portal:
                outer = (coord[0] == self.extent["xmin"] or  
                         coord[0] == self.extent["xmax"] or 
                         coord[1] == self.extent["ymin"] or 
                         coord[1] == self.extent["ymax"])

                if portal in self.portals:
                    assert(len(self.portals[portal]) == 1)
                    self.portals[portal].append((coord, outer))
                else:
                    # We just add the start and end like this - no portal 
                    # hopping as 2nd element always None
                    self.portals[portal] = [(coord, outer)]

    def _add_dir(self, coord, dir):
        new_coord = tuple(c + d for c, d in zip(coord, dir))
        return new_coord
    
    def _is_upper(self, char):
        return ord(char) >= 65 and ord(char) <= 90

    def _is_portal(self, coord):
        """
        State whether is both . on the map and next to a portal. 
        """
        if self.map[coord] != ".":
            return None
    
        for dir in self.DIRS:
            tempcoord = self._add_dir(coord, dir)
            if self._is_upper(self.map[tempcoord]):
                # portal in this direction - find out what it is 
                tempcoord2 = self._add_dir(tempcoord, dir)
                assert(self._is_upper(self.map[tempcoord2]))
                # need to go L->R and U->D i.e. increasing x, increasing y
                if tempcoord[0] < tempcoord2[0] or tempcoord[1] < tempcoord2[1]:
                    portal = self.map[tempcoord] + self.map[tempcoord2]
                else:
                    portal = self.map[tempcoord2] + self.map[tempcoord]
                
                return portal 
               
        
    def _find_possible_dirs(self, coord, visited):
        for dir in self.DIRS:
            tempcoord = self._add_dir(coord, dir)

            if tempcoord in visited:
                continue

            if tempcoord not in self.map:
                continue

            if self.map[tempcoord] == ".":
                yield dir
                
                
    def _find_reachable_portals(self, coord):
        # cache now being called for different levels same coord     
        if coord in self.reachable_portals_cache: 
            return self.reachable_portals_cache[coord]
        
        visited = set()
        d = deque([(coord, 0)])
        reachable_portals = {}
        while len(d) > 0:
            node, steps = d.popleft()
            visited.add(node)

            # Search self.portals for the node
            if node != coord:
                for key, val in self.portals.items():
                    if val[0][0] == node:
                        reachable_portals[key] = (steps, 0)
                    elif len(val) == 2 and val[1][0] == node:
                        reachable_portals[key] = (steps, 1)
                    
            for dir in self._find_possible_dirs(node, visited):
                d.append((self._add_dir(node, dir), steps + 1))
        
        self.reachable_portals_cache[coord] = reachable_portals

        return reachable_portals
    
    def _add_new_node(self, G, d, oldnode, newnode, weight):
        if newnode[2] < 0 or \
           newnode[0] == "AA" or \
           (newnode[0] == "ZZ" and newnode[2] != 0):
            return
        if newnode not in G:
            G.add_node(newnode)
            if newnode[0] != "ZZ":
                d.append(newnode)
        if not G.has_edge(oldnode, newnode):
            G.add_edge(oldnode, newnode, weight=weight)            

    def shortest_path(self, recursive):
        G = nx.Graph()
        # format: (portal name, portal index (0 or 1), maze level)
        d = deque([("AA", 0, 0)]) 
        G.add_node(("AA", 0, 0))
        visited = []

        # Construct graph
        while len(d) > 0:
            node, index, level = d.popleft()
                    
            for newnode, (dist, newindex)  in \
                self._find_reachable_portals(self.portals[node][index][0]).items():
                
                # add the other side of the portal to the graph and queue
                if len(self.portals[newnode]) == 2:
                    if recursive:
                        newlevel = level + (-1 if self.portals[newnode][newindex][1] else 1)
                        if newlevel > len(self.portals):
                            continue
                    else:
                        newlevel = 0

                    self._add_new_node(G, d,
                                       (node, index, level),
                                       (newnode, 1-newindex, newlevel),
                                       dist + 1)
                elif newnode == "ZZ":
                    self._add_new_node(G, d, 
                                       (node, index, level),
                                       (newnode, newindex, level),
                                       dist)
        
        def astar_heur(node1, node2):
            # this doesn't really make much difference.. 
            return node1[2]

        print(nx.astar_path_length(G, ("AA", 0, 0), ("ZZ", 0, 0), 
                                   heuristic=astar_heur, weight="weight"))


bot = MapWalker()
print("PART 1:")
bot.shortest_path(False)

print("PART 2:")
bot.shortest_path(True)

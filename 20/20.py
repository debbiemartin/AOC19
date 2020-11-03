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
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip("\n")):
                self.map[(x, y)] = char
                
        for coord in self.map.keys():
            portal = self._is_portal(coord)
            if portal:
                if portal in self.portals:
                    assert(self.portals[portal][1] == None)
                    self.portals[portal] = (self.portals[portal][0], coord)
                else:
                    # We just add the start and end like this - no portal 
                    # hopping as 2nd element always None
                    self.portals[portal] = (coord, None)

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
        visited = set()
        d = deque([(coord, 0)])
        reachable_portals = {}
        while len(d) > 0:
            node, steps = d.popleft()
            visited.add(node)

            portal = self._is_portal(node)
            if portal and node != coord:
                reachable_portals[portal] = (steps, 0 if node == self.portals[portal][0] else 1)
                    
            for dir in self._find_possible_dirs(node, visited):
                d.append((self._add_dir(node, dir), steps + 1))

        return reachable_portals

    def shortest_path(self):
        G = nx.Graph()
        d = deque([("AA", 0)])
        G.add_node(("AA", 0))

        # Construct graph
        while len(d) > 0:
            node, index = d.popleft()
            
            # add the other side of the portal to the graph and queue
            if self.portals[node][1-index]:
                if (node, 1-index) not in G:
                    G.add_node((node, 1-index))
                    d.append((node, 1-index))
                if not G.has_edge((node, index), (node, 1-index)):
                    G.add_edge((node, index), (node, 1-index), weight=1)
            
            for newnode, (dist, newindex)  in \
                self._find_reachable_portals(self.portals[node][index]).items():

                if (newnode, newindex) not in G: 
                    G.add_node((newnode, newindex))
                    d.append((newnode, newindex)) 
                
                if not G.has_edge((node, index), (newnode, newindex)):
                    G.add_edge((node, index), (newnode, newindex), weight=dist) 

        print(nx.dijkstra_path_length(G, ("AA", 0), ("ZZ", 0), "weight"))


print("PART 1:")
bot = MapWalker()
bot.shortest_path()
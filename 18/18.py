#!/usr/bin/python3
import copy

class MapWalker(object):
    def __init__(self):
        with open("18/map.txt", "r") as f:
            lines = f.readlines()

        self.map = list(line.strip("\n") for line in lines)
        self.XMAX = len(self.map[0])
        self.YMAX = len(self.map)
        self.shortest = 0

    def _add_dir(self, coord, dir):
        new_coord = tuple(c + d for c, d in zip(coord, dir))
        return new_coord

    def _find_possible_dirs(self, coord, map, camefrom=None):
        poss_dirs = []

        for dir in [(1, 0), (0, -1), (0, 1), (-1, 0)]:
            x, y = self._add_dir(coord, dir)

            if camefrom and (x, y) == camefrom:
                continue

            if x > self.XMAX or y > self.YMAX:
                continue

            asciicode = ord(map[y][x])
            if asciicode != 35 and not (asciicode >= 65 and asciicode <= 90):
                # not a wall or upper case letter
                poss_dirs.append(dir)

        return poss_dirs

    def _shortest_from(self, coord, dir, map, steps):
        steps += 1
        if self.shortest != 0 and steps >= self.shortest:
            return

        mapcpy = copy.deepcopy(map)
        newcoord = self._add_dir(coord, dir)
        asciicode = ord(mapcpy[newcoord[1]][newcoord[0]])

        # found a key
        if asciicode >= 97 and asciicode <= 122:
            #print(f"found a key: {chr(asciicode)}")
            mapcpy[newcoord[1]] = mapcpy[newcoord[1]].replace(chr(asciicode), ".")
            for i, line in enumerate(mapcpy):
                mapcpy[i] = line.replace(chr(asciicode - 32), ".")
            # ok to go back on yourself if you've found a key
            poss_dirs = self._find_possible_dirs(newcoord, mapcpy)
        else:
            poss_dirs = self._find_possible_dirs(newcoord, mapcpy, camefrom=coord)

        if not any(chr(a) in l for l in mapcpy for a in range(97, 123)):
            print(f"all keys found! steps: {steps}")
            self.shortest = steps

        for d in poss_dirs:
            self._shortest_from(newcoord, d, mapcpy, steps)

    def get_keys(self):
        for y, line in enumerate(self.map):
            if "@" in line:
                x = line.find("@")
                coord = (x, y)
                break

        poss_dirs = self._find_possible_dirs(coord, self.map)
        assert(len(poss_dirs) > 0)

        for d in poss_dirs:
            self._shortest_from(coord, d, self.map, 0)

        print(f"shortest solution: {self.shortest}")

    def plot(self):

        for line in self.map:
            print(line)

bot = MapWalker()
bot.plot()
bot.get_keys()



#!/auto/ensoft/bin/python3

import math
import collections

def los_equivalent(los1, los2):
    # lines of sight are tuples of x, y coord. los equivalent if transformation
    # to polar coords and the radial angle coincides
    theta1 = math.atan2(los1[0], los1[1])
    theta2 = math.atan2(los2[0], los2[1])

    return theta1 == theta2


asteroids = []
with open("asteroids.txt", 'r') as f:
    lines = f.readlines()
    for linenum, line in enumerate(lines):
        for charnum, char in enumerate(line):
            if char == "#":
                asteroids.append((charnum, linenum))

MAX_LOS = 0
ASTEROID = (-1,-1)
for asteroid in asteroids:
    unique_los = {}

    for other in (other for other in asteroids if other != asteroid):
        los = (asteroid[0] - other[0], asteroid[1] - other[1])
        # use -x, y not y, x to rotate clockwise from upwards
        theta = math.fmod(-math.atan2(los[0], los[1]) + 2*math.pi, 2*math.pi)
        if theta not in unique_los:
            unique_los[theta] = []
        unique_los[theta].append(los)

    if len(unique_los) > MAX_LOS:
        MAX_LOS = len(unique_los)
        ASTEROID = asteroid
        UNIQUE_LOS = unique_los

print(MAX_LOS)
print(ASTEROID)

od = collections.OrderedDict(sorted(UNIQUE_LOS.items()))
for key, val in od.items():
    # sort based on r magnitude polar coords
    od[key] = sorted(val, key=lambda x: x[0]**2 + x[1]**2)

count = 0
while count < 200:
    for los, coords in od.items():
        if len(coords) > 0:
            first = coords.pop(0)
            count += 1
            if count == 1 or count == 200:
                absolute_coords = (ASTEROID[0] - first[0],  ASTEROID[1] - first[1])
                print("found item count {}: rel {} abs {}".format(count, first, absolute_coords))
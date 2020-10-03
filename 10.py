#!/auto/ensoft/bin/python3

def los_equivalent(los1, los2):
    # lines of sight are tuples of x, y coord. Technically should transform to
    # polar coordinates but then we still have to worry about dividing by 0
    # and choosing correct arctan solution so just do it manually
    if los1[0] == 0:
        # to be equivalent, los2 x coord also 0 and same sign
        if los2[0] == 0 and los1[1]*los2[1] > 0:
            return True
    elif los1[1] == 0:
        # to be equivalent, los2 y coord also 0 and same sign
        if los2[1] == 0 and los1[0]*los2[0] > 0:
            return True
    elif los2[0]/los1[0] == los2[1]/los1[1] and los1[0]*los2[0] > 0:
        # same ratio and each have same sign, prevents e.g. (1,2), (-2,-4)
        return True
    return False

asteroids = []
with open("asteroids.txt", 'r') as f:
    lines = f.readlines()
    for linenum, line in enumerate(lines):
        for charnum, char in enumerate(line):
            if char == "#":
                asteroids.append((charnum, linenum))
                #add coord to list of asteroids

MAX_LOS = 0
ASTEROID = (-1,-1)
for asteroid in asteroids:
    unique_los = []

    for other in (other for other in asteroids if other != asteroid):
        los = (other[0] - asteroid[0], other[1] - asteroid[1])
        if not any([los_equivalent(los, unique) for unique in unique_los]):
            unique_los.append(los)

    if len(unique_los) > MAX_LOS:
        MAX_LOS = len(unique_los)
        ASTEROID = asteroid

print(MAX_LOS)
print(ASTEROID)

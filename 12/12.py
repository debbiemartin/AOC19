#!/usr/bin/python3

import math

def pairs(list):
    for i in range(len(list)):
        for j in range(i + 1, len(list)):
            yield((list[i], list[j]))

def lcm(x, y):
   return int(x*y/math.gcd(x,y))

#4 moons: I, E, G, C
with open("12/positions.txt",  'r') as f:
    lines = f.readlines()

# convert e.g. <x=19, y=-10, z=7> to (19,-10,7)
moons = []
moons_initial = []
for line in lines:
    coords = list(int(coord.split("=")[1]) for coord in line.strip("<>\n").lstrip().split(","))
    moons.append({"x":coords[:], "v":[0,0,0]})
    moons_initial.append({"x":coords[:], "v":[0,0,0]})

periods = [0,0,0]

step = 0
while True:
    step += 1

    # apply gravity to each pair of moons
    for (moon1, moon2) in pairs(moons):
        for i in range(3):
            if moon1["x"][i] != moon2["x"][i]:
                diff = (-1 if moon1["x"][i] > moon2["x"][i] else 1)
                moon1["v"][i] += diff
                moon2["v"][i] -= diff

    # apply new velocity to the position
    for moon in moons:
        for n, (x, v) in enumerate(zip(moon["x"], moon["v"])):
            moon["x"][n] = x + v

    for i in range(3):
        if all(moon["v"][i] == 0 for moon in moons):
            print("found period for spacial dimension {}: {}".format(i, step))
            periods[i] = step
            print(periods)

    if not any(period == 0 for period in periods):
        print("all periods found")
        break

answer = lcm(periods[0], periods[1])
answer = lcm(answer, periods[2])

print(answer * 2)

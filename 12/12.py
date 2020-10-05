#!/auto/ensoft/bin/python3

def pairs(list):
    for i in range(len(list)):
        for j in range(i + 1, len(list)):
            yield((list[i], list[j]))

#4 moons: I, E, G, C
#
with open("12/positions.txt",  'r') as f:
    lines = f.readlines()

# convert e.g. <x=19, y=-10, z=7> to (19,-10,7)
moons = []
for line in lines:
    coords = list(int(coord.split("=")[1]) for coord in line.strip("<>\n").lstrip().split(","))
    moons.append({"x":coords, "v":[0,0,0]})

moons_initial = moons[:]
print(moons_initial)

step = 0
while True:
    step += 1
    # apply gravity to each pair of moons
    for (moon1, moon2) in pairs(moons):
        for i in range(3):
            if moon1["x"][i] != moon2["x"][i]:
                diff = (-1 if moon1["x"][i] < moon2["x"][i] else 1)
                moon1["v"][i] -= diff
                moon2["v"][i] += diff

    # apply new velocity to the position
    for moon in moons:
        for num, (x, v) in enumerate(zip(moon["x"], moon["v"])):
            moon["x"][num] = x + v

print(moons)
energy = sum(sum(list(map(abs, moon["x"]))) * sum(list(map(abs, moon["v"]))) for moon in moons)
print(energy)


#!/usr/bin/python

orbits = {}
planets = {}
lookups = []


def add_orbits(planet):

    orbit_num = planets[planet]

    if planet in orbits:
        for orbiters in orbits[planet]:
            planets[orbiters] = orbit_num + 1
            add_orbits(orbiters)


with open('6/orbits.txt', 'r') as f:
    for line in f:
        orbit_pair = line.split(")")
        orbit_pair[1] = orbit_pair[1].strip('\n')
        if orbit_pair[0] not in orbits:
            orbits[orbit_pair[0]] = []
        orbits[orbit_pair[0]].append(orbit_pair[1])

        if orbit_pair[0] not in planets.keys():
            planets[orbit_pair[0]] = 0
        if orbit_pair[1] not in planets.keys():
            planets[orbit_pair[1]] = 0

        if orbit_pair[0] == "COM":
            lookups.append(orbit_pair[1])
            planets[orbit_pair[1]] = 1

for lookup in lookups:
    add_orbits(lookup)

print(lookups)
print(orbits)
print(planets)

total = sum(planets[name] for name in planets)

print(total)


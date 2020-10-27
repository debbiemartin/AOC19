#!/usr/bin/python

orbits = {} # planet with a list of orbiteds
hops_from_you = {} # planet with shortest number of hops from you
hops_from_san = {} # planet with shortest number of hops from santa

def calculate_hops(planet, hops, lookup):
    if not planet in lookup:
        # not in the dictionary already - add it with num hops
        lookup[planet] = hops
    else:
        # already got a number of hops, but we want the smallest
        if hops < lookup[planet]:
            lookup[planet] = hops

    if planet in orbits: # protects for "COM"
        for orbitted_planet in orbits[planet]:
            calculate_hops(orbitted_planet, hops + 1, lookup)

with open('6/orbits.txt', 'r') as f:
    for line in f:
        orbit_pair = line.split(")")
        orbit_pair[1] = orbit_pair[1].strip('\n')
        if orbit_pair[1] not in orbits:
            orbits[orbit_pair[1]] = []
        orbits[orbit_pair[1]].append(orbit_pair[0])

if not "SAN" in orbits:
    print("ERROR: santa not orbiting")
if not "YOU" in orbits:
    print("ERROR: you aren't orbiting")

for planet in orbits:
    calculate_hops("YOU", 0, hops_from_you)
    calculate_hops("SAN", 0, hops_from_san)

hops = 0
for planet in hops_from_san:
    if planet in hops_from_you and (hops == 0 or hops_from_san[planet] + hops_from_you[planet] < hops):
        hops = hops_from_san[planet] + hops_from_you[planet]
        print("Found new ancestor: {}. Hops: {}. From San: {}. From you: {}".format(planet, hops, hops_from_san[planet], hops_from_you[planet]))

hops = hops-2
print(hops)


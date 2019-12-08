#!/auto/ensoft/bin/python


orbits = []
names = {}
lookups = []


def add_orbits(planet):

    orbit_num = names[planet]
    for pair in orbits:
        if pair[0] == planet:
            print(pair[1])
            names[pair[1]] = orbit_num + 1
            add_orbits(pair[1])


with open('orbits.txt', 'r') as f:
    for line in f:
        orbit_pair = line.split(")")
        orbit_pair[1] = orbit_pair[1].strip('\n')
        orbits.append(orbit_pair)

        if orbit_pair[0] not in names.keys():
            print(orbit_pair[0])
            names[orbit_pair[0]] = 0
        if orbit_pair[1] not in names.keys():
            names[orbit_pair[1]] = 0
        
        if orbit_pair[0] == "COM":
            lookups.append(orbit_pair[1])
            names[orbit_pair[1]] = 1    


for lookup in lookups:
    add_orbits(lookup)

print(lookups)
print(orbits)
print(names)

total = sum(names[name] for name in names)

print(total)    
    

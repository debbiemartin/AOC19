#!/auto/ensoft/bin/python3

import math

class ReactionSimulator(object):

    def __init__(self, reactions, num):
        self.reactions = reactions
        self.amounts = {"FUEL": num}
        self.ore = 0
        self.levels = {}
        self._assign_levels()

    def _assign_level(self, number):
        # find all the elements which can be made just from less number levels
        keep_going = False
        for elem, reaction in self.reactions.items():
            if elem not in self.levels:
                if all((key in self.levels and self.levels[key] < number) for key in reaction[1].keys()):
                    # all reactants must have lower numbers
                    self.levels[elem] = number
                else:
                    keep_going = True

        if keep_going:
            self._assign_level(number + 1)


    def _assign_levels(self):
        self.levels["ORE"] = 0
        self._assign_level(1)

    def _convert(self, element, amount):
        if amount != 0:
            factor = math.floor(amount/reactions[element][0])

            if factor == 0:
                return False

            self.amounts[element] -= factor * reactions[element][0]
            if self.amounts[element] <= 0:
                del self.amounts[element]

            for reactant, coeff in reactions[element][1].items():
                if reactant == "ORE":
                    self.ore += factor * coeff
                elif reactant in self.amounts:
                    self.amounts[reactant] += factor * coeff
                else:
                    self.amounts[reactant] = factor * coeff

            return True
        return False


    def start(self):
        while True:
            none_converted = True
            amountcpy = self.amounts.copy()
            for key, val in amountcpy.items():
                if self._convert(key, val):
                    none_converted = False

            if len(self.amounts) == 0:
                return self.ore

            if none_converted:
                # convert one load of the first element which isn't a reactant
                # in self.amounts
                convert_elem = None
                for key, val in amountcpy.items():
                    if not convert_elem or self.levels[key] > self.levels[convert_elem]:
                        convert_elem = key

                self._convert(convert_elem, self.reactions[convert_elem][0])

with open("14/reactions.txt", 'r') as f:
    lines = f.readlines()

reactions = {}
for line in lines:
    reactants_product = line.strip("\n").split(" => ")
    reactants = {}
    for reactant in reactants_product[0].split(", "):
        reactants[reactant.split(" ")[1]] = int(reactant.split(" ")[0])
    reactions[reactants_product[1].split(" ")[1]] = (int(reactants_product[1].split(" ")[0]), reactants)

sim = ReactionSimulator(reactions, 1)
ore = sim.start()
print(f"part 1 ore: {ore}")


TRILLION = 1000000000000
sim = ReactionSimulator(reactions, TRILLION)
ore = sim.start()
print(f"part 2 fuel: {int(TRILLION**2/ore)}")


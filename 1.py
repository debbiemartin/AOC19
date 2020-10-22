#!/auto/ensoft/bin/python

import sys
import math


def calc_fuel(mass):
    fuel = math.floor(mass/3) - 2
    if fuel < 0:
        fuel = 0

    return(fuel)

def account_for_fuel(fuel):
    additional_fuel = calc_fuel(fuel)
    if additional_fuel > 0:
        total = account_for_fuel(additional_fuel)
        return (total + fuel)
    else:
        return (fuel)



def main():
    total_fuel = 0
    with open('spaceship_data.txt', 'r') as f:
        for line in f:
            fuel = calc_fuel(int(line))
            fuel = account_for_fuel(fuel)

            total_fuel = total_fuel + fuel
    print(total_fuel)


if __name__ == "__main__":
    main()




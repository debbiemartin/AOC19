#!/usr/bin/python3

from subprocess import Popen, PIPE, STDOUT

class ASCII(object):
    def __init__(self, txtfile):
        self.p = Popen(['python3', '-u', '9/9.py', txtfile],
                       stdout=PIPE, stdin=PIPE, stderr=PIPE)
        self.coords = {}

    def read(self):
        coord = (0,0)
        while True:
            char = self.p.stdout.readline().decode('utf-8').strip('\n')

            if char == '' or char == "Need input":
                break
            else:
                char = int(char)

            if char == 10:
                coord = (0, coord[1] + 1)
            else:
                self.coords[coord] = chr(char)
                coord = (coord[0] + 1, coord[1])

    def _writestdin(self, input):
        self.p.stdin.write("{}\n".format(input).encode('utf-8'))
        self.p.stdin.flush()
        if True: #not end:
            while True:
                output = self.p.stdout.readline().decode('utf-8').strip("\n")
                if output == "Need input":
                    break
                elif output == "":
                    return
                elif int(output) > 137:
                    print(f"Answer: {output}")
                else:
                    print(chr(int(output)), end="")

    def instruct(self, instructions):
        # separate by comma and 10 at the end for newline
        for i, inst in enumerate(instructions):
            # if it's an integer write the integer
            if type(inst) != str:
                inst = str(inst)

            for char in inst:
                self._writestdin(str(ord(char)))

            if i < len(instructions) - 1:
                self._writestdin(str(ord(",")))

        self._writestdin(str(ord("\n")))

    def plot(self):
        coord = (0,0)
        while True:
            if coord in self.coords:
                print(self.coords[coord], end="")
                coord = (coord[0] + 1, coord[1])
            else:
                print("")
                coord = (0, coord[1] + 1)
                if not coord in self.coords:
                    break

class ASCII_random(ASCII):
    def __init__(self):
        super().__init__('17/asciicomp.txt')

    def find_alignment_parameters(self):
        # search for any coords of intersections
        sum = 0
        for coord in self.coords.keys():
            if self.coords[coord] == "#":
                neighbours =  [(coord[0], coord[1] + 1),
                               (coord[0], coord[1] - 1),
                               (coord[0] + 1, coord[1]),
                               (coord[0] - 1, coord[1])]

                if all(n in self.coords and self.coords[n] == "#" for n in neighbours):
                    sum += coord[0] * coord[1]

        print(f"found alignment parameters, sum = {sum}")

class ASCII_instructed(ASCII):
    def __init__(self):
        super().__init__('17/asciicomp_instructed.txt')
        self.functions = {}
        self.main_routine = None

    def _transform_direction(self, dir, right):
        # looks weird because y measured downwards..
        # R: (0, 1) -> (-1, 0) -> (0, -1) -> (1, 0)
        # L: (0, 1) -> (1, 0) -> (0, -1) -> (-1, 0)
        new_dir = (dir[1], dir[0])
        if (right and dir[0] == 0) or (not right and dir[1] == 0):
            new_dir = tuple(i * (-1) for i in new_dir)

        return new_dir

    def _add_coord(self, coord, dir):
        new_coord = (coord[0] + dir[0], coord[1] + dir[1])

        return new_coord

    def _look_straight(self, coord, dir):
        new_coord = self._add_coord(coord, dir)

        return (self.coords[new_coord] if new_coord in self.coords else "")

    def _look_in_dir(self, coord, dir, right):
        new_dir = self._transform_direction(dir, right)

        return self._look_straight(coord, new_dir)

    def _find_path(self):
        # need to find the complete set of R,10,L,12 etc to get all the way
        # around
        # split this up into 3 identical patterns and put repeating in first as
        # A,B,B,C,A e.g.
        bot_vals = {"^":(0,-1), ">":(1,0), "<":(-1,0), "v":(0,1)}
        for coord, val in self.coords.items():
            if val in bot_vals.keys():
                bot_coord = coord
                bot_dir = bot_vals[val]

        sequence = []

        while True:
            # start with direction, see whether right or left gives #
            if self._look_in_dir(bot_coord, bot_dir, True) == "#":
                right = True
            elif self._look_in_dir(bot_coord, bot_dir, False) == "#":
                right = False
            else:
                print(f"finished finding bot sequence:\n{str(sequence)}")
                break

            # go in dir for as long as possible
            bot_dir = self._transform_direction(bot_dir, right)
            steps = 0
            while self._look_straight(bot_coord, bot_dir) == "#":
                steps += 1
                bot_coord = self._add_coord(bot_coord, bot_dir)

            sequence.append(("R" if right else "L", steps))

        return sequence

    def _find_longest_subseq(self, sequence, letter):
        for i in range(len(sequence)):
            if type(sequence[i]) == tuple:
                start = i
                break

        for end in range(start+1, start+min(int(len(sequence)/2), 10), 1):
            if any(type(elem) != tuple for elem in sequence[start:end]):
                break

            if any(sequence[end+offset:end+offset+(end-start)] == sequence[start:end] \
                   for offset in range(0, len(sequence) - end + start, 1)):
                best_end = end

        # store subsequence in instance for instructing intcode
        subseq = sequence[start:best_end]
        self.functions[letter] = []
        for tuples in subseq:
            self.functions[letter].append(tuples[0])
            self.functions[letter].append(tuples[1])

        # replace all instances of subsequence with the letter specified
        new_sequence = []
        i = 0
        while i < len(sequence):
            if sequence[i:i+len(subseq)] == subseq:
                new_sequence.append(letter)
                i += len(subseq)
            else:
                new_sequence.append(sequence[i])
                i += 1

        return new_sequence

    def _find_repeats(self, sequence):
        # find A
        sequence = self._find_longest_subseq(sequence, "A")
        # find B
        sequence = self._find_longest_subseq(sequence, "B")
        #find C
        sequence = self._find_longest_subseq(sequence, "C")
        self.main_routine = sequence

    def _send_instructions(self):
        self.instruct(self.main_routine)
        self.instruct(self.functions["A"])
        self.instruct(self.functions["B"])
        self.instruct(self.functions["C"])
        self.instruct(["y"])

    def walk_scaffolding(self):
        sequence = self._find_path()
        self._find_repeats(sequence)
        self._send_instructions()

print("PART 1:")
bot = ASCII_random()
bot.read()
bot.plot()
bot.find_alignment_parameters()


print("PART 2:")
bot = ASCII_instructed()
bot.read()
bot.walk_scaffolding()
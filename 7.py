#!/auto/ensoft/bin/python3

from subprocess import Popen, PIPE, STDOUT
import time

MAXIMUM=0
class Intcode():
    def __init__(self, cb, phase):
        self.cb = cb
        self.phase = phase
        self.p = Popen(['python3', '-u', './5.py'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        phasestr = str(self.phase + 5) + "\n"
        self.p.stdin.write(phasestr.encode('utf-8'))

    def set_cb(self, cb):
        self.cb = cb

    def operate(self, input):
        self.p.stdin.write(input)
        try:
            self.p.stdin.flush()
        except BrokenPipeError:
            pass
        output = self.p.stdout.readline()
        if output == b'':
            phase_answer(input)
        else:
            self.cb(output)

def phase_answer(input):
    global MAXIMUM
    if int(input.decode('utf-8')) > MAXIMUM:
        MAXIMUM = int(input.decode('utf-8'))

def test_permutation(phases):
    e = Intcode(None, phases[4])
    d = Intcode(e.operate, phases[3])
    c = Intcode(d.operate, phases[2])
    b = Intcode(c.operate, phases[1])
    a = Intcode(b.operate, phases[0])
    e.set_cb(a.operate)

    a.operate("0\n".encode('utf-8'))

def test_phase(phases, index):
    if index < 4:
        for i in range(5):
            if not any(i == phases[j] for j in range(index + 1)):
                phases[index + 1] = i
                test_phase(phases, index + 1)
    elif index == 4:
        # All filled in - test permutation
        test_permutation(phases)

for i in range(5):
    test_phase([i,0,0,0,0], 0)

print("Maximum found: {}".format(MAXIMUM))
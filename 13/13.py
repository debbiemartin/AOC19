#!/auto/ensoft/bin/python3

from subprocess import Popen, PIPE, STDOUT

def process(tiles):
    p = Popen(['python3', '-u', './9.py'], stdout=PIPE, stdin=PIPE, stderr=PIPE)

    while True:
        outputs = [0,0,0]

        for i in range(3):
            output = p.stdout.readline()
            if output == b'':
                print("finished")
                return
            outputs[i] = int(output.decode('utf-8').strip('\n'))
        tiles[(outputs[0], outputs[1])] = outputs[2]


#    0 is an empty tile. No game object appears in this tile.
#    1 is a wall tile. Walls are indestructible barriers.
#    2 is a block tile. Blocks can be broken by the ball.
#    3 is a horizontal paddle tile. The paddle is indestructible.
#    4 is a ball tile. The ball moves diagonally and bounces off objects.


#    If the joystick is in the neutral position, provide 0.
#    If the joystick is tilted to the left, provide -1.
#    If the joystick is tilted to the right, provide 1.


tiles = {}
process(tiles)
print(sum(1 for value in tiles.values() if value == 2))
# count up #2s in tiles
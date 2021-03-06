#!/usr/bin/python3

from subprocess import Popen, PIPE, STDOUT

#    ***CODES***
#
#    0 is an empty tile. No game object appears in this tile.
#    1 is a wall tile. Walls are indestructible barriers.
#    2 is a block tile. Blocks can be broken by the ball.
#    3 is a horizontal paddle tile. The paddle is indestructible.
#    4 is a ball tile. The ball moves diagonally and bounces off objects.
CODE_PLOT = [" ", "|", "x", "_", "O"]

def get_tiles(p, tiles, score):
    while True:
        outputs = [0,0,0]

        for i in range(3):
            output = p.stdout.readline()
            if output == b'' or output == b"Need input\n":
                return score
            outputs[i] = int(output.decode('utf-8').strip('\n'))
        coords = (outputs[0], outputs[1])
        if coords == (-1, 0):
            score = outputs[2]
        else:
            tiles[coords] = outputs[2]

    return score

def plot(tiles, score):
    print("SCORE: {}".format(score))

    XMAX = max(coord[0] for coord in tiles.keys())
    YMAX = max(coord[1] for coord in tiles.keys())
    for y in range(YMAX, -1, -1):
        for x in range(XMAX+1):
            coord = (x, y)
            if coord not in tiles:
                print(" ", end='')
            elif y == 0 or y == YMAX and tiles[coord] == 1:
                # horizontal wall tile
                print("-", end='')
            else:
                print(CODE_PLOT[tiles[coord]], end='')
        print("")



def play():
    #    If the joystick is in the neutral position, provide 0.
    #    If the joystick is tilted to the left, provide -1.
    #    If the joystick is tilted to the right, provide 1.

    p = Popen(['python3', '-u', '9/9.py', '13/instructions.txt'], 
              stdout=PIPE, stdin=PIPE, stderr=PIPE)
    tiles = {}
    i = 0
    score = 0
    while True:
        score = get_tiles(p, tiles, score)
        #plot(tiles, score)

        for key, val in tiles.items():
            if val == 4:
                ball_coords = key
            elif val == 3:
                paddle_coords = key

        num_blocks = sum(1 for value in tiles.values() if value == 2)

        if ball_coords[1] == paddle_coords[1]:
            # ball is travelling past paddle
            print("ball passed paddle...")
            break
        elif num_blocks == 0:
            print("Finished!!! all blocks gone")
            break

        nextmove = (0 if ball_coords[0] == paddle_coords[0] else (1 if ball_coords[0] > paddle_coords[0] else -1))

        p.stdin.write("{}\n".format(nextmove).encode('utf-8'))
        p.stdin.flush()

        i += 1

    return (num_blocks, score, i)

def smash_all_blocks():
    num_blocks = -1

    num_blocks, endscore, moves = play()
    print("iteration num_blocks {} endscore {} nummoves {}".format(num_blocks, endscore, moves))

smash_all_blocks()

#!/bin/python3
# -*- coding: utf-8 -*-

from xo import XOXO

# For the output decoration
red = '\x1b[31m'
green = '\x1b[32m'
blue = '\x1b[34m'
reset = '\x1b[0m'

def main():
    game = XOXO()

    # Start the game and see who is the winner
    the_winner = game.start()
    if None != the_winner:
        if 'X' == the_winner:
            print("%sThe winner is: X!%s" % (green, reset))
        else:
            print("%sThe winner is: O!%s" % (red, reset))
    else:
        print("%sIt's a tie!%s" % (blue, reset))


if __name__ == '__main__':
    main()

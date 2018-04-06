#!/bin/python3
# -*- coding: utf-8 -*-

from random import shuffle


class XOXO:
    """ Tic-tac-toe representing class using alpha-beta algorithm
        You are player X and you are playing firs"""
    def __init__(self):
        self.board = [['-' for x in range(3)] for y in range(3)]
        self.player = 'X'

    def print_board(self):
        """ The method used to print the board """
        print()
        for row in self.board:
            for item in row:
                print(item, end=' ')
            print()
        print()

    def empty_fields(self):
        """ The method which returns possible moves """
        empty_fields = []
        for i in range(3):
            for j in range(3):
                if '-' == self.board[i][j]:
                    empty_fields.append((i, j))
        shuffle(empty_fields)
        return empty_fields

    def game_over(self):
        """ The method which indicates whether the game is over """
        if not self.empty_fields() or None != self.winner():
            return True
        else:
            return False

    def winner(self):
        """ The method which returns the winner of the game
            or None if it's a tie """
        if '-' != self.board[0][0] == self.board[0][1] == self.board[0][2] \
        or '-' != self.board[1][0] == self.board[1][1] == self.board[1][2] \
        or '-' != self.board[2][0] == self.board[2][1] == self.board[2][2] \
        or '-' != self.board[0][0] == self.board[1][1] == self.board[2][2] \
        or '-' != self.board[2][0] == self.board[1][1] == self.board[0][2] \
        or '-' != self.board[0][0] == self.board[1][0] == self.board[2][0] \
        or '-' != self.board[0][1] == self.board[1][1] == self.board[2][1] \
        or '-' != self.board[0][2] == self.board[1][2] == self.board[2][2]:
            return 'X' if 'O' == self.player else 'O'
        else:
            return None

    def move(self, i, j):
        """ The method used to make a move """
        if '-' != self.board[i][j]:
            return

        self.board[i][j] = self.player
        self.player = 'X' if 'O' == self.player else 'O'

    def unmove(self, i, j):
        """ The method used to unplay a move that is previously played """
        if '-' == self.board[i][j]:
            return

        self.board[i][j] = '-'
        self.player = 'X' if 'O' == self.player else 'O'

    def value(self):
        """ The method which returns the valuation of end state """
        player = self.winner()
        if 'X' == player:
            return 1
        elif 'O' == player:
            return -1
        else:
            return 0

    def min(self, alpha, beta):
        """ The min method (originally from minimax) """

        # Exit recursion
        if self.game_over():
            return (self.value(), None)

        # The initialization of the value and the best move
        value = float('inf')
        best_move = None

        # Iteration through the possible moves
        for (i, j) in self.empty_fields():
            # Try one of the possible moves
            self.move(i, j)
            maximum = self.max(alpha, beta)[0]

            # If maximum is less than the value, set the value to it and
            # remember the played move
            if maximum < value:
                value = maximum
                best_move = (i, j)

            # Unplay the move that is previously played
            self.unmove(i, j)

            # -----------------------------------------------------------------
            # If the value is less (or equal) than alpha, perform an alpha cut
            # off or else if the value is less than beta then set the beta to
            # the value
            # -----------------------------------------------------------------
            if value <= alpha:
                return(value, (i, j))
            elif value < beta:
                beta = value

        return(value, best_move)

    def max(self, alpha, beta):
        """ The max method (originally from minimax) """

        # Exit recursion
        if self.game_over():
            return(self.value(), None)

        # The initialization of the value and the best move
        value = float('-inf')
        best_move = None

        # Iteration through the possible moves
        for (i, j) in self.empty_fields():
            # Try one of the possible moves
            self.move(i, j)
            minimum = self.min(alpha, beta)[0]

            # If minimum is greater than the value, set the value to it and
            # remember the played move
            if minimum > value:
                value = minimum
                best_move = (i, j)
            # Unplay the move that is previously played
            self.unmove(i, j)

            # -----------------------------------------------------------------
            # If the value is greater (or equal) than beta, perform an beta
            # cut off or else if the value is less than alpha then set the
            # alpha to the value
            # -----------------------------------------------------------------
            if value >= beta:
                return(value, (i, j))
            elif value > alpha:
                alpha = value

        return(value, best_move)

    def start(self):
        """ The method that starts a game of Tic-tac-toe """
        # Run the loop until the game is over
        while not self.game_over():
            i, j = int(input()), int(input())

            # Your move
            self.move(i, j)
            self.print_board()

            # The game is over, exiting the while loop
            if self.game_over():
                break

            # Let the opponent play
            (i, j) = self.min(float('-inf'), float('inf'))[1]
            self.move(i, j)
            self.print_board()

        # Return the winner
        return self.winner()

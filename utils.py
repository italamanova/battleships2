from random import randint

from constants import HORIZONTAL, SIZE


def get_random_row(orientation, ship_size):
    if orientation == HORIZONTAL:
        return randint(0, SIZE - 1)
    else:
        return randint(0, SIZE - ship_size)


def get_random_col(orientation, ship_size):
    if orientation == HORIZONTAL:
        return randint(ship_size - 1, SIZE - 1)
    else:
        return randint(0, SIZE - 1)


def print_board(player_board, player_guesses, size):
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("  0 1 2 3 4 5 6 7 8 9 || 0 1 2 3 4 5 6 7 8 9")
    i = 0
    for row in range(size):
        print(i, " ".join(player_guesses.board[row]), "||", " ".join(player_board.board[row]))
        i += 1

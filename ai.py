from random import randint

from constants import UNKNOWN, HORIZONTAL, VERTICAL, SIZE


# Guesses cell if
def guess_cell(ai_guesses_board):
    busy = True
    while busy:
        row_to_check = randint(0, SIZE - 1)
        col_to_check = randint(0, SIZE - 1)
        busy = not ai_guesses_board.is_cell_water(row_to_check, col_to_check)
    return row_to_check, col_to_check


def get_ship_orientation(hit_row, hit_col, ai_guesses_board):
    orientation = UNKNOWN
    if ai_guesses_board.is_cell_hit(hit_row + 1, hit_col):
        orientation = VERTICAL
    if ai_guesses_board.is_cell_hit(hit_row - 1, hit_col):
        orientation = VERTICAL
    if ai_guesses_board.is_cell_hit(hit_row, hit_col + 1):
        orientation = HORIZONTAL
    if ai_guesses_board.is_cell_hit(hit_row, hit_col - 1):
        orientation = HORIZONTAL
    return orientation


def guess_cell_after_hit(hit_row, hit_col, ai_guesses_board):
    orientation = get_ship_orientation(hit_row, hit_col, ai_guesses_board)
    if orientation == UNKNOWN:
        print('This is the first hit')
        guessed_row, guessed_col = guess_cell_no_orientation(hit_row, hit_col, ai_guesses_board)
    else:
        print('There are more than one hit cells')
        if orientation == HORIZONTAL:
            guessed_row, guessed_col = guess_cell_horizontal(hit_row, hit_col, ai_guesses_board)

        if orientation == VERTICAL:
            guessed_row, guessed_col = guess_cell_vertical(hit_row, hit_col, ai_guesses_board)
    return guessed_row, guessed_col


def guess_cell_no_orientation(hit_row, hit_col, ai_guesses_board):
    if ai_guesses_board.is_cell_water(hit_row + 1, hit_col):
        guessed_row = hit_row + 1
        guessed_col = hit_col
    elif ai_guesses_board.is_cell_water(hit_row - 1, hit_col):
        guessed_row = hit_row - 1
        guessed_col = hit_col
    elif ai_guesses_board.is_cell_water(hit_row, hit_col + 1):
        guessed_row = hit_row
        guessed_col = hit_col + 1
    elif ai_guesses_board.is_cell_water(hit_row, hit_col - 1):
        guessed_row = hit_row
        guessed_col = hit_col - 1
    return guessed_row, guessed_col


def guess_cell_vertical(hit_row, hit_col, ai_guesses_board):
    if ai_guesses_board.is_cell_water(hit_row + 1, hit_col):
        guessed_row = hit_row + 1
        guessed_col = hit_col
    elif ai_guesses_board.is_cell_water(hit_row - 1, hit_col):
        guessed_row = hit_row - 1
        guessed_col = hit_col
    else:
        if ai_guesses_board.is_cell_hit(hit_row + 1, hit_col):
            opposite_hit_row = hit_row + 1
            while ai_guesses_board.is_cell_hit(opposite_hit_row, hit_col):
                opposite_hit_row += 1
            guessed_row = opposite_hit_row
            guessed_col = hit_col

        elif ai_guesses_board.is_cell_hit(hit_row - 1, hit_col):
            opposite_hit_row = hit_row - 1
            while ai_guesses_board.is_cell_hit(opposite_hit_row, hit_col):
                opposite_hit_row -= 1
            guessed_row = opposite_hit_row
            guessed_col = hit_col
    return guessed_row, guessed_col


def guess_cell_horizontal(hit_row, hit_col, ai_guesses_board):
    if ai_guesses_board.is_cell_water(hit_row, hit_col + 1):
        guessed_row = hit_row
        guessed_col = hit_col + 1
    elif ai_guesses_board.is_cell_water(hit_row, hit_col - 1):
        guessed_row = hit_row
        guessed_col = hit_col - 1

    else:
        if ai_guesses_board.is_cell_hit(hit_row, hit_col + 1):
            opposite_hit_col = hit_col + 1
            while ai_guesses_board.is_cell_hit(hit_row, opposite_hit_col):
                opposite_hit_col += 1
            guessed_row = hit_row
            guessed_col = opposite_hit_col

        elif ai_guesses_board.is_cell_hit(hit_row, hit_col - 1):
            opposite_hit_col = hit_col - 1
            while ai_guesses_board.is_cell_hit(hit_row, opposite_hit_col):
                opposite_hit_col -= 1
            guessed_row = hit_row
            guessed_col = opposite_hit_col
    return guessed_row, guessed_col

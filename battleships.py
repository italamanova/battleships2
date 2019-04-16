from random import randint

from constants import UNKNOWN, HORIZONTAL, VERTICAL, MISS, SIZE, ALIVE, FLEET, HIT
from helpers import ShipBoard, Board, Ship
from utils import print_board

# player_board = ShipBoard(10)
# ship = Ship('koko', 5)
# ship.set_parameters(row=0, col=0, orientation=VERTICAL)
# player_board.add_ship(ship)
#
# ai_guesses_board = Board(10)

player_status = ALIVE
player_guesses = Board(SIZE)
player_board = ShipBoard(SIZE)

ai_status = ALIVE
ai_guesses = Board(SIZE)
ai_board = ShipBoard(SIZE)




def place_ships(board):
    for ship in FLEET:
        created_ship = board.create_random_ship(ship, FLEET[ship])
        board.add_ship(created_ship)


# AI
# Guesses cell if
def guess_cell(last_row, last_col, ai_guesses_board):
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


'''''''''''''''
    GAME
'''''''''''''''


def game():
    last_row = UNKNOWN
    last_col = UNKNOWN
    last_hit_row = UNKNOWN
    last_hit_col = UNKNOWN
    target_ship = None
    hits = []

    ai_ships_left = len(FLEET)
    player_ships_left = len(FLEET)

    place_ships(player_board)
    place_ships(ai_board)

    print('Player board', player_board)
    print('AI board', ai_board)

    print('Battleships')
    print_board(player_board, player_guesses, SIZE)
    print('AI BOARD')
    print_board(ai_board, ai_guesses, SIZE)
    while ai_ships_left and player_ships_left:
        # _row = int(input("Which row?"))
        # _col = int(input("Which column?"))
        #
        # # if the guess is not legal
        # while not player_guesses.is_cell_on_board(_row, _col):
        #     print("Incorrect input, please try again")
        #     _row = int(input("Which row?"))
        #     _col = int(input("Which column?"))
        #
        # if not ai_board.is_cell_water(_row, _col):
        #     if ai_ships_left:
        #         print('Hit!')
        #         player_guesses.board[_row][_col] = HIT
        #     #     check ship sunk
        #     else:
        #         player_guesses.board[_row][_col] = HIT
        #         print('You win!')
        #         break
        # else:
        #     print("Missed!")
        #     player_guesses.board[_row][_col] = MISS

        # AI turn
        if last_hit_row == UNKNOWN:
            guessed_row, guessed_col = guess_cell(last_row, last_col, ai_guesses)
        else:
            guessed_row, guessed_col = guess_cell_after_hit(last_hit_row, last_hit_col, ai_guesses)

        hit = player_board.is_hit(guessed_row, guessed_col, ai_guesses.board)
        while hit:
            last_hit_row = guessed_row
            last_hit_col = guessed_col

            if (last_hit_row, last_hit_col) not in hits:
                hits.append((last_hit_row, last_hit_col))

            if not target_ship:
                target_ship = player_board.get_hit_ship(guessed_row, guessed_col)
            else:
                is_ship_sunk = target_ship.is_sunk(hits)
                if is_ship_sunk:

                    last_hit_row = UNKNOWN
                    last_hit_col = UNKNOWN
                    hits = []
                    target_ship = None

                    player_ships_left -= 1
            if player_ships_left:
                if last_hit_row == UNKNOWN:
                    guessed_row, guessed_col = guess_cell(last_row, last_col, ai_guesses)
                else:
                    guessed_row, guessed_col = guess_cell_after_hit(last_hit_row, last_hit_col, ai_guesses)
            else:
                print('AI WIN!')
                break

            last_row = guessed_row
            last_col = guessed_col
            hit = player_board.is_hit(last_row, last_col, ai_guesses.board)
        last_row = guessed_row
        last_col = guessed_col

        player_board.board[guessed_row][guessed_col] = MISS
        ai_guesses.board[guessed_row][guessed_col] = MISS

        print('----------------')
        print('ME')
        print_board(player_board, player_guesses, SIZE)
        print('AI BOARD')
        print_board(ai_board, ai_guesses, SIZE)
        print('----------------')



game()

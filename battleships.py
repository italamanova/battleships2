from ai import guess_cell, guess_cell_after_hit
from constants import UNKNOWN, MISS, SIZE, ALIVE, FLEET, HIT
from helpers import ShipBoard, Board
from utils import print_board

player_status = ALIVE
player_guesses = Board(SIZE)
player_board = ShipBoard(SIZE)

ai_status = ALIVE
ai_guesses = Board(SIZE)
ai_board = ShipBoard(SIZE)

'''''''''''''''
    GAME
'''''''''''''''


def player_turn(ai_ships_left, player_target_ship, player_hits):
    _row = int(input("Which row?"))
    _col = int(input("Which column?"))

    # if the guess is not legal
    while not player_guesses.is_cell_on_board(_row, _col):
        print("Incorrect input, please try again")
        _row = int(input("Which row?"))
        _col = int(input("Which column?"))

    player_hit = not ai_board.is_cell_water(_row, _col)
    while player_hit:
        player_guesses.board[_row][_col] = HIT
        if ai_ships_left:
            print('Hit!')
            player_hits.append((_row, _col))

            # check if any ai ship is sunk
            if not player_target_ship:
                player_target_ship = ai_board.get_hit_ship(_row, _col)
            else:
                is_ai_ship_sunk = player_target_ship.is_sunk(player_hits)
                if is_ai_ship_sunk:
                    player_hits = []
                    ai_ships_left -= 1
                    print('AI ship sunk!')

            print_board(player_board, player_guesses, SIZE)

            _row = int(input("Which row?"))
            _col = int(input("Which column?"))

            player_hit = not ai_board.is_cell_water(_row, _col)
        else:
            print('You win!')
            break
    print("Miss!")
    player_guesses.board[_row][_col] = MISS

    print_board(player_board, player_guesses, SIZE)


def ai_turn(last_hit_row, last_hit_col, player_ships_left, ai_target_ship, ai_hits):
    if last_hit_row == UNKNOWN:
        guessed_row, guessed_col = guess_cell(ai_guesses)
    else:
        guessed_row, guessed_col = guess_cell_after_hit(last_hit_row, last_hit_col, ai_guesses)

    print('\nAI move: (%s, %s)' % (guessed_row, guessed_col))

    hit = player_board.is_hit(guessed_row, guessed_col, ai_guesses.board)
    while hit:
        last_hit_row = guessed_row
        last_hit_col = guessed_col

        if (last_hit_row, last_hit_col) not in ai_hits:
            ai_hits.append((last_hit_row, last_hit_col))

        if not ai_target_ship:
            ai_target_ship = player_board.get_hit_ship(guessed_row, guessed_col)

        else:
            is_ship_sunk = ai_target_ship.is_sunk(ai_hits)
            if is_ship_sunk:
                last_hit_row = UNKNOWN
                last_hit_col = UNKNOWN
                ai_hits = []
                ai_target_ship = None

                player_ships_left -= 1
                print('Player ship sunk!')
        if player_ships_left:
            if last_hit_row == UNKNOWN:
                guessed_row, guessed_col = guess_cell(ai_guesses)
            else:
                guessed_row, guessed_col = guess_cell_after_hit(last_hit_row, last_hit_col, ai_guesses)
        else:
            print('AI win!')
            break
        hit = player_board.is_hit(guessed_row, guessed_col, ai_guesses.board)

    player_board.board[guessed_row][guessed_col] = MISS
    ai_guesses.board[guessed_row][guessed_col] = MISS

    print('AI turn')
    print_board(player_board, player_guesses, SIZE)
    # print('AI BOARD')


def game():
    ai_ships_left = len(FLEET)
    player_ships_left = len(FLEET)

    last_hit_row = UNKNOWN
    last_hit_col = UNKNOWN
    ai_target_ship = None
    ai_hits = []

    player_target_ship = None
    player_hits = []

    player_board.place_ships()
    ai_board.place_ships()

    print('Battleships')
    print_board(player_board, player_guesses, SIZE)

    while ai_ships_left and player_ships_left:
        # Player turn
        player_turn(ai_ships_left, player_target_ship, player_hits)
        # AI turn
        ai_turn(last_hit_row, last_hit_col, player_ships_left, ai_target_ship, ai_hits)


if __name__ == "__main__":
    game()

from ai_helpers import guess_cell, guess_cell_after_hit
from constants import UNKNOWN, MISS, SIZE, FLEET, HIT
from structure import ShipBoard, Board
from utils import print_board

player_guesses = Board(SIZE)
player_board = ShipBoard(SIZE)

ai_guesses = Board(SIZE)
ai_board = ShipBoard(SIZE)

'''''''''''''''
    GAME
'''''''''''''''


def player_turn(ai_ships_left, player_target_ship, player_hits):
    """
    :param ai_ships_left: int
    :param player_target_ship: Ship
    :param player_hits: list of made hits
    """
    _row = int(input("Which row?"))
    _col = int(input("Which column?"))

    # If player chose the wrong cell
    while not player_guesses.is_cell_on_board(_row, _col):
        print("Incorrect input, please try again")
        _row = int(input("Which row?"))
        _col = int(input("Which column?"))

    # If a player can hit this cell
    player_hit = not ai_board.is_cell_water(_row, _col)
    while player_hit:
        player_guesses.board[_row][_col] = HIT
        if ai_ships_left:
            print('Hit!')
            player_hits.append((_row, _col))

            # Check if any ai ship is sunk
            if not player_target_ship:
                player_target_ship = ai_board.get_hit_ship(_row, _col)
            else:
                is_ai_ship_sunk = player_target_ship.is_sunk(player_hits)
                if is_ai_ship_sunk:
                    player_hits = []
                    ai_ships_left -= 1
                    player_target_ship = None
                    print('AI ship sunk!')

            print_board(player_board, player_guesses, SIZE)

            # Asking again
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
    """
    :param last_hit_row: int
    :param last_hit_col: int
    :param player_ships_left: int
    :param ai_target_ship: Ship
    :param ai_hits: list of hits made by ai
    """
    if last_hit_row == UNKNOWN:
        # If a shoot is in the beginning of the game
        guessed_row, guessed_col = guess_cell(ai_guesses)
    else:
        # If the ship was already hit
        guessed_row, guessed_col = guess_cell_after_hit(last_hit_row, last_hit_col, ai_guesses)

    print('\nAI move: (%s, %s)' % (guessed_row, guessed_col))

    # If the cell contains a ship
    hit = player_board.is_hit(guessed_row, guessed_col, ai_guesses.board)
    while hit:
        last_hit_row = guessed_row
        last_hit_col = guessed_col

        # Save the hit for checking whether the ship is sunk or not
        if (last_hit_row, last_hit_col) not in ai_hits:
            ai_hits.append((last_hit_row, last_hit_col))

        # If we don't know which ship is hit
        if not ai_target_ship:
            ai_target_ship = player_board.get_hit_ship(guessed_row, guessed_col)

        else:
            # Check whether the ship is sunk
            is_ship_sunk = ai_target_ship.is_sunk(ai_hits)
            if is_ship_sunk:
                last_hit_row = UNKNOWN
                last_hit_col = UNKNOWN
                ai_hits = []
                ai_target_ship = None

                player_ships_left -= 1
                print('Player ship sunk!')
        # If there are any other ships
        if player_ships_left:
            if last_hit_row == UNKNOWN:
                # If the ship was sunk
                guessed_row, guessed_col = guess_cell(ai_guesses)
            else:
                # Else continue with existing hits
                guessed_row, guessed_col = guess_cell_after_hit(last_hit_row, last_hit_col, ai_guesses)
        else:
            print('AI win!')
            break
        hit = player_board.is_hit(guessed_row, guessed_col, ai_guesses.board)

    player_board.board[guessed_row][guessed_col] = MISS
    ai_guesses.board[guessed_row][guessed_col] = MISS

    print('AI turn')
    print_board(player_board, player_guesses, SIZE)


def game():
    # Count of the left ships
    ai_ships_left = len(FLEET)
    player_ships_left = len(FLEET)

    # Variables for storing AI move state
    last_hit_row = UNKNOWN
    last_hit_col = UNKNOWN
    ai_target_ship = None
    ai_hits = []

    # Variables for storing player move state
    player_target_ship = None
    player_hits = []

    # Add random ships to boards
    player_board.place_random_ships()
    ai_board.place_random_ships()

    print('Battleships')
    print_board(player_board, player_guesses, SIZE)

    while ai_ships_left and player_ships_left:
        # Player turn
        player_turn(ai_ships_left, player_target_ship, player_hits)
        # AI turn
        ai_turn(last_hit_row, last_hit_col, player_ships_left, ai_target_ship, ai_hits)


if __name__ == "__main__":
    game()

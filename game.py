from bot import Bot
from constants import ALIVE, FLEET, WATER, HIT, MISS, SIZE
from structure import Board, ShipBoard
from utils import print_board

player_status = ALIVE
player_guesses = Board(SIZE)
player_board = ShipBoard(SIZE)

ai_status = ALIVE
ai_guesses = Board(SIZE)
ai_board = ShipBoard(SIZE)

bot = Bot(ai_guesses)

'''
TODO 
1.Pep8 comments
2. Tests for ai
'''

def place_ships(board):
    for ship in FLEET:
        created_ship = board.create_random_ship(ship, FLEET[ship])
        board.add_ship(created_ship)
    # ship1 = board.create_ship_with_coordinates('koko1', 4, 8, 9, 1)
    # board.add_ship(ship1)
    # ship2 = board.create_ship_with_coordinates('koko2', 3, 0, 1, 0)
    # board.add_ship(ship2)


def game():
    place_ships(player_board)
    place_ships(ai_board)

    print('Player board', player_board)
    print('AI board', ai_board)

    print('Battleships')
    print_board(player_board, player_guesses, SIZE)
    print('AI BOARD')
    print_board(ai_board, ai_guesses, SIZE)
    while player_status == ALIVE and ai_status == ALIVE:
        # _row = int(input("Which row?"))
        # _col = int(input("Which column?"))
        #
        # # if the guess is not legal
        # while not player_guesses.is_cell_on_board(_row, _col):
        #     print("Incorrect input, please try again")
        #     _row = int(input("Which row?"))
        #     _col = int(input("Which column?"))
        #
        # # if the guess is legal
        # if ai_board.board[_row][_col] != WATER:
        #     # ai_board.spots -= 1
        #     if ai_status == ALIVE:
        #         print('Hit!')
        #         player_guesses.board[_row][_col] = HIT
        #     else:
        #         player_guesses.board[_row][_col] = HIT
        #         print('You win!')
        #         break
        # else:
        #     print("Missed!")
        #     player_guesses.board[_row][_col] = MISS

        bot.hunt_parity_shoot(player_board)
        print('-------------')
        print_board(player_board, ai_guesses, SIZE)
        print('-------------')


game()

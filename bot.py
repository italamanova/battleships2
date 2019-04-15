from random import randint

from constants import ALIVE, HORIZONTAL, VERTICAL, UNKNOWN


class Bot:
    def __init__(self, guesses_board):
        self.status = ALIVE
        self.checked_cells = []
        self.guesses_board = guesses_board
        # self.player_board = player_board
        self.last_checked_row = UNKNOWN
        self.last_checked_col = UNKNOWN

        self.hits = []
        self.found_ships = []
        self.orientation = UNKNOWN

    def random_shot(self):
        ai_guess_row = randint(0, self.board_size - 1)
        ai_guess_col = randint(0, self.board_size - 1)

    def hunt_down(self):
        guess_row = self.last_checked_row + 1
        guess_col = self.last_checked_col
        return guess_row, guess_col

    def hunt_up(self):
        guess_row = self.last_checked_row - 1
        guess_col = self.last_checked_col
        return guess_row, guess_col

    def hunt_right(self):
        guess_row = self.last_checked_row + 1
        guess_col = self.last_checked_col
        return guess_row, guess_col

    def hunt_left(self):
        guess_row = self.last_checked_row
        guess_col = self.last_checked_col - 1
        return guess_row, guess_col

    def hunt(self):
        if self.orientation == UNKNOWN:
            print('HUNT', 'NO ORIENTATION')
            if self.guesses_board.is_cell_water(self.last_checked_row + 1,
                                                self.last_checked_col):
                guessed_row, guessed_col = self.hunt_down()
                self.orientation = VERTICAL
                print('HUNT', 'DOWN')
            elif self.guesses_board.is_cell_water(self.last_checked_row - 1,
                                                  self.last_checked_col):
                guessed_row, guessed_col = self.hunt_up()
                self.orientation = VERTICAL
                print('HUNT', 'UP')
            elif self.guesses_board.is_cell_water(self.last_checked_row,
                                                  self.last_checked_col + 1):
                guessed_row, guessed_col = self.hunt_right()
                self.orientation = HORIZONTAL
                print('HUNT', 'RIGHT')
            else:
                guessed_row, guessed_col = self.hunt_left()
                self.orientation = HORIZONTAL
                print('HUNT', 'LEFT')
        elif self.orientation == HORIZONTAL:
            print('HUNT', 'HORIZONTAL')
            if self.guesses_board.is_cell_water(self.last_checked_row,
                                                self.last_checked_col + 1):
                guessed_row, guessed_col = self.hunt_right()
                print('HUNT', 'RIGHT')
            else:
                guessed_row, guessed_col = self.hunt_left()
                print('HUNT', 'LEFT')
        else:
            print('HUNT', 'VERTICAL')
            if self.guesses_board.is_cell_water(self.last_checked_row + 1,
                                                self.last_checked_col):
                guessed_row, guessed_col = self.hunt_down()
                print('HUNT', 'DOWN')
            elif self.guesses_board.is_cell_water(self.last_checked_row - 1,
                                                  self.last_checked_col):
                guessed_row, guessed_col = self.hunt_up()
                print('HUNT', 'UP')
        print('HUNT GUESSED: ', guessed_row, guessed_col)
        return guessed_row, guessed_col

    def get_next_cell(self):
        if len(self.hits) == 0:
            if self.last_checked_row == UNKNOWN and self.last_checked_col == UNKNOWN:
                row_to_check = 0
                col_to_check = 0
            else:
                row_to_check = self.last_checked_row + 2
                col_to_check = self.last_checked_col
                if row_to_check > (self.guesses_board.size - 1):
                    col_to_check = self.last_checked_col + 1
                    row_to_check = (self.last_checked_row + 2) % (self.guesses_board.size - 1)
        elif len(self.hits) == 1:
            row_to_check = self.hits[0][0]
            col_to_check = self.hits[0][1]
        else:
            row_to_check, col_to_check = self.hunt()

        print("NEXT CELL: ", row_to_check, col_to_check)
        return row_to_check, col_to_check

    def hunt_parity_shoot(self, player_board):
        check_row, check_col = self.get_next_cell()
        hit = player_board.is_hit(check_row, check_col, self.guesses_board.board)
        print('HIT ', hit)
        while hit:
            self.hits.append((check_row, check_col))
            self.last_checked_row = check_row
            self.last_checked_col = check_col
            is_ship_sunk = player_board.is_ship_sunk(self.hits)
            if is_ship_sunk:
                # self.hits = []
                print('SUNK')
                # TODO and check next
            check_row, check_col = self.hunt()
            hit = player_board.is_hit(check_row, check_col, self.guesses_board.board)
            # append a hit to ships
        self.orientation = UNKNOWN
        self.last_checked_row = check_row
        self.last_checked_col = check_col


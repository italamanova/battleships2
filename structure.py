from random import randint

from constants import HORIZONTAL, VERTICAL, WATER, SHIP, HIT, MISS
from utils import get_random_row, get_random_col


class Ship:
    def __init__(self, name, size, row=None, col=None, orientation=None):
        self.name = name
        self.size = size
        self.row = row
        self.col = col
        self.orientation = orientation

    def __repr__(self):
        return 'Ship %s, size: %s, row: %s, col: %s, orientation: %s\n' % (
            self.name, self.size, self.row, self.col, self.orientation)


class Board:
    def __init__(self, size):
        self.size = size
        self.board = []
        self.fill_board()

    def fill_board(self):
        for row in range(self.size):
            self.board.append([WATER] * self.size)

    def is_cell_on_board(self, row, col):
        if row < 0 or row >= self.size:
            return False
        elif col < 0 or col >= self.size:
            return False
        return True

    def is_cell_water(self, row, col):
        if self.is_cell_on_board(row, col):
            if self.board[row][col] == WATER:
                return True
        return False

    def __str__(self):
        return str(self.ships)


class ShipBoard(Board):
    def __init__(self, size):
        super().__init__(size)
        self.ships = []

    def check_ship_overlap(self, ship):
        overlap = False
        if ship.orientation == HORIZONTAL:
            for cell in range(ship.size):
                if not self.is_cell_water(ship.row, ship.col + cell):
                    overlap = True
        else:
            for cell in range(ship.size):
                if not self.is_cell_water(ship.row + cell, ship.col):
                    overlap = True
        return overlap

    def create_random_ship(self, ship_name, ship_size):
        ship = Ship(ship_name, ship_size)
        _orientation = randint(VERTICAL, HORIZONTAL)
        ship.orientation = _orientation

        overlap = True
        while overlap:
            _row = get_random_row(_orientation, ship.size)
            _col = get_random_col(_orientation, ship.size)
            ship.row = _row
            ship.col = _col
            overlap = self.check_ship_overlap(ship)
        return ship

    def create_ship_with_coordinates(self, ship_name, ship_size, row, col, orientation):
        ship = Ship(ship_name, ship_size)
        ship.orientation = orientation

        ship.row = row
        ship.col = col
        overlap = self.check_ship_overlap(ship)
        if not overlap:
            return ship
        else:
            return None

    def add_ship(self, ship):
        self.ships.append(ship)
        if ship.orientation == HORIZONTAL:
            for cell in range(ship.size):
                self.board[ship.row][ship.col + cell] = SHIP
        else:
            for cell in range(ship.size):
                self.board[ship.row + cell][ship.col] = SHIP

    # Checks is someone hits a cell and adds a sign to the board
    def is_hit(self, row, col, guesses_board):
        if self.board[row][col] == SHIP:
            guesses_board[row][col] = HIT
            return True
        else:
            guesses_board[row][col] = MISS
            return False

    def is_ship_sunk(self, hits):
        # for ship in self.ships:
        #     if ship.has_cells(hits):
        print('is_ship_sunk')
        pass



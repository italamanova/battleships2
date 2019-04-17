from random import randint

from constants import WATER, HIT, HORIZONTAL, VERTICAL, SHIP, MISS, FLEET
from utils import get_random_row, get_random_col


class Ship:
    def __init__(self, name, size, row=None, col=None, orientation=None):
        """
        :param name: str
        :param size: int
        :param row: int
        :param col: int
        :param orientation: VERTICAL, HORIZONTAL or UNKNOWN
        """
        self.name = name
        self.size = size
        self.row = row
        self.col = col
        self.orientation = orientation
        self.coordinates = None

    def __get_coordinates__(self):
        """
        :return: list of tuples
        """
        current_ship_coord = []
        for i in range(self.size):
            if self.orientation == HORIZONTAL:
                current_ship_coord.append((self.row, self.col + i))
            if self.orientation == VERTICAL:
                current_ship_coord.append((self.row + i, self.col))
        return current_ship_coord

    def set_parameters(self, row, col, orientation):
        """
        Set parameters to a new ship

        :param row: int
        :param col: int
        :param orientation: VERTICAL or HORIZONTAL
        """
        self.row = row
        self.col = col
        self.orientation = orientation
        self.coordinates = self.__get_coordinates__()

    def is_sunk(self, hits):
        """
        Checks if the ship is sunk

        :param hits: list of players hits
        :return: bool
        """
        if not len(set(self.coordinates) - set(hits)):
            return True
        return False

    def __repr__(self):
        return 'Ship %s, size: %s, row: %s, col: %s, orientation: %s\n' % (
            self.name, self.size, self.row, self.col, self.orientation)


class Board:
    def __init__(self, size):
        """
        :param size: int
        """
        self.size = size
        self.board = []
        self.fill_board()

    def fill_board(self):
        """
        Fills the board with water cells
        """
        for row in range(self.size):
            self.board.append([WATER] * self.size)

    def is_cell_on_board(self, row, col):
        """
        Checks is the cell belongs to a board
        :param row: int
        :param col: int
        :return: bool
        """
        if row < 0 or row >= self.size:
            return False
        elif col < 0 or col >= self.size:
            return False
        return True

    def is_cell_water(self, row, col):
        """
        Checks is the cell contains water
        :param row: int
        :param col: int
        :return: bool
        """
        if self.is_cell_on_board(row, col):
            if self.board[row][col] == WATER:
                return True
        return False

    def is_cell_hit(self, row, col):
        """
        Checks is the cell contains hit
        :param row: int
        :param col: int
        :return: bool
        """
        if self.is_cell_on_board(row, col):
            if self.board[row][col] == HIT:
                return True
        return False

    def __str__(self):
        return str(self.ships)


class ShipBoard(Board):
    def __init__(self, size):
        """
        :param size: int
        """
        super().__init__(size)
        self.ships = []

    def get_ship_surroundings(self, ship):
        """
        Returns all neighbour cell coordinates for a particular ships.
        Helps to place ships one cell out of each other
        :param ship: Ship
        :return: list of (int, int)
        """
        surroundings = []
        for coord in ship.coordinates:
            if self.is_cell_on_board(coord[0] + 1, coord[1]):
                surroundings.append((coord[0] + 1, coord[1]))
            if self.is_cell_on_board(coord[0] - 1, coord[1]):
                surroundings.append((coord[0] - 1, coord[1]))
            if self.is_cell_on_board(coord[0], coord[1] + 1):
                surroundings.append((coord[0], coord[1] + 1))
            if self.is_cell_on_board(coord[0], coord[1] - 1):
                surroundings.append((coord[0], coord[1] - 1))
        return surroundings

    def check_ship_overlap(self, ship):
        """
        Checks if ship overlaps other ships or their surroundings
        :param ship: Ship
        :return: bool
        """
        surroundings = self.get_ship_surroundings(ship) + ship.coordinates[:]
        overlap = False
        for cell in surroundings:
            if not self.is_cell_water(cell[0], cell[1]):
                overlap = True
        return overlap

    def create_random_ship(self, ship_name, ship_size):
        """
        Creates a random ship that doesn't overlap with others
        :param ship_name: str
        :param ship_size: int
        :return: Ship
        """
        ship = Ship(ship_name, ship_size)
        _orientation = randint(VERTICAL, HORIZONTAL)

        overlap = True
        while overlap:
            _row = get_random_row(_orientation, ship.size)
            _col = get_random_col(_orientation, ship.size)
            ship.set_parameters(_row, _col, _orientation)
            overlap = self.check_ship_overlap(ship)
        return ship

    def create_ship_with_coordinates(self, ship_name, ship_size, row, col, orientation):
        """
        Debug function for creating a ship with coordinates
        :param ship_name: str
        :param ship_size: int
        :param row: int
        :param col: int
        :param orientation: VERTICAL or HORIZONTAL
        :return: bool
        """
        ship = Ship(ship_name, ship_size)
        ship.set_parameters(row=row, col=col, orientation=orientation)
        overlap = self.check_ship_overlap(ship)
        if not overlap:
            return ship
        else:
            return None

    def add_ship(self, ship):
        """
        Helper function that adds a ship to board ships and draws them at the board
        :param ship: Ship
        """
        self.ships.append(ship)
        if ship.orientation == HORIZONTAL:
            for cell in range(ship.size):
                self.board[ship.row][ship.col + cell] = SHIP
        else:
            for cell in range(ship.size):
                self.board[ship.row + cell][ship.col] = SHIP

    def place_random_ships(self):
        """
        Helper function for placing random ships to the board
        """
        for ship in FLEET:
            created_ship = self.create_random_ship(ship, FLEET[ship])
            self.add_ship(created_ship)

    def is_hit(self, row, col, guesses_board):
        """
        Checks if the enemy's ship was hit
        :param row: int
        :param col: int
        :param guesses_board: Board
        :return: bool
        """
        if self.board[row][col] == SHIP:
            guesses_board[row][col] = HIT
            return True
        else:
            guesses_board[row][col] = MISS
            return False

    def get_hit_ship(self, hit_row, hit_col):
        """
        Returns a ship that was hit
        :param hit_row: int
        :param hit_col: int
        :return: Ship
        """
        for ship in self.ships:
            if (hit_row, hit_col) in ship.coordinates:
                return ship

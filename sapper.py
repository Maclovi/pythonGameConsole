from random import randrange as rr, seed
seed(20)


class Descr:

    def __set_name__(self, owner, name):
        self.name = f"_{owner.__name__}__{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return property()
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not (isinstance(value, (bool, int)) and 0 <= value <= 8):
            raise ValueError("недопустимое значение атрибута")
        setattr(instance, self.name, value)


class Cell:
    is_mine = Descr()
    is_open = Descr()
    number = Descr()

    def __init__(self, mine=False, fl_open=False):
        self.is_mine = mine
        self.is_open = fl_open
        self.number = 0

    def __bool__(self):
        return not self.is_open


class GamePole:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, n, m, total_mines):
        self.n = n
        self.m = m
        self.total_mines = total_mines
        self.__pole_cells = [[Cell()] * m for _ in range(n)]
        self.mines = set()

    @property
    def pole(self):
        return self.__pole_cells

    def init_pole(self):
        self.random_mines()
        self.insert_mine()
        self.counter_around()

    def random_mines(self):
        while len(self.mines) != self.total_mines:
            self.mines.add((rr(self.n), rr(self.m)))

    def insert_mine(self):
        for row in range(self.n):
            for col in range(self.m):
                mine = Cell(True) if (row, col) in self.mines else Cell()
                self.__pole_cells[row][col] = mine

    def counter_around(self):
        n, m = self.n, self.m
        for row in range(n):
            for col in range(m):
                check = self.__pole_cells[row][col]
                if check.is_mine:
                    go_row = row - (row > 0), row + (row + 1 < n) + 1
                    go_col = col - (col > 0), col + (col + 1 < m) + 1
                    for i in range(*go_row):
                        for j in range(*go_col):
                            current = self.__pole_cells[i][j]
                            if not current.is_mine:
                                current.number += 1

    def open_cell(self, i, j, area=1):
        if not (0 <= i < self.n and 0 <= j < self.m):
            raise IndexError('некорректные индексы i, j клетки игрового поля')

        row = (i - area) * (i >= area), (i + area) * (i + area < self.n) + 1
        col = (j - area) * (j >= area), (j + area) * (j + area < self.m) + 1
        for i in range(*row):
            for j in range(*col):
                cell = self.__pole_cells[i][j]
                if not cell.is_mine:
                    cell.is_open = True

    def show_pole(self):
        for row in self.__pole_cells:
            for cell in row:
                check = "#" * bool(cell) or "*" * cell.is_mine
                print(check or cell.number or ".", end=" ")
            print()


class Game:
    pass

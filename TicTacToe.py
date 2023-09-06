import random


class Cell:
    symbols = {0: "□", 1: "X", 2: "O"}

    def __init__(self):
        self.value = 0

    def __bool__(self):
        return not self.value

    def __repr__(self):
        return self.symbols.get(self.value)


class TicTacToe:
    _instance = None
    FREE_CELL = 0
    HUMAN_X = 1
    COMPUTER_O = 2

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, row=3, col=3):
        self.pole = None
        self.free_cells = None
        self.row = 0
        self.col = 0
        self.init(row, col)

    def __getitem__(self, item):
        self._valid_index(item)
        return self.pole[item[0]][item[1]].value

    def __setitem__(self, key, value):
        self._valid_index(key)
        self.pole[key[0]][key[1]].value = value

    def __bool__(self):
        return not any((self.is_draw,
                        self.is_human_win,
                        self.is_computer_win))

    @property
    def is_human_win(self):
        return self._check_win(self.HUMAN_X)

    @property
    def is_computer_win(self):
        return self._check_win(self.COMPUTER_O)

    @property
    def is_draw(self):
        return not self.free_cells

    def init(self, row=3, cl=3):
        self.pole = tuple(tuple(Cell() for _ in range(cl)) for _ in range(row))
        self.free_cells = [(i, j) for i in range(row) for j in range(cl)]
        self.row = row
        self.col = cl

    def show(self):
        for row in self.pole:
            for col in row:
                print(col, end=" ")
            print()

    def human_go(self):
        while True:
            go = tuple(map(int, input("Введите координаты клетки -> ")))
            if not self[go]:
                self._go(go, self.HUMAN_X)
                break
            else:
                print("Эта клетка уже занята")

    def computer_go(self):
        go = random.choice(self.free_cells)
        self._go(go, self.COMPUTER_O)

    def _go(self, index, value):
        self.free_cells.remove(index)
        self[index] = value

    def _check_win(self, player):
        pole = self.pole
        rows = (all(obj.value == player for obj in row) for row in pole)
        cols = (all(obj.value == player for obj in row) for row in zip(*pole))
        main_diagonal = secondary_diagonal = 3
        for i in range(self.row):
            main_diagonal -= (pole[i][i].value == player)
            secondary_diagonal -= (pole[3 - 1 - i][i].value == player)

        is_diagonal = not (main_diagonal and secondary_diagonal)
        return any(rows) or any(cols) or is_diagonal

    def _valid_index(self, key):
        index, column = key
        checker = (isinstance(index, int) and 0 <= index < self.row,
                   isinstance(column, int) and 0 <= column < self.col)
        if not all(checker):
            raise IndexError("некорректно указанные индексы")


game = TicTacToe()
game.init()
step_game = 0
while game:
    game.show()

    if step_game % 2 == 0:
        game.human_go()
    else:
        game.computer_go()

    step_game += 1

game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")

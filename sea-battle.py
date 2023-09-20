from random import shuffle, randint


class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._is_move = True
        self._cells = [1] * length
        self._x, self._y = x, y
        self._tp = tp

        self.count_alive = length
        self.width = length if tp == 1 else 1
        self.height = length if tp == 2 else 1
        self.set_coords(x, y)

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key].is_alive = value

    def set_coords(self, x, y):
        if None not in (x, y):
            self.left = x
            self.right = x + self.width
            self.bottom = y
            self.up = y + self.height

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y
        self.set_coords(x, y)

    def get_start_coords(self):
        return self._x, self._y

    @property
    def get_points(self):
        if None in (self._x, self._y):
            raise Exception("Начальные точки координат не установлены")

        width = self.left, self.right
        height = self.bottom, self.up
        return ((row, col) for row in range(*width) for col in range(*height))

    def move(self, go):
        x, y = self._x, self._y
        if self._tp == 1:
            x += go
        elif self._tp == 2:
            y += go
        self.set_start_coords(x, y)
        return self

    def is_collide(self, ship):
        check_side1 = self.left > ship.right
        check_side2 = self.right < ship.left
        check_side3 = self.bottom > ship.up
        check_side4 = self.up < ship.bottom
        if check_side1 or check_side2 or check_side3 or check_side4:
            return False
        return True

    def is_out_pole(self, size):
        return (self.right > size or self.up > size or
                self.bottom < 0 or self.left < 0)


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._pole = None
        self._ships = None

        self._free_cells = None

    def init(self):
        self.clear(self._size)
        self.set_start_coords_ships()
        self.update_pole()

    def set_start_coords_ships(self):
        for length_ in reversed(range(1, 5)):
            for amount in range(length_, 5):
                for coords in self._free_cells:
                    ship = Ship(length_, randint(1, 2), *coords)
                    if self.is_collisions(ship, self._ships):
                        self._ships.append(ship)
                        self.del_points(ship)
                        break

    def is_collisions(self, ship, all_ships):
        is_out_pole = ship.is_out_pole(self._size)
        is_collide = any(ship.is_collide(sp) for sp in all_ships if sp != ship)
        return not (is_collide or is_out_pole)

    def generate_free_cells(self, shake=False):
        points = [(i, j) for i in range(self._size) for j in range(self._size)]
        if shake:
            shuffle(points)
        return points

    def clear(self, size):
        self._ships = []
        self._free_cells = self.generate_free_cells(shake=True)

    def clear_pole(self, size):
        self._pole = [["." for _ in range(size)] for _ in range(size)]

    def del_points(self, ship):
        for points in ship.get_points:
            self._free_cells.remove(points)

    def update_pole(self):
        self.clear_pole(self._size)
        for ship in self._ships:
            for i, (x, y) in enumerate(ship.get_points):
                self._pole[x][y] = ship[i]

    def move_ships(self):
        for ship in self._ships:
            if ship._is_move:
                x, y = ship.get_start_coords()
                go = [1, -1]
                move1, move2 = go.pop(randint(0, 1)), go.pop() * 2
                if not (self.is_collisions(ship.move(move1), self._ships) or
                        self.is_collisions(ship.move(move2), self._ships)):
                    ship.set_start_coords(x, y)
        self.update_pole()

    def get_ships(self):
        return self._ships

    def get_pole(self):
        return self._pole

    def show(self):
        for row in self._pole:
            print(*row)


class SeaBattle:
    end = "    |    "
    digits = " ".join(map(str, range(1, 11)))
    ascii_leterrs = __import__("string").ascii_uppercase

    class Abstract:
        shake = False

        def __init__(self):
            self.pole = GamePole()
            self.pole.init()

            self.matrix = self.pole._pole
            self.ships = self.pole._ships
            self.total_ships = len(self.ships)
            self.free_cells = self.pole.generate_free_cells(shake=self.shake)

        def checker_ships(self, point, other_obj):
            all_ships = other_obj.ships
            for ship in all_ships:
                if self.logic_killer_deck(point, ship):
                    if not ship.count_alive:
                        if self.logic_killer_ship(other_obj):
                            return "Вы победили!"
                        return "Вы уничтожили корабль!"
                    return "Вы попали в палубу!"
            return "Промах!"

        def logic_killer_deck(self, point, ship):
            if point in ship.get_points:
                ship.count_alive -= 1
                return True

        def logic_killer_ship(self, other_obj):
            other_obj.total_ships -= 1
            return not other_obj.total_ships

    class Player(Abstract):
        shake = False

        def action(self, obj):
            point = self.handler_points()
            self.checker_ships(point, obj)

        def handler_points(self, txt="Введите координаты"):
            point = map(int, input(f"{txt} --->: ").replace(" ", ""))
            point = tuple(point)

            self.valid_length(point)
            self.valid_index(point)
            self.valid_has(point)
            self.free_cells.remove(point)
            return point

        def valid_length(self, point):
            length = len(point)
            if length > 2:
                txt = f"Вы ввели больше данных {length}, нужно 2"
                self.again_call(txt)

        def valid_index(self, point):
            for x in point:
                if not (0 <= x < self.pole._size):
                    txt = "Введены некорректные координаты"
                    self.again_call(txt)

        def valid_has(self, point):
            if point not in self.free_cells:
                txt = "Нельзя повторяться"
                self.again_call(txt)

        def again_call(self, txt):
            self.handler_points(f"{txt}, повторите попытку")

    class Bot(Abstract):
        shake = True

        def action(self, obj):
            point = self.handler_points()
            self.checker_ships(point, obj)

        def handler_points(self):
            point = self.free_cells.pop()
            self.free_cells.remove(point)
            return point

    def __init__(self):
        self.player = self.Player()
        self.bot = self.Bot()

    def show(self, size=10):
        end = self.end
        digits = self.digits
        ascii_leterrs = self.ascii_leterrs
        print(f" {digits}{end} {digits}")

        for i in range(size):
            print(ascii_leterrs[i], *self.player.pole._pole[i], end=end)
            print(ascii_leterrs[i], *self.bot.pole._pole[i])

    def moves(self):
        self.player.pole.move_ships()
        self.bot.pole.move_ships()

    def play(self):
        while True:
            self.show()
            self.moves()
            input("update: ---> ")


s = SeaBattle()
s.play()

# p = GamePole(10)
# p.init()
# while True:
#     p.show()
#     print("-------------------")
#     p.move_ships()
#     p.show()
#     input("stop ---> ")

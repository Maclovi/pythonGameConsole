from random import shuffle, randint
from string import ascii_uppercase, digits


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
        self._cells[key] = value

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
    def get_perimeter_points(self, size=10):
        row = self.left - (self.left > 0), self.right + (self.right < size)
        col = self.bottom - (self.bottom > 0), self.up + (self.up < size)
        return ((i, j) for i in range(*row) for j in range(*col))

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
                        self.del_points(ship, self._free_cells)
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

    def del_points(self, ship, link_free_cells):
        pt = ship.get_perimeter_points
        overkill = filter(lambda x: x in link_free_cells, pt)
        for points in overkill:
            link_free_cells.remove(points)

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

    class Abstract:
        shake = False
        maketrans = str.maketrans(ascii_uppercase[:10], digits)
        message_out_console = {0: "Промах!", 1: "Вы попали в палубу!",
                               2: "Вы уничтожили корабль!",
                               3: "Человек победил!"}

        def __init__(self):
            self.pole = GamePole()
            self.pole.init()

            self.ships = self.pole._ships
            self.matrix = self.pole._pole
            self.total_ships = len(self.ships)
            self.other_ships = []
            self.open_cells = []
            self.free_cells = self.pole.generate_free_cells(shake=self.shake)

        def __len__(self):
            return self.total_ships

        def main_logics(self, point, other_obj):
            all_ships = other_obj.ships
            for ship in all_ships:
                if self.logic_killer_deck(point, ship):
                    if not ship.count_alive:
                        if self.logic_killer_ship(other_obj):
                            return 3
                        return 2
                    return 1
            return 0

        def logic_killer_deck(self, point, ship):
            for i, in_point in enumerate(ship.get_points):
                if point == in_point:
                    ship.count_alive -= 1
                    ship._is_move = False
                    ship[i] = 2
                    return True

        def logic_killer_ship(self, other_obj):
            other_obj.total_ships -= 1
            return not other_obj.total_ships

        def add_killed_ships(self, points):
            for point in points:
                self.open_cells.append(point)

        def handler_kill_ship(self, ships):
            for ship in ships:
                if not (ship in self.other_ships or ship.count_alive):
                    self.other_ships.append(ship)

                    self.pole.del_points(ship, self.free_cells)
                    self.add_killed_ships(ship.get_perimeter_points)

    class Player(Abstract):
        shake = False

        @staticmethod
        def handler(func):
            def wrapper(instance, *args, **kwargs):
                txt = ""
                point = func(instance, *args, **kwargs)
                point = point.translate(instance.maketrans)

                if (length := len(point)) != 2:
                    txt = f"Вы ввели неверное количество <{length}>, нужно 2"
                elif not point.isdigit():
                    txt = "Вы ввели не числовые координаты"
                elif not ("00" <= point <= "99"):
                    txt = "Вы ввели неверные координаты"
                if not txt:
                    point = tuple(map(int, point))
                    if point not in instance.free_cells:
                        txt = "Эти клетки ужe заняты"
                if txt:
                    txt = f"{txt}, повторите попытку"
                    return getattr(instance, func.__name__)(txt)

                return point

            return wrapper

        @handler
        def user_input(self, txt="Введите координаты"):
            return input(f"{txt} --->: ").replace(" ", "").upper()

        def action(self, bot):
            point = self.user_input()
            response = self.main_logics(point, bot)

            self.open_cells.append(point)
            if response == 2:
                self.handler_kill_ship(bot.ships)

            print(self.message_out_console.get(response))
            return response

    class Bot(Abstract):
        shake = True

        def action(self, player):
            point = self.free_cells.pop()

            response = self.main_logics(point, player)
            self.open_cells.append(point)
            if response == 2:
                self.handler_kill_ship(player.ships)
            return response

    def __init__(self):
        self.player = self.Player()
        self.bot = self.Bot()

    def handler_out(self, row_pole, hide=False):
        maketrans = str.maketrans("23", "XO")
        row = " ".join(map(str, row_pole)).translate(maketrans)
        if hide:
            row = row.replace("1", ".")
        return row

    def put_open_cells(self, row_pole, index, link_open_lst):
        for j in range(len(row_pole)):
            if (index, j) in link_open_lst:
                if row_pole[j] == ".":
                    row_pole[j] = 3

    def show(self, size=10):
        end = "    |    "
        ascii_leterrs = ascii_uppercase[:size]
        row_letters = ascii_leterrs.replace("", " ").strip()
        print(f"  {row_letters}{end}  {row_letters}")

        for i in range(size):
            bot_pole = self.bot.pole._pole[i]
            player_pole = self.player.pole._pole[i]
            self.put_open_cells(bot_pole, i, self.player.open_cells)
            self.put_open_cells(player_pole, i, self.bot.open_cells)

            print(ascii_leterrs[i], self.handler_out(player_pole), end=end)
            print(ascii_leterrs[i], self.handler_out(bot_pole, hide=True))

    def moves(self):
        self.player.pole.move_ships()
        self.bot.pole.move_ships()

    def play(self, moves=True):
        print(
        	"Добро пожаловать мой друг!\nПомни, чтобы выйти с игры"
        	" Достаточно нажать одновременно клавиши Ctrl + c\n"
        	"Приятной игры!"
        	)
        try:
            game_step = 0
            while self.player and self.bot:
                if game_step % 2 == 0:
                    self.show()
                    print("Ходит человек:")
                    if self.player.action(self.bot):
                        game_step -= 1
                else:
                    if self.bot.action(self.player):
                        game_step -= 1
                game_step += 1
                if moves:
                	self.moves()

            if not self.player:
                print("Победил компьютер.")
            raise KeyboardInterrupt

        except KeyboardInterrupt:
            print("\nДо новых встреч!")


if __name__ == "__main__":
    s = SeaBattle()
    s.play(moves=True)

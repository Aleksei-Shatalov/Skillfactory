
board = [[' ', '1', '2', '3', '4', '5', '6'],
         ['1', 'O', 'O', 'O', 'O', 'O', 'O'],
         ['2', 'O', 'O', 'O', 'O', 'O', 'O'],
         ['3', 'O', 'O', 'O', 'O', 'O', 'O'],
         ['4', 'O', 'O', 'O', 'O', 'O', 'O'],
         ['5', 'O', 'O', 'O', 'O', 'O', 'O'],
         ['6', 'O', 'O', 'O', 'O', 'O', 'O']]

def display_board(board):
    for row in board:
        print(" | ".join(row))

display_board(board)


# Исключения для внутренней логики игры
class BoardException(Exception):
    """Базовый класс для всех исключений, связанных с игровым полем."""
    pass

class BoardOutException(BoardException):
    """Выбрасывается, если выстрел за пределами поля."""
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы игрового поля!"

class BoardUsedException(BoardException):
    """Выбрасывается, если выстрел в уже использованную клетку."""
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"

class BoardShipException(BoardException):
    """Выбрасывается, если что-то не так с кораблём (например, неправильное размещение)."""
    def __str__(self):
        return "Ошибка в размещении корабля!"

class Dot:
    def __init__(self, x, y):
        """
        Инициализация точки.
        :param x: Координата по оси X (строка)
        :param y: Координата по оси Y (столбец)
        """
        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        Проверяет равенство двух точек.
        :param other: Другая точка (объект класса Dot)
        :return: True, если точки равны, иначе False
        """
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        """
        Представление точки в текстовом виде для отладки.
        :return: строка вида Dot(x, y)
        """
        return f"Dot({self.x}, {self.y})"

class Ship:
    def __init__(self, bow, length, direction):
        """
        Инициализация корабля.
        :param bow: Нос корабля (объект Dot)
        :param length: Длина корабля
        :param direction: Направление (0 — горизонтально, 1 — вертикально)
        """
        self.bow = bow  # Нос корабля
        self.length = length  # Длина корабля
        self.direction = direction  # Направление (0 — горизонтально, 1 — вертикально)
        self.lives = length  # Количество жизней корабля (изначально равно длине)

    def dots(self):
        """
        Возвращает список всех точек, которые занимает корабль.
        :return: Список объектов Dot
        """
        ship_dots = []
        for i in range(self.length):
            # Определяем координаты каждой точки корабля
            cur_x = self.bow.x + (i if self.direction == 1 else 0)  # Смещение по X, если направление вертикальное
            cur_y = self.bow.y + (i if self.direction == 0 else 0)  # Смещение по Y, если направление горизонтальное
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def hit(self, shot):
        """
        Проверяет, попал ли выстрел в корабль, и уменьшает количество жизней, если попал.
        :param shot: Точка выстрела (объект Dot)
        :return: True, если выстрел попал, иначе False
        """
        if shot in self.dots():
            self.lives -= 1
            return True
        return False

class Board:
    def __init__(self, hid=False):
        self.size = 6
        self.hid = hid
        self.field = [["O"] * self.size for _ in range(self.size)]
        self.ships = []
        self.busy_shots = []  # Занятые клетки (клетки, по которым уже стреляли)
        self.shots = []  # Список выстрелов
        self.alive_ships = 0

    def out(self, dot):
        """Проверяет, находится ли точка за пределами поля."""
        return not (0 <= dot.x < self.size and 0 <= dot.y < self.size)

    def add_ship(self, ship):
        """Добавляет корабль на доску."""
        for dot in ship.dots():
            if self.out(dot) or dot in self.busy_shots:
                raise ValueError("Невозможно разместить корабль: точка занята или выходит за пределы.")
        for dot in ship.dots():
            self.field[dot.x][dot.y] = "■"
            self.busy_shots.append(dot)
        self.ships.append(ship)
        self.alive_ships += 1
        self.contour(ship)

    def contour(self, ship, mark=False):
        """Обводит корабль по контуру."""
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots():
            for dx, dy in near:
                cur = Dot(dot.x + dx, dot.y + dy)
                if not self.out(cur) and cur not in self.busy_shots:
                    self.busy_shots.append(cur)
                    if mark:
                        self.field[cur.x][cur.y] = "."

    def shot(self, dot):
        """Делает выстрел по доске."""
        print(f"Текущий выстрел по точке: {dot.x + 1}, {dot.y + 1}")
        if self.out(dot):
            raise BoardOutException()  # Выстрел за пределы поля
        if dot in self.shots:
            print(f"Ошибка! Уже стреляли по точке: {dot}")
            raise BoardUsedException()  # Повторный выстрел в эту клетку

        self.shots.append(dot)  # Запоминаем выстрел
        for ship in self.ships:
            if dot in ship.dots():
                ship.lives -= 1
                self.field[dot.x][dot.y] = "X"  # Попадание
                print(f"Попал по кораблю: {dot.x + 1}, {dot.y + 1}")
                if ship.lives == 0:
                    self.alive_ships -= 1
                    self.contour(ship, mark=True)
                    print("Корабль уничтожен!")
                else:
                    print(f"Корабль ранен. Осталось жизней: {ship.lives}")
                return True

        self.field[dot.x][dot.y] = "T"  # Промах
        print("Мимо!")
        return False

    def display(self):
        """
        Отображение поля с учётом скрытия кораблей, если hid=True.
        """
        board_display = [[" "] + [str(i + 1) for i in range(self.size)]]  # Заголовок
        for i, row in enumerate(self.field):
            visible_row = [
                "■" if cell == "■" and not self.hid else "O" if cell == "■" and self.hid else cell
                for cell in row
            ]
            board_display.append([str(i + 1)] + visible_row)

        for row in board_display:
            print(" | ".join(row))
        print()

    def begin(self):
        """Очищает список занятых точек."""
        self.busy_shots = []


class Player:
    def __init__(self, board, enemy_board):
        self.board = board  # Собственная доска
        self.enemy_board = enemy_board  # Доска врага

    def ask(self):
        """Запрашивает у пользователя координаты для выстрела."""
        raise NotImplementedError("Метод ask должен быть реализован в дочернем классе")

    def move(self):
        """Основной метод для хода игрока (или ИИ)."""
        while True:
            try:
                dot = self.ask()  # Спрашиваем точку для выстрела
                print(f"Игрок стреляет по точке {dot.x + 1}, {dot.y + 1}")  # Выводим, по какой точке идет выстрел
                hit = self.enemy_board.shot(dot)  # Делаем выстрел

                # Если попадание, проверяем, нужно ли повторить ход
                if hit:
                    print(f"Попадание в точку {dot.x + 1}, {dot.y + 1}")
                    print(
                        f"Осталось кораблей у противника: {self.enemy_board.alive_ships}")  # Печатаем оставшиеся корабли противника
                    return True  # Повторный ход после попадания
                else:
                    print(f"Мимо в точке {dot.x + 1}, {dot.y + 1}")
                    return False  # Ход завершен, если не было попадания

            except BoardOutException as e:
                print(e)  # Обработка ошибки выстрела за пределы
            except BoardUsedException as e:
                print(e)  # Обработка ошибки повторного выстрела
            except ValueError as e:
                print(e)  # Обработка ошибок


class User(Player):
    def ask(self):
        """Запрашивает у пользователя координаты для выстрела."""
        while True:
            try:
                coords = input("Введите координаты выстрела (формат: x y): ").split()
                if len(coords) != 2:
                    raise ValueError("Введите две координаты, разделённые пробелом.")
                x, y = map(int, coords)
                return Dot(x - 1, y - 1)  # Преобразуем к индексации с нуля
            except ValueError as e:
                print(f"Ошибка ввода: {e}. Попробуйте снова.")

    def move(self):
        """Основной метод для хода игрока."""
        while True:
            try:
                dot = self.ask()  # Спрашиваем точку для выстрела
                print(f"Игрок стреляет по точке {dot.x + 1}, {dot.y + 1}")  # Выводим, по какой точке идет выстрел
                hit = self.enemy_board.shot(dot)  # Делаем выстрел

                # Если попадание, проверяем, нужно ли повторить ход
                if hit:
                    print(f"Попадание в точку {dot.x + 1}, {dot.y + 1}")
                    print(
                        f"Осталось кораблей у противника: {self.enemy_board.alive_ships}")  # Печатаем оставшиеся корабли противника
                    return True  # Повторный ход после попадания
                else:
                    print(f"Мимо в точке {dot.x + 1}, {dot.y + 1}")
                    return False  # Ход завершен, если не было попадания

            except BoardOutException as e:
                print(e)  # Обработка ошибки выстрела за пределы
            except BoardUsedException as e:
                print(e)  # Обработка ошибки повторного выстрела
            except ValueError as e:
                print(e)  # Обработка ошибок



import random

class AI(Player):
    def move(self):
        """Основной метод для хода ИИ."""
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            dot = Dot(x, y)

            try:
                print(f"ИИ стреляет по точке {dot.x + 1}, {dot.y + 1}")
                self.enemy_board.shot(dot)
                return
            except BoardOutException as e:
                print(f"Ошибка ИИ: {e}")
            except BoardUsedException as e:
                print(f"Ошибка ИИ: {e}")



class Game:
    def __init__(self):
        self.board_player = Board()
        self.board_enemy = Board(hid=True)  # Скрытая доска ИИ
        self.user = User(self.board_player, self.board_enemy)
        self.ai = AI(self.board_enemy, self.board_player)

    def random_board(self, board):
        """
        Случайно расставляет корабли на доске.
        """
        ships = [3, 2, 2, 1, 1, 1, 1]  # Длины кораблей
        board.ships = []
        board.alive_ships = 0

        for length in ships:
            placed = False
            for _ in range(500):  # Ограничиваем число попыток
                x = random.randint(0, board.size - 1)
                y = random.randint(0, board.size - 1)
                direction = random.choice([0, 1])  # 0 — горизонтально, 1 — вертикально
                ship = Ship(Dot(x, y), length, direction)
                try:
                    board.add_ship(ship)
                    placed = True
                    break
                except (ValueError, IndexError):
                    continue

            if not placed:
                # Если корабль не удалось разместить, перезаполняем доску
                return self.random_board(board)

    def greet(self):
        """
        Приветственное сообщение пользователю, рассказывающее правила.
        """
        print("Добро пожаловать в игру 'Морской бой'!")
        print("Правила игры: вы и компьютер по очереди стреляете по клеткам на поле.")
        print("Координаты ввода для выстрела: x y, например: 1 1.")
        print("Кто уничтожит все корабли противника первым, тот и победит!")

    def start(self):
        self.greet()
        self.board_player.begin()
        self.board_enemy.begin()
        self.random_board(self.board_player)  # Сначала расставляем корабли игрока
        self.random_board(self.board_enemy)  # Потом расставляем корабли для ИИ

        turn = 0  # Ход игрока
        while self.board_player.alive_ships > 0 and self.board_enemy.alive_ships > 0:
            if turn % 2 == 0:  # Ход игрока
                print("\nВаш ход:")
                self.board_enemy.display()  # Показать поле противника
                hit = self.user.move()  # Игрок делает ход
                if hit:
                    continue  # Игрок может сделать второй ход, если был попадание
            else:  # Ход ИИ
                print("\nХод ИИ:")
                self.board_player.display()  # Показать поле игрока
                self.ai.move()  # ИИ делает ход

            # Печать состояния после каждого хода
            print(f"Осталось кораблей у игрока: {self.board_player.alive_ships}")
            print(f"Осталось кораблей у ИИ: {self.board_enemy.alive_ships}")

            turn += 1

        if self.board_enemy.alive_ships == 0:
            print("Вы победили!")
        else:
            print("Компьютер победил!")


game = Game()
game.start()

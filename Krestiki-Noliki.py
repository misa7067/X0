def hello():
    # Приветствие
    print("---")
    print("Приветствую вас в игре Крестики - Нолики")
    print("Правила")
    print("Ходим в формате: x y")
    print("x - номер столбца")
    print("y - номер строки")
    print("---")


def field():
    # Вывод поля на консоль
    print(f"  0 1 2")
    for i in range(3):
        print(f"{i} {pole[i][0]} {pole[i][1]} {pole[i][2]}")


def X0():
    # Ход игрока и выводит текущего состояние поля
    count = 2
    marcer = 0
    while True:
        if count % 2 == 0:
            symbol = "0"
        else:
            symbol = "X"
        print(f"Ходит игрок {symbol}")
        x, y = pass_()
        pole[x][y] = symbol
        if check_win():
            return True
        field()
        count += 1
        marcer += 1

pole = [[" "] * 3 for i in range(3)]
def check_win():
    win_cord = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for cord in win_cord:
        symbols = []
        for c in cord:
            symbols.append(pole[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("Выиграл X!!!")
            return True
        if symbols == ["0", "0", "0"]:
            print("Выиграл 0!!!")
            return True
    return False


def pass_():
    # Получаем координаты хода от пользователя и возвращаем их,
    # если введены неверные данные или клетка уже занята, — запрашиваем новые
    while True:
        cords = input("Ваш ход: ").split()
        if len(cords) != 2:
            raise ValueError("Вы должны ввести две координаты через пробел")
        x, y = cords
        if not (x.isdigit() and y.isdigit()):
            print("Введите числа")
            continue
        x, y = int(x), int(y)
        if not (0 <= x <= 2 and 0 <= y <= 2):
            print("Неверные значения")
            continue
        if pole[x][y] != " ":
            print("Клетка занята")
            continue
        return x, y



hello()
field()

while True:
    try:
        check_win()
        x, y = pass_()
        pole[x][y] = "X"
        field()
        if X0():
            print("Поздравляю!")
            break
        if marcer == 8:
            print("Ничья!!!")
            break

    except ValueError as e:
        print(e)
    else:
        pass
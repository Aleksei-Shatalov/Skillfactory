# Создание игрового поля
board = [[' ', ' ', ' '],
         [' ', ' ', ' '],
         [' ', ' ', ' ']]

# Функция для отображения игрового поля
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

# Функция для выполнения хода игрока
def make_move(board, player):
    print(f"Ход игрока {player}")
    while True:
        try:
            row = int(input("Введите номер строки (1-3): ")) - 1  # Преобразуем в индекс (1 -> 0, 2 -> 1, 3 -> 2)
            col = int(input("Введите номер столбца (1-3): ")) - 1  # То же самое для столбца
            if 0 <= row < 3 and 0 <= col < 3:  # Проверяем, что ввод в пределах 1-3 (но после -1 становится 0-2)
                if board[row][col] == ' ':
                    board[row][col] = player
                    break
                else:
                    print("Эта клетка уже занята, попробуйте снова.")
            else:
                print("Номер строки и столбца должен быть от 1 до 3.")
        except (ValueError, IndexError):
            print("Некорректный ввод. Введите числа от 1 до 3.")

# Функция для проверки победителя
def check_winner(board):
    # Проверяем строки и столбцы
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':  # Строки
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':  # Столбцы
            return board[0][i]

    # Проверяем диагонали
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    return None

# Основная функция игры
def play_game(board):
    print_board(board)

    current_player = 'X'
    for turn in range(9):  # Максимум 9 ходов (3x3 поле)
        make_move(board, current_player)
        print_board(board)

        # Проверяем, есть ли победитель
        winner = check_winner(board)
        if winner:
            print(f"Игрок {winner} победил!")
            break

        # Меняем игрока
        current_player = 'O' if current_player == 'X' else 'X'
    else:
        print("Ничья!")

# Запуск игры
play_game(board)
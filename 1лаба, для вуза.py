# 1 лаба, Сухоруков Михаил, 421701, ППОИС
# Пятнашки
# Объявление функций:

import random
import sys


# MM
def main(): ...  # главное меню


def show_menu(): ...  # показ меню


def rules(): ...  # правила игры


# G
class Tag_game: ...


# create_board():...
# check_board():...
# game()
# print_board
# check_win


# Реализация:
def main():
    print("Добро пожаловать в игру \"Пятнашки\"")
    while True:
        show_menu()
        try:
            choice = int(input("Выберите один из подходящих для вас вариантов (1-3)"))
            if choice not in [1, 2, 3]:
                print("Выберите число от 1 до 3!")
                continue
        except ValueError:
            print("Нужно ввести число")
            continue
        match choice:
            case 1:
                rules()
            case 2:
                game_instance = Tag_game()
                game_instance.game()
            case 3:
                print("Спасибо за игру!")
                sys.exit(0)


def show_menu():
    print("=" * 30)
    print("         МЕНЮ ИГРЫ")
    print("=" * 30)
    print("1. Правила игры")
    print("2. Начать игру")
    print("3. Выход")
    print("=" * 30)


def rules():
    print("\n📖 ПРАВИЛА ИГРЫ:")
    print("Цель игры - расставить числа по порядку")
    print("от 1 до 15, оставив пустую клетку в правом нижнем углу.")
    print("Используйте стрелки или WASD для перемещения клеток.")
    input("Нажмите Enter чтобы вернуться в меню...")


class Tag_game:

    def __init__(self, size=4):
        self.board = []
        self.zero_index = []
        self.size = size
        self.board_win = []

    def check_board(self, board):
        size = len(board)
        one_mass = []
        for i in range(size):
            for j in range(size):
                if board[i][j] != 0:
                    one_mass.append(board[i][j])

        inversia = 0
        for x in range(len(one_mass)):
            for y in range(x + 1, len(one_mass)):
                if one_mass[x] > one_mass[y]:
                    inversia += 1

        zero = 0
        for i in range(size):
            for j in range(size):
                if board[i][j] == 0:
                    zero = size - i
                    break

        if size % 2 == 1:
            return inversia % 2 == 0
        else:
            return (inversia + zero) % 2 == 1

    def create_board(self):
        numbers = list(range(1, self.size * self.size)) + [0]

        # Создаем выигрышную доску
        self.board_win = []
        num = 1
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    row.append(0)
                else:
                    row.append(num)
                    num += 1
            self.board_win.append(row)

        # Создаем игровую доску
        while True:
            random.shuffle(numbers)
            self.board = []
            index = 0
            for i in range(self.size):
                row = []
                for j in range(self.size):
                    row.append(numbers[index])
                    index += 1
                self.board.append(row)

            if self.check_board(self.board):
                break

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    self.zero_index = [i, j]
                    return

    def print_board(self):
        print("\n" + "=" * (self.size * 3))
        for x in range(self.size):
            row = []
            for num in self.board[x]:
                if num != 0:
                    row.append(f"{num:2d}")
                else:
                    row.append("  ")
            print(" | ".join(row))
            if x < self.size - 1:
                print("-" * (self.size * 4 - 1))
        print("=" * (self.size * 3))

    def check_win(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != self.board_win[i][j]:
                    return False
        print("Наливай, победа!")
        input("Нажмите Enter чтобы вернуться в меню...")
        return True

    def game(self):
        self.create_board()
        while True:
            print("\nВыбери вариант:")
            print("W/S/D/A - ход (введи символ)")
            print("1. Пересоздание карты")
            print("2. Выход в меню")
            self.print_board()

            choice = input("Твой ход: ").strip().lower()

            if choice not in ["1", "2", "w", "a", "s", "d"]:
                print("Выберите W/A/S/D, 1 или 2!")
                continue

            if choice == "w":
                if self.zero_index[0] > 0:
                    value_above = self.board[self.zero_index[0] - 1][self.zero_index[1]]
                    self.board[self.zero_index[0]][self.zero_index[1]] = value_above
                    self.board[self.zero_index[0] - 1][self.zero_index[1]] = 0
                    self.zero_index[0] -= 1
                    if self.check_win():
                        return True
                else:
                    print("Невозможный ход")

            elif choice == "s":
                if self.zero_index[0] < self.size - 1:
                    value_below = self.board[self.zero_index[0] + 1][self.zero_index[1]]
                    self.board[self.zero_index[0]][self.zero_index[1]] = value_below
                    self.board[self.zero_index[0] + 1][self.zero_index[1]] = 0
                    self.zero_index[0] += 1
                    if self.check_win():
                        return True
                else:
                    print("Невозможный ход")

            elif choice == "a":
                if self.zero_index[1] > 0:
                    value_left = self.board[self.zero_index[0]][self.zero_index[1] - 1]
                    self.board[self.zero_index[0]][self.zero_index[1]] = value_left
                    self.board[self.zero_index[0]][self.zero_index[1] - 1] = 0
                    self.zero_index[1] -= 1
                    if self.check_win():
                        return True
                else:
                    print("Невозможный ход")

            elif choice == "d":
                if self.zero_index[1] < self.size - 1:
                    value_right = self.board[self.zero_index[0]][self.zero_index[1] + 1]
                    self.board[self.zero_index[0]][self.zero_index[1]] = value_right
                    self.board[self.zero_index[0]][self.zero_index[1] + 1] = 0
                    self.zero_index[1] += 1
                    if self.check_win():
                        return True
                else:
                    print("Невозможный ход")

            elif choice == "1":
                self.create_board()
                print("Доска пересоздана!")

            elif choice == "2":
                print("Ты всё равно победитель :)")
                return False


# Главная:
if __name__ == "__main__":
    main()
import unittest
from Tag_game import TagGame
import random


class TestTagGameLogic(unittest.TestCase):

    def test_game_initialization(self):
        """Тест инициализации игры"""
        game = TagGame()
        self.assertEqual(game.size, 4)
        self.assertEqual(game.board, [])
        self.assertEqual(game.zero_index, [])
        self.assertEqual(game.board_win, [])

    def test_custom_size_initialization(self):
        """Тест инициализации с кастомным размером"""
        game = TagGame(3)
        self.assertEqual(game.size, 3)

    def test_check_board_solvable(self):
        """Тест проверки решаемой доски"""
        game = TagGame()

        # Решаемая доска (четное количество инверсий для размера 4)
        solvable_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        result = game.check_board(solvable_board)
        self.assertTrue(result)

    def test_check_board_unsolvable(self):
        """Тест проверки нерешаемой доски"""
        game = TagGame()

        # Нерешаемая доска (нечетное количество инверсий для размера 4)
        unsolvable_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 15, 14, 0]
        ]
        result = game.check_board(unsolvable_board)
        self.assertFalse(result)

    def test_create_board_valid(self):
        """Тест создания валидной доски"""
        game = TagGame()
        game.create_board()

        # Проверяем размер доски
        self.assertEqual(len(game.board), 4)
        for row in game.board:
            self.assertEqual(len(row), 4)

        # Проверяем, что доска решаема
        self.assertTrue(game.check_board(game.board))

        # Проверяем наличие нуля
        has_zero = any(0 in row for row in game.board)
        self.assertTrue(has_zero)

        # Проверяем, что все числа от 0 до 15 присутствуют
        all_numbers = set()
        for row in game.board:
            for num in row:
                all_numbers.add(num)

        self.assertEqual(all_numbers, set(range(16)))

    def test_check_win_true(self):
        """Тест проверки победы (True)"""
        game = TagGame()
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        game.board_win = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        result = game.check_win()
        self.assertTrue(result)

    def test_check_win_false(self):
        """Тест проверки победы (False)"""
        game = TagGame()
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 15, 14, 0]
        ]
        game.board_win = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        result = game.check_win()
        self.assertFalse(result)

    def test_move_valid(self):
        """Тест валидных ходов"""
        game = TagGame()
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 0, 12],
            [13, 14, 15, 11]
        ]
        game.zero_index = [2, 2]

        # Движение вверх
        result = game.move('w')
        self.assertTrue(result)
        self.assertEqual(game.zero_index, [1, 2])
        self.assertEqual(game.board[1][2], 0)
        self.assertEqual(game.board[2][2], 7)

        # Сброс для следующего теста
        game.zero_index = [2, 2]
        game.board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 0, 12],
            [13, 14, 15, 11]
        ]

    def test_move_invalid(self):
        """Тест невалидных ходов"""
        game = TagGame()
        game.board = [
            [0, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 1]
        ]
        game.zero_index = [0, 0]

        # Попытка движения вверх (невалидно)
        result = game.move('w')
        self.assertFalse(result)

        # Попытка движения влево (невалидно)
        result = game.move('a')
        self.assertFalse(result)

    def test_get_board(self):
        """Тест получения доски"""
        game = TagGame()
        test_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        game.board = test_board
        result = game.get_board()
        self.assertEqual(result, test_board)

    def test_get_win_board(self):
        """Тест получения выигрышной доски"""
        game = TagGame()
        test_win_board = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        game.board_win = test_win_board
        result = game.get_win_board()
        self.assertEqual(result, test_win_board)


if __name__ == "__main__":
    unittest.main()
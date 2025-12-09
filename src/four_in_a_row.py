# Author:       Chris "C.J" Irwin
# GitHub:       ircjwin
# Email:        christopherjamesirwin@gmail.com
# Description:  This is the game Four In A Row, implemented with a
#               text UI. It runs in terminals and IDEs like PyCharm.


from itertools import chain


class FourInARow:
    """
    Represents a single game of Four In A Row

    Attributes:
            player (bool):  True if player 1; False if player 2
            winner (bool):  True if a player has won
            turns (int):  Total number of player turns
            last_turn (tuple):  Row and column of last chip placed
            chip_choices (list[str]):  A list of symbols players use as chips
            chips (list[str]):  A list of the chosen symbols to use as chips
            board (list[list[str]]):  2D list representing the game board
    """

    def __init__(self):
        """
        Initializes a Four In A Row object.

        :param: N/A
        :return: N/A
        """
        self._player = True
        self._winner = False
        self._turns = 0
        self._last_turn = (0, 0)
        self._chips = ['', '']
        self._chip_choices = ['&', '@', '#', '%', '?', '*']
        self._board = [[' ' for i in range(7)] for j in range(6)]

    def game_start(self):
        """
        Prints welcome message and prompts players
        for their chip choices.

        :param: N/A
        :return: N/A
        """
        print("Welcome to Four In A Row!\n")

        for i in range(2):
            print(f"Choose your chip, Player {i + 1}:")
            print(f"{self._chip_choices}     ")

            while True:
                chosen_chip = input()
                print("")
                if chosen_chip in self._chip_choices:
                    break
                print("Please enter a valid chip:")

            self._chips[i] = chosen_chip
            self._chip_choices.remove(chosen_chip)

    def print_board(self):
        """
        Prints current game board.

        :param: N/A
        :return: N/A
        """
        col_num = "  "

        for i in range(len(self._board[0])):
            col_num += f"{i + 1}    "
        print(col_num)

        for row in self._board:
            print(row)
        print("")

    def player_turn(self):
        """
        Prompts current player for their turn and
        places chip on the board.

        :param: N/A
        :return: N/A
        """
        player_num = 1 if self._player else 2
        chip = self._chips[player_num - 1]
        print(f"Pick a column, Player {player_num}!")

        while True:
            col = int(input()) - 1
            print("")

            if col < 0 or col >= len(self._board[0]):
                print("Please enter a valid column:")
                continue

            # Starts at bottom of column and fills first empty space
            for row in range(len(self._board) - 1, -1, -1):
                if self._board[row][col] == ' ':
                    self._board[row][col] = chip
                    self._turns += 1
                    self._last_turn = row, col
                    return

            print("Column is full. Try again:")

    def _count_opposite_sides(self, steps, chip):
        """
        Counts consecutive player chips on opposite
        sides of most recently placed chip.

        :param steps: tuple holding row, col iterative step
        :param chip: str that matches current player chip

        :return: N/A
        """
        row, col = self._last_turn
        row_len, col_len = len(self._board), len(self._board[0])
        row_step, col_step = steps
        chip_count = 0
        flip_sides = False

        # Counts one side then its opposite
        for i in chain(range(-1, -4, -1), range(1, 4)):

            # Skips ahead if first side counted
            if flip_sides is True and i < 1:
                continue

            new_row = row + i * row_step
            new_col = col + i * col_step
            in_bounds = 0 <= new_row < row_len and 0 <= new_col < col_len

            if in_bounds and self._board[new_row][new_col] == chip:
                chip_count += 1
            else:
                if flip_sides is False:
                    flip_sides = True
                else:
                    break

        # Last placed chip plus 3+ is four in a row
        if chip_count >= 3:
            self._winner = True

    def check_game_over(self):
        """
        Checks if last player move meets win condition
        and checks for a tie game.

        :param: N/A
        :return: bool that represents game over state
        """
        player_num = 1 if self._player else 2
        chip = self._chips[player_num - 1]

        # Number of steps and direction for row, col iteration
        steps = [(1, 0), (0, 1), (1, 1), (1, -1)]
        win_msg = f"Player {player_num} wins!"
        tie_msg = "It's a tie!"

        for i in range(4):
            self._count_opposite_sides(steps[i], chip)
            if self._winner is True:
                break

        if self._winner is True or self._turns >= 42:
            self.print_board()
            print(win_msg if self._winner else tie_msg)
            return True

        self._player = not self._player
        return False


def main():
    new_game = FourInARow()
    new_game.game_start()
    game_over = False
    while game_over is False:
        new_game.print_board()
        new_game.player_turn()
        game_over = new_game.check_game_over()


if __name__ == '__main__':
    main()

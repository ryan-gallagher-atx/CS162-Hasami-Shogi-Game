# Author: Ryan Gallagher
# Date: 11/18/2021
# Description: A fun and exciting abstract chess like game!

class HasamiShogiGame:
    """An instance of a game of Hasami Shogi that is fully playable."""

    def __init__(self, state='UNFINISHED', active_player='BLACK', captured_black=0, captured_red=0):
        """Initializes the attributes of a game of Hasami Shogi """
        self._state = state
        self._active_player = active_player
        self._captured_black = captured_black
        self._captured_red = captured_red
        self._board = [
            [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
            ['a', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
            ['b', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
            ['c', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
            ['d', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
            ['e', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
            ['f', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
            ['g', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
            ['h', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
            ['i', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
        ]

    def get_game_state(self):
        """Returns the game state"""
        if self._captured_red >= 8:
            self._state = 'BLACK_WON'
        if self._captured_black >= 8:
            self._state = 'RED_WON'
        return self._state

    def get_active_player(self):
        """Returns which player's turn it is"""
        return self._active_player

    def get_num_captured_pieces(self, color='RED' or 'BLACK'):
        """Returns how many pieces of a chosen color have been captured"""
        if color == 'RED':
            return self._captured_red
        elif color == 'BLACK':
            return self._captured_black
        else:
            raise ValueError('You did not input either "BLACK" or "RED"')

    def make_move(self, start, finish):
        """Takes the starting position of a piece, and moves it the end ending piece, if possible. Captures opponent."""
        # checks what color the piece is, checks to make sure it is that players turn, if it is
        if self._state != 'UNFINISHED':
            return False  # the game has already been won
        player = self._active_player
        if player == 'BLACK':
            space = 'B'
        else:
            space = 'R'
        occupant = self.get_square_occupant(start)
        if player == occupant:
            # checks to see if the move is legal or not. If it is, the move happens.
            legal = self._is_move_legal(start, finish)
            if legal is True:
                # move piece and change board
                start_index = self._convert_index(start)
                finish_index = self._convert_index(finish)
                self._board[start_index[0]][start_index[1]] = '*'
                self._board[finish_index[0]][finish_index[1]] = space
                # check to see if any captures have taken place
                # add the captures to the correct counter
                # removes the captures from the board
                self._piece_capture(finish_index)
                # check game state
                self.get_game_state()
                # switch whose turn it is
                self._switch_active_player()
                return True

            else:
                return False  # not a legal move

        else:
            return False  # it is not that players turn

    def _switch_active_player(self):
        """Switches which player is active."""
        if self._active_player == 'BLACK':
            self._active_player = 'RED'
        else:
            self._active_player = 'BLACK'

    def _piece_capture(self, location):
        """Checks to see if any piece captures have occurred, and if they have it calls its helper."""
        # Determine targets, and create variables to compare to.
        reference = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        player = self.get_active_player()
        row_index = location[0]
        column_index = location[1]
        captured = []
        if player == 'BLACK':
            enemy = 'R'
            player_piece = 'B'
        else:
            enemy = 'B'
            player_piece = 'R'

        # Checks to see if there are opposing pieces that can be captured horizontally.

        # Check for a capture to the right
        if column_index + 1 in reference:
            if self._board[row_index][column_index + 1] == enemy:
                i = 1
                while column_index + i in reference:
                    if self._board[row_index][column_index + i] == enemy:
                        captured.append([row_index, column_index + i])
                        i += 1
                    elif self._board[row_index][column_index + i] == player_piece:
                        self._piece_capture_helper(captured)  # capture the enemy pieces and update board
                        i = 10  # ends loop
                    else:
                        i = 10  # a no capture scenario, ends loop

                # check for corner capture to the right
                captured = []
                if row_index == 9 and column_index + 1 == 9:
                    if self._board[row_index - 1][column_index + 1] == player_piece:
                        captured.append([row_index, column_index + 1])
                        self._piece_capture_helper(captured)
                elif row_index == 1 and column_index + 1 == 9:
                    if self._board[row_index + 1][column_index + 1] == player_piece:
                        captured.append([row_index, column_index + 1])
                        self._piece_capture_helper(captured)

        # check for a capture to the left
        if column_index - 1 in reference:
            if self._board[row_index][column_index - 1] == enemy:
                i = 1
                while column_index - i in reference:
                    if self._board[row_index][column_index - i] == enemy:
                        captured.append([row_index, column_index - i])
                        i += 1
                    elif self._board[row_index][column_index - i] == player_piece:
                        self._piece_capture_helper(captured)  # capture enemy pieces and update board
                        i = 10  # ends loop
                    else:
                        i = 10  # no capture scenario, ends loop

                # check for corner capture to the left
                captured = []
                if row_index == 9 and column_index - 1 == 1:
                    if self._board[row_index - 1][column_index - 1] == player_piece:
                        captured.append([row_index, column_index - 1])
                        self._piece_capture_helper(captured)
                elif row_index == 1 and column_index - 1 == 1:
                    if self._board[row_index + 1][column_index - 1] == player_piece:
                        captured.append([row_index, column_index - 1])
                        self._piece_capture_helper(captured)

        # Checks to see if there are opposing pieces that can be captured vertically.

        # check for captures below
        if row_index + 1 in reference:
            if self._board[row_index + 1][column_index] == enemy:
                i = 1
                while row_index + i in reference:
                    if self._board[row_index + i][column_index] == enemy:
                        captured.append([row_index + i, column_index])
                        i += 1
                    elif self._board[row_index + i][column_index] == player_piece:
                        self._piece_capture_helper(captured)  # capture enemy pieces and update board
                        i = 10  # ends loop
                    else:
                        i = 10  # no capture scenario, ends loop

                # check for corner capture below
                captured = []
                if row_index + 1 == 9 and column_index == 1:
                    if self._board[row_index + 1][column_index + 1] == player_piece:
                        captured.append([row_index + 1, column_index])
                        self._piece_capture_helper(captured)
                elif row_index + 1 == 9 and column_index == 9:
                    if self._board[row_index + 1][column_index - 1] == player_piece:
                        captured.append([row_index + 1, column_index])
                        self._piece_capture_helper(captured)

        # check for captures above
        if row_index - 1 in reference:
            if self._board[row_index - 1][column_index] == enemy:
                i = 1
                while row_index - i in reference:
                    if self._board[row_index - i][column_index] == enemy:
                        captured.append([row_index - i, column_index])
                        i += 1
                    elif self._board[row_index - i][column_index] == player_piece:
                        self._piece_capture_helper(captured)  # capture enemy pieces and update board
                        i = 10  # ends loop
                    else:
                        i = 10  # no capture scenario, ends loop

                # check for corner capture above
                captured = []
                if row_index - 1 == 1 and column_index == 1:
                    if self._board[row_index - 1][column_index + 1] == player_piece:
                        captured.append([row_index - 1, column_index])
                        self._piece_capture_helper(captured)
                elif row_index - 1 == 1 and column_index == 9:
                    if self._board[row_index - 1][column_index - 1] == player_piece:
                        captured.append([row_index - 1, column_index])
                        self._piece_capture_helper(captured)

        # Checks to see if there are any opposing pieces that can be captured orthogonally.

    def _piece_capture_helper(self, captured):
        """Takes a list of coordinates of captured pieces, changes the spaces to stars and increments counter."""
        # takes the list, iterates over it, and if the space is the opposing player's pieces it changes the space to
        # a star and increments the count
        for space in captured:
            if self._board[space[0]][space[1]] == 'B':
                self._captured_black += 1
                self._board[space[0]][space[1]] = '*'
            elif self._board[space[0]][space[1]] == 'R':
                self._captured_red += 1
                self._board[space[0]][space[1]] = '*'
            else:
                pass

    def _is_move_legal(self, start, finish):
        """Checks to see if a move is legal. If it is, returns true."""
        start_index = self._convert_index(start)
        finish_index = self._convert_index(finish)
        # checks to see if the piece is moving either vertically or horizontally by comparing the start and end
        # rows and columns to each other
        reference = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if start_index == finish_index:  # makes sure the player wasn't trying to move the piece to the same spot
            return False
        # checks to make sure either the rows or columns are the same
        if start_index[0] != finish_index[0] and start_index[1] != finish_index[1]:
            return False
        # checks to see if the move is out of bounds of the board
        if finish_index[0] not in reference or finish_index[1] not in reference:
            return False
        # also it needs to check if there are any pieces in way
        if start_index[0] == finish_index[0]:  # checks to see if there are any pieces in the way on a horizontal move
            if start_index[1] < finish_index[1]:  # checks for a move to the right
                # check for pieces in the way
                for i in reference[start_index[1]:finish_index[1]]:
                    occupant = self._board[start_index[0]][i]
                    if occupant == 'B' or occupant == 'R':
                        return False
                return True
            else:  # checks for a move to the left
                for i in reference[finish_index[1] - 1:start_index[1] - 1]:
                    occupant = self._board[start_index[0]][i]
                    if occupant == 'B' or occupant == 'R':
                        return False
                return True
        elif start_index[1] == finish_index[1]:  # checks to see if there are any pieces in the way on a vertical move
            if start_index[0] < finish_index[0]:  # checks for a move down
                for i in reference[start_index[0]:finish_index[0]]:
                    occupant = self._board[i][start_index[1]]
                    if occupant == 'B' or occupant == 'R':
                        return False
                return True
            else:  # checks for a move up
                for i in reference[finish_index[0] - 1:start_index[0] - 1]:
                    occupant = self._board[i][start_index[1]]
                    if occupant == 'B' or occupant == 'R':
                        return False
                return True
        else:
            return False  # if it passes all of these tests, it will return True, if it fails any, it will return False

    def get_square_occupant(self, location):
        """Takes a position, and returns if there is a piece there, and if so, which color it is."""
        index = self._convert_index(location)
        row_index = index[0]
        column_index = index[1]
        occupant = self._board[row_index][column_index]
        if occupant == 'B':
            return 'BLACK'
        elif occupant == 'R':
            return 'RED'
        else:
            return 'NONE'

    def print_board(self):
        """Prints out the game board."""
        for row in self._board:
            print(row)

    @staticmethod
    def _convert_index(location):
        """Takes a location and returns the row index"""
        letter = location[0]
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
        row_index = alphabet.index(letter) + 1
        column_index = int(location[1])
        index = [row_index, column_index]
        return index

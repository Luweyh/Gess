# Author: Luwey Hon
# Description: This program plays the gess game which is a
# 20x20 board game with two players. The goal of the game
# is to remove the ring board piece from the other player.
# The player will move a 3x3 foot that is depending on the middle
# piece. If there is no middle piece, they can only move
# 3 direction depending if there is a piece in that position
# and if its an unbostrcuted movement. while if there is a center piece,
# it can move as much as it wants as long as it is in the 18x18
# position and has no piece blocking it. The game has an option
# for the player to resign and the player can't suicide on their turn.

class GessGame:
    """
    Represents the game Gess which is a 20x20 board game
    for two players to play. The goal is to remove the
    opponents ring piece
    """

    def __init__(self):
        """
        Initializes the Gess game which includes the game state,
        whose turn it is, the board for debugging purposes,
        the source footprint, a variable to keep track of unobstructed
        path, and finally a variable to help check for suicide.
        """
        self._game_state = 'UNFINISHED'
        self._turn = 'black'
        self._board = [['_' for num in range(20)] for num in range(20)]
        self._source_foot_print = []
        self._unobstructed_path = 0
        self._suicide = 0

        # fills row 2,-2,4,-4 of board
        row_2_4 = [2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17]
        for col in row_2_4:
            self._board[1][col] = 'b'
            self._board[-2][col] = 'w'
            self._board[3][col] = 'b'
            self._board[-4][col] = 'w'

        # fills row 3, -3 on board
        row_3 = [1, 2, 3, 5, 7, 8, 9, 10, 12, 14, 16, 17, 18]
        for col in row_3:
            self._board[2][col] = 'b'
            self._board[-3][col] = 'w'

        # fills row 7, -7
        row_7 = [2, 5, 8, 11, 14, 17]
        for col in row_7:
            self._board[6][col] = 'b'
            self._board[-7][col] = 'w'

    def get_game_state(self):
        """Gets the current game state"""
        return self._game_state

    def resign_game(self):
        """
        Resigns the game depending on whose turn it is. If this
        method is called during black's turn, then white win, else
        black wins.
        """

        if self._turn == 'black':
            self._game_state = 'WHITE_WON'

        else:
            self._game_state = 'BLACK_WON'


    def display_board(self):
        """ Displays the board for debugging purposes"""
        line_number = 20
        for row in reversed(self._board):
            print(str(row) + ' ' + str(line_number))
            line_number -= 1

        print('  a  ', ' b  ', ' c  ', ' d  ', ' e  ', \
              ' f  ', ' g  ', ' h  ', ' i  ', ' j  ', ' k  ' \
              , ' l  ', ' m  ', ' n  ', ' o  ', ' p  ', \
              ' q  ', ' r  ', ' s  ', ' t  ')

    def make_move(self, source, destination):
        """
        This method takes in the parameter of a source and destination
        which are strings. This method converts the string to numbers by using
        a dictionary. It then does validations to make sure it is a valid
        move. Validations include checking for out of range moves,
        invalid keys, and incorrect formatting of parameters. It
        then looks at whose turn it and then moves accordingly
        depending if there is a center piece or not. This is because
        a center piece would mean that they can move any unobstructed
        direction if there is a piece in that footprint towards that
        direction. While a no center piece means they can only move
        in 3 direction. It moves accordingly by comparing the
        source footprint with the destination footprint. It uses
        ranges to make sure it moves in the correct range. It calls
        several different methods such as check_source_footprint,
        check_suicide, and move_footprint. It uses all those methods
        to make sure we get a valid move. After the move passes
        validation, the move_footprint is where it updates
        the board and check for winner and returns the true or
        false for this method.
        """

        letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
                   'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
                   'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14,
                   'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19}

        str_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        # to check if the game still continues
        if self._game_state != 'UNFINISHED':
            return False

        # invalid string length. string length can only be size 2 or 3
        if len(source) > 3 or len(destination) > 3:
            return False
        if len(source) < 2 or len(destination) < 2:
            return False

        # not a valid number or letter (letters and special symbols checker)
        for char in source:
            if char not in letters and char not in str_numbers:
                return False

        # Convert the column letters into numbers
        if source[0] in letters:
            col_source = letters[source[0]]
        if destination[0] in letters:
            col_destination = letters[destination[0]]

        # checking source that has has 1 digit. (e.g.  'a5')
        if len(source) == 2:
            if int(source[-1]) not in range(1, 10):  # if not a digit
                return False
            row_source = int(source[-1]) - 1  # store the source row as an int

        # checking destination that has 1 digit
        if len(destination) == 2:
            if int(destination[-1]) not in range(1, 10):  # if not a digit
                return False
            row_destination = int(destination[-1]) - 1  # store the destination row as an int

        # checking sources that input two digits (eg. 'a15')
        if len(source) == 3:
            if int(source[1:3]) not in range(1, 21):  # not a number in 1-20
                return False
            row_source = int(source[1:3]) - 1  # store the source row  as an int

        # checking destination that inputs with two digits
        if len(destination) == 3:
            if int(destination[1:3]) not in range(1, 21):
                return False
            row_destination = int(destination[1:3]) - 1  # store the destination row as an int

        # out of bounds move not allowed
        if row_source <= 0 or col_source <= 0:
            return False
        if row_source >= 20 or col_source >= 20:
            return False
        if row_destination <= 0 or col_destination <= 0:
            return False
        if row_destination >= 20 or col_destination >= 20:
            return False

        self.check_suicide(row_source, col_source)  # check for suicide at it's source
        if self._suicide == 0:
            return False
        self._suicide = 0       # reset suicide for future loops

        self.check_suicide(row_destination, col_destination) # check for suicide at it's destination
        if self._suicide == 0:
            return False
        self._suicide = 0

        self.find_source_footprint(row_source, col_source)  # finds the source foot print

        row_diff = abs(row_destination - row_source)
        col_diff = abs(col_destination - col_source)

        # black piece turn
        if self._turn == 'black':

            # in case there is a white piece in the footprint
            for piece in self._source_foot_print:
                if piece == 'w':
                    return False

            # if center piece is empty
            if self._board[row_source][col_source] == '_':

                # moving diagonal up-left
                if self._board[row_source + 1][col_source - 1] == 'b':
                    for num in range(1, 4):

                        # the source and destination is within range and allowed
                        if row_source + num == row_destination and col_source - num == col_destination:

                            # check to see if there is an unobstructed path
                            # it starts at 2 since the first empty box is two spaces away
                            # (pos - 2) is so that it moves diagonal accordingly
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source + pos][col_source - i - (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source + i + (pos - 2)][col_source - pos] != '_':
                                        self._unobstructed_path += 1

                            # move the footprint
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                #  !! THE PATTERN WILL CONTINUE FOR A WHILE !! It's the same logic as  the one above

                # moving up
                if self._board[row_source + 1][col_source] == 'b':
                    for num in range(1, 4):
                        if row_source + num == row_destination and col_source == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source + pos][col_source - 1 + i] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving diagonal up-right
                if self._board[row_source + 1][col_source + 1] == 'b':
                    for num in range(1, 4):
                       if row_source + num == row_destination and col_source + num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source + pos][col_source + i + (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source + i + (pos - 2)][col_source + pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving left
                if self._board[row_source][col_source - 1] == 'b':
                    for num in range(1, 4):
                       if row_source == row_destination and col_source - num == col_destination:
                            for pos in range(2, col_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - 1 + i][col_source - pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving right
                if self._board[row_source][col_source + 1] == 'b':
                    for num in range(1, 4):
                        if row_source == row_destination and col_source + num == col_destination:
                            for pos in range(2, col_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - 1 + i][col_source + pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving diagonal bottom-left
                if self._board[row_source - 1][col_source - 1] == 'b':
                    for num in range(1, 4):
                        if row_source - num == row_destination and col_source - num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - pos][col_source - i - (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source - i - (pos - 2)][col_source - pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving bottom
                if self._board[row_source - 1][col_source] == 'b':
                    for num in range(1, 4):
                        if row_source - num == row_destination and col_source == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - pos][col_source - 1 + i] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving diagonal bottom right
                if self._board[row_source - 1][col_source + 1] == 'b':
                    for num in range(1, 4):
                        if row_source - num == row_destination and col_source + num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - pos][col_source + i + (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source - i - (pos - 2)][col_source + pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

            # if the center piece is there
            elif self._board[row_source][col_source] == 'b':

                # moving diagonal up left
                if self._board[row_source + 1][col_source - 1] == 'b':
                    for num in range(1, row_diff + 1):
                        if row_source + num > 19 or col_source - num < 0:
                            continue
                        elif row_source + num == row_destination and col_source - num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source + pos][col_source - (pos - 2) - i] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source + i + (pos - 2)][col_source - pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving up
                if self._board[row_source + 1][col_source] == 'b':
                    for num in range(1, row_diff + 1):
                        if row_source + num == row_destination and col_source == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source + pos][col_source - 1 + i] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving diagonal up-right
                if self._board[row_source + 1][col_source + 1] == 'b':
                    for num in range(1, row_diff + 1):
                        if row_source + num == row_destination and col_source + num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source + pos][col_source + i + (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source + i + (pos - 2)][col_source + pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving left
                if self._board[row_source][col_source - 1] == 'b':
                    for num in range(1, col_diff + 1):
                       if row_source == row_destination and col_source - num == col_destination:
                            for pos in range(2, col_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - 1 + i][col_source - pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving right
                if self._board[row_source][col_source + 1] == 'b':
                    for num in range(1, col_diff + 1):
                       if row_source == row_destination and col_source + num == col_destination:
                            for pos in range(2, col_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - 1 + i][col_source + pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving diagonal bottom-left
                if self._board[row_source - 1][col_source - 1] == 'b':
                    for num in range(1, row_diff + 1):
                       if row_source - num == row_destination and col_source - num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - pos][col_source - i - (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source - i - (pos - 2)][col_source - pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving bottom
                if self._board[row_source - 1][col_source] == 'b':
                    for num in range(1, row_diff + 1):
                        if row_source - num == row_destination and col_source == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - pos][col_source - 1 + i] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving diagonal  bottom right
                if self._board[row_source - 1][col_source + 1] == 'b':
                    for num in range(1, row_diff + 1):
                       if row_source - num == row_destination and col_source + num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - pos][col_source + i + (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source - i - (pos - 2)][col_source + pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

        # white piece turn
        if self._turn == 'white':

            # in case there is a black piece in the footprint
            for piece in self._source_foot_print:
                if piece == 'b':
                    return False

            # if center piece is empty
            if self._board[row_source][col_source] == '_':

                # moving diagonal up-left
                if self._board[row_source + 1][col_source - 1] == 'w':
                    for num in range(1, 4):
                        if row_source + num == row_destination and col_source - num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source + pos][col_source - (pos - 2) - i] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source + i + (pos - 2)][col_source - pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving up
                if self._board[row_source + 1][col_source] == 'w':
                    for num in range(1, 4):
                        if row_source + num == row_destination and col_source == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source + pos][col_source - 1 + i] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving diagonal up-right
                if self._board[row_source + 1][col_source + 1] == 'w':
                    for num in range(1, 4):
                        if row_source + num == row_destination and col_source + num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source + pos][col_source + i + (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source + i + (pos - 2)][col_source + pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving left
                if self._board[row_source][col_source - 1] == 'w':
                    for num in range(1, 4):
                        if row_source == row_destination and col_source - num == col_destination:
                            for pos in range(2, col_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - 1 + i][col_source - pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving right
                if self._board[row_source][col_source + 1] == 'w':
                    for num in range(1, 4):
                        if row_source == row_destination and col_source + num == col_destination:
                            for pos in range(2, col_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - 1 + i][col_source + pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving diagonal bottom-left
                if self._board[row_source - 1][col_source - 1] == 'w':
                    for num in range(1, 4):
                        if row_source - num == row_destination and col_source - num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - pos][col_source - i - (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source - i - (pos - 2)][col_source - pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving bottom
                if self._board[row_source - 1][col_source] == 'w':
                    for num in range(1, 4):
                        if row_source - num == row_destination and col_source == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - pos][col_source - 1 + i] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving bottom right
                if self._board[row_source - 1][col_source + 1] == 'w':
                    for num in range(1, 4):
                        if row_source - num == row_destination and col_source + num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - pos][col_source + i + (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source - i - (pos - 2)][col_source + pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

            # if the center piece is not empty
            elif self._board[row_source][col_source] == 'w':

                # moving diagonal left
                if self._board[row_source + 1][col_source - 1] == 'w':
                    for num in range(1, row_diff + 1):
                        if row_source + num == row_destination and col_source - num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source + pos][col_source - (pos - 2) - i] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source + i + (pos - 2)][col_source - pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving up
                if self._board[row_source + 1][col_source] == 'w':
                    for num in range(1, row_diff + 1):
                        if row_source + num == row_destination and col_source == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source + pos][col_source - 1 + i] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving diagonal up-right
                if self._board[row_source + 1][col_source + 1] == 'w':
                    for num in range(1, row_diff + 1):
                        if row_source + num == row_destination and col_source + num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source + pos][col_source + i + (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source + i + (pos - 2)][col_source + pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving left
                if self._board[row_source][col_source - 1] == 'w':
                    for num in range(1, col_diff + 1):
                        if row_source == row_destination and col_source - num == col_destination:
                            for pos in range(2, col_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - 1 + i][col_source - pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving right
                if self._board[row_source][col_source + 1] == 'w':
                    for num in range(1, col_diff + 1):
                        if row_source == row_destination and col_source + num == col_destination:
                            for pos in range(2, col_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - 1 + i][col_source + pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving diagonal bottom-left
                if self._board[row_source - 1][col_source - 1] == 'w':
                    for num in range(1, row_diff + 1):
                        if row_source - num == row_destination and col_source - num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - pos][col_source - i - (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source - i - (pos - 2)][col_source - pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving bottom
                if self._board[row_source - 1][col_source] == 'w':
                    for num in range(1, row_diff + 1):
                        if row_source - num == row_destination and col_source == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - pos][col_source - 1 + i] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

                # moving bottom right
                if self._board[row_source - 1][col_source + 1] == 'w':
                    for num in range(1, row_diff + 1):
                        if row_source - num == row_destination and col_source + num == col_destination:
                            for pos in range(2, row_diff + 1):
                                for i in range(3):
                                    if self._board[row_source - pos][col_source + i + (pos - 2)] != '_':
                                        self._unobstructed_path += 1
                                    if self._board[row_source - i - (pos - 2)][col_source + pos] != '_':
                                        self._unobstructed_path += 1
                            return self.move_footprint(row_source, col_source, row_destination, col_destination)

    def find_source_footprint(self, row_source, col_source):
        """
        Finds the source footprint and adds it to a list. This method is called from the
        make_move method and is necessary so that I can compare the range for
        the source footprint to the destination footprint
        """

        self._source_foot_print = []  # clear footprint every time this is called

        # iterate to add each position of the footprint into a list
        for num in range(3):
            self._source_foot_print.append(self._board[row_source + 1][col_source - 1 + num])
            self._source_foot_print.append(self._board[row_source][col_source - 1 + num])
            self._source_foot_print.append(self._board[row_source - 1][col_source - 1 + num])

    def check_suicide(self, row_source, col_source):
        """
        Checks for suicide by temporarily removing the footprint of the source
        and then iterating through the board to see if there is a ring. It there is no
        ring, self._suicide will increase. It then restores the board back to original.
        This method is called from the make_move and is set as a condition before a
        move can be made since all move must be valid before they can move.
        """

        # check if the ring exist depending on player
        if self._turn == 'black':
            player = 'b'
        else:
            player = 'w'

        # if moving the whole ring, you can't suicide
        if self._board[row_source][col_source] == '_':
            if self._board[row_source + 1][col_source - 1] == player and self._board[row_source + 1][col_source] == player \
                    and self._board[row_source + 1][col_source + 1] == player and self._board[row_source][col_source - 1] == player \
                    and self._board[row_source][col_source + 1] == player and self._board[row_source - 1][col_source - 1] == player \
                    and self._board[row_source - 1][col_source] == player and self._board[row_source - 1][col_source + 1] == player:
                self._suicide = 1
                return False

        # save the old positions
        pos_1 = self._board[row_source + 1][col_source-1]
        pos_2 = self._board[row_source + 1][col_source]
        pos_3 = self._board[row_source + 1][col_source + 1]
        pos_4 = self._board[row_source][col_source - 1]
        pos_5 = self._board[row_source][col_source + 1]
        pos_6 = self._board[row_source - 1][col_source - 1]
        pos_7 = self._board[row_source - 1][col_source]
        pos_8 = self._board[row_source - 1][col_source+1]
        pos_9 = self._board[row_source][col_source]

        # temporarily clear the positions
        self._board[row_source + 1][col_source-1] = '_'
        self._board[row_source + 1][col_source] = '_'
        self._board[row_source + 1][col_source + 1] = '_'
        self._board[row_source][col_source - 1] = '_'
        self._board[row_source][col_source + 1] = '_'
        self._board[row_source - 1][col_source - 1] = '_'
        self._board[row_source - 1][col_source] = '_'
        self._board[row_source - 1][col_source + 1] = '_'
        self._board[row_source][col_source] = '_'

        # iterate through whole board to see if a ring exist
        for row in range(1, 19):
            for col in range(1, 19):
                if self._board[row][col] == '_':
                    if self._board[row + 1][col - 1] == player and self._board[row + 1][col] == player \
                            and self._board[row + 1][col + 1] == player and self._board[row][col - 1] == player \
                            and self._board[row][col + 1] == player and self._board[row - 1][col - 1] == player \
                            and self._board[row - 1][col] == player and self._board[row - 1][col + 1] == player:
                        self._suicide += 1  # ring found

        # restore the old board
        self._board[row_source + 1][col_source-1] = pos_1
        self._board[row_source + 1][col_source] = pos_2
        self._board[row_source + 1][col_source + 1] = pos_3
        self._board[row_source][col_source - 1] = pos_4
        self._board[row_source][col_source + 1] = pos_5
        self._board[row_source - 1][col_source - 1] = pos_6
        self._board[row_source - 1][col_source] = pos_7
        self._board[row_source - 1][col_source + 1] = pos_8
        self._board[row_source][col_source] = pos_9

    def check_winner(self):
        """
        Checks for winner by iterating through the whole board. Checks to see if
        the opposite player still has a ring. Since the user can't suicide, the program
        only needs to check opposite player
        """

        if self._turn == 'black':
            piece = 'w'
        elif self._turn == 'white':
            piece = 'b'

        # iterating through the board that is not included the edge cases
        for row in range(1, 19):
            for col in range(1, 19):
                if self._board[row][col] == '_':

                    # If there is a ring
                    if self._board[row + 1][col - 1] == piece and self._board[row + 1][col] == piece \
                            and self._board[row + 1][col + 1] == piece and self._board[row][col - 1] == piece \
                            and self._board[row][col + 1] == piece and self._board[row - 1][col - 1] == piece \
                            and self._board[row - 1][col] == piece and self._board[row - 1][col + 1] == piece:
                        return True

        # if no ring is found from other player's piece, the one hwo just made the turn wins
        if self._turn == 'black':
            self._game_state = 'BLACK_WON'
        else:
            self._game_state = 'WHITE_WON'

    def move_footprint(self, row_source, col_source, row_destination, col_destination):
        """
        Moves the source foot print to the destination footprint if there
        is not an unobstructed path. It then changes turn if move is successful
        This is called from the make_move method and recieve a variable to
        see if there was an unobstructed path. Also this recieves the list from
        the find_source_footprint method that saved the source footprint in a list.
        The move is made by clearing the old source footprint and then adding
        it to the new destination. It then calls the check_winner method to
        check for winner and then changes turns after every successful move.
        """

        # can't move footprint if there is an unobstructive path
        if self._unobstructed_path > 0:
            self._unobstructed_path = 0  # reset for future loops
            return False

        # clear old source footprint
        for num in range(3):
            self._board[row_source + -1 + num][col_source - 1] = '_'
            self._board[row_source + -1 + num][col_source] = '_'
            self._board[row_source + -1 + num][col_source + 1] = '_'

        # creates the new footprint at the destination
        for num in range(3):
            self._board[row_destination + 1 - num][col_destination - 1] = self._source_foot_print[num]
        for num in range(3):
            self._board[row_destination + 1 - num][col_destination] = self._source_foot_print[num + 3]
        for num in range(3):
            self._board[row_destination + 1 - num][col_destination + 1] = self._source_foot_print[num + 6]

        # edge pieces are removed at the end of the move
        for num in range(20):
            self._board[0][num] = '_'
            self._board[19][num] = '_'
            self._board[num][0] = '_'
            self._board[num][19] = '_'

        # check for winner
        self.check_winner()

        # change turns
        if self._turn == 'black':
            self._turn = 'white'
        else:
            self._turn = 'black'

        return True


if __name__ == "__main__":
    game = GessGame()
    print(game.make_move('j3', 'j4'))          # should be false. it messes up own ring
    print(game.make_move('i3', 'i6'))          # black moves up with center piece
    print(game.make_move('i18', 'i15'))        # white moves down
    print(game.make_move('l3', 'l6'))            # ring piece moves up
    print(game.make_move('i15', 'e11'))         # diagonal bottom left false move. path block
    print(game.make_move('i15', 'k13'))         # diagonal bottom right
    print(game.make_move('i6', 'd11'))          # moving diagonla right false. path block
    print(game.make_move('i6', 'g8'))           # moving diagonal up left
    print(game.make_move('k13', 'k8'))          # moving down to ring piece
    print(game.get_game_state())                # white should win
    print(game.make_move('c3', 'c4'))           # can't move after someone wins
    # print(game.make_move('m3', 'm6'))
    # print(game.make_move('k18', 'k7'))

    game.display_board()

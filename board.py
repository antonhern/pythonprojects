class Board:
    def __init__(self):
        # board is a list of cells that are represented
        # by strings (" ", "O", and "X")
        # initially it is made of empty cells represented
        # by " " strings
        self.sign = " "
        self.size = 3
        self.board = list(self.sign * self.size ** 2)
        # the winner's sign O or X
        self.winner = ""

    def getSign(self, cell):
        valid_choices = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
        index = valid_choices.index(cell)
        return self.board[index]

    def get_size(self):
        return self.size

    def get_winner(self):
        return self.winner

    def set(self, cell, sign):
        # mark the cell on the board with the sign X or O
        valid_choices = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
        index = valid_choices.index(cell)
        self.board[index] = sign

    def isempty(self, cell):
        valid_choices = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
        index = valid_choices.index(cell)
        for i in self.board:
            for j in self.board:
                if self.board[index] == " ":
                    return True
                else:
                    return False
        # return True if the cell is empty (not marked with X or O)

    def isdone(self):
        done = False
        if " " not in self.board:
            done = True
            self.winner = ""
        for i in range(0, 7, 3):
            if self.board[i] == self.board[i + 1] == self.board[i + 2] != " ":
                done = True
                self.winner = self.board[i]
        for i in range(0, 3, 1):
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != " ":
                done = True
                self.winner = self.board[i]
        if self.board[0] == self.board[4] == self.board[8] != " ":
            done = True
            self.winner = self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != " ":
            done = True
            self.winner = self.board[4]
        return done
        # check all game terminating conditions, if one of them is present, assign the
        # var done to True
        # depending on conditions assign the instance var winner to O or X

    def show(self):
        # draw the board
        # need to complete the code
        print('\n A B C')
        print(' +---+---+---+')
        print('1| {} | {} | {} |'.format(self.board[0], self.board[1], self.board[2]))
        print(' +---+---+---+')
        print('2| {} | {} | {} |'.format(self.board[3], self.board[4], self.board[5]))
        print(' +---+---+---+')
        print('3| {} | {} | {} |'.format(self.board[6], self.board[7], self.board[8]))
        print(' +---+---+---+')

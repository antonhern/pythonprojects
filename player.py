from random import choice
from math import inf

class Player:
    def __init__(self, name, sign):
        self.name = name  # player's name
        self.sign = sign  # player's sign O or X

    def get_sign(self):
        return self.sign
        # return an instance sign

    def get_name(self):
        return self.name
        # return an instance name

    def choose(self, board):
        # prompt the user to choose a cell
        # if the user enters a valid string and the cell on the board is empty, update the board
        # otherwise print a message that the input is wrong and rewrite the prompt
        # use the methods board.isempty(cell), and board.set(cell, sign)
        valid_choices = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
        while True:
            cell = input(f'{self.name}, {self.sign}: Enter a cell [A-C][1-3]:').upper()
            if cell in valid_choices:
                if board.isempty(cell):
                    board.set(cell, self.sign)
                    break
                else:
                    print("\nYou did not choose correctly.")
            else:
                print("\nNot Valid Input.")

class AI(Player):
    def __init__(self, name, sign, board):
        super().__init__(name, sign)
        self.board = board

    def choose(self, board):
        valid_choices = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
        x = choice(valid_choices)
        if self.board.isempty(x):
            board.set(x, self.sign)

class SmartAI(AI):
    def choose(self, board):
        best_choice = self.wins()
        board.set(best_choice, self.sign)

    def wins(self):
        valid_choices = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
        sign = self.sign
        if sign == 'X':
            op_sign = 'O'
        else:
            op_sign = 'X'
        for i in valid_choices:
            if self.board.isempty(i):
                self.board.set(i, self.sign)
                if self.board.isdone():
                    move = i
                    self.board.winner = ''
                    self.board.set(i, ' ')
                    return move
                else:
                    self.board.set(i, ' ')
        for i in valid_choices:
            if self.board.isempty(i):
                self.board.set(i, op_sign)
                if self.board.isdone():
                    move = i
                    self.board.winner = ''
                    self.board.set(i, ' ')
                    return move
                else:
                    self.board.set(i, ' ')
        if self.board.isempty('B2'):
            move = 'B2'
            return move
        cornersOpen = []
        for i in valid_choices:
            if i in ['A1', 'C1', 'A3', 'C3']:
                if self.board.isempty(i):
                    cornersOpen.append(i)
        y = choice(cornersOpen)
        if self.board.isempty(y):
            move = y
            return move
        edgesOpen = []
        for i in valid_choices:
            if i in ['B1', 'A2', 'C2', 'B3']:
                if self.board.isempty(i):
                    edgesOpen.append(i)
        y = choice(edgesOpen)
        if self.board.isempty(y):
            move = y
            return move

class MiniMax(SmartAI):
    def choose(self, board):
        print(f"\n{self.name}, {self.name}: Enter a cell [A-C][1-3]: ")
        cell = MiniMax.minimax(self, board, True, True)
        print(cell)
        board.set(cell, self.sign)

    def minimax(self, board, self_player, start):
        if self.sign == 'X':
            op_sign = 'O'
        else:
            op_sign = 'X'
            self.sign = 'O'
        if self.board.isdone():
            if self.board.get_winner() == self.sign:
                return 1
            elif self.board.get_winner() == op_sign:
                return -1
            else:
                return 0
        minscore = inf
        maxscore = -inf
        valid_choices = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
        best_moves = []
        for i in valid_choices:
            if self.board.isempty(i):
                if self_player:
                    board.set(i, self.sign)
                    score = MiniMax.minimax(self, board, False, False)
                    if score > maxscore:
                        maxscore = score
                        best_moves.append(i)
                    board.set(i, " ")
                else:
                    board.set(i, op_sign)
                    score = MiniMax.minimax(self, board, True, False)
                    if score < minscore:
                        minscore = score
                        best_moves.append(i)
                    board.set(i, " ")
        if start:
            return best_moves[-1]
        elif self_player:
            return maxscore
        else:
            return minscore

from time import sleep
import math
from math import inf
from random import randint

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score = 0
        if isMax:
            if self.checkWinner() == 1:
                return self.winnerMaxUtility
            else:
                score = self.evaluatePredifined_helper_attack(isMax) * self.twoInARowMaxUtility + \
                        self.evaluatePredifined_helper_defense(isMax) * self.preventThreeInARowMaxUtility
                if score == 0:
                    score = self.evaluatePredifined_helper_corner(isMax) * self.cornerMaxUtility
        else:
            if self.checkWinner() == -1:
                return self.winnerMinUtility
            else:
                score = self.evaluatePredifined_helper_attack(isMax) * self.twoInARowMinUtility + \
                        self.evaluatePredifined_helper_defense(isMax) * self.preventThreeInARowMinUtility
                if score == 0:
                    score = self.evaluatePredifined_helper_corner(isMax) * self.cornerMinUtility
        return score

    def evaluatePredifined_helper_attack(self, isMax):
        # Helper defined by Peilin Rao
        # For each local board, count the number of two-in-a-row without the third spot
        # taken by the opposing player (unblocked two-in-a-row).
        count = 0
        my_char = 'O'
        if isMax:
            my_char = 'X'
        for index in self.globalIdx:
            local_board = [['_', '_', '_'],['_', '_', '_'],['_', '_', '_']]
            # Hard coding the situation of board
            for i in range(0, 3):
                for j in range(0, 3):
                    local_board[i][j] = self.board[index[0]+i][index[1]+j]
            if (local_board[0][0] == my_char and local_board[0][1] == my_char and local_board[0][2] == '_') \
                    or (local_board[0][0] == my_char and local_board[0][1] == '_' and local_board[0][2] == my_char) \
                    or (local_board[0][0] == '_' and local_board[0][1] == my_char and local_board[0][2] == my_char):
                count += 1
            if(local_board[1][0] == my_char and local_board[1][1] == my_char and local_board[1][2] == '_') \
                    or (local_board[1][0] == my_char and local_board[1][1] == '_' and local_board[1][2] == my_char) \
                    or (local_board[1][0] == '_' and local_board[1][1] == my_char and local_board[1][2] == my_char):
                count += 1
            if(local_board[2][0] == my_char and local_board[2][1] == my_char and local_board[2][2] == '_') \
                    or (local_board[2][0] == my_char and local_board[2][1] == '_' and local_board[2][2] == my_char) \
                    or (local_board[2][0] == '_' and local_board[2][1] == my_char and local_board[2][2] == my_char):
                count += 1
            if(local_board[0][0] == my_char and local_board[1][0] == my_char and local_board[2][0] == '_') \
                    or (local_board[0][0] == my_char and local_board[1][0] == '_' and local_board[2][0] == my_char) \
                    or (local_board[0][0] == '_' and local_board[1][0] == my_char and local_board[2][0] == my_char):
                count += 1
            if(local_board[0][1] == my_char and local_board[1][1] == my_char and local_board[2][1] == '_') \
                    or (local_board[0][1] == my_char and local_board[1][1] == '_' and local_board[2][1] == my_char) \
                    or (local_board[0][1] == '_' and local_board[1][1] == my_char and local_board[2][1] == my_char):
                count += 1
            if(local_board[0][2] == my_char and local_board[1][2] == my_char and local_board[2][2] == '_') \
                    or (local_board[0][2] == my_char and local_board[1][2] == '_' and local_board[2][2] == my_char) \
                    or (local_board[0][2] == '_' and local_board[1][2] == my_char and local_board[2][2] == my_char):
                count += 1
            if(local_board[0][0] == my_char and local_board[1][1] == my_char and local_board[2][2] == '_') \
                    or (local_board[0][0] == my_char and local_board[1][1] == '_' and local_board[2][2] == my_char) \
                    or (local_board[0][0] == '_' and local_board[1][1] == my_char and local_board[2][2] == my_char):
                count += 1
            if(local_board[0][2] == my_char and local_board[1][1] == my_char and local_board[2][0] == '_') \
                    or (local_board[0][2] == my_char and local_board[1][1] == '_' and local_board[2][0] == my_char) \
                    or (local_board[0][2] == '_' and local_board[1][1] == my_char and local_board[2][0] == my_char):
                count += 1
        return count
    def evaluatePredifined_helper_defense(self, isMax):
        # Helper defined by Peilin Rao
        # For each local board, count the number of places in which you have prevented
        # the opponent player forming two-in-a-row (two-in-a-row of opponent player but with the third spot taken by offensive agent).
        count = 0
        my_char = 'X'
        player_char = 'O'
        if isMax:
            my_char = 'O'
            player_char = 'X'
        for index in self.globalIdx:
            # Hard coding the situation of board
            local_board = [['_', '_', '_'],['_', '_', '_'],['_', '_', '_']]
            for i in range(0, 3):
                for j in range(0, 3):
                    local_board[i][j] = self.board[index[0]+i][index[1]+j]
            if (local_board[0][0] == my_char and local_board[0][1] == my_char and local_board[0][2] == player_char) \
                    or (local_board[0][0] == my_char and local_board[0][1] == player_char and local_board[0][2] == my_char) \
                    or (local_board[0][0] == player_char and local_board[0][1] == my_char and local_board[0][2] == my_char):
                count += 1
            if(local_board[1][0] == my_char and local_board[1][1] == my_char and local_board[1][2] == player_char) \
                    or (local_board[1][0] == my_char and local_board[1][1] == player_char and local_board[1][2] == my_char) \
                    or (local_board[1][0] == player_char and local_board[1][1] == my_char and local_board[1][2] == my_char):
                count += 1
            if(local_board[2][0] == my_char and local_board[2][1] == my_char and local_board[2][2] == player_char) \
                    or (local_board[2][0] == my_char and local_board[2][1] == player_char and local_board[2][2] == my_char) \
                    or (local_board[2][0] == player_char and local_board[2][1] == my_char and local_board[2][2] == my_char):
                count += 1
            if(local_board[0][0] == my_char and local_board[1][0] == my_char and local_board[2][0] == player_char) \
                    or (local_board[0][0] == my_char and local_board[1][0] == player_char and local_board[2][0] == my_char) \
                    or (local_board[0][0] == player_char and local_board[1][0] == my_char and local_board[2][0] == my_char):
                count += 1
            if(local_board[0][1] == my_char and local_board[1][1] == my_char and local_board[2][1] == player_char) \
                    or (local_board[0][1] == my_char and local_board[1][1] == player_char and local_board[2][1] == my_char) \
                    or (local_board[0][1] == player_char and local_board[1][1] == my_char and local_board[2][1] == my_char):
                count += 1
            if(local_board[0][2] == my_char and local_board[1][2] == my_char and local_board[2][2] == player_char) \
                    or (local_board[0][2] == my_char and local_board[1][2] == player_char and local_board[2][2] == my_char) \
                    or (local_board[0][2] == player_char and local_board[1][2] == my_char and local_board[2][2] == my_char):
                count += 1
            if(local_board[0][0] == my_char and local_board[1][1] == my_char and local_board[2][2] == player_char) \
                    or (local_board[0][0] == my_char and local_board[1][1] == player_char and local_board[2][2] == my_char) \
                    or (local_board[0][0] == player_char and local_board[1][1] == my_char and local_board[2][2] == my_char):
                count += 1
            if(local_board[0][2] == my_char and local_board[1][1] == my_char and local_board[2][0] == player_char) \
                    or (local_board[0][2] == my_char and local_board[1][1] == player_char and local_board[2][0] == my_char) \
                    or (local_board[0][2] == player_char and local_board[1][1] == my_char and local_board[2][0] == my_char):
                count += 1
        return count
    def evaluatePredifined_helper_corner(self, isMax):
        # Helper defined by Peilin Rao
        # Rule 3
        count = 0
        my_char = 'O'
        op_char = 'X'
        if isMax:
            my_char = 'X'
            op_char = 'O'
        for index in self.globalIdx:
            local_board = [['_', '_', '_'],['_', '_', '_'],['_', '_', '_']]
            for i in range(0, 3):
                for j in range(0, 3):
                    local_board[i][j] = self.board[index[0]+i][index[1]+j]
            # Check if the corners are filled
            if local_board[0][0] == my_char or local_board[0][2] == my_char \
            or local_board[2][0] == my_char or local_board[2][2] == my_char:
                    count += 1
        return count

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score = 0
        if isMax:
            if self.checkWinner() == -1:
                return -100000
            if self.checkWinner() == 1:
                return self.winnerMaxUtility
            else:
                score = self.evaluatePredifined_helper_attack(isMax) * self.twoInARowMaxUtility + \
                        self.evaluatePredifined_helper_defense(isMax) * self.preventThreeInARowMaxUtility
                if score == 0:
                    score = self.evaluatePredifined_helper_corner(isMax) * self.cornerMaxUtility
        else:
            if self.checkWinner() == 1:
                return +100000
            if self.checkWinner() == -1:
                return self.winnerMinUtility
            else:
                score = self.evaluatePredifined_helper_attack(isMax) * self.twoInARowMinUtility + \
                        self.evaluatePredifined_helper_defense(isMax) * self.preventThreeInARowMinUtility
                if score == 0:
                    score = self.evaluatePredifined_helper_corner(isMax) * self.cornerMinUtility
        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        for i in range(0,9):
            for j in range(0,9):
                if self.board[i][j] == '_':
                    return True
        return False

    def is_terminal_node(self, currBoardIdx):
        """
        Check if there is any available moves in the local TTT (3*3)

        :param currBoardIdx:
        :return: True if it is terminal node
        """
        index = self.globalIdx[currBoardIdx]
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[i][j] == '_':
                    return False
        return True

    def get_possible_moves(self, currBoardIdx):
        """
        Check if there is any available moves in the local TTT (3*3)

        :param currBoardIdx:
        :return: A list of possible moves
        """
        list_of_possible_moves = []
        index = self.globalIdx[currBoardIdx]
        for i in range(index[0],index[0]+3):
            for j in range(index[1],index[1]+3):
                if self.board[i][j] == '_':
                    list_of_possible_moves.append([i, j])
        return list_of_possible_moves

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer(X) is the winner.
                     Return -1 if miniPlayer(O) is the winner.
        """
        #YOUR CODE HERE
        for index in self.globalIdx:
            local_board = [['_', '_', '_'],['_', '_', '_'],['_', '_', '_']]
            for i in range(0, 3):
                for j in range(0, 3):
                    local_board[i][j] = self.board[index[0]+i][index[1]+j]
            if (local_board[0][0] == 'X' and local_board[0][1] == 'X' and local_board[0][2] == 'X')\
                    or (local_board[1][0] == 'X' and local_board[1][1] == 'X' and local_board[1][2] == 'X') \
                    or (local_board[2][0] == 'X' and local_board[2][1] == 'X' and local_board[2][2] == 'X') \
                    or (local_board[0][0] == 'X' and local_board[1][0] == 'X' and local_board[2][0] == 'X') \
                    or (local_board[0][1] == 'X' and local_board[1][1] == 'X' and local_board[2][1] == 'X') \
                    or (local_board[0][2] == 'X' and local_board[1][2] == 'X' and local_board[2][2] == 'X') \
                    or (local_board[0][0] == 'X' and local_board[1][1] == 'X' and local_board[2][2] == 'X') \
                    or (local_board[0][2] == 'X' and local_board[1][1] == 'X' and local_board[2][0] == 'X'):
                return 1
            elif (local_board[0][0] == 'O' and local_board[0][1] == 'O' and local_board[0][2] == 'O') \
                    or (local_board[1][0] == 'O' and local_board[1][1] == 'O' and local_board[1][2] == 'O') \
                    or (local_board[2][0] == 'O' and local_board[2][1] == 'O' and local_board[2][2] == 'O') \
                    or (local_board[0][0] == 'O' and local_board[1][0] == 'O' and local_board[2][0] == 'O') \
                    or (local_board[0][1] == 'O' and local_board[1][1] == 'O' and local_board[2][1] == 'O') \
                    or (local_board[0][2] == 'O' and local_board[1][2] == 'O' and local_board[2][2] == 'O') \
                    or (local_board[0][0] == 'O' and local_board[1][1] == 'O' and local_board[2][2] == 'O') \
                    or (local_board[0][2] == 'O' and local_board[1][1] == 'O' and local_board[2][0] == 'O'):
                return -1
        return 0

    def alphabeta(self,depth,currBoardIdx,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        # A the first time the function is called, alpha == -inf and beta == inf
        return alphabeta_max(self, depth, currBoardIdx, -inf, inf, isMax)

    def alphabeta_helper(self, depth, currBoardIdx, alpha, beta, isMax):
        if depth == 0 or self.is_terminal_node(currBoardIdx) == True:
            return self.evaluatePredifined(not isMax)
        if isMax:
            # X is making the move
            value = -(inf)
            move_list = self.get_possible_moves(currBoardIdx)
            for new_moves in move_list:
                temp = ultimateTicTacToe()
                for i in range(0,9):
                    for j in range(0,9):
                        temp.board[i][j] = self.board[i][j]
                temp.board[new_moves[0]][new_moves[1]] = 'X'
                self.expandedNodes+=1
                currBoardIdx_new = self.local_to_global(new_moves)
                value_store = value;
                value = max(value, temp.alphabeta_helper(depth-1, currBoardIdx_new, alpha, beta, not isMax))
                if value != value_store:
                    self.expandedNodes += temp.expandedNodes
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        else:
            # O is making the move
            value = inf
            move_list = self.get_possible_moves(currBoardIdx)
            for new_moves in move_list:
                temp = ultimateTicTacToe()
                for i in range(0,9):
                    for j in range(0,9):
                        temp.board[i][j] = self.board[i][j]
                temp.board[new_moves[0]][new_moves[1]] = 'O'
                self.expandedNodes+=1
                currBoardIdx_new = self.local_to_global(new_moves)
                value_store = value;
                value = min(value, temp.alphabeta_helper(depth-1, currBoardIdx_new, alpha, beta, not isMax))
                if value != value_store:
                    self.expandedNodes += temp.expandedNodes
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return value

    def alphabeta_tracking_helper(self, depth, currBoardIdx, alpha, beta, isMax, path):
        if depth == 0 or self.is_terminal_node(currBoardIdx) == True:
            return (self.evaluatePredifined(not isMax),path.copy())
        if isMax:
            # X is making the move
            value = -(inf)
            move_list = self.get_possible_moves(currBoardIdx)
            for new_moves in move_list:
                temp = ultimateTicTacToe()
                for i in range(0,9):
                    for j in range(0,9):
                        temp.board[i][j] = self.board[i][j]
                temp.board[new_moves[0]][new_moves[1]] = 'X'
                newPath = path.copy()
                newPath.append(new_moves)
                self.expandedNodes+=1
                currBoardIdx_new = self.local_to_global(new_moves)
                value_store = value;
                value = max(value, temp.alphabeta_tracking_helper(depth-1, currBoardIdx_new, alpha, beta, not isMax, newPath)[0])
                self.expandedNodes += temp.expandedNodes
                if value != value_store:
                    pathkeeping = temp.alphabeta_tracking_helper(depth-1, currBoardIdx_new, alpha, beta, not isMax, newPath)[1].copy()
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        else:
            # O is making the move
            value = inf
            move_list = self.get_possible_moves(currBoardIdx)
            for new_moves in move_list:
                temp = ultimateTicTacToe()
                for i in range(0,9):
                    for j in range(0,9):
                        temp.board[i][j] = self.board[i][j]
                temp.board[new_moves[0]][new_moves[1]] = 'O'
                newPath = path.copy()
                newPath.append(new_moves)
                self.expandedNodes+=1
                currBoardIdx_new = self.local_to_global(new_moves)
                value_store = value;
                value = min(value, temp.alphabeta_tracking_helper(depth-1, currBoardIdx_new, alpha, beta, not isMax, newPath)[0])
                self.expandedNodes += temp.expandedNodes
                if value != value_store:
                    pathkeeping = temp.alphabeta_tracking_helper(depth-1, currBoardIdx_new, alpha, beta, not isMax, newPath)[1].copy()
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return (value, pathkeeping)

    def alphabeta_tracking(self,depth,currBoardIdx,isMax,path):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        # A the first time the function is called, alpha == -inf and beta == inf

        (value, pathkeeping) = self.alphabeta_tracking_helper(depth, currBoardIdx, -inf, inf, isMax, path)
        return (value, pathkeeping)

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE
        value = 0

        if depth == 0 or self.is_terminal_node(currBoardIdx) == True: # or self.checkWinner()!=0:
            return self.evaluatePredifined(not isMax)
        if isMax:
            # X is making the move
            value = -(inf)
            move_list = self.get_possible_moves(currBoardIdx)
            for new_moves in move_list:
                temp = ultimateTicTacToe()
                for i in range(0,9):
                    for j in range(0,9):
                        temp.board[i][j] = self.board[i][j]
                temp.board[new_moves[0]][new_moves[1]] = 'X'
                self.expandedNodes+=1
                currBoardIdx_new = self.local_to_global(new_moves)
                value_store = value;
                value = max(value, temp.minimax(depth-1, currBoardIdx_new, not isMax))
                if value != value_store:
                    self.expandedNodes += temp.expandedNodes
        else:
            # O is making the move
            value = inf
            move_list = self.get_possible_moves(currBoardIdx)
            for new_moves in move_list:
                temp = ultimateTicTacToe()
                for i in range(0,9):
                    for j in range(0,9):
                        temp.board[i][j] = self.board[i][j]
                temp.board[new_moves[0]][new_moves[1]] = 'O'
                self.expandedNodes+=1
                currBoardIdx_new = self.local_to_global(new_moves)
                value_store = value;
                value = min(value, temp.minimax(depth-1, currBoardIdx_new, not isMax))
                if value != value_store:
                    self.expandedNodes += temp.expandedNodes
        return value

    def minimax_tracking(self, depth, currBoardIdx, isMax, path):
        """
        Improved version of minimax. It keeps the tracking
        """
        pathkeeping = path.copy()
        value = 0

        if depth == 0 or self.is_terminal_node(currBoardIdx) == True:
            return (self.evaluatePredifined(not isMax),path.copy())
        if isMax:
            # X is making the move
            value = -(inf)
            move_list = self.get_possible_moves(currBoardIdx)
            for new_moves in move_list:
                temp = ultimateTicTacToe()
                for i in range(0,9):
                    for j in range(0,9):
                        temp.board[i][j] = self.board[i][j]
                temp.board[new_moves[0]][new_moves[1]] = 'X'
                currBoardIdx_new = self.local_to_global(new_moves)
                newPath = path.copy()
                newPath.append(new_moves)
                self.expandedNodes += 1
                value_store = value
                value = max(value, temp.minimax_tracking(depth-1, currBoardIdx_new, not isMax,newPath)[0])
                self.expandedNodes += temp.expandedNodes
                if value != value_store:
                    pathkeeping = temp.minimax_tracking(depth-1, currBoardIdx_new, not isMax,newPath)[1].copy()
        else:
            # O is making the move
            value = inf
            move_list = self.get_possible_moves(currBoardIdx)
            for new_moves in move_list:
                temp = ultimateTicTacToe()
                for i in range(0,9):
                    for j in range(0,9):
                        temp.board[i][j] = self.board[i][j]
                temp.board[new_moves[0]][new_moves[1]] = 'O'
                currBoardIdx_new = self.local_to_global(new_moves)
                newPath = path.copy()
                newPath.append(new_moves)
                self.expandedNodes += 1
                value_store = value
                value = min(value, temp.minimax_tracking(depth-1, currBoardIdx_new, not isMax,newPath)[0])
                self.expandedNodes += temp.expandedNodes
                if value != value_store:
                    pathkeeping = temp.minimax_tracking(depth-1, currBoardIdx_new, not isMax,newPath)[1].copy();
        return (value, pathkeeping)

    def minimax_tracking_designed(self, depth, currBoardIdx, isMax, path):
        """
        Improved version of minimax. It keeps the tracking
        """
        pathkeeping = path.copy()
        value = 0

        if depth == 0 or self.is_terminal_node(currBoardIdx) == True:
            return (self.evaluateDesigned(not isMax),path.copy())
        if isMax:
            # X is making the move
            value = -(inf)
            move_list = self.get_possible_moves(currBoardIdx)
            for new_moves in move_list:
                temp = ultimateTicTacToe()
                for i in range(0,9):
                    for j in range(0,9):
                        temp.board[i][j] = self.board[i][j]
                temp.board[new_moves[0]][new_moves[1]] = 'X'
                currBoardIdx_new = self.local_to_global(new_moves)
                newPath = path.copy()
                newPath.append(new_moves)
                self.expandedNodes+=1
                value_store = value
                value = max(value, temp.minimax_tracking_designed(depth-1, currBoardIdx_new, not isMax,newPath)[0])
                if value != value_store:
                    self.expandedNodes += temp.expandedNodes
                    pathkeeping = temp.minimax_tracking_designed(depth-1, currBoardIdx_new, not isMax,newPath)[1].copy()
        else:
            # O is making the move
            value = inf
            move_list = self.get_possible_moves(currBoardIdx)
            for new_moves in move_list:
                temp = ultimateTicTacToe()
                for i in range(0,9):
                    for j in range(0,9):
                        temp.board[i][j] = self.board[i][j]
                temp.board[new_moves[0]][new_moves[1]] = 'O'
                currBoardIdx_new = self.local_to_global(new_moves)
                newPath = path.copy()
                newPath.append(new_moves)
                self.expandedNodes+=1
                value_store = value
                value = min(value, temp.minimax_tracking_designed(depth-1, currBoardIdx_new, not isMax,newPath)[0])
                if value != value_store:
                    self.expandedNodes += temp.expandedNodes
                    pathkeeping = temp.minimax_tracking_designed(depth-1, currBoardIdx_new, not isMax,newPath)[1].copy();
        return (value, pathkeeping)

    def local_to_global(self, new_moves):
        """
        Helper function defined by Peilin Rao
        Takes in a move, from [0,0] to [8,8]
        Returns a local move index, from 0 to 8
        """
        tempx = new_moves[0] % 3
        tempy = new_moves[1] % 3
        currBoardIdx_temp = 10 # initalizied to an impossible value
        if(tempx == 0 and tempy == 0):
            currBoardIdx_temp = 0
        elif(tempx == 0 and tempy == 1):
            currBoardIdx_temp = 1
        elif(tempx == 0 and tempy == 2):
            currBoardIdx_temp = 2
        elif(tempx == 1 and tempy == 0):
            currBoardIdx_temp = 3
        elif(tempx == 1 and tempy == 1):
            currBoardIdx_temp = 4
        elif(tempx == 1 and tempy == 2):
            currBoardIdx_temp = 5
        elif(tempx == 2 and tempy == 0):
            currBoardIdx_temp = 6
        elif(tempx == 2 and tempy == 1):
            currBoardIdx_temp = 7
        elif(tempx == 2 and tempy == 2):
            currBoardIdx_temp = 8
        return currBoardIdx_temp

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        # Initialization
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        expandedNodes = []
        winner=0

        currBoardIdx = 4
        if maxFirst:
            while(1):
                if isMinimaxOffensive:
                    (value_temp, path_temp) = self.minimax_tracking(self.maxDepth, currBoardIdx, 1,[])
                    best_value_now = value_temp
                    best_move_now = path_temp[0]
                else:
                    (value_temp, path_temp) = self.alphabeta_tracking(self.maxDepth, currBoardIdx, 1,[])
                    best_value_now = value_temp
                    best_move_now = path_temp[0]
                bestValue.append(best_value_now)
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'X'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                expandedNodes.append(self.expandedNodes)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break

                if isMinimaxDefensive:
                    (value_temp, path_temp) = self.minimax_tracking(self.maxDepth, currBoardIdx, 0,[])
                    best_value_now = value_temp
                    best_move_now = path_temp[0]
                else:
                    (value_temp, path_temp) = self.alphabeta_tracking(self.maxDepth, currBoardIdx, 0,[])
                    best_value_now = value_temp
                    best_move_now = path_temp[0]
                bestValue.append(best_value_now)
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'O'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                expandedNodes.append(self.expandedNodes)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break
        else:
            while(1):
                if isMinimaxDefensive:
                    (value_temp, path_temp) = self.minimax_tracking(self.maxDepth, currBoardIdx, 0,[])
                    best_value_now = value_temp
                    best_move_now = path_temp[0]
                else:
                    (value_temp, path_temp) = self.alphabeta_tracking(self.maxDepth, currBoardIdx, 0,[])
                    best_value_now = value_temp
                    best_move_now = path_temp[0]
                bestValue.append(best_value_now)
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'O'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                expandedNodes.append(self.expandedNodes)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break

                if isMinimaxOffensive:
                    (value_temp, path_temp) = self.minimax_tracking(self.maxDepth, currBoardIdx, 1,[])
                    best_value_now = value_temp
                    best_move_now = path_temp[0]
                else:
                    (value_temp, path_temp) = self.alphabeta_tracking(self.maxDepth, currBoardIdx, 1,[])
                    best_value_now = value_temp
                    best_move_now = path_temp[0]
                bestValue.append(best_value_now)
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'X'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                expandedNodes.append(self.expandedNodes)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break

        expandedNodes_noncul = []
        expandedNodes_noncul.append(expandedNodes[0])
        for i in range(1, len(expandedNodes)):
            expandedNodes_noncul.append(expandedNodes[i]-expandedNodes[i-1])
        return gameBoards, bestMove, expandedNodes_noncul, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        expandedNodes = []
        winner=0
        pcFirst = randint(0,1)
        currBoardIdx = randint(0,8)
        if pcFirst:
            while(1):
                (value_temp, path_temp) = self.minimax_tracking(self.maxDepth, currBoardIdx, 1,[])
                best_value_now = value_temp
                best_move_now = path_temp[0]
                bestValue.append(best_value_now)
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'X'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                expandedNodes.append(self.expandedNodes)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break

                (value_temp, path_temp) = self.minimax_tracking_designed(self.maxDepth, currBoardIdx, 0,[])
                best_value_now = value_temp
                best_move_now = path_temp[0]
                bestValue.append(best_value_now)
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'O'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                expandedNodes.append(self.expandedNodes)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break
        else:
            while(1):
                (value_temp, path_temp) = self.minimax_tracking_designed(self.maxDepth, currBoardIdx, 0,[])
                best_value_now = value_temp
                best_move_now = path_temp[0]
                bestValue.append(best_value_now)
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'O'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                expandedNodes.append(self.expandedNodes)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break

                (value_temp, path_temp) = self.minimax_tracking(self.maxDepth, currBoardIdx, 1,[])
                best_value_now = value_temp
                best_move_now = path_temp[0]
                bestValue.append(best_value_now)
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'X'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                expandedNodes.append(self.expandedNodes)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break

        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        pcFirst = randint(0,1)
        currBoardIdx = randint(0,8)
        if pcFirst:
            while(1):
                (value_temp, path_temp) = self.minimax_tracking_designed(self.maxDepth, currBoardIdx, 1,[])
                best_value_now = value_temp
                best_move_now = path_temp[0]
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'X'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break

                Input = input("Make your move! Type x and y without space: ")
                best_move_now = [int(int(Input)/10),int(int(Input)%10)]
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'O'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break
        else:
            while(1):
                Input = input("Make your move! Type x and y without space: ")
                best_move_now = [int(int(Input)/10),int(int(Input)%10)]
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'O'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break

                (value_temp, path_temp) = self.minimax_tracking_designed(self.maxDepth, currBoardIdx, 1,[])
                best_value_now = value_temp
                best_move_now = path_temp[0]
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'X'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break

        return gameBoards, bestMove, winner


class ultimateTicTacToeExtraCredit:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.controlBoard=[['_','_','_'],['_','_','_'],['_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')

    def evaluatePredifined_helper_attack(self, isMax):
        # Helper defined by Peilin Rao
        # For each local board, count the number of two-in-a-row without the third spot
        # taken by the opposing player (unblocked two-in-a-row).
        count = 0
        my_char = 'O'
        if isMax:
            my_char = 'X'
        for index in self.globalIdx:
            local_board = [['_', '_', '_'],['_', '_', '_'],['_', '_', '_']]
            # Hard coding the situation of board
            for i in range(0, 3):
                for j in range(0, 3):
                    local_board[i][j] = self.board[index[0]+i][index[1]+j]
            if (local_board[0][0] == my_char and local_board[0][1] == my_char and local_board[0][2] == '_') \
                    or (local_board[0][0] == my_char and local_board[0][1] == '_' and local_board[0][2] == my_char) \
                    or (local_board[0][0] == '_' and local_board[0][1] == my_char and local_board[0][2] == my_char):
                count += 1
            if(local_board[1][0] == my_char and local_board[1][1] == my_char and local_board[1][2] == '_') \
                    or (local_board[1][0] == my_char and local_board[1][1] == '_' and local_board[1][2] == my_char) \
                    or (local_board[1][0] == '_' and local_board[1][1] == my_char and local_board[1][2] == my_char):
                count += 1
            if(local_board[2][0] == my_char and local_board[2][1] == my_char and local_board[2][2] == '_') \
                    or (local_board[2][0] == my_char and local_board[2][1] == '_' and local_board[2][2] == my_char) \
                    or (local_board[2][0] == '_' and local_board[2][1] == my_char and local_board[2][2] == my_char):
                count += 1
            if(local_board[0][0] == my_char and local_board[1][0] == my_char and local_board[2][0] == '_') \
                    or (local_board[0][0] == my_char and local_board[1][0] == '_' and local_board[2][0] == my_char) \
                    or (local_board[0][0] == '_' and local_board[1][0] == my_char and local_board[2][0] == my_char):
                count += 1
            if(local_board[0][1] == my_char and local_board[1][1] == my_char and local_board[2][1] == '_') \
                    or (local_board[0][1] == my_char and local_board[1][1] == '_' and local_board[2][1] == my_char) \
                    or (local_board[0][1] == '_' and local_board[1][1] == my_char and local_board[2][1] == my_char):
                count += 1
            if(local_board[0][2] == my_char and local_board[1][2] == my_char and local_board[2][2] == '_') \
                    or (local_board[0][2] == my_char and local_board[1][2] == '_' and local_board[2][2] == my_char) \
                    or (local_board[0][2] == '_' and local_board[1][2] == my_char and local_board[2][2] == my_char):
                count += 1
            if(local_board[0][0] == my_char and local_board[1][1] == my_char and local_board[2][2] == '_') \
                    or (local_board[0][0] == my_char and local_board[1][1] == '_' and local_board[2][2] == my_char) \
                    or (local_board[0][0] == '_' and local_board[1][1] == my_char and local_board[2][2] == my_char):
                count += 1
            if(local_board[0][2] == my_char and local_board[1][1] == my_char and local_board[2][0] == '_') \
                    or (local_board[0][2] == my_char and local_board[1][1] == '_' and local_board[2][0] == my_char) \
                    or (local_board[0][2] == '_' and local_board[1][1] == my_char and local_board[2][0] == my_char):
                count += 1
        return count
    def evaluatePredifined_helper_defense(self, isMax):
        # Helper defined by Peilin Rao
        # For each local board, count the number of places in which you have prevented
        # the opponent player forming two-in-a-row (two-in-a-row of opponent player but with the third spot taken by offensive agent).
        count = 0
        my_char = 'X'
        player_char = 'O'
        if isMax:
            my_char = 'O'
            player_char = 'X'
        for index in self.globalIdx:
            # Hard coding the situation of board
            local_board = [['_', '_', '_'],['_', '_', '_'],['_', '_', '_']]
            for i in range(0, 3):
                for j in range(0, 3):
                    local_board[i][j] = self.board[index[0]+i][index[1]+j]
            if (local_board[0][0] == my_char and local_board[0][1] == my_char and local_board[0][2] == player_char) \
                    or (local_board[0][0] == my_char and local_board[0][1] == player_char and local_board[0][2] == my_char) \
                    or (local_board[0][0] == player_char and local_board[0][1] == my_char and local_board[0][2] == my_char):
                count += 1
            if(local_board[1][0] == my_char and local_board[1][1] == my_char and local_board[1][2] == player_char) \
                    or (local_board[1][0] == my_char and local_board[1][1] == player_char and local_board[1][2] == my_char) \
                    or (local_board[1][0] == player_char and local_board[1][1] == my_char and local_board[1][2] == my_char):
                count += 1
            if(local_board[2][0] == my_char and local_board[2][1] == my_char and local_board[2][2] == player_char) \
                    or (local_board[2][0] == my_char and local_board[2][1] == player_char and local_board[2][2] == my_char) \
                    or (local_board[2][0] == player_char and local_board[2][1] == my_char and local_board[2][2] == my_char):
                count += 1
            if(local_board[0][0] == my_char and local_board[1][0] == my_char and local_board[2][0] == player_char) \
                    or (local_board[0][0] == my_char and local_board[1][0] == player_char and local_board[2][0] == my_char) \
                    or (local_board[0][0] == player_char and local_board[1][0] == my_char and local_board[2][0] == my_char):
                count += 1
            if(local_board[0][1] == my_char and local_board[1][1] == my_char and local_board[2][1] == player_char) \
                    or (local_board[0][1] == my_char and local_board[1][1] == player_char and local_board[2][1] == my_char) \
                    or (local_board[0][1] == player_char and local_board[1][1] == my_char and local_board[2][1] == my_char):
                count += 1
            if(local_board[0][2] == my_char and local_board[1][2] == my_char and local_board[2][2] == player_char) \
                    or (local_board[0][2] == my_char and local_board[1][2] == player_char and local_board[2][2] == my_char) \
                    or (local_board[0][2] == player_char and local_board[1][2] == my_char and local_board[2][2] == my_char):
                count += 1
            if(local_board[0][0] == my_char and local_board[1][1] == my_char and local_board[2][2] == player_char) \
                    or (local_board[0][0] == my_char and local_board[1][1] == player_char and local_board[2][2] == my_char) \
                    or (local_board[0][0] == player_char and local_board[1][1] == my_char and local_board[2][2] == my_char):
                count += 1
            if(local_board[0][2] == my_char and local_board[1][1] == my_char and local_board[2][0] == player_char) \
                    or (local_board[0][2] == my_char and local_board[1][1] == player_char and local_board[2][0] == my_char) \
                    or (local_board[0][2] == player_char and local_board[1][1] == my_char and local_board[2][0] == my_char):
                count += 1
        return count
    def evaluatePredifined_helper_corner(self, isMax):
        # Helper defined by Peilin Rao
        # Rule 3
        count = 0
        my_char = 'O'
        op_char = 'X'
        if isMax:
            my_char = 'X'
            op_char = 'O'
        for index in self.globalIdx:
            local_board = [['_', '_', '_'],['_', '_', '_'],['_', '_', '_']]
            for i in range(0, 3):
                for j in range(0, 3):
                    local_board[i][j] = self.board[index[0]+i][index[1]+j]
            # Check if the corners are filled
            if local_board[0][0] == my_char or local_board[0][2] == my_char \
            or local_board[2][0] == my_char or local_board[2][2] == my_char:
                    count += 1
        return count

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score = 0
        if isMax:
            if self.checkWinner() == -1:
                return -100000
            if self.checkWinner() == -2:
                return -50000
            if self.checkWinner() == 1:
                return self.winnerMaxUtility
            else:
                score = self.evaluatePredifined_helper_attack(isMax) * self.twoInARowMaxUtility + \
                        self.evaluatePredifined_helper_defense(isMax) * self.preventThreeInARowMaxUtility
                if score == 0:
                    score = self.evaluatePredifined_helper_corner(isMax) * self.cornerMaxUtility
        else:
            if self.checkWinner() == 1:
                return +100000
            if self.checkWinner() == -2:
                return +50000
            if self.checkWinner() == -1:
                return self.winnerMinUtility
            else:
                score = self.evaluatePredifined_helper_attack(isMax) * self.twoInARowMinUtility + \
                        self.evaluatePredifined_helper_defense(isMax) * self.preventThreeInARowMinUtility
                if score == 0:
                    score = self.evaluatePredifined_helper_corner(isMax) * self.cornerMinUtility
        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        for i in range(0,9):
            for j in range(0,9):
                if self.board[i][j] == '_':
                    return True
        return False

    def is_terminal_node(self, currBoardIdx):
        """
        Check if there is any available moves in the local TTT (3*3)

        :param currBoardIdx:
        :return: True if it is terminal node
        """
        index = self.globalIdx[currBoardIdx]
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[index[0]+i][index[1]+j] == '_':
                    return False
        return True

    def get_possible_moves(self, currBoardIdx):
        """
        Check if there is any available moves in the board

        :param currBoardIdx:
        :return: A list of possible moves
        """
        list_of_possible_moves=[]
        if self.controlBoard[self.get_cood(currBoardIdx)[0]][self.get_cood(currBoardIdx)[1]]=='_':
            list_of_possible_moves = []
            index = self.globalIdx[currBoardIdx]
            for i in range(index[0],index[0]+3):
                for j in range(index[1],index[1]+3):
                    if self.board[i][j] == '_':
                        list_of_possible_moves.append([i, j])
        if len(list_of_possible_moves) == 0:
            for x in range(0,3):
                for y in range(0,3):
                    if self.controlBoard[x][y] == '_':
                        for i in range(x*3,x*3+3):
                            for j in range(y*3,y*3+3):
                                if self.board[i][j] == '_':
                                    list_of_possible_moves.append([i, j])

        return list_of_possible_moves

    def get_cood(self, currBoardIdx):
          if currBoardIdx == 0:
              return (0,0)
          if currBoardIdx == 1:
              return (0,1)
          if currBoardIdx == 2:
              return (0,2)
          if currBoardIdx == 3:
              return (1,0)
          if currBoardIdx == 4:
              return (1,1)
          if currBoardIdx == 5:
              return (1,2)
          if currBoardIdx == 6:
              return (2,0)
          if currBoardIdx == 7:
              return (2,1)
          if currBoardIdx == 8:
              return (2,2)
    def update_controlBoard(self):
        #YOUR CODE HERE
        for index in self.globalIdx:
            local_board = [['_', '_', '_'],['_', '_', '_'],['_', '_', '_']]
            for i in range(0, 3):
                for j in range(0, 3):
                    local_board[i][j] = self.board[index[0]+i][index[1]+j]
            if (local_board[0][0] == 'X' and local_board[0][1] == 'X' and local_board[0][2] == 'X')\
                    or (local_board[1][0] == 'X' and local_board[1][1] == 'X' and local_board[1][2] == 'X') \
                    or (local_board[2][0] == 'X' and local_board[2][1] == 'X' and local_board[2][2] == 'X') \
                    or (local_board[0][0] == 'X' and local_board[1][0] == 'X' and local_board[2][0] == 'X') \
                    or (local_board[0][1] == 'X' and local_board[1][1] == 'X' and local_board[2][1] == 'X') \
                    or (local_board[0][2] == 'X' and local_board[1][2] == 'X' and local_board[2][2] == 'X') \
                    or (local_board[0][0] == 'X' and local_board[1][1] == 'X' and local_board[2][2] == 'X') \
                    or (local_board[0][2] == 'X' and local_board[1][1] == 'X' and local_board[2][0] == 'X'):

                self.controlBoard[int(index[0]/3)][int(index[1]/3)] = 'X'

            elif (local_board[0][0] == 'O' and local_board[0][1] == 'O' and local_board[0][2] == 'O') \
                    or (local_board[1][0] == 'O' and local_board[1][1] == 'O' and local_board[1][2] == 'O') \
                    or (local_board[2][0] == 'O' and local_board[2][1] == 'O' and local_board[2][2] == 'O') \
                    or (local_board[0][0] == 'O' and local_board[1][0] == 'O' and local_board[2][0] == 'O') \
                    or (local_board[0][1] == 'O' and local_board[1][1] == 'O' and local_board[2][1] == 'O') \
                    or (local_board[0][2] == 'O' and local_board[1][2] == 'O' and local_board[2][2] == 'O') \
                    or (local_board[0][0] == 'O' and local_board[1][1] == 'O' and local_board[2][2] == 'O') \
                    or (local_board[0][2] == 'O' and local_board[1][1] == 'O' and local_board[2][0] == 'O'):

                self.controlBoard[int(index[0]/3)][int(index[1]/3)] = 'O'
            else:
                count = 0
                for i in range(0, 3):
                    for j in range(0, 3):
                        if local_board[i][j] != '_':
                            count+=1
                if count == 9:
                    self.controlBoard[int(index[0]/3)][int(index[1]/3)] = '-'

    def local_to_global(self, new_moves):
        """
        Helper function defined by Peilin Rao
        Takes in a move, from [0,0] to [8,8]
        Returns a local move index, from 0 to 8
        """
        tempx = new_moves[0] % 3
        tempy = new_moves[1] % 3
        currBoardIdx_temp = 10 # initalizied to an impossible value
        if(tempx == 0 and tempy == 0):
            currBoardIdx_temp = 0
        elif(tempx == 0 and tempy == 1):
            currBoardIdx_temp = 1
        elif(tempx == 0 and tempy == 2):
            currBoardIdx_temp = 2
        elif(tempx == 1 and tempy == 0):
            currBoardIdx_temp = 3
        elif(tempx == 1 and tempy == 1):
            currBoardIdx_temp = 4
        elif(tempx == 1 and tempy == 2):
            currBoardIdx_temp = 5
        elif(tempx == 2 and tempy == 0):
            currBoardIdx_temp = 6
        elif(tempx == 2 and tempy == 1):
            currBoardIdx_temp = 7
        elif(tempx == 2 and tempy == 2):
            currBoardIdx_temp = 8
        return currBoardIdx_temp

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer(X) is the winner.
                     Return -1 if miniPlayer(O) is the winner.
                     Return -2 if tie
        """
        #YOUR CODE HERE
        if (self.controlBoard[0][0] == 'X' and self.controlBoard[0][1] == 'X' and self.controlBoard[0][2] == 'X')\
                or (self.controlBoard[1][0] == 'X' and self.controlBoard[1][1] == 'X' and self.controlBoard[1][2] == 'X') \
                or (self.controlBoard[2][0] == 'X' and self.controlBoard[2][1] == 'X' and self.controlBoard[2][2] == 'X') \
                or (self.controlBoard[0][0] == 'X' and self.controlBoard[1][0] == 'X' and self.controlBoard[2][0] == 'X') \
                or (self.controlBoard[0][1] == 'X' and self.controlBoard[1][1] == 'X' and self.controlBoard[2][1] == 'X') \
                or (self.controlBoard[0][2] == 'X' and self.controlBoard[1][2] == 'X' and self.controlBoard[2][2] == 'X') \
                or (self.controlBoard[0][0] == 'X' and self.controlBoard[1][1] == 'X' and self.controlBoard[2][2] == 'X') \
                or (self.controlBoard[0][2] == 'X' and self.controlBoard[1][1] == 'X' and self.controlBoard[2][0] == 'X'):
            return 1
        elif (self.controlBoard[0][0] == 'O' and self.controlBoard[0][1] == 'O' and self.controlBoard[0][2] == 'O') \
                or (self.controlBoard[1][0] == 'O' and self.controlBoard[1][1] == 'O' and self.controlBoard[1][2] == 'O') \
                or (self.controlBoard[2][0] == 'O' and self.controlBoard[2][1] == 'O' and self.controlBoard[2][2] == 'O') \
                or (self.controlBoard[0][0] == 'O' and self.controlBoard[1][0] == 'O' and self.controlBoard[2][0] == 'O') \
                or (self.controlBoard[0][1] == 'O' and self.controlBoard[1][1] == 'O' and self.controlBoard[2][1] == 'O') \
                or (self.controlBoard[0][2] == 'O' and self.controlBoard[1][2] == 'O' and self.controlBoard[2][2] == 'O') \
                or (self.controlBoard[0][0] == 'O' and self.controlBoard[1][1] == 'O' and self.controlBoard[2][2] == 'O') \
                or (self.controlBoard[0][2] == 'O' and self.controlBoard[1][1] == 'O' and self.controlBoard[2][0] == 'O'):
            return -1

        flag_tie = 1
        for i in range(0, 3):
            for j in range(0, 3):
                if self.controlBoard[i][j] == '_':
                    flag_tie = 0
        if flag_tie == 1:
            return -2
        else:
            return 0

    def minimax_tracking_designed(self, depth, currBoardIdx, isMax, path):
        """
        Improved version of minimax. It keeps the tracking
        """
        pathkeeping = path.copy()
        value = 0
        if depth == 0 or self.is_terminal_node(currBoardIdx):
            return (self.evaluateDesigned(not isMax),pathkeeping)
        if isMax:
            # X is making the move
            value = -(inf)
            move_list = self.get_possible_moves(currBoardIdx)
            for new_moves in move_list:
                temp = ultimateTicTacToeExtraCredit()
                for i in range(0,9):
                    for j in range(0,9):
                        temp.board[i][j] = self.board[i][j]
                for i in range(0,3):
                    for j in range(0,3):
                        temp.controlBoard[i][j] = self.controlBoard[i][j]
                temp.board[new_moves[0]][new_moves[1]] = 'X'
                currBoardIdx_new = self.local_to_global(new_moves)
                newPath = path.copy()
                newPath.append(new_moves)
                self.expandedNodes+=1
                value_store = value
                a, b = temp.minimax_tracking_designed(depth-1, currBoardIdx_new, not isMax,newPath)
                value = max(value, a)
                if value != value_store:
                    self.expandedNodes += temp.expandedNodes
                    pathkeeping = b.copy();
        else:
            # O is making the move
            value = inf
            move_list = self.get_possible_moves(currBoardIdx)
            for new_moves in move_list:
                temp = ultimateTicTacToeExtraCredit()
                for i in range(0,9):
                    for j in range(0,9):
                        temp.board[i][j] = self.board[i][j]
                for i in range(0,3):
                    for j in range(0,3):
                        temp.controlBoard[i][j] = self.controlBoard[i][j]
                temp.board[new_moves[0]][new_moves[1]] = 'O'
                currBoardIdx_new = self.local_to_global(new_moves)
                newPath = path.copy()
                newPath.append(new_moves)
                self.expandedNodes+=1
                value_store = value
                a, b = temp.minimax_tracking_designed(depth-1, currBoardIdx_new, not isMax,newPath)
                value = min(value, a)
                if value != value_store:
                    self.expandedNodes += temp.expandedNodes
                    pathkeeping = b.copy();
        return (value, pathkeeping)


    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        flag_surrender = 0
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        expandedNodes = []
        winner=0
        pcFirst = randint(0,1)
        currBoardIdx = randint(0,8)
        if pcFirst:
            while(1):
                (value_temp, path_temp) = self.minimax_tracking_designed(self.maxDepth, currBoardIdx, 1,[])
                if(len(path_temp) == 0):
                    if self.checkWinner() == -2:
                        winner = 0
                        break
                    flag_surrender = 1
                    winner = -1
                    break
                best_value_now = value_temp
                best_move_now = path_temp[0]
                bestValue.append(best_value_now)
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'X'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                expandedNodes.append(self.expandedNodes)
                self.update_controlBoard()
                print(self.controlBoard)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break
                if self.checkWinner() == -2:
                    winner = 0
                    break

                (value_temp, path_temp) = self.minimax_tracking_designed(self.maxDepth, currBoardIdx, 0,[])
                if(len(path_temp) == 0):
                    if self.checkWinner() == -2:
                        winner = 0
                        break
                    flag_surrender = 1
                    winner = 1
                    break
                best_value_now = value_temp
                best_move_now = path_temp[0]
                bestValue.append(best_value_now)
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'O'
                temp_board = self.board.copy()
                self.printGameBoard()
                gameBoards.append(temp_board)
                expandedNodes.append(self.expandedNodes)
                self.update_controlBoard()
                print(self.controlBoard)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break
                if self.checkWinner() == -2:
                    winner = 0
                    break
        else:
            while(1):
                (value_temp, path_temp) = self.minimax_tracking_designed(self.maxDepth, currBoardIdx, 0,[])
                if(len(path_temp) == 0):
                    if self.checkWinner() == -2:
                        winner = 0
                        break
                    flag_surrender = 1
                    winner = 1
                    break
                best_value_now = value_temp
                best_move_now = path_temp[0]
                bestValue.append(best_value_now)
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'O'
                temp_board = self.board.copy()
                self.update_controlBoard()
                self.printGameBoard()
                print(self.controlBoard)
                gameBoards.append(temp_board)
                expandedNodes.append(self.expandedNodes)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break
                if self.checkWinner() == -2:
                    winner = 0
                    break

                (value_temp, path_temp) = self.minimax_tracking_designed(self.maxDepth, currBoardIdx, 1,[])
                if(len(path_temp) == 0):
                    if self.checkWinner() == -2:
                        winner = 0
                        break
                    flag_surrender = 1
                    winner = -1
                    break
                best_value_now = value_temp
                best_move_now = path_temp[0]
                bestValue.append(best_value_now)
                bestMove.append(best_move_now)
                currBoardIdx = self.local_to_global(best_move_now)
                self.board[best_move_now[0]][best_move_now[1]] = 'X'
                temp_board = self.board.copy()
                self.update_controlBoard()
                self.printGameBoard()
                gameBoards.append(temp_board)
                expandedNodes.append(self.expandedNodes)
                if self.checkWinner() == 1:
                    winner = 1
                    break
                if self.checkWinner() == -1:
                    winner = -1
                    break
                if self.checkWinner() == -2:
                    winner = 0
                    break

        return gameBoards, bestMove, expandedNodes, bestValue, winner, flag_surrender

if __name__=="__main__":

    # Uncomment this section to use the predefined agent
    # uttt=ultimateTicTacToe()
    # gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True, True, True)
    # print("bestMove:", bestMove)
    # print("bestValue:", bestValue)
    # print("expandedNodes:",expandedNodes)
    # total_expandedNodes = 0
    # for i in expandedNodes:
    #     total_expandedNodes += i
    # print("total_expandedNodes:",total_expandedNodes)
    # if winner == 1:
    #     print("The winner is maxPlayer!!!")
    # elif winner == -1:
    #     print("The winner is minPlayer!!!")
    # else:
    #     print("Tie. No winner:(")


    # Uncomment this section to use the agent designed by Peilin Rao vs predefined agent for 20 games
    # count_my_ai_winning = 0;
    # for i in range(20):
    #     uttt=ultimateTicTacToe()
    #     gameBoards, bestMove, expandedNodes, bestValue, winner = uttt.playGameYourAgent()
    #     if winner == -1:
    #         count_my_ai_winning += 1
    # print(count_my_ai_winning)

    # Uncomment this section to use the agent designed by Peilin Rao vs predefined agent for 1 game
    # uttt=ultimateTicTacToe()
    # gameBoards, bestMove, expandedNodes, bestValue, winner = uttt.playGameYourAgent()
    # print("bestMove:", bestMove)
    # print("bestValue:", bestValue)
    # print("expandedNodes:",expandedNodes)
    # total_expandedNodes = 0
    # for i in expandedNodes:
    #     total_expandedNodes += i
    # print("total_expandedNodes:",total_expandedNodes)
    # if winner == 1:
    #     print("The winner is maxPlayer!!!")
    # elif winner == -1:
    #     print("The winner is minPlayer!!!")
    # else:
    #     print("Tie. No winner:(")

    # Uncomment this section to play against human
    uttt=ultimateTicTacToe()
    gameBoards, bestMove,winner = uttt.playGameHuman()
    print("bestMove:", bestMove)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")

    # Uncomment this section to use the agent in Extra Credit attempt
    # uttt=ultimateTicTacToeExtraCredit()
    # gameBoards, bestMove, expandedNodes, bestValue, winner, flag_surrender = uttt.playGameYourAgent()
    # print("bestMove:", bestMove)
    # print("bestValue:", bestValue)
    # print("expandedNodes:",expandedNodes)
    # total_expandedNodes = 0
    # for i in expandedNodes:
    #     total_expandedNodes += i
    # print("total_expandedNodes:",total_expandedNodes)
    # if winner == 1:
    #     print("The winner is maxPlayer!!!")
    #     if flag_surrender:
    #        print("The minPlayer surrendered because he cannot win.")
    # elif winner == -1:
    #     print("The winner is minPlayer!!!")
    #     if flag_surrender:
    #         print("The maxPlayer surrendered because he cannot win.")
    # elif winner == 0:
    #     print("Tie. No winner:(")

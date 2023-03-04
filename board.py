import peices
from ratings import Ratings
class ChessBoard:
    """
    Chessboard class will contain the 8x8 board array as well
    as all the functions needed to evaluate moves
    """
    def __init__(self):
        '''
        boardArray format: for our implementation we used an 8x8 board
        to represent each peice in the board. the array is represented in then
        form boardArray[row][column]; example boardArray[0][0] == "r", boardArray[7][7] == "R"
        Capitalised letters represent 'friendly' peiced and lowercase letters represent
        'enemy' peices.
        '''
        self.boardArray = [
        ["r", "k", "b", "q", "a", "b", "k", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "K", "B", "Q", "A", "B", "K", "R"]
        ]
        self.TOTALPIECES = 64
        self.kingPosition_White = 60
        self.kingPosition_Black = 4
        self.MAXDEPTH = 3
    def generateMoveList(self):
        """
        Description: Evalutates the entire board and will return a list of all possible
        moves available to make. By going through entire array and evaluating reach
        spot and piece's individual move set to return every individual moveset
        Returns: movelist - a string that stores every possible move my every peice
        Individual moves are in the format "[oldRow][oldColumn][newRow][newColumn][Captured Piece or blank space]"
        oldRow and oldColumn represent the current position peice is in and newRow
        and newColumn represent the new potential position piece can move to.
        Piece represents either an empty space or an opponent piece our piece can capture
        """
        movelist = ""
        rook = peices.Rook(self)
        knight = peices.Knight(self)
        bishop = peices.Bishop(self)
        queen = peices.Queen(self)
        king = peices.King(self)
        pawn = peices.Pawn(self)
        for index in range(self.TOTALPIECES):
            currentPosition = self.boardArray[index//8][index%8]
            if currentPosition == 'R':
                movelist += rook.findMoveSet(index)
            elif currentPosition == 'K':
                movelist += knight.findMoveSet(index)
            elif currentPosition == 'B':
                movelist += bishop.findMoveSet(index)
            elif currentPosition == 'Q':
                movelist += queen.findMoveSet(index)
            elif currentPosition == 'A':
                movelist += king.findMoveSet(index)
            elif currentPosition == 'P':
                movelist += pawn.findMoveSet(index)
        return movelist
    def kingissafe(self):
        """
        Function that evaluates if a king is in check or is at risk of being in check
        This is very important, as this function affects the move sets of every Other
        peice if king is not safe (in check or at risk in being check)
        Returns: True if king is not at risk of being in check. False if king is
        at risk of being in check
        """
        kingRow = self.kingPosition_White//8
        kingColumn = self.kingPosition_White % 8
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                try:
                    if self.boardArray[kingRow + i][kingColumn + 2*j] == "k" and kingRow + i >= 0 and kingColumn + 2*j >=0:
                        return False
                except IndexError:
                    pass
                try:
                    if self.boardArray[kingRow + 2*i][kingColumn +j] == "k" and kingRow + 2*i >= 0 and kingColumn + j >=0:
                        return False
                except IndexError:
                    pass
        board_roamer = 1
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if i != 0 or j != 0:
                    try:
                        if self.boardArray[kingRow + i][kingColumn + j] == "a" and kingRow + i >= 0 and kingColumn + j >=0:
                            return False
                    except IndexError:
                        pass
        if self.kingPosition_White >= 16:
            try:
                if self.boardArray[kingRow -1][kingColumn -1] == "p" and kingRow - 1 >= 0 and kingColumn -1 >=0:
                    return False
            except IndexError:
                pass
            try:
                if self.boardArray[kingRow -1][kingColumn +1] == "p" and kingRow - 1 >= 0:
                    return False
            except IndexError:
                pass
        for i in range(-1, 2, 2):
            try:
                while self.boardArray[kingRow][kingColumn + board_roamer*i] == " ":
                    board_roamer += 1
                if self.boardArray[kingRow][kingColumn + board_roamer*i] == "r" or self.boardArray[kingRow][kingColumn + board_roamer*i] == "q" and kingColumn + board_roamer*i >= 0:
                    return False
            except IndexError:
                pass
            board_roamer = 1
            try:
                while self.boardArray[kingRow + board_roamer*i][kingColumn] == " ":
                    board_roamer += 1
                if self.boardArray[kingRow + board_roamer*i][kingColumn] == "r" or self.boardArray[kingRow + board_roamer*i][kingColumn] == "q" and kingRow + board_roamer*i >= 0:
                    return False
            except IndexError:
                pass
            board_roamer = 1
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                try:
                    while self.boardArray[kingRow + board_roamer*i][kingColumn + board_roamer*j] == " ":
                        board_roamer += 1
                    if self.boardArray[kingRow + board_roamer*i][kingColumn + board_roamer*j] == "b" or self.boardArray[kingRow + board_roamer*i][kingColumn + board_roamer*j] == "q" and kingRow + board_roamer*i >= 0 and kingColumn + board_roamer*j >= 0:
                        return False
                except IndexError:
                    pass
                board_roamer = 1
        return True
    def computeMove(self, givenMove):
        """
        Function used to move a peice makes in the board to a legal position.
        Args: givenMove in the following forms:
            For regular Moves: [oldRow][oldColumn][newRow][newColumn][Peice]
            For Pawn Promotion: [oldColumn][newColumn][capturedPeice][PromotionPeice]["P"]
            For Castling: [columnRookOld][columnRookFinal][columnKing]["R"]["C"]
        """
        if givenMove[4] == "P" or givenMove[4] == "C":
            if givenMove[4] == "P":
                self.boardArray[1][int(givenMove[0])] = " "
                self.boardArray[0][int(givenMove[1])] = givenMove[3]
            elif givenMove[4] == "C":
                self.boardArray[7][int(givenMove[0])] = " "
                self.boardArray[7][int(givenMove[1])] = "A"
                self.boardArray[7][int(givenMove[2])] = givenMove[3]
        else:
            self.boardArray[int(givenMove[2])][int(givenMove[3])] = self.boardArray[int(givenMove[0])][int(givenMove[1])]
            self.boardArray[int(givenMove[0])][int(givenMove[1])] = " "
            if self.boardArray[int(givenMove[2])][int(givenMove[3])] == "A":
                self.kingPosition_White = 8*int(givenMove[2])+int(givenMove[3])
    def uncomputeMove(self, givenMove):
        """
        Function used to undo a move a peice makes in the board to a position. Move made
        will be unmade. Function is essentially the reverse of computeMove
        Args: givenMove in the form "[oldRow][oldColumn][newRow][newColumn][Piece]" for capturing or moving
        or "[column1][column2][captured-piece][new-piece][P]'' for pawn promotions
        """
        if givenMove[4] == "P" or givenMove[4] == "C":
            if givenMove[4] == "P":
                self.boardArray[1][int(givenMove[0])] = "P"
                self.boardArray[0][int(givenMove[1])] = givenMove[2]
            elif givenMove[4] == "C":
                self.boardArray[7][int(givenMove[1])] = " "
                self.boardArray[7][int(givenMove[2])] = "A"
                self.boardArray[7][int(givenMove[0])] = givenMove[3]
        else:
            self.boardArray[int(givenMove[0])][int(givenMove[1])] = self.boardArray[int(givenMove[2])][int(givenMove[3])]
            self.boardArray[int(givenMove[2])][int(givenMove[3])] = givenMove[4]
            if self.boardArray[int(givenMove[0])][int(givenMove[1])] == "A":
                self.kingPosition_White = 8*int(givenMove[0])+int(givenMove[1])
    def alphaBeta(self, depth, beta, alpha, givenMove, maxPlayer):
        """
        Description: a search algorithm function based off the known alphaBeta pruning
        algorithm (https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
        This algorithm is meant to find the best potential move the computer player can make
        For more information on the algorithm: http://web.cs.ucla.edu/~rosen/161/notes/alphabeta.html
        Args:
                depth: How deep are we evaluating the tree (MAXDEPTH is 3 which is the deepest function will go to)
                Beta: is the minimum upper bound of possible solutions
                Alpha: is the maximum lower bound of possible solutions
                givenMove: is the move we are evaluating for rating
                maxPlayer: represented as either a 0 or 1 : the main idea is for a two-maxPlayer game,
                there are two kinds of nodes: nodes representing our moves and nodes representing our opponent's (The computer) moves.
        Returns: the optimal move with it's rating, represented in the form [move][score] (refer to findMoveSet for move format
                 The optimal rating will be alpha <= rating <= beta
        """
        moveslist = self.generateMoveList()
        ratingE = Ratings(self)
        if depth == 0 or len(moveslist) == 0:
            if givenMove == "":
                return None
            else:
                return givenMove + str(ratingE.evaluateRating(len(moveslist), depth)*(maxPlayer*2-1))
        maxPlayer = 1 - maxPlayer
        for i in range(0, len(moveslist), 5):
            self.computeMove(moveslist[i:(i+5)])
            self.changePerspective()
            nextNode = self.alphaBeta(depth-1, beta, alpha, moveslist[i:(i+5)], maxPlayer)
            value = int(nextNode[5:])
            self.changePerspective()
            self.uncomputeMove(moveslist[i:(i+5)])
            if maxPlayer == 0:
                if value <= beta:
                    beta = value
                    if depth == self.MAXDEPTH:
                        givenMove = nextNode[0:5]
            else:
                if value > alpha:
                    alpha = value
                    if depth == self.MAXDEPTH:
                        givenMove = nextNode[0:5]
                if alpha >= beta:
                    if maxPlayer == 0:
                        return givenMove + str(beta)
                    else:
                        return givenMove + str(alpha)
        if maxPlayer == 0:
            return givenMove + str(beta)
        else:
            return givenMove + str(alpha)
    def changePerspective(self):
        """
        Function to switch the point of view of the chessboard.
        Will switch maxPlayer's peices to opponent's chessPieces
        IMPORTANT NOTE: Don't think of this function as a visual flip of a Board
        but rather a change of perspective
        Example:
        Board is in Player's perspective
        call changePerspective
        Board is in opponent's perspective
        call call changePerspective
        Board is again in Player's perspective
        """
        for index in range(32):
            row = index//8
            column = index % 8
            if self.boardArray[row][column].isupper():
                flipPeice = self.boardArray[row][column].lower()
            else:
                flipPeice = self.boardArray[row][column].upper()
            if self.boardArray[7-row][7-column].isupper():
                self.boardArray[row][column] = self.boardArray[7-row][7-column].lower()
            else:
                self.boardArray[row][column] = self.boardArray[7-row][7-column].upper()
            self.boardArray[7-row][7-column] = flipPeice
        kingFlipped = self.kingPosition_White
        self.kingPosition_White = 63 - self.kingPosition_Black
        self.kingPosition_Black = 63 - kingFlipped

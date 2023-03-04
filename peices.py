class Piece:
    """
    Creation of abstract Piece class, for each individual piece to inherit
    the chessboard class, as well as their own respective find_move_set method
    """
    def __init__(self, board):
        self.chessboard = board

    def find_move_set(self, index):
        """
        This will be the abstract function that all pieces has to evaluate what moves
        can be made by that respective piece
        """
        pass
class Rook(Piece):
    """
    Inherited piece class of the rook. This class includes all the methods
    used to evaluate all the moves that can be made by the rook
    """
    def test_castling(self, row, column, i, board_roamer):
        """
        Helper function to check if rook can perform the special castling move
        """
        castling = ""
        if row == 7:
            if column == 0 or column == 7:
                board_array = self.chessboard.boardArray
                if board_array[row][column+board_roamer*i] == "A":
                    previous_position = board_array[row][column+board_roamer*i]
                    board_array[row][column] = "A"
                    board_array[row][column+board_roamer*i] = "R"
                    if self.chessboard.king_is_safe() and (column+board_roamer*i) >= 0:
                        if column == 0:
                            castling += str(column)+str(column+board_roamer*i-1) + str(column+board_roamer*i)+"R"+"C"
                        elif column == 7:
                                castling += str(column)+ str(column+board_roamer*i+1) + str(column+board_roamer*i)+"R"+"C"
                    board_array[row][column] = "R"
                    board_array[row][column+board_roamer*i] = previous_position
        return castling
    def testMove(self, row, col, row_offset, col_offset, piece, movelist):
        """
        Helper function to test if a move is valid
        """
        board_size = len(self.chessboard.boardArray)
        new_row = row + row_offset
        new_col = col + col_offset
        if new_row < 0 or new_col < 0 or new_row >= board_size or new_col >= board_size:
            return movelist
        dest_piece = self.chessboard.boardArray[new_row][new_col]
        if dest_piece == " ":
            self.chessboard.boardArray[row][col] = " "
            self.chessboard.boardArray[new_row][new_col] = piece
            if self.chessboard.kingissafe():
                movelist += str(row) + str(col) + str(new_row) + str(new_col) + " "
            self.chessboard.boardArray[row][col] = piece
            self.chessboard.boardArray[new_row][new_col] = dest_piece
        elif dest_piece.islower():
            self.chessboard.boardArray[row][col] = " "
            self.chessboard.boardArray[new_row][new_col] = piece
            if self.chessboard.kingissafe():
                movelist += str(row) + str(col) + str(new_row) + str(new_col) + dest_piece
            self.chessboard.boardArray[row][col] = piece
            self.chessboard.boardArray[new_row][new_col] = dest_piece
        return movelist


    def testHorizontal(self, row, col, movelist):
        """
        Helper function to check if horizontal move is valid
        """
        board_size = len(self.chessboard.boardArray)
        for col_offset in [-1, 1]:
            for i in range(1, board_size):
                new_col = col + i * col_offset
                if new_col < 0 or new_col >= board_size:
                    break
                dest_piece = self.chessboard.boardArray[row][new_col]
                if dest_piece == " ":
                    movelist = self.testMove(row, col, 0, i*col_offset, "R", movelist)
                elif dest_piece.islower():
                    movelist = self.testMove(row, col, 0, i*col_offset, "R", movelist)
                    break
                else:
                    break
        return movelist

    def testVertical(self, row, col, movelist):
        """
        Helper function to check if vertical move is valid
        """
        board_size = len(self.chessboard.boardArray)
        for row_offset in [-1, 1]:
            for i in range(1, board_size):
                new_row = row + i * row_offset
                if new_row < 0 or new_row >= board_size:
                    break
                dest_piece = self.chessboard.boardArray[new_row][col]
                if dest_piece == " ":
                    movelist = self.testMove(row, col, i*row_offset, 0, "R", movelist)
                elif dest_piece.islower():
                    movelist = self.testMove(row, col, i*row_offset, 0, "R", movelist)
                    break
                else:
                    break
        return movelist


    def findMoveSet(self, index):
        """
        Goes through the potential moves a rook can make and if it's a safe move
        (The king is not in check) and a legal move, then that move is a potential move.
        Args: index: Current position of the board we are evaluating
        Returns: Move set of all potential moves rook can make
        """
        movelist = ""
        row = index//8
        column = index % 8
        for i in range(-1, 2, 2):
            movelist = self.testVertical(row, column, movelist)
            movelist = self.testHorizontal(row, column, movelist)
        return movelist

import itertools

class Knight(Piece):
    """
    Inherited peice class of the knight. This class includes all the methods
    used to evaluate all the moves that can be made by the knight
    """
    def findMoveSet(self, index):
        """
        Goes through the potential moves a knight can make and if it's a safe move
        (The king is not in check) and a legal move, then that move is a potential move.
        Args: index: Current position of the board we are evaluating
        Returns: Move set of all potential moves knight can make
        """
        movelist = []
        row = index//8
        column = index % 8
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                try:
                    if self.chessboard.boardArray[row+i][column+j*2] == " " or self.chessboard.boardArray[row+i][column+j*2].islower():
                        previousPosition = self.chessboard.boardArray[row+i][column+j*2]
                        self.chessboard.boardArray[row][column] = " "
                        self.chessboard.boardArray[row+i][column+j*2] = "K"
                        if self.chessboard.kingissafe()and row+i >= 0 and column+j*2 >= 0:
                            movelist.append(str(row)+str(column) + str(row+i) + str(column+j*2) + str(previousPosition))
                        self.chessboard.boardArray[row][column] = "K"
                        self.chessboard.boardArray[row+i][column+j*2] = previousPosition
                except IndexError:
                    pass
                try:
                    if self.chessboard.boardArray[row+i*2][column+j] == " " or self.chessboard.boardArray[row+i*2][column+j].islower():
                        previousPosition =self.chessboard.boardArray[row+i*2][column+j]
                        self.chessboard.boardArray[row][column] = " "
                        self.chessboard.boardArray[row+i*2][column+j] = "K"
                        if self.chessboard.kingissafe() and row+i*2 >= 0 and column+j >=0:
                            movelist.append(str(row)+str(column) + str(row+i*2) + str(column+j) + str(previousPosition))
                        self.chessboard.boardArray[row][column] = "K"
                        self.chessboard.boardArray[row+i*2][column+j] = previousPosition
                except IndexError:
                    pass
        return ''.join(movelist)


class Bishop(Piece):
    """
    Inherited peice class of the Bishop. This class includes all the methods
    used to evaluate all the moves that can be made by the Bishop
    """
    def checkDiagonal(self, movelist, row, column, i, j):
        """
        Helper function to check if diagonal move is valid
        """
        board_roamer = 1
        try:
            while(self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j] == " "):
                previousPosition = self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j]
                self.chessboard.boardArray[row][column] = " "
                self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j] = "B"
                if self.chessboard.kingissafe() and (row+board_roamer*i) >=0 and (column+board_roamer*j) >= 0:
                    movelist += str(row)+str(column)+str(row+board_roamer*i)+str(column+board_roamer*j)+str(previousPosition)
                self.chessboard.boardArray[row][column] = "B"
                self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j] = previousPosition
                board_roamer +=1
            if self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j].islower() :
                previousPosition = self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j]
                self.chessboard.boardArray[row][column] = " "
                self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j] = "B"
                if self.chessboard.kingissafe() and (row+board_roamer*i) >=0 and (column+board_roamer*j) >= 0:
                    movelist += str(row)+str(column)+str(row+board_roamer*i)+str(column+board_roamer*j)+str(previousPosition)
                self.chessboard.boardArray[row][column] = "B"
                self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j] = previousPosition
        except IndexError:
            pass
        return movelist
    def findMoveSet(self, index):
        """
        Goes through the potential moves a bishop can make and if it's a safe move
        (The king is not in check) and a legal move, then that move is a potential move.
        Args: index: Current position of the board we are evaluating
        Returns: Move set of all potential moves bishop can make
        """
        movelist = ""
        row = index//8
        column = index % 8
        for i in range(-1, 2, 2):
            for j in range(-1, 2,2):
                movelist = self.checkDiagonal(movelist, row, column, i, j)
        return movelist
class Queen(Piece):
    """
    Inherited peice class of the Queen. This class includes all the methods
    used to evaluate all the moves that can be made by the Queen
    """
    def testMovement(self, row, column, i, j, movelist):
        board_roamer = 1
        try:
            while(self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j] == " "):
                previousPosition = self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j]
                self.chessboard.boardArray[row][column] = " "
                self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j] = "Q"
                if self.chessboard.kingissafe() and (row+board_roamer*i) >=0 and (column+board_roamer*j) >= 0:
                    movelist += str(row)+str(column)+str(row+board_roamer*i)+str(column+board_roamer*j)+str(previousPosition)
                self.chessboard.boardArray[row][column] = "Q"
                self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j] = previousPosition
                board_roamer += 1
            if self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j].islower():
                previousPosition = self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j]
                self.chessboard.boardArray[row][column] = " "
                self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j] = "Q"
                if self.chessboard.kingissafe() and (row+board_roamer*i) >=0 and (column+board_roamer*j) >= 0:
                    movelist += str(row)+str(column)+str(row+board_roamer*i)+str(column+board_roamer*j)+str(previousPosition)
                self.chessboard.boardArray[row][column] = "Q"
                self.chessboard.boardArray[row+board_roamer*i][column+board_roamer*j] = previousPosition
        except IndexError:
            pass
        return movelist
    def findMoveSet(self, index):
        """
        Goes through the potential moves a Queen can make and if it's a safe move
        (The king is not in check) and a legal move, then that move is a potential move.
        Args: index: Current position of the board we are evaluating
        Returns: Move set of all potential moves Queen can make
        """
        movelist = ""
        row = index//8
        column = index % 8
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    movelist = self.testMovement(row, column, i, j, movelist)
        return movelist
class King(Piece):
    """
    Inherited peice class of the king. This class includes all the methods
    used to evaluate all the moves that can be made by the king
    """
    def testMove(self, index, row, column, i, movelist):
        try:
            if self.chessboard.boardArray[row - 1 + i//3][column-1+ i%3].islower() or self.chessboard.boardArray[row - 1 + i//3][column-1+ i%3] == " ":
                previousPosition = self.chessboard.boardArray[row - 1 + i//3][column-1+ i%3]
                self.chessboard.boardArray[row][column] = " "
                self.chessboard.boardArray[row - 1 + i//3][column-1+ i%3] = "A"
                kingTemp = self.chessboard.kingPosition_White
                self.chessboard.kingPosition_White = index+(i//3)*8 +i%3-9
                if self.chessboard.kingissafe() and row-1+i//3 >=0 and column-1+ i%3>=0:
                        movelist += str(row)+str(column)+str(row-1+i//3)+str(column-1+i%3)+str(previousPosition)
                self.chessboard.boardArray[row][column] = "A"
                self.chessboard.boardArray[row - 1 + i//3][column-1+ i%3] = previousPosition
                self.chessboard.kingPosition_White = kingTemp
        except IndexError:
            pass
        return movelist
    def findMoveSet(self, index):
        """
        Goes through the potential moves a king can make and if it's a safe move
        (The king is not in check) and a legal move, then that move is a potential move.
        Args: index: Current position of the board we are evaluating
        Returns: Move set of all potential moves king can make
        """
        movelist = ""
        row = index//8
        column = index % 8
        for i in range(9):
            if i != 4:
                movelist = self.testMove(index, row, column, i, movelist)
        return movelist
class Pawn(Piece):
    """
    Inherited peice class of the pawn. This class includes all the methods
    used to evaluate all the moves that can be made by the pawn
    """
    def testMovement(self, row, column, index, movelist):
        try:
            if self.chessboard.boardArray[row-1][column] == " " and index >= 16:
                previousPosition = self.chessboard.boardArray[row-1][column]
                self.chessboard.boardArray[row][column] = " "
                self.chessboard.boardArray[row-1][column] = "P"
                if self.chessboard.kingissafe() and (row-1) >= 0:
                    movelist += str(row) + str(column) + str(row-1) + str(column) + str(previousPosition)
                self.chessboard.boardArray[row][column] = "P"
                self.chessboard.boardArray[row-1][column] = previousPosition
        except IndexError:
            pass
        try:
            if self.chessboard.boardArray[row-1][column] == " " and self.chessboard.boardArray[row-2][column] == " " and index >= 48:
                previousPosition = self.chessboard.boardArray[row-2][column]
                self.chessboard.boardArray[row][column] = " "
                self.chessboard.boardArray[row-2][column] = "P"
                if self.chessboard.kingissafe() and row-2 >=0:
                    movelist += str(row) + str(column) + str(row-2) + str(column) + str(previousPosition)
                self.chessboard.boardArray[row][column] = "P"
                self.chessboard.boardArray[row-2][column] = previousPosition
        except IndexError:
            pass
        try:
            if self.chessboard.boardArray[row-1][column] == " " and index < 16:
                promotionList = ["Q", "R", "B", "K"]
                for promPiece in promotionList:
                    previousPosition = self.chessboard.boardArray[row-1][column]
                    self.chessboard.boardArray[row][column] = " "
                    self.chessboard.boardArray[row-1][column] = promPiece
                    if self.chessboard.kingissafe():
                        movelist += str(column) + str(column) + str(previousPosition) + str(promPiece) + "P"
                    self.chessboard.boardArray[row][column] = "P"
                    self.chessboard.boardArray[row-1][column] = previousPosition
        except IndexError:
            pass
        return movelist
    def testCapture(self, index, row, column, movelist):
        for i in range(-1, 2, 2):
            try:
                if self.chessboard.boardArray[row-1][column+i].islower():
                    if index < 16:
                        promotionList = ["Q", "R", "B", "K"]
                        for promPiece in promotionList:
                            previousPosition = self.chessboard.boardArray[row-1][column+i]
                            self.chessboard.boardArray[row][column] = " "
                            self.chessboard.boardArray[row-1][column+i] = promPiece
                            if self.chessboard.kingissafe() and (column+i) >= 0:
                                movelist += str(column) + str(column+i)+str(previousPosition)+str(promPiece)+"P"
                            self.chessboard.boardArray[row][column] = "P"
                            self.chessboard.boardArray[row-1][column+i] = previousPosition
                    else:
                        previousPosition = self.chessboard.boardArray[row-1][column+i]
                        self.chessboard.boardArray[row][column] = " "
                        self.chessboard.boardArray[row-1][column+i] = "P"
                        if self.chessboard.kingissafe() and (row-1) >= 0 and (column+i) >= 0:
                            movelist += str(row) + str(column) + str(row-1)+str(column+i) + str(previousPosition)
                        self.chessboard.boardArray[row][column] = "P"
                        self.chessboard.boardArray[row-1][column+i] = previousPosition
            except IndexError:
                pass
        return movelist
    def findMoveSet(self, index):
        """
        Goes through the potential moves a pawn can make and if it's a safe move
        (The king is not in check) and a legal move, then that move is a potential move.
        Args: index: Current position of the board we are evaluating
        Returns: Move set of all potential moves pawn can make
        """
        movelist = ""
        row = index//8
        column = index % 8
        movelist = self.testCapture(index, row, column, movelist)
        movelist = self.testMovement(row, column, index, movelist)
        return movelist

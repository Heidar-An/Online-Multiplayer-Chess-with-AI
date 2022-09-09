from chess.PieceMovements import Pawn, Knight, Bishop, Rook, Queen, King
import copy

bp = Pawn("b")
bk = King("b")
br = Rook("b")
bb = Bishop("b")
bq = Queen("b")
bn = Knight("b")

wp = Pawn("w")
wk = King("w")
wr = Rook("w")
wb = Bishop("w")
wq = Queen("w")
wn = Knight("w")


class Board:
    def __init__(self):
        self.board = [["" for i in range(8)] for j in range(8)]
        self.possible = [["" for i in range(8)] for j in range(8)]
        self.playerOneTurn = True
        self.otherPlayer = False
        position = [
            [br, bn, bb, bq, bk, bb, bn, br],
            [bp, bp, bp, bp, bp, bp, bp, bp],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            [wp, wp, wp, wp, wp, wp, wp, wp],
            [wr, wn, wb, wq, wk, wb, wn, wr]
        ]
        for i in range(8):
            for j in range(8):
                self.board[i][j] = position[i][j]

    def movePossible(self, mousePos, oldPieceX, oldPieceY):
        """Check if move is allowed"""

        # pieceX = column, pieceY = row
        pieceX, pieceY = mousePos
        pieceX, pieceY = pieceX // 70, (pieceY - 110) // 70
        playerMove = False
        
        # check if the move is possible for this piece
        if self.possible[pieceY][pieceX] == "green":
            kingInCheck = self.kingInCheck(self.board, self.playerOneTurn)
            if kingInCheck:
                # king is in check, now check if this move will make king not be in check
                if self.moveEndCheck(pieceX, pieceY, oldPieceX, oldPieceY, self.board, self.playerOneTurn) is False:
                    self.movePiece(pieceX, pieceY, oldPieceX, oldPieceY)
                    playerMove = True
                    self.playerOneTurn = not self.playerOneTurn
            else:
                self.movePiece(pieceX, pieceY, oldPieceX, oldPieceY)
                self.playerOneTurn = not self.playerOneTurn
                playerMove = True

        return playerMove

    def movePiece(self, newPieceX, newPieceY, oldPieceX, oldPieceY):
        """Move Piece on board"""
        # Castling function

        if self.board[oldPieceY][oldPieceX].type == "k" or self.board[oldPieceY][oldPieceX].type == "r":
            self.board[oldPieceY][oldPieceX].moved = True
            colour = self.board[oldPieceY][oldPieceX].colour
            if colour == "w":
                if oldPieceY == 7 and oldPieceX == 4:
                    if newPieceY == 7 and newPieceX == 6:
                        self.board[7][5] = self.board[7][7]
                        self.board[7][7] = ""
                    if newPieceY == 7 and newPieceX == 2:
                        self.board[7][3] = self.board[7][0]
                        self.board[7][0] = ""
            if colour == "b":
                if oldPieceY == 0 and oldPieceX == 4:
                    if newPieceY == 0 and newPieceX == 6:
                        self.board[0][5] = self.board[0][7]
                        self.board[0][7] = ""
                    if newPieceY == 0 and newPieceX == 2:
                        self.board[0][3] = self.board[0][0]
                        self.board[0][0] = ""

        # Promotion of pawn
        self.board[newPieceY][newPieceX] = self.board[oldPieceY][oldPieceX]
        if self.board[oldPieceY][oldPieceX].type == "p" and (newPieceY == 0 or newPieceY == 7):
            colour = self.board[oldPieceY][oldPieceX].colour
            if colour == "w":
                self.board[newPieceY][newPieceX] = wq
            elif colour == "b":
                self.board[newPieceY][newPieceX] = bq
        self.board[oldPieceY][oldPieceX] = ""
        self.possible = [["" for i in range(8)] for j in range(8)]

    def moveEndCheck(self, newPieceX, newPieceY, oldPieceX, oldPieceY, boardPosition, playerOneTurn):
        """checks if move sent to function would remove check, false means that the king won't be in check"""

        # make sure that pieces aren't empty
        if oldPieceX is None or oldPieceY is None:
            return
        boardPositionCopy = copy.deepcopy(boardPosition)
        boardPositionCopy[newPieceY][newPieceX] = boardPositionCopy[oldPieceY][oldPieceX]
        boardPositionCopy[oldPieceY][oldPieceX] = ""
        return self.kingInCheck(boardPositionCopy, playerOneTurn)

    def kingInCheck(self, boardPosition, playerOneTurn):
        # print("Yes, KingInCheck is being called")
        """"find out if king is in check"""
        kingColour = "b"
        if playerOneTurn:
            kingColour = "w"

        kingI, kingJ = self.findKingPos(boardPosition, playerOneTurn)

        # check diagonals around king
        diagonals = [[[kingI + i, kingJ + i] for i in range(1, 8)],
                     [[kingI + i, kingJ - i] for i in range(1, 8)],
                     [[kingI - i, kingJ + i] for i in range(1, 8)],
                     [[kingI - i, kingJ - i] for i in range(1, 8)]]
        for i in range(len(diagonals)):
            for j in range(len(diagonals[i])):
                posX = diagonals[i][j][0]
                posY = diagonals[i][j][1]
                if 0 <= posX < 8 and 0 <= posY < 8:
                    if boardPosition[posX][posY] != "":
                        if boardPosition[posX][posY].colour == kingColour:
                            continue
                        if boardPosition[posX][posY].colour != kingColour:
                            possibleCopy = [["" for i in range(8)] for j in range(8)]
                            possibleCopy = boardPosition[posX][posY].possibleMoves(diagonals[i][j][0],
                                                                                   diagonals[i][j][1], possibleCopy,
                                                                                   boardPosition)
                            # possibleCopy = pieceMoves(boardPosition[posX][posY].type, diagonals[i][j][0],
                            #                           diagonals[i][j][1], possibleCopy, boardPosition)
                            if possibleCopy[kingI][kingJ] == "green":
                                # kingInCheckCondition = True
                                return True

        # check horizontal / vertical around king
        cross = [[[kingI + i, kingJ] for i in range(1, 8 - kingI)],
                 [[kingI - i, kingJ] for i in range(1, kingI + 1)],
                 [[kingI, kingJ + i] for i in range(1, 8 - kingJ)],
                 [[kingI, kingJ - i] for i in range(1, kingJ + 1)]]
        for i in range(len(cross)):
            for j in range(len(cross[i])):
                posX = cross[i][j][0]
                posY = cross[i][j][1]
                if 0 <= posX < 8 and 0 <= posY < 8:
                    if boardPosition[posX][posY] != "":
                        if boardPosition[posX][posY].colour == kingColour:
                            continue
                        if boardPosition[posX][posY].colour != kingColour:
                            possibleCopy = [["" for i in range(8)] for j in range(8)]
                            possibleCopy = boardPosition[posX][posY].possibleMoves(cross[i][j][0],
                                                                                   cross[i][j][1], possibleCopy,
                                                                                   boardPosition)
                            if possibleCopy[kingI][kingJ] == "green":
                                return True

        # find knight movements around king
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i ** 2 + j ** 2 == 5:
                    if 0 <= kingI + i < 8 and 0 <= kingJ + j < 8:
                        posX = kingI + i
                        posY = kingJ + j
                        if boardPosition[posX][posY] != "":
                            if boardPosition[posX][posY].colour != kingColour:
                                if boardPosition[posX][posY].type == "n":
                                    possibleCopy = [["" for i in range(8)] for j in range(8)]
                                    possibleCopy = boardPosition[posX][posY].possibleMoves(posX,
                                                                                           posY, possibleCopy,
                                                                                           boardPosition)
                                    if possibleCopy[kingI][kingJ] == "green":
                                        return True
        return False

    def findKingPos(self, boardPosition, playerOneTurn):
        """finds the position of the king """
        kingI, kingJ = -1, -1
        checkColour = "b"
        if playerOneTurn:
            checkColour = "w"

        for i in range(8):
            for j in range(8):
                if boardPosition[i][j] != "" and boardPosition[i][j].colour == checkColour:
                    if boardPosition[i][j].type == "k":
                        kingI = i
                        kingJ = j
                        break
        return kingI, kingJ

    def getEval(self, boardPosition, playerOneTurn, fakePosition):
        """get the value of the board by adding up values of pieces"""
        evaluation = 0
        for i in range(8):
            for j in range(8):
                if boardPosition[i][j] != "":
                    evaluation += boardPosition[i][j].eval(i, j, playerOneTurn)

        if self.checkmateCheck(boardPosition, playerOneTurn):
            if playerOneTurn:
                evaluation += 900
            else:
                evaluation -= 900
        return evaluation

    def checkmateCheck(self, boardPosition, playerOneTurn):
        """Find out if there is a checkmate on the board"""
        checkColour = "b"
        if playerOneTurn:
            checkColour = "w"

        for i in range(8):
            for j in range(8):
                if boardPosition[i][j] != "":
                    if boardPosition[i][j].colour == checkColour:
                        possibleCopy = [["" for i in range(8)] for j in range(8)]
                        possibleCopy = boardPosition[i][j].possibleMoves(i, j, possibleCopy, boardPosition)
                        for k in range(8):
                            for m in range(8):
                                if possibleCopy[k][m] != "":
                                    if self.moveEndCheck(m, k, j, i, boardPosition, playerOneTurn) is False:
                                        return False

        return True

    def checkPlayerTurn(self, pos):
        """check who's turn it is"""
        column, row = pos
        column, row = column // 70, (row - 110) // 70

        colour = self.board[row][column].colour
        if (colour == "w" and self.playerOneTurn) or (colour == "b" and self.playerOneTurn is False):
            return True
        return False

    def checkPieceExists(self, pos):
        """check if there is a piece at certain position"""
        column, row = pos
        column, row = column // 70, (row - 110) // 70
        if self.board[row][column] == "":
            return False
        return True

    def getPosition(self):
        """get position of board"""
        return self.board

    def checkEmpty(self, i, j):
        """Check whether board is empty in position"""
        if self.board[i][j] == "":
            return True
        return False

    def setPossible(self, possible):
        """Set the value of possible moves"""
        self.possible = possible

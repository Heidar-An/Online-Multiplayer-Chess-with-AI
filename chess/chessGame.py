import pygame as pg
from pygame import *
import copy
import time


class Piece:
    """ Each piece is part of a class called Piece, where they are assigned important features"""

    def __init__(self, colour, inputType, inputImage, value, killable=False):
        self.colour = colour
        self.type = inputType
        if inputType == "k":
            self.moved = False
        if inputType == "r":
            self.moved = False
        self.killable = killable
        self.image = inputImage
        self.value = value


"""with values add them all up and take the negative of this"""
"""naming each piece, assigning it to the class and passing the image (which isn't that good yet)"""
bp = Piece("b", "p", "bp.svg", -10)
bk = Piece("b", "k", "bk.svg", 0)
br = Piece("b", "r", "br.svg", -50)
bb = Piece("b", "b", "bb.svg", -30)
bq = Piece("b", "q", "bq.svg", -90)
bn = Piece("b", "n", "bn.svg", -30)

wp = Piece("w", "p", "wp.svg", 10)
wk = Piece("w", "k", "wk.svg", 0)
wr = Piece("w", "r", "wr.svg", 50)
wb = Piece("w", "b", "wb.svg", 30)
wq = Piece("w", "q", "wq.svg", 90)
wn = Piece("w", "n", "wn.svg", 30)

"""some initialising things, colours, screen, global variables"""
display = [800, 800]
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
brown = (165, 42, 42)
green = (0, 128, 0)
pink = (255, 192, 203)
turquoise = (64, 224, 208)

possible = [["" for i in range(8)] for j in range(8)]
row = None
column = None
kingInCheckCondition = False
clock = pg.time.Clock()
whiteKingHasMoved = False
kingWillMove = False
playerMove = False
checkmateCondition = False
twoPlayer = False
AIPlayer = False

""" the board as an array """
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
"""
position[i][j], i represents the row, j represents the column
"""

pg.init()
window = pg.display.set_mode(display)
mediumFont = pg.font.SysFont("Helvetica", 28)


class Game:
    def __init__(self):
        """
        This is to create the board, I used a variable first to signify when the brown coloured block should be
        first, and it should just be white
        """

        window.fill(white)
        first = False
        for i in range(8):
            for j in range(8):
                if not first:
                    if j % 2 != 0:
                        rectangle = pg.Rect((j * 100), i * 100, 100, 100)
                        pg.draw.rect(window, brown, rectangle)
                if first:
                    if j % 2 == 0:
                        rectangle = pg.Rect((j * 100), i * 100, 100, 100)
                        pg.draw.rect(window, brown, rectangle)
            first = not first
        """
        This is where the pieces come onto the board
        """
        self.images()
        pg.display.update()

    def images(self):
        for i in range(8):
            for j in range(8):
                if position[i][j] != "":
                    img = pg.image.load(position[i][j].image).convert_alpha()
                    img = pg.transform.smoothscale(img, (100, 100))
                    window.blit(img, (j * 100, i * 100))


def kingEval(i, j, player):
    """kings evaluation at positions"""
    evals = [
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
        [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
        [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
        [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
        [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
    ]
    if player:
        evals.reverse()
    evalPos = evals[i][j]
    return evalPos


def bishopEval(i, j, player):
    evals = [
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
        [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
        [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
        [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
        [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
        [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
    ]
    if player:
        evals.reverse()
    evalPos = evals[i][j]
    return evalPos


def knightEval(i, j, player):
    evals = [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
        [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
        [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
        [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
        [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
        [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
    ]
    if player:
        evals.reverse()
    evalPos = evals[i][j]
    return evalPos


def pawnEval(i, j, player):
    evals = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
        [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
        [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
        [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
        [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
        [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ]
    if player:
        evals.reverse()
    evalPos = evals[i][j]
    return evalPos


def queenEval(i, j, player):
    evals = [
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
        [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
        [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
        [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
    ]

    if player:
        evals.reverse()
    evalPos = evals[i][j]
    return evalPos


def rookEval(i, j, player):
    evals = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
        [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
    ]
    if player:
        evals.reverse()
    evalPos = evals[i][j]
    return evalPos


def getEvaluation(positionCheck, condition, test):
    """get the value of the board by adding up values of pieces"""
    """condition = True if AIs turn"""
    evaluation = 0
    for i in range(8):
        for j in range(8):
            if positionCheck[i][j] != "":
                if positionCheck[i][j].type == "k":
                    evaluation += kingEval(i, j, condition)
                if positionCheck[i][j].type == "q":
                    evaluation += queenEval(i, j, condition)
                if positionCheck[i][j].type == "r":
                    evaluation += rookEval(i, j, condition)
                if positionCheck[i][j].type == "b":
                    evaluation += bishopEval(i, j, condition)
                if positionCheck[i][j].type == "n":
                    evaluation += knightEval(i, j, condition)
                if positionCheck[i][j].type == "p":
                    evaluation += pawnEval(i, j, condition)
                evaluation += positionCheck[i][j].value
    if checkmate(positionCheck, condition, test):
        if condition:
            evaluation += 900
        else:
            evaluation -= 900
    return evaluation


def check_piece(pos):
    """checks whether there is a piece where the mouse is clicking"""
    x, y = pos
    checkColumn = x // 100
    checkRow = y // 100
    if position[checkRow][checkColumn] != "":
        return True
    else:
        return False


def checkPlayer(rowCheck, columnCheck):
    """checks if player can move this turn"""
    colour = position[rowCheck][columnCheck].colour
    if (colour == "w" and player1) or (colour == "b" and player1 is False):
        return True
    return False


def check(checkRow, checkColumn):
    """checks if this row and column is valid, used when looking at possible piece movement"""
    if 0 <= checkRow <= 7 and 0 <= checkColumn <= 7:
        return True
    return False


def checkmate(positionCheck, condition, test):
    """checks if there is a checkmate"""
    global checkmateCondition
    if condition:
        checkColour = "w"
    else:
        checkColour = "b"
    findKing(positionCheck)
    """to make this more efficient, instead of checking every square, make it the 8 directions around it."""
    for i in range(8):
        for j in range(8):
            if positionCheck[i][j] != "":
                if positionCheck[i][j].colour == checkColour:
                    possibleCopy = [["" for i in range(8)] for j in range(8)]
                    possibleCopy = pieceMoves(positionCheck[i][j].type, i, j, possibleCopy, positionCheck)
                    for k in range(8):
                        for m in range(8):
                            if possibleCopy[k][m] != "":
                                if moveEndCheckPosition(m, k, j, i, positionCheck, condition) is False:
                                    return False
    if test is False:
        checkmateCondition = True
    return True


def moves(possibleMoves):
    """shows all the possible moves available"""
    Game()
    for i in range(8):
        for j in range(8):
            if possibleMoves[i][j] != "":
                pg.draw.circle(window, green, (j * 100 + 50, (i * 100 + 50)), 10)
    pg.display.update()


def findKing(positionCheck):
    """finds the position of the king"""
    kingI = -1
    kingJ = -1
    if player1:
        checkColour = "w"
    else:
        checkColour = "b"
    for i in range(8):
        for j in range(8):
            if positionCheck[i][j] != "":
                if positionCheck[i][j].type == "k" and positionCheck[i][j].colour == checkColour:
                    kingI = i
                    kingJ = j
                    break
    return kingI, kingJ


def kingInCheck(positionCheck, condition):
    """check if king is in check"""
    global kingInCheckCondition
    kingInCheckCondition = False
    if condition:
        checkColour = "w"
    else:
        checkColour = "b"
    kingI, kingJ = findKing(positionCheck)

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
                if positionCheck[posX][posY] != "":
                    if positionCheck[posX][posY].colour == checkColour:
                        continue
                    if positionCheck[posX][posY].colour != checkColour:
                        possibleCopy = [["" for i in range(8)] for j in range(8)]
                        possibleCopy = pieceMoves(positionCheck[posX][posY].type, diagonals[i][j][0],
                                                  diagonals[i][j][1], possibleCopy, positionCheck)
                        if possibleCopy[kingI][kingJ] == "green":
                            kingInCheckCondition = True
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
                if positionCheck[posX][posY] != "":
                    if positionCheck[posX][posY].colour == checkColour:
                        continue
                    if positionCheck[posX][posY].colour != checkColour:
                        possibleCopy = [["" for i in range(8)] for j in range(8)]
                        possibleCopy = pieceMoves(positionCheck[posX][posY].type, cross[i][j][0],
                                                  cross[i][j][1], possibleCopy, positionCheck)
                        if possibleCopy[kingI][kingJ] == "green":
                            kingInCheckCondition = True
                            return True
    # find knight movements around king
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if 0 <= kingI + i < 8 and 0 <= kingJ + j < 8:
                    posX = kingI + i
                    posY = kingJ + j
                    if positionCheck[posX][posY] != "":
                        if positionCheck[posX][posY].colour != checkColour:
                            if positionCheck[posX][posY].type == "n":
                                possibleCopy = [["" for i in range(8)] for j in range(8)]
                                possibleCopy = pieceMoves(positionCheck[posX][posY].type, posX,
                                                          posY, possibleCopy, positionCheck)
                                if possibleCopy[kingI][kingJ] == "green":
                                    kingInCheckCondition = True
                                    return True

    return kingInCheckCondition


def moveEndCheck(newColumn, newRow, positionCheck, condition):
    """checks if move sent to function would remove check, false means that the king won't be in check"""
    positionCopy = copy.deepcopy(positionCheck)
    # print(row, column, newRow, newColumn)
    if row is None or column is None:
        return
    positionCopy[newRow][newColumn] = positionCopy[row][column]
    positionCopy[row][column] = ""
    return kingInCheck(positionCopy, condition)


def moveEndCheckPosition(newColumn, newRow, oldColumn, oldRow, positionCheck, condition):
    """checks if move sent to function would remove check used for checkmate function, false means that the king
    won't be in check """
    positionCopy = copy.deepcopy(positionCheck)
    # print(row, column, newRow, newColumn)
    positionCopy[newRow][newColumn] = positionCopy[oldRow][oldColumn]
    positionCopy[oldRow][oldColumn] = ""
    return kingInCheck(positionCopy, condition)


def pawnCheck(row, column, possibleMoves, positionCheck):
    """make sure that it is player1's turn, as there are different cases for a black or white pawn"""
    currentColour = positionCheck[row][column].colour
    if currentColour == "w":
        if check(row - 1, column):
            if positionCheck[row - 1][column] == "":
                possibleMoves[row - 1][column] = "green"
        """if the row = 6, the pawn is allowed to move two pieces up."""
        if row == 6:
            if positionCheck[row - 1][column] == "" and positionCheck[row - 2][column] == "":
                possibleMoves[row - 2][column] = "green"
        """check if there is an enemy to the top left or top right of the pawn"""
        if check(row - 1, column - 1):
            if positionCheck[row - 1][column - 1] != "" and positionCheck[row - 1][column - 1].colour == "b":
                possibleMoves[row - 1][column - 1] = "green"
        if check(row - 1, column + 1):
            if positionCheck[row - 1][column + 1] != "" and positionCheck[row - 1][column + 1].colour == "b":
                possibleMoves[row - 1][column + 1] = "green"

    """do the same as what happened to white, but with a black pawn now"""
    if currentColour == "b":
        if check(row + 1, column):
            if positionCheck[row + 1][column] == "":
                possibleMoves[row + 1][column] = "green"
        if row == 1:
            if positionCheck[row + 1][column] == "" and positionCheck[row + 2][column] == "":
                possibleMoves[row + 2][column] = "green"
        if check(row + 1, column - 1):
            if positionCheck[row + 1][column - 1] != "" and positionCheck[row + 1][column - 1].colour == "w":
                possibleMoves[row + 1][column - 1] = "green"
        if check(row + 1, column + 1):
            if positionCheck[row + 1][column + 1] != "" and positionCheck[row + 1][column + 1].colour == "w":
                possibleMoves[row + 1][column + 1] = "green"
    return possibleMoves


def knightCheck(row, column, possibleMoves, positionCheck):
    """show all possible knight moves"""
    colour = positionCheck[row][column].colour
    for i in range(-2, 3):
        for j in range(-2, 3):
            """use pythagoras"""
            if i ** 2 + j ** 2 == 5:
                if check(row + i, column + j):
                    if positionCheck[row + i][column + j] == "":
                        possibleMoves[row + i][column + j] = "green"
                    elif positionCheck[row + i][column + j].colour != colour:
                        positionCheck[row + i][column + j].killable = True
                        possibleMoves[row + i][column + j] = "green"
    return possibleMoves


def bishopCheck(row, column, possibleMoves, positionCheck):
    """find all possible bishop moves"""
    """there are four loops because there are two possible diagonals """
    temp = column
    colour = positionCheck[row][column].colour
    """check top left diagonal"""
    for i in range(row - 1, -1, -1):
        temp -= 1
        if check(row, temp):
            if (colour == "w") or (colour == "b"):
                if positionCheck[i][temp] == "":
                    possibleMoves[i][temp] = "green"
                elif positionCheck[i][temp].colour != colour:
                    positionCheck[i][temp].killable = True
                    possibleMoves[i][temp] = "green"
                    break
                else:
                    break
    temp = column
    """check bottom right diagonal"""
    for i in range(row + 1, 8):
        temp += 1
        if check(row, temp):
            if (colour == "w") or (colour == "b"):
                if positionCheck[i][temp] == "":
                    possibleMoves[i][temp] = "green"
                elif positionCheck[i][temp].colour != colour:
                    positionCheck[i][temp].killable = True
                    possibleMoves[i][temp] = "green"
                    break
                else:
                    break
    """"check top right diagonal"""
    temp = column
    for i in range(row - 1, -1, -1):
        temp += 1
        if check(row, temp):
            if (colour == "w") or (colour == "b"):
                if positionCheck[i][temp] == "":
                    possibleMoves[i][temp] = "green"
                elif positionCheck[i][temp].colour != colour:
                    positionCheck[i][temp].killable = True
                    possibleMoves[i][temp] = "green"
                    break
                else:
                    break
    """check bottom left diagonal"""
    temp = column
    for i in range(row + 1, 8):
        temp -= 1
        if check(row, temp):
            if (colour == "w") or (colour == "b"):
                if positionCheck[i][temp] == "":
                    possibleMoves[i][temp] = "green"
                elif positionCheck[i][temp].colour != colour:
                    positionCheck[i][temp].killable = True
                    possibleMoves[i][temp] = "green"
                    break
                else:
                    break
    return possibleMoves


def rookCheck(row, column, possibleMoves, positionCheck):
    """find all possible rook moves"""
    colour = positionCheck[row][column].colour
    """check up direction"""
    for i in range(row - 1, -1, -1):
        if (colour == "w") or (colour == "b"):
            if positionCheck[i][column] == "":
                possibleMoves[i][column] = "green"
            elif positionCheck[i][column].colour != colour:
                possibleMoves[i][column] = "green"
                break
            else:
                break
    """check down direction"""
    for i in range(row + 1, 8):
        if (colour == "w") or (colour == "b"):
            if positionCheck[i][column] == "":
                possibleMoves[i][column] = "green"
            elif positionCheck[i][column].colour != colour:
                possibleMoves[i][column] = "green"
                break
            else:
                break

    """check right direction"""
    for i in range(column + 1, 8):
        if (colour == "w") or (colour == "b"):
            if positionCheck[row][i] == "":
                possibleMoves[row][i] = "green"
            elif positionCheck[row][i].colour != colour:
                possibleMoves[row][i] = "green"
                break
            else:
                break

    """check left direction"""
    for i in range(column - 1, -1, -1):
        if (colour == "w") or (colour == "b"):
            if positionCheck[row][i] == "":
                possibleMoves[row][i] = "green"
            elif positionCheck[row][i].colour != colour:
                possibleMoves[row][i] = "green"
                break
            else:
                break
    return possibleMoves


def kingCheck(row, column, possibleMoves, positionCheck):
    global kingWillMove
    colour = positionCheck[row][column].colour
    """all king moves"""
    for i in range(-1, 2):
        for j in range(-1, 2):
            if check(row + i, column + j):
                if positionCheck[row + i][column + j] == "":
                    possibleMoves[row + i][column + j] = "green"
                elif positionCheck[row + i][column + j].colour != colour:
                    possibleMoves[row + i][column + j] = "green"
    """Castling"""
    if colour == "w":
        if row == 7 and column == 4:
            if positionCheck[7][4].moved is False:
                if positionCheck[7][5] == "" and positionCheck[7][6] == "" and positionCheck[7][7] != "":
                    if positionCheck[7][7].type == "r":
                        if positionCheck[7][7].moved is False:
                            possibleMoves[7][6] = "green"
                            kingWillMove = True
                if positionCheck[7][3] == "" and positionCheck[7][2] == "" and positionCheck[7][1] == "" and \
                        positionCheck[7][0] != "":
                    if positionCheck[7][0].type == "r":
                        if positionCheck[7][0].moved is False:
                            possibleMoves[7][2] = "green"
                            kingWillMove = True
    if colour == "b":
        if row == 0 and column == 4:
            if positionCheck[0][4].moved is False:
                if positionCheck[0][5] == "" and positionCheck[0][6] == "" and positionCheck[0][7] != "":
                    if positionCheck[0][7].type == "r":
                        if positionCheck[0][7].moved is False:
                            possibleMoves[0][6] = "green"
                            kingWillMove = True
                if positionCheck[0][3] == "" and positionCheck[0][2] == "" and positionCheck[0][1] == "" and \
                        positionCheck[0][0] != "":
                    if positionCheck[0][0].type == "r":
                        if positionCheck[0][0].moved is False:
                            possibleMoves[0][2] = "green"
                            kingWillMove = True

    return possibleMoves


def pieceMoves(pieceType, row, column, possibleMoves, positionCheck):
    """each piece will have different possible moves, this calls the correct one"""

    if pieceType == "p":
        return pawnCheck(row, column, possibleMoves, positionCheck)

    elif pieceType == "n":
        return knightCheck(row, column, possibleMoves, positionCheck)

    elif pieceType == "b":
        return bishopCheck(row, column, possibleMoves, positionCheck)

    elif pieceType == "r":
        return rookCheck(row, column, possibleMoves, positionCheck)

    elif pieceType == "q":
        possibleMoves = bishopCheck(row, column, possibleMoves, positionCheck)
        return rookCheck(row, column, possibleMoves, positionCheck)

    elif pieceType == "k":
        return kingCheck(row, column, possibleMoves, positionCheck)


def movePiece(moveX, moveY):
    global player1
    Game()
    """castling"""
    if position[row][column].type == "k" or position[row][column].type == "r":
        position[row][column].moved = True
        colour = position[row][column].colour
        if colour == "w":
            if row == 7 and column == 4:
                if moveY == 7 and moveX == 6:
                    position[7][5] = position[7][7]
                    position[7][7] = ""
                if moveY == 7 and moveX == 2:
                    position[7][3] = position[7][0]
                    position[7][0] = ""
        if colour == "b":
            if row == 0 and column == 4:
                if moveY == 0 and moveX == 6:
                    position[0][5] = position[0][7]
                    position[0][7] = ""
                if moveY == 0 and moveX == 2:
                    position[0][3] = position[0][0]
                    position[0][0] = ""
    """promotion of pawn"""
    position[moveY][moveX] = position[row][column]
    if position[row][column].type == "p" and (moveY == 0 or moveY == 7):
        colour = position[row][column].colour
        if colour == "w":
            position[moveY][moveX] = wq
        elif colour == "b":
            position[moveY][moveX] = bq
    position[row][column] = ""
    player1 = not player1
    Game()


def checkmateCheck(condition):
    global font, textPrint, text, checkmateCondition
    if checkmate(position, condition, False):
        font = pg.font.SysFont("Helvetica", 75)
        if player1:
            textPrint = "Player 2 Won!"
        else:
            textPrint = "Player 1 Won!"
        text = font.render(textPrint, True, turquoise)
        window.blit(text, (display[0] // 4, display[1] // 4))
        pg.display.update()
        checkmateCondition = True
        return True
    return False


def AIMinimax(positionCheck, alpha, beta, depth, maximise):
    # maximise is True when it's AI's turn
    if maximise:
        maxValue = 9999
        evaluationCheck = getEvaluation(positionCheck, True, True)
    else:
        maxValue = -9999
        evaluationCheck = getEvaluation(positionCheck, False, True)
    if evaluationCheck >= 900 or evaluationCheck <= -900 or depth == 0:
        return evaluationCheck

    for i in range(8):
        for j in range(8):
            if positionCheck[i][j] != "":
                if (positionCheck[i][j].colour == "b" and maximise) or (
                        maximise is False and positionCheck[i][j].colour == "w"):
                    possibleCopy = [["" for i in range(8)] for j in range(8)]
                    possibleCopy = pieceMoves(positionCheck[i][j].type, i, j, possibleCopy, positionCheck)
                    if not any("green" in checkRow for checkRow in possibleCopy):
                        continue
                    for x in range(8):
                        for y in range(8):
                            if possibleCopy[x][y] == "green":
                                positionCopy = copy.deepcopy(positionCheck)
                                positionCopy[x][y] = positionCheck[i][j]
                                positionCopy[i][j] = ""
                                if maximise:
                                    if kingInCheck(positionCopy, False) is False:
                                        newEval = AIMinimax(positionCopy, alpha, beta, depth - 1, not maximise)
                                        maxValue = min(newEval, maxValue)
                                        beta = min(beta, maxValue)
                                        if beta <= alpha:
                                            return maxValue
                                else:
                                    if kingInCheck(positionCopy, True) is False:
                                        newEval = AIMinimax(positionCopy, alpha, beta, depth - 1, not maximise)
                                        maxValue = max(newEval, maxValue)
                                        alpha = max(alpha, maxValue)
                                        if beta <= alpha:
                                            return maxValue

    return maxValue


def mainAIFunction(positionCheck):
    global row, column, newY, newX
    evaluation = 10000
    rowMove, columnMove = -1, -1
    previousRow, previousColumn = 0, 0
    if checkmateCondition:
        return 0
    for i in range(8):
        for j in range(8):
            if positionCheck[i][j] != "":
                if positionCheck[i][j].colour == "b":
                    possibleCopy = [["" for i in range(8)] for j in range(8)]
                    possibleCopy = pieceMoves(positionCheck[i][j].type, i, j, possibleCopy, positionCheck)
                    if not any("green" in row for row in possibleCopy):
                        continue
                    for x in range(8):
                        for y in range(8):
                            if possibleCopy[x][y] == "green":
                                positionCopy = copy.deepcopy(positionCheck)
                                positionCopy[x][y] = positionCheck[i][j]
                                positionCopy[i][j] = ""
                                if kingInCheck(positionCopy, False) is False:
                                    newEval = AIMinimax(positionCopy, -10000, 10000, 2, False)
                                    if newEval <= evaluation:
                                        evaluation = newEval
                                        rowMove, columnMove = x, y
                                        previousRow, previousColumn = i, j
    row, column = previousRow, previousColumn
    movePiece(columnMove, rowMove)


def mainMoveFunction():
    global newPos, playerMove, newX, newY
    newPos = pg.mouse.get_pos()
    newX, newY = newPos
    newX, newY = newX // 100, newY // 100
    """hint: newX = column, newY = row"""

    """make sure that the king will not be in check as a result of this move"""
    if moveEndCheck(newX, newY, position, player1) is False:
        if possible[newY][newX] == "green" and kingInCheck(position, player1) is False:
            """make sure that move is possible and king is not currently in check"""
            movePiece(newX, newY)
            playerMove = False
        elif kingInCheck(position, player1) and possible[newY][newX] == "green":
            """ if the move is possible but the king is in check"""
            if moveEndCheck(newX, newY, position, player1) is False:
                movePiece(newX, newY)
                playerMove = False


"""mouse click is registered and then dealt with / pieces are moved"""

player1 = True
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            break
        elif twoPlayer is False and AIPlayer is False:
            """display buttons"""
            window.fill(black)

            widthCheck = display[0]
            heightCheck = display[1]
            playAIButton = pg.Rect((widthCheck / 8), (heightCheck / 2), widthCheck / 4, 50)
            playAI = mediumFont.render("Against AI", True, black)
            playAIRect = playAI.get_rect()
            playAIRect.center = playAIButton.center
            pg.draw.rect(window, white, playAIButton)
            window.blit(playAI, playAIRect)

            playTwoButton = pg.Rect(5 * (widthCheck / 8), (heightCheck / 2), widthCheck / 4, 50)
            playTwo = mediumFont.render("Same computer", True, black)
            playTwoRect = playTwo.get_rect()
            playTwoRect.center = playTwoButton.center
            pg.draw.rect(window, white, playTwoButton)
            window.blit(playTwo, playTwoRect)
            pg.display.update()
            """if the mouse clicks button then assign what game to play"""
            click, _, _ = pg.mouse.get_pressed()
            if click == 1:
                mouse = pg.mouse.get_pos()
                if playTwoButton.collidepoint(mouse):
                    twoPlayer = True
                    time.sleep(0.6)
                    Game()
                    pg.display.update()
                elif playAIButton.collidepoint(mouse):
                    AIPlayer = True
                    time.sleep(0.6)
                    Game()
                    pg.display.update()
        elif event.type == MOUSEBUTTONDOWN and checkmateCondition is False and AIPlayer:
            """moves system for AI"""
            # print(moveChecker(position, 0, 3, True))
            if playerMove and player1:
                mainMoveFunction()
                if checkmateCheck(player1):
                    break
            possible = [["" for i in range(8)] for j in range(8)]
            pos = pg.mouse.get_pos()
            column, row = pos[0] // 100, pos[1] // 100
            if check_piece(pos) and checkPlayer(row, column):
                playerMove = True
                kingWillMove = False
                Game()
                piece = position[row][column].type
                possible = pieceMoves(piece, row, column, possible, position)
            moves(possible)
            if player1 is False:
                mainAIFunction(position)
                checkmateCheck(player1)
                Game()
            continue
        elif event.type == MOUSEBUTTONUP and checkmateCondition is False and AIPlayer:
            """when the mouse is lifted, then the piece pressed originally is checked if it can move in the new 
            position """
            mainMoveFunction()
            continue
        elif event.type == MOUSEBUTTONDOWN and checkmateCondition is False and twoPlayer:
            """move system for chess on the same computer"""
            """ if the mouse is pressed down, then the piece is found, and then it goes to that function"""
            if playerMove:
                # print(newPos)
                mainMoveFunction()
            possible = [["" for i in range(8)] for j in range(8)]
            pos = pg.mouse.get_pos()
            column, row = pos[0] // 100, pos[1] // 100
            if check_piece(pos) and checkPlayer(row, column):
                playerMove = True
                kingWillMove = False
                Game()
                piece = position[row][column].type
                possible = pieceMoves(piece, row, column, possible, position)
            moves(possible)
            continue
        elif event.type == MOUSEBUTTONUP and checkmateCondition is False and twoPlayer:
            """when the mouse is lifted, then the piece pressed originally is checked if it can move in the new 
            position """
            mainMoveFunction()
            continue
        checkmateCheck(player1)
        if AIPlayer and player1 is False:
            mainAIFunction(position)

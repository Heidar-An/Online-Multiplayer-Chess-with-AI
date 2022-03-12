import pygame as pg ## used for display and graphics ##
from pygame import * ## so the program does not need to say pygame.something##
from chess.layoutBoardObject import Board ## imports the board class ##
from chess.client import Client ## imports the client class ##
import time ## imports time so it can be used for the timer of each player ##
import copy ## used to copy variables and arrays and not change the original variable ##

chessBoard = Board()


# defining colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
TURQUOISE = (64, 224, 208)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
BoardColour = (165, 42, 42)

display = [800, 800]

# defining some datastructures and variables
onlinePossible = [["" for i in range(8)] for j in range(8)]
onlineBoardPosition = [["" for x in range(8)] for y in range(8)]
onlineBoardObject, onlinePreviousBoardPosition = None, onlineBoardPosition
clock = pg.time.Clock()
row, column = None, None

whiteKingHasMoved, kingWillMove = False, False
playerMove, checkmateCondition, twoPlayer, AIPlayer, onlinePlayer, playerMode = False, False, False, False, False, False
changeColor, AiDifficulty = False, False
networkClient, onlinePlayerOneTurn, onlineColourId = None, None, ""
AiDepth, seconds = 2, 0

rDrag, gDrag, bDrag = False, False, False
rXPos = (display[0] // 8) + 30
gXPos = (display[0] // 8) + 30
bXPos = (display[0] // 8) + 30
rCol, gCol, bCol = 0, 0, 0

previousTime = time.time()
playerOneTime, playerTwoTime = 600, 600
playerOneMin, playerOneSec = divmod(playerOneTime, 60)
playerTwoMin, playerTwoSec = divmod(playerTwoTime, 60)
timeSeconds = 0

pg.init()
window = pg.display.set_mode(display, pg.RESIZABLE)
mediumFont = pg.font.SysFont("Helvetica", 28)

def updateChessScreen():
    """used to create the chessboard and call updateImages"""
    window.fill(BLACK)
    for j in range(8):
        for i in range(8):
            if (i + j) % 2 == 0:
                rectangle = pg.Rect(i * 70, j * 70 + 110, 70, 70)
                pg.draw.rect(window, BoardColour, rectangle)
            else:
                rectangle = pg.Rect(i * 70, j * 70 + 110, 70, 70)
                pg.draw.rect(window, WHITE, rectangle)


    # put chess images on the screen
    updateImages()
    pg.display.update()


def updateImages():
    """used to add images to the chessboard"""
    currentBoard = chessBoard.board
    if networkClient is not None:
        currentBoard = networkClient.chessBoard.board
    for i in range(8):
        for j in range(8):
            if currentBoard[j][i] != "":
                img = pg.image.load(currentBoard[j][i].image).convert_alpha()
                img = pg.transform.smoothscale(img, (68, 68))
                window.blit(img, (i * 70, j * 70 + 110))


def getEvaluation(positionCheck, condition, fakePosition):
    """get the value of the board by adding up values of pieces"""
    # condition = True if AIs turn / Not Player One Turn
    # fakePosition is whether this is for the real position, or one that the AI is checking
    return chessBoard.getEval(positionCheck, condition, fakePosition)


def checkPiece(mousePos):
    """checks whether there is a piece where the mouse is clicking"""
    return chessBoard.checkPieceExists(mousePos)


def check(checkRow, checkColumn):
    """checks if this row and column is valid, used when looking at possible piece movement"""
    if 0 <= checkRow <= 7 and 0 <= checkColumn <= 7:
        return True
    return False


def checkmate(boardPosition, playerOneTurn, test):
    """checks if there is a checkmate"""
    global checkmateCondition

    if chessBoard.checkmateCheck(boardPosition, playerOneTurn):
        if test is False:
            checkmateCondition = True
        return True
    return False


def moves(possibleMoves):
    """shows all the possible moves available"""
    updateChessScreen()
    for i in range(8):
        for j in range(8):
            if possibleMoves[i][j] != "":
                pg.draw.circle(window, GREEN, (j * 70 + 35, i * 70 + 110 + 35), 7)
    pg.display.update()


def findKing(boardPosition):
    """finds the position of the king"""
    return chessBoard.findKingPos(boardPosition, chessBoard.playerOneTurn)


def kingInCheck(boardPosition, playerOneTurn):
    """check if king is in check"""

    return chessBoard.kingInCheck(boardPosition, playerOneTurn)


def moveEndCheck(newColumn, newRow, boardPosition, playerOneTurn):
    """checks if move sent to function would remove check, false means that the king won't be in check"""

    return chessBoard.moveEndCheck(newColumn, newRow, row, column, boardPosition, playerOneTurn)


def moveEndCheckPosition(newColumn, newRow, oldColumn, oldRow, boardPosition, playerOneTurn):
    """checks if move sent to function would remove check used for checkmate function, false means that the king
    won't be in check """
    return chessBoard.moveEndCheck(newColumn, newRow, oldRow, oldColumn, boardPosition, playerOneTurn)


# def kingCheck(row, column, possibleMoves, positionCheck):
#     """Get king's possible moves"""
#     global kingWillMove
#     colour = positionCheck[row][column].colour
#     # all king moves
#     for i in range(-1, 2):
#         for j in range(-1, 2):
#             if check(row + i, column + j):
#                 if positionCheck[row + i][column + j] == "":
#                     possibleMoves[row + i][column + j] = "green"
#                 elif positionCheck[row + i][column + j].colour != colour:
#                     possibleMoves[row + i][column + j] = "green"
#     # Castling
#     if colour == "w":
#         if row == 7 and column == 4:
#             if positionCheck[7][4].moved is False:
#                 if positionCheck[7][5] == "" and positionCheck[7][6] == "" and positionCheck[7][7] != "":
#                     if positionCheck[7][7].type == "r":
#                         if positionCheck[7][7].moved is False:
#                             possibleMoves[7][6] = "green"
#                             kingWillMove = True
#                 if positionCheck[7][3] == "" and positionCheck[7][2] == "" and positionCheck[7][1] == "" and \
#                         positionCheck[7][0] != "":
#                     if positionCheck[7][0].type == "r":
#                         if positionCheck[7][0].moved is False:
#                             possibleMoves[7][2] = "green"
#                             kingWillMove = True
#     if colour == "b":
#         if row == 0 and column == 4:
#             if positionCheck[0][4].moved is False:
#                 if positionCheck[0][5] == "" and positionCheck[0][6] == "" and positionCheck[0][7] != "":
#                     if positionCheck[0][7].type == "r":
#                         if positionCheck[0][7].moved is False:
#                             possibleMoves[0][6] = "green"
#                             kingWillMove = True
#                 if positionCheck[0][3] == "" and positionCheck[0][2] == "" and positionCheck[0][1] == "" and \
#                         positionCheck[0][0] != "":
#                     if positionCheck[0][0].type == "r":
#                         if positionCheck[0][0].moved is False:
#                             possibleMoves[0][2] = "green"
#                             kingWillMove = True
#
#     return possibleMoves


def pieceMoves(pieceY, pieceX, possibleMoves, boardPosition):
    """each piece will have different possible moves, this calls the correct one"""
    return chessBoard.board[pieceY][pieceX].possibleMoves(pieceY, pieceX, possibleMoves, boardPosition)


def changeColorMenu(events):
    """Show the sliders for changing colour of the board"""
    global rDrag, gDrag, bDrag, rXPos, gXPos, bXPos, rCol, gCol, bCol, changeColor, BoardColour

    window.fill(WHITE)

    widthCheck = display[0]
    heightCheck = display[1]
    xStart = (widthCheck // 8) + 30

    # Text
    currentColorText = mediumFont.render("Current Color", True, BLACK)
    window.blit(currentColorText, (widthCheck // 3 + 50, 20))

    rgbSentence = "RGB: (" + str(rCol) + ", " + str(gCol) + ", " + str(bCol) + ")"
    rgbText = mediumFont.render(rgbSentence, True, BLACK)
    window.blit(rgbText, (widthCheck // 3 + 50, 290))

    rText = mediumFont.render("R: ", True, BLACK)
    gText = mediumFont.render("G: ", True, BLACK)
    bText = mediumFont.render("B: ", True, BLACK)
    window.blit(rText, (xStart - 50, heightCheck // 2 + 45))
    window.blit(gText, (xStart - 50, (heightCheck // 2) + 125))
    window.blit(bText, (xStart - 50, (heightCheck // 2) + 205))

    # Sliders to control colors
    rectWidth = 255 * 2
    rRect = Rect(xStart, heightCheck // 2 + 50, rectWidth + 30, heightCheck // 30)
    gRect = Rect(xStart, (heightCheck // 2) + 130, rectWidth + 30, heightCheck // 30)
    bRect = Rect(xStart, (heightCheck // 2) + 210, rectWidth + 30, heightCheck // 30)

    pg.draw.rect(window, GREY, rRect)
    pg.draw.rect(window, GREY, gRect)
    pg.draw.rect(window, GREY, bRect)

    rSlide = Rect(rXPos, heightCheck // 2 + 50, 30, heightCheck // 30)
    gSlide = Rect(gXPos, (heightCheck // 2) + 130, 30, heightCheck // 30)
    bSlide = Rect(bXPos, (heightCheck // 2) + 210, 30, heightCheck // 30)

    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            if rSlide.collidepoint(event.pos):
                rDrag = True
            if gSlide.collidepoint(event.pos):
                gDrag = True
            if bSlide.collidepoint(event.pos):
                bDrag = True
        if event.type == pg.MOUSEBUTTONUP and (rDrag or gDrag or bDrag):
            mousePos = pg.mouse.get_pos()

            if mousePos[0] > rRect.right:
                if rDrag:
                    rXPos = rRect.right - 30
                elif gDrag:
                    gXPos = gRect.right - 30
                elif bDrag:
                    bXPos = bRect.right - 30
            elif mousePos[0] < rRect.left:
                if rDrag:
                    rXPos = rRect.left
                elif gDrag:
                    gXPos = gRect.left
                elif bDrag:
                    bXPos = bRect.left
            else:
                if rDrag:
                    rXPos = mousePos[0]
                elif gDrag:
                    gXPos = mousePos[0]
                elif bDrag:
                    bXPos = mousePos[0]

            rDrag, gDrag, bDrag = False, False, False

    pg.draw.rect(window, BLACK, rSlide)
    pg.draw.rect(window, BLACK, gSlide)
    pg.draw.rect(window, BLACK, bSlide)

    rCol = ((rSlide.x - rRect.left) // 2)
    gCol = ((gSlide.x - gRect.left) // 2)
    bCol = ((bSlide.x - bRect.left) // 2)

    # rectangle that shows current color
    currentColorRect = Rect((widthCheck // 3) + 50, 70, widthCheck // 5, heightCheck // 5)
    currCol = (rCol, gCol, bCol)
    pg.draw.rect(window, currCol, currentColorRect)

    # button that allows user to go back to the main menu
    goBackButton = pg.Rect((widthCheck // 16), 150, widthCheck // 5, 50)
    goBack = mediumFont.render("Go Back", True, WHITE)
    goBackRect = goBack.get_rect()
    goBackRect.center = goBackButton.center
    pg.draw.rect(window, BLACK, goBackButton)
    window.blit(goBack, goBackRect)

    click, _, _ = pg.mouse.get_pressed()
    if click == 1:
        mouse = pg.mouse.get_pos()
        if goBackButton.collidepoint(mouse):
            BoardColour = (rCol, gCol, bCol)
            changeColor = False
            time.sleep(0.6)
            pg.display.update()

    pg.display.update()


def AiDifficultyMenu():
    """Menu to select the difficulty of the AI"""
    global AIPlayer, AiDifficulty, AiDepth
    window.fill(WHITE)
    widthCheck = display[0]

    # Title for the screen
    difficultyTitle = mediumFont.render("Choose Difficulty", True, RED)
    window.blit(difficultyTitle, (widthCheck // 3 + 40, 40))

    # Three buttons for each difficulty
    difficultOneButton = pg.Rect(2 * (widthCheck / 8), 200, widthCheck / 2, 50)
    difficultOne = mediumFont.render("Difficulty 1 - Easiest (Low Power Mode)", True, WHITE)
    difficultOneRect = difficultOne.get_rect()
    difficultOneRect.center = difficultOneButton.center
    pg.draw.rect(window, BLACK, difficultOneButton)
    window.blit(difficultOne, difficultOneRect)

    difficultTwoButton = pg.Rect((widthCheck / 8), 300, widthCheck / 3, 50)
    difficultTwo = mediumFont.render("Difficulty 2 - Medium", True, WHITE)
    difficultTwoRect = difficultTwo.get_rect()
    difficultTwoRect.center = difficultTwoButton.center
    pg.draw.rect(window, BLACK, difficultTwoButton)
    window.blit(difficultTwo, difficultTwoRect)

    difficultThreeButton = pg.Rect(5 * (widthCheck / 8), 300, widthCheck / 4, 50)
    difficultThree = mediumFont.render("Difficulty 3 - Hard", True, WHITE)
    difficultThreeRect = difficultThree.get_rect()
    difficultThreeRect.center = difficultThreeButton.center
    pg.draw.rect(window, BLACK, difficultThreeButton)
    window.blit(difficultThree, difficultThreeRect)

    # button that allows user to go back to the main menu
    goBackButton = pg.Rect((widthCheck // 16), 100, widthCheck // 5, 50)
    goBack = mediumFont.render("Go Back", True, WHITE)
    goBackRect = goBack.get_rect()
    goBackRect.center = goBackButton.center
    pg.draw.rect(window, BLACK, goBackButton)
    window.blit(goBack, goBackRect)

    click, _, _ = pg.mouse.get_pressed()
    if click == 1:
        mouse = pg.mouse.get_pos()
        if difficultOneButton.collidepoint(mouse):
            time.sleep(0.6)
            AIPlayer = True
            AiDifficulty = False
            AiDepth = 1
            updateChessScreen()
            pg.display.update()
        elif difficultTwoButton.collidepoint(mouse):
            AIPlayer = True
            AiDifficulty = False
            AiDepth = 2
            updateChessScreen()
            pg.display.update()
        elif difficultThreeButton.collidepoint(mouse):
            AIPlayer = True
            AiDifficulty = False
            AiDepth = 3
            updateChessScreen()
            pg.display.update()
        elif goBackButton.collidepoint(mouse):
            AiDifficulty = False
            pg.display.update()

    pg.display.update()


def mainMenu():
    """Main Menu Function"""
    global changeColor, twoPlayer, AIPlayer, AiDifficulty, playerMode
    window.fill(BLACK)
    widthCheck = display[0]
    heightCheck = display[1]

    # Title of the program
    chessTitle = mediumFont.render("Chess With Me", True, RED)
    window.blit(chessTitle, (widthCheck // 3 + 40, 20))

    # button to select color of board
    changeColButton = pg.Rect((widthCheck // 16), 50, widthCheck // 5, 50)
    changeCol = mediumFont.render("Change Color", True, BLACK)
    changeColRect = changeCol.get_rect()
    changeColRect.center = changeColButton.center
    pg.draw.rect(window, TURQUOISE, changeColButton)
    window.blit(changeCol, changeColRect)

    # Two buttons, against AI, or against others
    playAIButton = pg.Rect((widthCheck / 8), (heightCheck / 2), widthCheck / 4, 50)
    playAI = mediumFont.render("Against AI", True, BLACK)
    playAIRect = playAI.get_rect()
    playAIRect.center = playAIButton.center
    pg.draw.rect(window, WHITE, playAIButton)
    window.blit(playAI, playAIRect)

    playTwoButton = pg.Rect(5 * (widthCheck / 8), (heightCheck / 2), widthCheck / 4, 50)
    playTwo = mediumFont.render("Against others", True, BLACK)
    playTwoRect = playTwo.get_rect()
    playTwoRect.center = playTwoButton.center
    pg.draw.rect(window, WHITE, playTwoButton)
    window.blit(playTwo, playTwoRect)
    pg.display.update()

    # if the mouse clicks button then assign what menu to go to
    click, _, _ = pg.mouse.get_pressed()
    if click == 1:
        mouse = pg.mouse.get_pos()
        if playTwoButton.collidepoint(mouse):
            playerMode = True
            pg.display.update()
        elif playAIButton.collidepoint(mouse):
            AiDifficulty = True
            pg.display.update()
        elif changeColButton.collidepoint(mouse):
            changeColor = True

def againstOthersMenu():
"""Against Others Menu"""
global onlinePlayer, twoPlayer, playerMode, networkClient, onlinePlayerOneTurn, onlineColourId, onlineBoardObject, onlinePreviousBoardPosition
window.fill(WHITE)
widthCheck = display[0]
heightCheck = display[1]

# Title of program
chessTitle = mediumFont.render("Choose Mode", True, RED)
window.blit(chessTitle, (widthCheck // 3 + 40, 20))

# Two Buttons
playOnlineButton = pg.Rect((widthCheck / 8), (heightCheck / 3), widthCheck / 4, 50)
playOnline = mediumFont.render("Online Play", True, WHITE)
playOnlineRect = playOnline.get_rect()
playOnlineRect.center = playOnlineButton.center
pg.draw.rect(window, BLACK, playOnlineButton)
window.blit(playOnline, playOnlineRect)

playLocalButton = pg.Rect(5 * (widthCheck / 8), (heightCheck / 3), widthCheck / 4, 50)
playLocal = mediumFont.render("Local Play", True, WHITE)
playLocalRect = playLocal.get_rect()
playLocalRect.center = playLocalButton.center
pg.draw.rect(window, BLACK, playLocalButton)
window.blit(playLocal, playLocalRect)

# button that allows user to go back to the main menu
goBackButton = pg.Rect((widthCheck // 16), 100, widthCheck // 5, 50)
goBack = mediumFont.render("Go Back", True, WHITE)
goBackRect = goBack.get_rect()
goBackRect.center = goBackButton.center
pg.draw.rect(window, BLACK, goBackButton)
window.blit(goBack, goBackRect)

# if the mouse clicks button then assign what menu to go to
click, _, _ = pg.mouse.get_pressed()
if click == 1:
    mouse = pg.mouse.get_pos()
    if playOnlineButton.collidepoint(mouse):
        # move to online game mode
        onlinePlayer = True
        playerMode = False

        networkClient = Client()
        onlineColourId = networkClient.colourId
        onlinePreviousBoardPosition = networkClient.chessBoard.board
        if onlineColourId == "b":
            networkClient.chessBoard.otherPlayer = True

        onlinePlayerOneTurn = True

        updateChessScreen()
        pg.display.update()
    elif playLocalButton.collidepoint(mouse):
        # play on the same computer
        twoPlayer = True
        playerMode = False
        updateChessScreen()
        pg.display.update()
    elif goBackButton.collidepoint(mouse):
        # go back to the main menu
        playerMode = False
        pg.display.update()
pg.display.update()

def AIMinimax(positionCheck, alpha, beta, depth, maximise):
    """Find the best move for the AI"""
    # maximise is True when it's AI's turn
    if maximise:
        maxValue = 9999
        evaluationCheck = getEvaluation(positionCheck, True, True)
    else:
        maxValue = -9999
        evaluationCheck = getEvaluation(positionCheck, False, True)
    if evaluationCheck >= 900 or evaluationCheck <= -900 or depth == 0:
        return evaluationCheck

    # search through all possible moves, and find what the best move is
    for i in range(8):
        for j in range(8):
            if positionCheck[i][j] != "":
                if (positionCheck[i][j].colour == "b" and maximise) or (
                        maximise is False and positionCheck[i][j].colour == "w"):
                    possibleCopy = [["" for i in range(8)] for j in range(8)]
                    possibleCopy = pieceMoves(i, j, possibleCopy, positionCheck)
                    if not any("green" in checkRow for checkRow in possibleCopy):
                        continue
                    for x in range(8):
                        for y in range(8):
                            # go through moves that are possible
                            if possibleCopy[x][y] == "green":
                                positionCopy = copy.deepcopy(positionCheck)
                                positionCopy[x][y] = positionCheck[i][j]
                                positionCopy[i][j] = ""

                                # apply AB pruning
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
    """Check each move possible for the AI and make the best move"""
    global row, column, newY, newX, AiDepth, checkmateCondition
    evaluation = 10000
    rowMove, columnMove = -1, -1
    previousRow, previousColumn = 0, 0
    if checkmateCondition or chessBoard.playerOneTurn is True:
        return 0

    # search through every move and send each to AI minimax
    for i in range(8):
        for j in range(8):
            if positionCheck[i][j] != "":
                if positionCheck[i][j].colour == "b":
                    possibleCopy = [["" for i in range(8)] for j in range(8)]
                    possibleCopy = pieceMoves(i, j, possibleCopy, positionCheck)  # changed this line
                    if not any("green" in row for row in possibleCopy):
                        continue

                    for x in range(8):
                        for y in range(8):
                            if possibleCopy[x][y] == "green":
                                positionCopy = copy.deepcopy(positionCheck)
                                positionCopy[x][y] = positionCheck[i][j]
                                positionCopy[i][j] = ""
                                if kingInCheck(positionCopy, False) is False:
                                    newEval = AIMinimax(positionCopy, -10000, 10000, AiDepth, False)
                                    if newEval <= evaluation:
                                        evaluation = newEval
                                        rowMove, columnMove = x, y
                                        previousRow, previousColumn = i, j

    row, column = previousRow, previousColumn
    movePiece(columnMove, rowMove)


def movePiece(moveX, moveY):
    # updateChessScreen() # - not sure if necessary
    """called to move piece when playing on same computer"""
    if chessBoard.playerOneTurn:
        return 0
    chessBoard.movePiece(moveX, moveY, column, row)

    chessBoard.playerOneTurn = True
    updateChessScreen()


def mainMoveFunction():
    """Move function for playing against others on the same computer and AI"""
    global newPos, playerMove, newX, newY, row, column, AIPlayer
    mousePos = pg.mouse.get_pos()
    newX, newY = mousePos
    newX, newY = newX // 70, (newY - 110) // 70

    playerMove = chessBoard.movePossible(mousePos, column, row)
    if playerMove is True:
        playerMove = False
        if AIPlayer:
            chessBoard.playerOneTurn = False

        # check if checkmate after game function so text can be blitzed onto screen
        updateChessScreen()
        checkmateCheck(chessBoard.playerOneTurn)


# Make sure that there is another player in the game
def onlineCheckForOtherPlayer():
    if onlineColourId == "b":
        # there is another player
        # code can start
        return True
    else:
        while True:
            otherPlayerCondition = networkClient.checkForOtherPlayer()
            if otherPlayerCondition



def onlineCompareLists(currentBoardPosition):
    """Used to compare if two game positions are different"""
    global onlinePreviousBoardPosition
    for i in range(8):
        for j in range(8):
            if onlinePreviousBoardPosition[i][j] == "":
                if currentBoardPosition[i][j] == "":
                    continue
                else:
                    return False
            else:
                if currentBoardPosition[i][j] == "":
                    # one board has a piece, the other doesn't, return false
                    return False
                elif onlinePreviousBoardPosition[i][j].type == currentBoardPosition[i][j].type:
                    # make sure that both boards have the same piece and both are the same colour, else return false
                    if onlinePreviousBoardPosition[i][j].colour == currentBoardPosition[i][j].colour:
                        continue
                    else:
                        return False
                else:
                    return False
    return True


def onlinePieceMoves(pieceY, pieceX, possibleMoves, boardPosition):
    """Returns the possible moves for the piece"""
    global onlineBoardPosition
    return onlineBoardPosition[pieceY][pieceX].possibleMoves(pieceY, pieceX, possibleMoves, boardPosition)


def OnlineCheckPiece(mousePos):
    """Check if there is a piece at the mouse position"""
    global onlineBoardPosition
    columnPiece, rowPiece = mousePos
    # convert the mouse position into the new format of the chess screen
    columnPiece, rowPiece = columnPiece // 70, (rowPiece - 110) // 70
    onlineBoardPosition = networkClient.getCurrentBoardPosition()
    if onlineBoardPosition[rowPiece][columnPiece] == "":
        return False
    return True


def OnlineCheckPlayerTurn(mousePos):
    """Get if the player can move piece"""
    global onlineBoardPosition, onlineColourId
    columnPiece, rowPiece = mousePos
    columnPiece, rowPiece = columnPiece // 70, (rowPiece - 110) // 70

    colour = onlineBoardPosition[rowPiece][columnPiece].colour
    # print(colour, onlinePlayerOneTurn, onlineColourId)
    if (colour == "w" and onlinePlayerOneTurn and onlineColourId == "w") \
            or (colour == "b" and onlinePlayerOneTurn is False and onlineColourId == "b"):
        return True
    return False


def createNetworkClient():
    """Make client connect to the server"""
    global networkClient
    networkClient = Client()


def onlineMoveFunction():
    """Move function for play against other online"""
    global newPos, playerMove, newX, newY, row, column, AIPlayer, onlinePlayerOneTurn, onlinePreviousBoardPosition, onlinePossible
    mousePos = pg.mouse.get_pos()

    # Send over message to move piece
    # has to look like "Move row column mousePos[0] mousePos[1]"
    movePieceCommand = "Move " + str(row) + " " + str(column) + " " + str(mousePos[0]) + " " + str(
        mousePos[1])

    playerMove = networkClient.sendMoveData(movePieceCommand)
    # print(f"Player move = {playerMove}")
    if playerMove is True:
        playerMove = False
        onlinePlayerOneTurn = not onlinePlayerOneTurn
        onlinePreviousBoardPosition = networkClient.chessBoard.board
        onlinePossible = [["" for i in range(8)] for j in range(8)]
        # Call checkmate after game function so text can be blited onto screen
        updateChessScreen()
        # checkmateCheck(chessBoard.playerOneTurn)


def OnlineSendPossible(possibleMoves):
    """Send the possible moves to the server"""
    global networkClient
    networkClient.setPossible(possibleMoves)


def OnlineGetPossible():
    """Get the possible moves from the server"""
    global networkClient
    possible = networkClient.getCurrentPossible()
    return possible


def OnlineGetBoard():
    """Get the current board object"""
    global networkClient
    currentBoard = networkClient.receiveBoard()
    return currentBoard


def OnlineGetBoardPosition():
    """Get the current board position from the server"""
    global networkClient
    currentBoardPosition = networkClient.getCurrentBoardPosition()
    return currentBoardPosition


def checkmateCheck(playerOneTurn):
    """check if there is a checkmate"""
    global font, textPrint, text, checkmateCondition
    if checkmate(chessBoard.board, playerOneTurn, False):
        # if there is a checkmate, show the text on screen
        font = pg.font.SysFont("Helvetica", 75)
        textPrint = "Player 1 Won!"
        if chessBoard.playerOneTurn:
            textPrint = "Player 2 Won!"
        text = font.render(textPrint, True, TURQUOISE)
        window.blit(text, (display[0] // 4, display[1] // 4))
        pg.display.update()
        checkmateCondition = True


def onlineOtherPlayerTurn():
    """Check if it's the other players turn"""
    if (onlineColourId == "b" and onlinePlayerOneTurn) \
            or (onlineColourId == "w" and onlinePlayerOneTurn is False):
        return True
    return False


def showTime():
    """Show the time and player name on the screen"""
    global playerOneSec, playerOneTime, playerOneMin, playerTwoTime, playerTwoMin, playerTwoSec, previousTime, \
        onlinePlayer, onlinePlayerOneTurn, onlinePossible, checkmateCondition

    if checkmateCondition:
        return

    updateChessScreen()
    if onlinePlayer:
        if onlineOtherPlayerTurn() is False:
            moves(onlinePossible)
    else:
        moves(chessBoard.possible)

    # every second, remove a second from the player's time
    currTime = time.time()
    if currTime - previousTime >= 1:
        previousTime = currTime
        playerTurn = chessBoard.playerOneTurn
        if onlinePlayer:
            playerTurn = onlinePlayerOneTurn
        if playerTurn:
            playerOneTime -= 1
            playerOneMin, playerOneSec = divmod(playerOneTime, 60)
            if playerOneTime <= 0:
                playerOneTime = 0
                timeText()
        else:
            playerTwoTime -= 1
            playerTwoMin, playerTwoSec = divmod(playerTwoTime, 60)
            if playerTwoTime <= 0:
                playerTwoTime = 0
                timeText()

    timeFont = pg.font.SysFont("Helvetica", 30)
    # player 2
    playerSentence = "Player 2"
    textPlayer = timeFont.render(playerSentence, True, ORANGE)
    window.blit(textPlayer, (display[0] - 120, display[1] // 8))

    timeSentence = '{:02d}:{:02d}'.format(playerTwoMin, playerTwoSec)
    textTime = timeFont.render(timeSentence, True, ORANGE)
    window.blit(textTime, (display[0] - 120, display[1] // 8 + 50))

    # player 1
    playerSentence = "Player 1"
    textPlayer = timeFont.render(playerSentence, True, ORANGE)
    window.blit(textPlayer, (display[0] - 120, display[1] - 200))

    timeSentence = '{:02d}:{:02d}'.format(playerOneMin, playerOneSec)
    textTime = timeFont.render(timeSentence, True, ORANGE)
    window.blit(textTime, (display[0] - 120, display[1] - 200 + 50))

    pg.display.update()


def timeText():
    """Display text showing player lost due to time"""
    global checkmateCondition, onlinePlayer, onlinePlayerOneTurn
    timeFont = pg.font.SysFont("Helvetica", 40)
    textPrint = "Player 1 Won! (due to time)"

    playerTurn = chessBoard.playerOneTurn
    if onlinePlayer:
        playerTurn = onlinePlayerOneTurn
    if playerTurn:
        textPrint = "Player 2 Won! (due to time)"

    text = timeFont.render(textPrint, True, ORANGE)
    window.blit(text, (display[0] // 6, 50))
    checkmateCondition = True


def mouseMovementForOthers():
    """Mouse movement for playing against others"""
    global column, row, placePiece
    # check if mouse is in same position as when mouse was pushed down
    pos = mouse.get_pos()

    if (pos[0] // 70) == column and ((pos[1] - 110) // 70) == row:
        return "c"
    if event.type == MOUSEBUTTONUP:
        # dragging the piece
        if placePiece:
            mainMoveFunction()
            placePiece = False
            return "c"

    if event.type == MOUSEBUTTONDOWN:
        # previously selected piece, now placing it
        if placePiece:
            if checkPiece(pos) and chessBoard.checkPlayerTurn(pos):
                # If the player pressed a piece before, and now presses on another piece
                # then show the moves for the new piece
                chessBoard.possible = [["" for i in range(8)] for j in range(8)]
                column, row = pos[0] // 70, (pos[1] - 110) // 70
                chessBoard.possible = pieceMoves(row, column, chessBoard.possible, chessBoard.board)
                moves(chessBoard.possible)
            else:
                # else if the new position is not another piece, then go the move function
                # place piece is made false in case they press a square that wasn't a move,
                # they are forced to press the piece again
                columnCheck, rowCheck = pos[0] // 70, (pos[1] - 110) // 70
                # print(f"there is a checkPiece(pos)")
                # print(f"the new position is {chessBoard.possible[rowCheck][columnCheck]}")
                if checkPiece(pos) is False and chessBoard.possible[rowCheck][columnCheck] == "":
                    # check if player has pressed an empty square NOT in possible moves
                    chessBoard.possible = [["" for i in range(8)] for j in range(8)]
                    column, row = None, None
                    updateChessScreen()
                elif checkPiece(pos) and chessBoard.possible[rowCheck][columnCheck]:
                    # Player has not clicked on an empty square, or another piece
                    # print("clicking function is working")
                    mainMoveFunction()
                    placePiece = False
        else:
            # selecting a piece
            chessBoard.possible = [["" for i in range(8)] for j in range(8)]
            column, row = pos[0] // 70, (pos[1] - 110) // 70
            if column > 7:
                return "b"
            if checkPiece(pos) and chessBoard.checkPlayerTurn(pos):
                chessBoard.possible = pieceMoves(row, column, chessBoard.possible, chessBoard.board)
                placePiece = True
            moves(chessBoard.possible)
    return 1


"""mouse click is registered and then dealt with / pieces are moved"""
chessBoard.playerOneTurn = True
placePiece = False
while True:
    clock.tick(60)
    eventList = pg.event.get()
    if AiDifficulty:
        AiDifficultyMenu()
    elif changeColor:
        changeColorMenu(eventList)
    elif playerMode:
        againstOthersMenu()
    elif AIPlayer and chessBoard.playerOneTurn is False and checkmateCondition is False:
        pass
    elif twoPlayer is False and AIPlayer is False and changeColor is False and onlinePlayer is False:
        # display the main menu for the player
        mainMenu()
    elif (onlineColourId == "b" and onlinePlayerOneTurn) \
            or (onlineColourId == "w" and onlinePlayerOneTurn is False):
        if timeSeconds >= 30:
            showTime()
            timeSeconds = 0
        else:
            timeSeconds += 1
        if seconds == 60:
            seconds = 0
            checkBoardPosition = networkClient.getCurrentBoardPosition()
            # get current board position from server, compare this to position from the previous frame,
            # keep doing until a different chess board position is reached
            if onlineCompareLists(checkBoardPosition) is False:
                # print("Other player has made his move")
                onlinePlayerOneTurn = not onlinePlayerOneTurn
                networkClient.setSelfBoard()
                updateChessScreen()
        else:
            seconds += 3
    else:
        if timeSeconds >= 30:
            showTime()
            timeSeconds = 0
        else:
            timeSeconds += 1

    for event in eventList:
        if event.type == QUIT:
            if networkClient is not None:
                networkClient.lostConnection()
            pg.quit()
            break
        elif AiDifficulty or changeColor or playerMode:
            break
        elif checkmateCondition:
            break
        elif onlinePlayer:
            # clicking functions is the same as for normal play. Comments for how it works are shown there.
            if onlineOtherPlayerTurn():
                break
            pos = mouse.get_pos()
            if (pos[0] // 70) == column and ((pos[1] - 110) // 70) == row:
                continue

            if event.type == MOUSEBUTTONUP:
                if placePiece:
                    onlineMoveFunction()
                    placePiece = False
                    continue

            if event.type == MOUSEBUTTONDOWN:
                if placePiece:
                    if OnlineCheckPiece(pos) and OnlineCheckPlayerTurn(pos):

                        updateChessScreen()
                        column, row = pos[0] // 70, (pos[1] - 110) // 70
                        onlinePossible = [["" for i in range(8)] for j in range(8)]

                        onlinePossible = onlinePieceMoves(row, column, onlinePossible, onlineBoardPosition)
                        # print("[GETTING] Getting possible moves")
                        OnlineSendPossible(onlinePossible)
                        moves(onlinePossible)
                    else:
                        columnCheck, rowCheck = pos[0] // 70, (pos[1] - 110) // 70
                        if OnlineCheckPiece(pos) is False and onlinePossible[rowCheck][columnCheck] == "":
                            onlinePossible = [["" for i in range(8)] for j in range(8)]
                            OnlineSendPossible(onlinePossible)
                            column, row = None, None
                            placePiece = False
                            moves(onlinePossible)
                            updateChessScreen()
                        else:
                            onlineMoveFunction()
                            placePiece = False
                else:

                    onlinePossible = [["" for i in range(8)] for j in range(8)]
                    column, row = pos[0] // 70, (pos[1] - 110) // 70

                    if OnlineCheckPiece(pos) and OnlineCheckPlayerTurn(pos):
                        onlinePossible = onlinePieceMoves(row, column, onlinePossible, onlineBoardPosition)
                        # print("[GETTING] Getting possible moves now")
                        OnlineSendPossible(onlinePossible)
                        placePiece = True
                    OnlineSendPossible(onlinePossible)
                    moves(onlinePossible)

        elif twoPlayer:
            output = mouseMovementForOthers()
            if output == "c":
                continue
            elif output == "b":
                break
        elif AIPlayer:
            if chessBoard.playerOneTurn:
                output = mouseMovementForOthers()
                if output == "c":
                    continue
                elif output == "b":
                    break
            else:
                mainAIFunction(chessBoard.board)

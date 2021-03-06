import pygame as pg ## used for display and graphics ##
from pygame import * ## so the program does not need to say pygame.something##
from chess.layoutBoardObject import Board ## imports the board class ##
from chess.client import Client ## imports the client class ##
import time ## imports time so it can be used for the timer of each player ##
import copy ## used to copy variables and arrays and not change the original variable ##

chessBoard = Board() # create a new board object


# defining colours
# variables are in caps because they are constants
WHITE = (255, 255, 255) # colour in RGB form
BLACK = (0, 0, 0) # colour in RGB form
RED = (255, 0, 0) # colour in RGB form
GREEN = (0, 128, 0) # colour in RGB form
TURQUOISE = (64, 224, 208) # colour in RGB form
GREY = (128, 128, 128) # colour in RGB form
ORANGE = (255, 165, 0) # colour in RGB form
BoardColour = (165, 42, 42) # colour in RGB form

display = [800, 800]

# defining some datastructures and variables
onlinePossible = [["" for i in range(8)] for j in range(8)] # create empty 8x8 array
onlineBoardPosition = [["" for x in range(8)] for y in range(8)] # create empty 8x8 array
onlineBoardObject, onlinePreviousBoardPosition = None, onlineBoardPosition # assign variables
clock = pg.time.Clock() # assign variable
row, column = None, None # assign variables

whiteKingHasMoved, kingWillMove = False, False
playerMove, checkmateCondition, twoPlayer, AIPlayer, onlinePlayer, playerMode = False, False, False, False, False, False # assign variables
changeColor, AiDifficulty = False, False # assign variables
networkClient, onlinePlayerOneTurn, onlineColourId = None, None, "" # assign variables
AiDepth, seconds = 2, 0 # assign variables

rDrag, gDrag, bDrag = False, False, False # assign variables
rXPos = (display[0] // 8) + 30 # initial position of slider
gXPos = (display[0] // 8) + 30 # initial position of slider
bXPos = (display[0] // 8) + 30 # initial position of slider
rCol, gCol, bCol = 0, 0, 0 # initial value of sliders

previousTime = time.time() # assign variables
playerOneTime, playerTwoTime = 600, 600 # initial time of players in seconds
playerOneMin, playerOneSec = divmod(playerOneTime, 60) # make time in terms of minutes and seconds
playerTwoMin, playerTwoSec = divmod(playerTwoTime, 60) # make time in terms of minutes and seconds
timeSeconds = 0 # assign variable

pg.init() # start the program
window = pg.display.set_mode(display, pg.RESIZABLE) # show window and allow window to be resized
mediumFont = pg.font.SysFont("Helvetica", 28) # create a global font variable

def updateChessScreen():
    """used to create the chessboard and call updateImages"""
    window.fill(BLACK) # background of screen has to be black
    for j in range(8): # loop 8 times
        for i in range(8): # loop 8 times
            if (i + j) % 2 == 0: # check if even number
                rectangle = pg.Rect(i * 70, j * 70 + 110, 70, 70) # display 70 by 70 squares in this specific location
                pg.draw.rect(window, BoardColour, rectangle) # draw rectangle here
            else:
                rectangle = pg.Rect(i * 70, j * 70 + 110, 70, 70) # display 70 by 70 squares in this specific location
                pg.draw.rect(window, WHITE, rectangle) # draw rectangle here

    # put chess images on the screen
    updateImages() # call function to display images
    pg.display.update() # update the screen to show the changes to the user


def updateImages():
    """used to add images to the chessboard"""
    currentBoard = chessBoard.board # assign what the chessboard is
    if networkClient is not None: # check if there is an online mode
        currentBoard = networkClient.chessBoard.board # if there is an online game, change what the chessboard is
    for i in range(8): # loop 8 times
        for j in range(8): # loop 8 times
            if currentBoard[j][i] != "":
                img = pg.image.load(currentBoard[j][i].image).convert_alpha() # load the images in
                img = pg.transform.smoothscale(img, (68, 68)) # images are size 68 by 68, so this is native size
                window.blit(img, (i * 70, j * 70 + 110)) # display image on the correct location


def getEvaluation(positionCheck, condition, fakePosition):
    """get the value of the board by adding up values of pieces"""
    # condition = True if AIs turn / Not Player One Turn
    # fakePosition is whether this is for the real position, or one that the AI is checking
    return chessBoard.getEval(positionCheck, condition, fakePosition) # get evaluation


def checkPiece(mousePos):
    """checks whether there is a piece where the mouse is clicking"""
    return chessBoard.checkPieceExists(mousePos) # check if a piece exists


def check(checkRow, checkColumn):
    """checks if this row and column is valid, used when looking at possible piece movement"""
    if 0 <= checkRow <= 7 and 0 <= checkColumn <= 7: # check if the piece is in the board
        return True # return true
    return False # return false


def checkmate(boardPosition, playerOneTurn, test):
    """checks if there is a checkmate"""
    global checkmateCondition

    if chessBoard.checkmateCheck(boardPosition, playerOneTurn): # check for checkmate
        if test is False:
            checkmateCondition = True # set condition to true
        return True # return true
    return False # return false


def moves(possibleMoves):
    """shows all the possible moves available"""
    updateChessScreen() # call this function first to show the position of pieces
    for i in range(8): # loop 8 times
        for j in range(8): # loop 8 times
            if possibleMoves[i][j] != "": # check
                pg.draw.circle(window, GREEN, (j * 70 + 35, i * 70 + 110 + 35), 7) # display green circle
    pg.display.update() # update the screen for the player to see


def findKing(boardPosition):
    """finds the position of the king"""
    return chessBoard.findKingPos(boardPosition, chessBoard.playerOneTurn) # find the position of the king


def kingInCheck(boardPosition, playerOneTurn):
    """check if king is in check"""
    return chessBoard.kingInCheck(boardPosition, playerOneTurn) # check if the king is in check


def moveEndCheck(newColumn, newRow, boardPosition, playerOneTurn):
    """checks if move sent to function would remove check, false means that the king won't be in check"""
    return chessBoard.moveEndCheck(newColumn, newRow, row, column, boardPosition, playerOneTurn) # check if the move sent would mean the position is still in check


def moveEndCheckPosition(newColumn, newRow, oldColumn, oldRow, boardPosition, playerOneTurn):
    """checks if move sent to function would remove check used for checkmate function, false means that the king
    won't be in check """
    return chessBoard.moveEndCheck(newColumn, newRow, oldRow, oldColumn, boardPosition, playerOneTurn) # check if the move sent would mean the position is still in check

def pieceMoves(pieceY, pieceX, possibleMoves, boardPosition):
    """each piece will have different possible moves, this calls the correct one"""
    return chessBoard.board[pieceY][pieceX].possibleMoves(pieceY, pieceX, possibleMoves, boardPosition) # get the possible moves for a specific piece


def changeColorMenu(events):
    """Show the sliders for changing colour of the board"""
    global rDrag, gDrag, bDrag, rXPos, gXPos, bXPos, rCol, gCol, bCol, changeColor, BoardColour

    window.fill(WHITE) # fill the background to be white

    widthCheck = display[0] # create variable for width
    heightCheck = display[1] # create variable for height
    xStart = (widthCheck // 8) + 30 # assign variable for where position of slider starts

    # Text
    currentColorText = mediumFont.render("Current Color", True, BLACK) # create text for "current colour"
    window.blit(currentColorText, (widthCheck // 3 + 50, 20)) # put text onto the screen

    rgbSentence = "RGB: (" + str(rCol) + ", " + str(gCol) + ", " + str(bCol) + ")" # create string
    rgbText = mediumFont.render(rgbSentence, True, BLACK) # create text object
    window.blit(rgbText, (widthCheck // 3 + 50, 290)) # put text onto the screen

    rText = mediumFont.render("R: ", True, BLACK) # text for R:
    gText = mediumFont.render("G: ", True, BLACK) # text for G:
    bText = mediumFont.render("B: ", True, BLACK) # text for B:
    window.blit(rText, (xStart - 50, heightCheck // 2 + 45)) # put text onto the screen
    window.blit(gText, (xStart - 50, (heightCheck // 2) + 125)) # put text onto the screen
    window.blit(bText, (xStart - 50, (heightCheck // 2) + 205)) # put text onto the screen

    # Sliders to control colors
    rectWidth = 255 * 2 # make width of sliders double the RGB size
    rRect = Rect(xStart, heightCheck // 2 + 50, rectWidth + 30, heightCheck // 30) # create rectangle for the slider
    gRect = Rect(xStart, (heightCheck // 2) + 130, rectWidth + 30, heightCheck // 30) # create rectangle for the slider
    bRect = Rect(xStart, (heightCheck // 2) + 210, rectWidth + 30, heightCheck // 30) # create rectangle for the slider

    pg.draw.rect(window, GREY, rRect) # put rectangle onto the screen
    pg.draw.rect(window, GREY, gRect) # put rectangle onto the screen
    pg.draw.rect(window, GREY, bRect) # put rectangle onto the screen

    rSlide = Rect(rXPos, heightCheck // 2 + 50, 30, heightCheck // 30) # create slider moving object
    gSlide = Rect(gXPos, (heightCheck // 2) + 130, 30, heightCheck // 30) # create slider moving object
    bSlide = Rect(bXPos, (heightCheck // 2) + 210, 30, heightCheck // 30) # create slider moving object

    for event in events:
        if event.type == pg.MOUSEBUTTONDOWN:
            if rSlide.collidepoint(event.pos): # check if red moving slider has been changed
                rDrag = True # make rDrag true
            if gSlide.collidepoint(event.pos): # check if green moving slider has been changed
                gDrag = True # make gDrag true
            if bSlide.collidepoint(event.pos): # check if blue moving slider has been changed
                bDrag = True # make bDrag true
        if event.type == pg.MOUSEBUTTONUP and (rDrag or gDrag or bDrag):
            mousePos = pg.mouse.get_pos() # get mouse position

            if mousePos[0] > rRect.right: # if mouse has gone off the slider
                if rDrag: # check if r moving slider has been touched
                    rXPos = rRect.right - 30 # assign value of 255 to position of r slider
                elif gDrag: # check if g moving slider has been touched
                    gXPos = gRect.right - 30 # assign value of 255 to position of g slider
                elif bDrag: # check if b moving slider has been touched
                    bXPos = bRect.right - 30
            elif mousePos[0] < rRect.left: # check if moving slider is moved to before the slider
                if rDrag: # check if r moving slider has been touched
                    rXPos = rRect.left # assign value of 0 to position of b slider
                elif gDrag: # check if g moving slider has been touched
                    gXPos = gRect.left # assign value of 0 to position of b slider
                elif bDrag: # check if b moving slider has been touched
                    bXPos = bRect.left # assign value of 0 to position of b slider
            else:
                if rDrag: # check if r moving slider has been touched
                    rXPos = mousePos[0] # assign value to position of r slider
                elif gDrag: # check if g moving slider has been touched
                    gXPos = mousePos[0] # assign value to position of g slider
                elif bDrag: # check if b moving slider has been touched
                    bXPos = mousePos[0] # assign value to position of b slider

            rDrag, gDrag, bDrag = False, False, False

    pg.draw.rect(window, BLACK, rSlide) # put moving slider onto the screen
    pg.draw.rect(window, BLACK, gSlide) # put moving slider onto the screen
    pg.draw.rect(window, BLACK, bSlide) # put moving slider onto the screen

    rCol = ((rSlide.x - rRect.left) // 2) # get RGB from slider
    gCol = ((gSlide.x - gRect.left) // 2) # get RGB from slider
    bCol = ((bSlide.x - bRect.left) // 2) # get RGB from slider

    # rectangle that shows current color
    currentColorRect = Rect((widthCheck // 3) + 50, 70, widthCheck // 5, heightCheck // 5) # get current colour from rect
    currCol = (rCol, gCol, bCol) # get the colour by the sliders
    pg.draw.rect(window, currCol, currentColorRect) # draw a rectangle that shows the current colour

    # button that allows user to go back to the main menu
    goBackButton = pg.Rect((widthCheck // 16), 150, widthCheck // 5, 50) # create button for going back
    goBack = mediumFont.render("Go Back", True, WHITE) # create the text
    goBackRect = goBack.get_rect() # get the rectangle
    goBackRect.center = goBackButton.center
    pg.draw.rect(window, BLACK, goBackButton) # create the rectangle
    window.blit(goBack, goBackRect) # blit the button onto the screen

    click, _, _ = pg.mouse.get_pressed()
    if click == 1: # check if the left click button is being pressed
        mouse = pg.mouse.get_pos() # get the mouse position
        if goBackButton.collidepoint(mouse): # check if the go back button has been hit
            BoardColour = (rCol, gCol, bCol) # get the current colour
            changeColor = False # go back to main menu
            time.sleep(0.6)
            pg.display.update() # update screen

    pg.display.update() # update screen


def AiDifficultyMenu():
    """Menu to select the difficulty of the AI"""
    global AIPlayer, AiDifficulty, AiDepth
    window.fill(WHITE) # make screen white
    widthCheck = display[0] # get the width of the screen

    # Title for the screen
    difficultyTitle = mediumFont.render("Choose Difficulty", True, RED) # make text for AI
    window.blit(difficultyTitle, (widthCheck // 3 + 40, 40)) # put text onto screen

    # Three buttons for each difficulty
    difficultOneButton = pg.Rect(2 * (widthCheck / 8), 200, widthCheck / 2, 50) # create rectangle
    difficultOne = mediumFont.render("Difficulty 1 - Easiest (Low Power Mode)", True, WHITE) # put text onto screen
    difficultOneRect = difficultOne.get_rect() # get rectangle
    difficultOneRect.center = difficultOneButton.center # get centre of the button
    pg.draw.rect(window, BLACK, difficultOneButton) # put rectangle onto screen
    window.blit(difficultOne, difficultOneRect) # blit button onto screen

    difficultTwoButton = pg.Rect((widthCheck / 8), 300, widthCheck / 3, 50) # create rectangle for button
    difficultTwo = mediumFont.render("Difficulty 2 - Medium", True, WHITE) # create text
    difficultTwoRect = difficultTwo.get_rect() # get rectangle 
    difficultTwoRect.center = difficultTwoButton.center # get centre of button
    pg.draw.rect(window, BLACK, difficultTwoButton) # draw rectangle
    window.blit(difficultTwo, difficultTwoRect) # blit button onto screen

    difficultThreeButton = pg.Rect(5 * (widthCheck / 8), 300, widthCheck / 4, 50) # create rectangle for button
    difficultThree = mediumFont.render("Difficulty 3 - Hard", True, WHITE) # create text
    difficultThreeRect = difficultThree.get_rect() # get rectangle 
    difficultThreeRect.center = difficultThreeButton.center # get centre of button
    pg.draw.rect(window, BLACK, difficultThreeButton) # draw rectangle
    window.blit(difficultThree, difficultThreeRect) # blit button onto screen

    # button that allows user to go back to the main menu
    goBackButton = pg.Rect((widthCheck // 16), 100, widthCheck // 5, 50) # create rectangle for button
    goBack = mediumFont.render("Go Back", True, WHITE) # create text
    goBackRect = goBack.get_rect() # get rectangle 
    goBackRect.center = goBackButton.center # get centre of button
    pg.draw.rect(window, BLACK, goBackButton) # draw rectangle
    window.blit(goBack, goBackRect) # blit button onto screen

    click, _, _ = pg.mouse.get_pressed() # check if mouse has been pressed
    if click == 1: # check if left click has been pressed
        mouse = pg.mouse.get_pos() # check mouse position
        if difficultOneButton.collidepoint(mouse): # check if button has been pressed
            time.sleep(0.6)
            AIPlayer = True # start AI game
            AiDifficulty = False # exit menu
            AiDepth = 1 # set depth to 1
            updateChessScreen() # update the chess screen
            pg.display.update() # update screen
        elif difficultTwoButton.collidepoint(mouse): # check if button has been pressed
            AIPlayer = True # start AI game
            AiDifficulty = False # exit menu
            AiDepth = 2 # set depth to 2
            updateChessScreen() # update the chess screen
            pg.display.update() # update screen
        elif difficultThreeButton.collidepoint(mouse): # check if button has been pressed
            AIPlayer = True # start AI game
            AiDifficulty = False # exit menu
            AiDepth = 3 # set depth to 3
            updateChessScreen() # update the chess screen
            pg.display.update() # update screen
        elif goBackButton.collidepoint(mouse): # check if button has been pressed
            AiDifficulty = False # exit menu
            pg.display.update() # update screen

    pg.display.update() # update screen


def mainMenu():
    """Main Menu Function"""
    global changeColor, twoPlayer, AIPlayer, AiDifficulty, playerMode
    window.fill(BLACK) # make screen black
    widthCheck = display[0] # get width
    heightCheck = display[1] # get height

    # Title of the program
    chessTitle = mediumFont.render("Chess With Me", True, RED) # create text
    window.blit(chessTitle, (widthCheck // 3 + 40, 20)) # blit text onto screen

    # button to select color of board
    changeColButton = pg.Rect((widthCheck // 16), 50, widthCheck // 5, 50) # create rectangle
    changeCol = mediumFont.render("Change Color", True, BLACK) # create text
    changeColRect = changeCol.get_rect() # get rectangle
    changeColRect.center = changeColButton.center # get center of button
    pg.draw.rect(window, TURQUOISE, changeColButton) # draw rectangle 
    window.blit(changeCol, changeColRect) # blit button onto rectangle

    # Two buttons, against AI, or against others
    playAIButton = pg.Rect((widthCheck / 8), (heightCheck / 2), widthCheck / 4, 50) # create rectangle
    playAI = mediumFont.render("Against AI", True, BLACK) # create text
    playAIRect = playAI.get_rect() # get rectangle object
    playAIRect.center = playAIButton.center # get center 
    pg.draw.rect(window, WHITE, playAIButton) # draw rectangle onto screen
    window.blit(playAI, playAIRect) # blit button onto screen

    playTwoButton = pg.Rect(5 * (widthCheck / 8), (heightCheck / 2), widthCheck / 4, 50) # create rectangle 
    playTwo = mediumFont.render("Against others", True, BLACK) # create text
    playTwoRect = playTwo.get_rect() # get rectangle object
    playTwoRect.center = playTwoButton.center # get centre of button
    pg.draw.rect(window, WHITE, playTwoButton) # draw rectangle onto screen
    window.blit(playTwo, playTwoRect) # blit button onto screen
    pg.display.update() # update screen

    # if the mouse clicks button then assign what menu to go to
    click, _, _ = pg.mouse.get_pressed() # check if the mouse has been clicked
    if click == 1: # check if the left mouse button has been clicked
        mouse = pg.mouse.get_pos() # get position of mouse
        if playTwoButton.collidepoint(mouse): # check if button has been clicked
            playerMode = True # playing against others
            pg.display.update() # update screen
        elif playAIButton.collidepoint(mouse):
            AiDifficulty = True # choose difficulty of AI
            pg.display.update() # update screen
        elif changeColButton.collidepoint(mouse):
            changeColor = True # go to colour picker

def againstOthersMenu():
    """Against Others Menu"""
    global onlinePlayer, twoPlayer, playerMode, networkClient, onlinePlayerOneTurn, onlineColourId, onlineBoardObject, onlinePreviousBoardPosition
    window.fill(WHITE) # make screen white
    widthCheck = display[0] # get width
    heightCheck = display[1] # get height

    # Title of program
    chessTitle = mediumFont.render("Choose Mode", True, RED) # create text
    window.blit(chessTitle, (widthCheck // 3 + 40, 20)) # blit text onto screen

    # Two Buttons
    playOnlineButton = pg.Rect((widthCheck / 8), (heightCheck / 3), widthCheck / 4, 50) # create rectangle
    playOnline = mediumFont.render("Online Play", True, WHITE) # create text
    playOnlineRect = playOnline.get_rect() # get rectangle object
    playOnlineRect.center = playOnlineButton.center # get centre of rectangle
    pg.draw.rect(window, BLACK, playOnlineButton) # draw rectangle
    window.blit(playOnline, playOnlineRect) # blit button onto screen

    playLocalButton = pg.Rect(5 * (widthCheck / 8), (heightCheck / 3), widthCheck / 4, 50) # create rectangle 
    playLocal = mediumFont.render("Local Play", True, WHITE) # create text
    playLocalRect = playLocal.get_rect() # get rectangle object
    playLocalRect.center = playLocalButton.center # get centre of button
    pg.draw.rect(window, BLACK, playLocalButton) # get rectangle 
    window.blit(playLocal, playLocalRect) # blit button onto screen

    # button that allows user to go back to the main menu
    goBackButton = pg.Rect((widthCheck // 16), 100, widthCheck // 5, 50) # create rectangle
    goBack = mediumFont.render("Go Back", True, WHITE) # create text
    goBackRect = goBack.get_rect() # get rectangle object
    goBackRect.center = goBackButton.center # get centre of button
    pg.draw.rect(window, BLACK, goBackButton) # draw rectangle
    window.blit(goBack, goBackRect) # blit rectangle onto screen

    # if the mouse clicks button then assign what menu to go to
    click, _, _ = pg.mouse.get_pressed() # has mouse been clicked
    if click == 1: # check if left mouse button has been clicked
        mouse = pg.mouse.get_pos() # get position of mouse
        if playOnlineButton.collidepoint(mouse): # check if button has been clicked
            # move to online game mode
            onlinePlayer = True # go to online mode
            playerMode = False # exit menu

            networkClient = Client() # create client object
            onlineColourId = networkClient.colourId # get colour of user
            onlinePreviousBoardPosition = networkClient.chessBoard.board # get board object
            if onlineColourId == "b": # check if player is black
                networkClient.chessBoard.otherPlayer = True # other player's turn
            else:
                onlineCheckForOtherPlayer() # check if there is another player
            onlinePlayerOneTurn = True # move is true

            updateChessScreen() # update the entire screen
            pg.display.update() # update the pixels on the screen
        elif playLocalButton.collidepoint(mouse): # check if button has been clicked
            # play on the same computer
            twoPlayer = True # play against others
            playerMode = False # not selecting anymore
            updateChessScreen() # update the entire screen
            pg.display.update() # update the pixels on the screen
        elif goBackButton.collidepoint(mouse): # check if go back button has been clicked
            # go back to the main menu
            playerMode = False # go back to main menu
            pg.display.update() # update the pixels on the screen
    pg.display.update() # update the pixels on the screen

def AIMinimax(positionCheck, alpha, beta, depth, maximise):
    """Find the best move for the AI"""
    # maximise is True when it's AI's turn
    if maximise: # check if you are maximising the game
        maxValue = 9999 # maximum value
        evaluationCheck = getEvaluation(positionCheck, True, True) # get evaluation of board
    else:
        maxValue = -9999 # minimum value
        evaluationCheck = getEvaluation(positionCheck, False, True) # get evaluation of board
    if evaluationCheck >= 900 or evaluationCheck <= -900 or depth == 0:
        return evaluationCheck # return evaluation

    # search through all possible moves, and find what the best move is
    for i in range(8): # loop 8 times
        for j in range(8): # loop 8 times 
            if positionCheck[i][j] != "": # check if position is empty
                if (positionCheck[i][j].colour == "b" and maximise) or (
                        maximise is False and positionCheck[i][j].colour == "w"):
                    possibleCopy = [["" for i in range(8)] for j in range(8)]
                    possibleCopy = pieceMoves(i, j, possibleCopy, positionCheck)
                    if not any("green" in checkRow for checkRow in possibleCopy): # check if this piece can move
                        continue
                    for x in range(8): # loop 8 times
                        for y in range(8): # loop 8 times
                            # go through moves that are possible
                            if possibleCopy[x][y] == "green": # check if move is possible 
                                positionCopy = copy.deepcopy(positionCheck) # copy position
                                positionCopy[x][y] = positionCheck[i][j] # make move to position
                                positionCopy[i][j] = "" # make move to position

                                # apply AB pruning
                                if maximise: # check if maximising
                                    if kingInCheck(positionCopy, False) is False:
                                        newEval = AIMinimax(positionCopy, alpha, beta, depth - 1, not maximise)
                                        maxValue = min(newEval, maxValue) # get the min
                                        beta = min(beta, maxValue) # get the min
                                        if beta <= alpha:
                                            return maxValue # return max value
                                else: # or minimising
                                    if kingInCheck(positionCopy, True) is False:
                                        newEval = AIMinimax(positionCopy, alpha, beta, depth - 1, not maximise)
                                        maxValue = max(newEval, maxValue) # get the max
                                        alpha = max(alpha, maxValue) # get the max
                                        if beta <= alpha:
                                            return maxValue # return max value

    return maxValue # return max value


def mainAIFunction(positionCheck):
    """Check each move possible for the AI and make the best move"""
    global row, column, newY, newX, AiDepth, checkmateCondition
    evaluation = 10000 # eval = 10000
    rowMove, columnMove = -1, -1 # set current row and column to values not possible
    previousRow, previousColumn = 0, 0 # set previous row and column to  0 0 
    if checkmateCondition or chessBoard.playerOneTurn is True:
        return 0 # check if it is checkmate or the other player's turn

    # search through every move and send each to AI minimax
    for i in range(8): # loop 8 times
        for j in range(8): # loop 8 times
            if positionCheck[i][j] != "": # check if position is empty
                if positionCheck[i][j].colour == "b": # check if the piece is black
                    possibleCopy = [["" for i in range(8)] for j in range(8)] # create empty board
                    possibleCopy = pieceMoves(i, j, possibleCopy, positionCheck)  # changed this line
                    if not any("green" in row for row in possibleCopy): # check if there is green
                        continue # if there are no possible moves, skip the loop

                    for x in range(8): # loop 8 times
                        for y in range(8): # loop 8 times
                            if possibleCopy[x][y] == "green": # check for green
                                positionCopy = copy.deepcopy(positionCheck) # copy the position
                                positionCopy[x][y] = positionCheck[i][j] # make move
                                positionCopy[i][j] = "" # make move
                                if kingInCheck(positionCopy, False) is False:
                                    newEval = AIMinimax(positionCopy, -10000, 10000, AiDepth, False)
                                    if newEval <= evaluation: # check if new evaluation is lower
                                        evaluation = newEval # assign new eval
                                        rowMove, columnMove = x, y # set row and column to position
                                        previousRow, previousColumn = i, j # set previous row and column to position

    row, column = previousRow, previousColumn
    movePiece(columnMove, rowMove) # move piece


def movePiece(moveX, moveY):
    # updateChessScreen() # - not sure if necessary
    """called to move piece when playing on same computer"""
    if chessBoard.playerOneTurn: # check if other player's turn
        return 0
    chessBoard.movePiece(moveX, moveY, column, row) # move piece

    chessBoard.playerOneTurn = True # make player one's turn true
    updateChessScreen() # update the entire screen


def mainMoveFunction():
    """Move function for playing against others on the same computer and AI"""
    global newPos, playerMove, newX, newY, row, column, AIPlayer
    mousePos = pg.mouse.get_pos() # get mouse pos
    newX, newY = mousePos # seperate tuple
    newX, newY = newX // 70, (newY - 110) // 70 # get row and column

    playerMove = chessBoard.movePossible(mousePos, column, row)
    if playerMove is True:
        playerMove = False # make move false
        if AIPlayer:
            chessBoard.playerOneTurn = False

        # check if checkmate after game function so text can be blitzed onto screen
        updateChessScreen() # update the entire screen
        checkmateCheck(chessBoard.playerOneTurn) # check for checkmate

def waitingForOtherPlayer():
    """
    This function is responsible for displaying text
    showing the user is waiting for another player
    """
    font = pg.font.SysFont("Helvetica", 60) # create text
    textPrint = "Waiting for another player..." # sentence to show on screen
    text = font.render(textPrint, True, TURQUOISE) # put font on screen
    window.blit(text, (display[0] // 8, 0)) # blit text onto screen
    pg.display.update() # update the screen


# Make sure that there is another player in the game
def onlineCheckForOtherPlayer():
    if onlineColourId == "b":
        # there is another player
        # code can start
        return True
    else:
        updateChessScreen() # update the screen
        waitingForOtherPlayer() # wait for another player to join the game
        while True:
            otherPlayerCondition = networkClient.checkForOtherPlayer()
            # if the otherPlayerCondition is true, then there is another player
            if otherPlayerCondition:
                return True
            # else another player still has not come



def onlineCompareLists(currentBoardPosition):
    """Used to compare if two game positions are different"""
    global onlinePreviousBoardPosition
    for i in range(8): # loop 8 times 
        for j in range(8): # loop 8 times
            if onlinePreviousBoardPosition[i][j] == "": # check if position is empty
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
                        return False # lists are not the same
                else:
                    return False # lists are not the same
    return True # lists are the same


def onlinePieceMoves(pieceY, pieceX, possibleMoves, boardPosition):
    """Returns the possible moves for the piece"""
    global onlineBoardPosition
    return onlineBoardPosition[pieceY][pieceX].possibleMoves(pieceY, pieceX, possibleMoves, boardPosition)


def OnlineCheckPiece(mousePos):
    """Check if there is a piece at the mouse position"""
    global onlineBoardPosition
    columnPiece, rowPiece = mousePos
    # convert the mouse position into the new format of the chess screen
    columnPiece, rowPiece = columnPiece // 70, (rowPiece - 110) // 70 # get the row and column of mouse
    onlineBoardPosition = networkClient.getCurrentBoardPosition() # get current board
    if onlineBoardPosition[rowPiece][columnPiece] == "": # check if position is empty
        return False
    return True


def OnlineCheckPlayerTurn(mousePos):
    """Check if the player can move piece"""
    global onlineBoardPosition, onlineColourId
    columnPiece, rowPiece = mousePos # seperate tuple
    columnPiece, rowPiece = columnPiece // 70, (rowPiece - 110) // 70 # get row and column

    colour = onlineBoardPosition[rowPiece][columnPiece].colour # get colour of piece
    # print(colour, onlinePlayerOneTurn, onlineColourId)
    if (colour == "w" and onlinePlayerOneTurn and onlineColourId == "w") \
            or (colour == "b" and onlinePlayerOneTurn is False and onlineColourId == "b"):
        return True # player can move the piece
    return False # player cannot move the piece


def createNetworkClient():
    """Make client connect to the server"""
    global networkClient
    networkClient = Client() # create global client object


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
        onlinePlayerOneTurn = not onlinePlayerOneTurn # swap who the player's turn is
        onlinePreviousBoardPosition = networkClient.chessBoard.board # get previous board position
        onlinePossible = [["" for i in range(8)] for j in range(8)]
        # Call checkmate after game function so text can be blited onto screen
        updateChessScreen()
        # checkmateCheck(chessBoard.playerOneTurn)


def OnlineSendPossible(possibleMoves):
    """Send the possible moves to the server"""
    global networkClient
    networkClient.setPossible(possibleMoves) # set the possible moves


def OnlineGetPossible():
    """Get the possible moves from the server"""
    global networkClient
    possible = networkClient.getCurrentPossible() # get possible moves
    return possible # return possible moves


def OnlineGetBoard():
    """Get the current board object"""
    global networkClient
    currentBoard = networkClient.receiveBoard() # get current board object
    return currentBoard # return board object


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
        font = pg.font.SysFont("Helvetica", 75) # create font object
        textPrint = "Player 1 Won!" # create sentence 
        if chessBoard.playerOneTurn: # check who's turn it is
            textPrint = "Player 2 Won!" # create sentence
        text = font.render(textPrint, True, TURQUOISE) # create text
        window.blit(text, (display[0] // 4, display[1] // 4)) # blit text onto screen
        pg.display.update() # update the screen
        checkmateCondition = True # let program know that it is checkmate


def onlineOtherPlayerTurn():
    """Check if it's the other players turn"""
    if (onlineColourId == "b" and onlinePlayerOneTurn) \
            or (onlineColourId == "w" and onlinePlayerOneTurn is False):
        return True # check if it is the other player's turn
    return False


def showTime():
    """Show the time and player name on the screen"""
    global playerOneSec, playerOneTime, playerOneMin, playerTwoTime, playerTwoMin, playerTwoSec, previousTime, \
        onlinePlayer, onlinePlayerOneTurn, onlinePossible, checkmateCondition

    if checkmateCondition: # check if it is checkmate
        return

    updateChessScreen() # update the entire screen
    if onlinePlayer:
        if onlineOtherPlayerTurn() is False:
            moves(onlinePossible)
    else:
        moves(chessBoard.possible)

    # display possible moves onto screen

    # every second, remove a second from the player's time
    currTime = time.time()
    if currTime - previousTime >= 1:
        previousTime = currTime # make previous time, the current time
        playerTurn = chessBoard.playerOneTurn
        if onlinePlayer:
            playerTurn = onlinePlayerOneTurn
        if playerTurn:
            playerOneTime -= 1 # minus a second
            playerOneMin, playerOneSec = divmod(playerOneTime, 60) # get the minutes and seconds
            if playerOneTime <= 0: 
                playerOneTime = 0 # dont let time be negative
                timeText() # show who has won onto screen
        else:
            playerTwoTime -= 1 # minus a second
            playerTwoMin, playerTwoSec = divmod(playerTwoTime, 60) # get the minutes and seconds
            if playerTwoTime <= 0: 
                playerTwoTime = 0 # dont let time be negative
                timeText() # show who has won toonto screen

    timeFont = pg.font.SysFont("Helvetica", 30) # create font object
    # player 2
    playerSentence = "Player 2" # create text sentence
    textPlayer = timeFont.render(playerSentence, True, ORANGE) # create text object
    window.blit(textPlayer, (display[0] - 120, display[1] // 8)) # blit text object onto screen

    timeSentence = '{:02d}:{:02d}'.format(playerTwoMin, playerTwoSec) # show the time for player
    textTime = timeFont.render(timeSentence, True, ORANGE) # create the text object
    window.blit(textTime, (display[0] - 120, display[1] // 8 + 50)) # blit the text onto screen

    # player 1
    playerSentence = "Player 1" # text sentence
    textPlayer = timeFont.render(playerSentence, True, ORANGE) # create the text object
    window.blit(textPlayer, (display[0] - 120, display[1] - 200)) # blit the text onto screen

    timeSentence = '{:02d}:{:02d}'.format(playerOneMin, playerOneSec) 
    textTime = timeFont.render(timeSentence, True, ORANGE) # create the text object
    window.blit(textTime, (display[0] - 120, display[1] - 200 + 50)) # blit the text onto screen
 
    pg.display.update() # update screen


def timeText():
    """Display text showing player lost due to time"""
    global checkmateCondition, onlinePlayer, onlinePlayerOneTurn
    timeFont = pg.font.SysFont("Helvetica", 40) # create font object
    textPrint = "Player 1 Won! (due to time)" # create text sentence

    playerTurn = chessBoard.playerOneTurn
    if onlinePlayer:
        playerTurn = onlinePlayerOneTurn
    if playerTurn:
        textPrint = "Player 2 Won! (due to time)" # create text sentence

    text = timeFont.render(textPrint, True, ORANGE) # create text object
    window.blit(text, (display[0] // 6, 50)) # blit text onto screen
    checkmateCondition = True


def mouseMovementForOthers():
    """Mouse movement for playing against others"""
    global column, row, placePiece
    # check if mouse is in same position as when mouse was pushed down
    pos = mouse.get_pos() # get mouse position

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
    eventList = pg.event.get() # get what the player has done
    if AiDifficulty:
        AiDifficultyMenu() # display AI menu
    elif changeColor:
        changeColorMenu(eventList) # show the colour picker
    elif playerMode:
        againstOthersMenu() # show the against others menu
    elif AIPlayer and chessBoard.playerOneTurn is False and checkmateCondition is False:
        pass
    elif twoPlayer is False and AIPlayer is False and changeColor is False and onlinePlayer is False:
        # display the main menu for the player
        mainMenu() # show the main menu
    elif (onlineColourId == "b" and onlinePlayerOneTurn) \
            or (onlineColourId == "w" and onlinePlayerOneTurn is False):
        if timeSeconds >= 30:
            showTime() # show the time of the player
            timeSeconds = 0
        else:
            timeSeconds += 1
        if seconds == 60:
            seconds = 0
            checkBoardPosition = networkClient.getCurrentBoardPosition() # get current position from server
            # get current board position from server, compare this to position from the previous frame,
            # keep doing until a different chess board position is reached
            if onlinePreviousBoardPosition != checkBoardPosition:
                # print("Other player has made his move")
                onlinePlayerOneTurn = not onlinePlayerOneTurn
                networkClient.setSelfBoard()
                updateChessScreen() # update the board and pieces
        else:
            seconds += 1
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
            pg.quit() # exit program
            break # end program
        elif AiDifficulty or changeColor or playerMode:
            break
        elif checkmateCondition:
            break
        elif onlinePlayer:
            # clicking functions is the same as for normal play. Comments for how it works are shown there.
            if onlineOtherPlayerTurn():
                break
            # check if mouse is in same position as when mouse was pushed down
            pos = mouse.get_pos()
            if (pos[0] // 70) == column and ((pos[1] - 110) // 70) == row:
                continue

            if event.type == MOUSEBUTTONUP:
                # previously selected piece, now placing it
                if placePiece:
                    onlineMoveFunction()
                    placePiece = False
                    continue

            if event.type == MOUSEBUTTONDOWN:
                if placePiece:
                    if OnlineCheckPiece(pos) and OnlineCheckPlayerTurn(pos):
                        # If the player pressed a piece before, and now presses on another piece
                        # then show the moves for the new piece
                        updateChessScreen()
                        column, row = pos[0] // 70, (pos[1] - 110) // 70
                        onlinePossible = [["" for i in range(8)] for j in range(8)]

                        onlinePossible = onlinePieceMoves(row, column, onlinePossible, onlineBoardPosition)
                        # print("[GETTING] Getting possible moves")
                        OnlineSendPossible(onlinePossible)
                        moves(onlinePossible)
                    else:
                        # else if the new position is not another piece, then go the move function
                        # place piece is made false in case they press a square that wasn't a move,
                        # they are forced to press the piece again
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
                    # selecting a piece
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
            # check if you should continue or break
            if output == "c": # continue
                continue
            elif output == "b": # break
                break
        elif AIPlayer:
            if chessBoard.playerOneTurn:
                output = mouseMovementForOthers()
                # check if you should continue or break
                if output == "c": # continue
                    continue
                elif output == "b": # break
                    break
            else:
                mainAIFunction(chessBoard.board)

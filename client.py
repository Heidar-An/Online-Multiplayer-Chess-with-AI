import socket ## used for connecting users together ##
import pickle ## used for transferring data, almost like JSON ##


# used for client side of chess
class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.format = "utf-8"
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 5050
        self.address = (self.ip, self.port)
        self.colourId = ""
        self.chessBoard = self.getBoard()

    def getBoard(self):
        """Get the board from the Server"""
        print("[SENDING] GET BOARD")
        self.socket.connect(self.address)

        # Get the colour of the player
        colourId = self.socket.recv(8)
        self.colourId = colourId.decode(self.format)

        # Get the initial state of the board
        board = self.socket.recv(1024)
        try:
            board = pickle.loads(board)
        except pickle.UnpicklingError:
            otherPart = self.socket.recv(1024)
            otherPart = pickle.loads(otherPart)
            print(f"Other board = {otherPart}")
            return otherPart

        return board

    def checkForOtherPlayer(self):
        """Find out if the player with the black pieces is here"""
        print("[CHECKING] Checking for other player")
        self.socket.send("CheckOtherPlayer".encode(self.format))
        # the server will be returning if there is another player 
        # with a boolean value
        otherPlayerCondition = self.socket.recv(5)
        otherPlayerCondition = otherPlayerCondition.decode(self.format)

        otherPlayerCondition = bool(otherPlayerCondition)
        return otherPlayerCondition

    def lostConnection(self):
        """Called if user leaves/loses connection, close the socket"""
        print("[CLOSING] Connection has been lost")
        self.socket.close()

    def receiveBoard(self):
        """Retrieve the chess board object from the server"""
        print("[SENDING] Receive Board")
        # send code to server
        self.socket.send("GetBoardObject".encode(self.format))
        # receive board from server
        board = self.socket.recv(4096 * 10)
        try:
            board = pickle.loads(board)
        except pickle.UnpicklingError:
            otherPart = self.socket.recv(4096)
            otherPart = pickle.loads(otherPart)
            print(f"Other part = {otherPart}")
            return otherPart
        return board

    def setSelfBoard(self):
        print("[SENDING] Receive SELF.Board")
        # send code to server
        self.socket.send("GetBoardObject".encode(self.format))
        # receive board from server
        board = self.socket.recv(4096)
        try:
            board = pickle.loads(board)
            self.chessBoard = board
        except pickle.UnpicklingError:
            otherPart = self.socket.recv(4096)
            otherPart = pickle.loads(otherPart)
            print(f"Other part = {otherPart}")
            self.chessBoard = otherPart

    def sendMoveData(self, data):
        """Send data to move the piece on the board"""
        print("[SENDING] Send Move Data")
        # Send data to server
        self.socket.send(data.encode(self.format))
        # Get back if player successfully moved
        playerMove = self.socket.recv(5)

        playerMove = playerMove.decode(self.format)

        playerMove = bool(playerMove)
        # Get back board

        if playerMove:
            self.chessBoard = self.receiveBoard()
        return playerMove

    def setPossible(self, data):
        print("[SENDING] SET POSSIBlE")
        # send message to server
        self.socket.send("SetPossible".encode(self.format).strip())
        # get message back confirming that it worked
        message = self.socket.recv(1)
        message = message.decode(self.format)
        if message == "y":
            # send possibleMoves to server
            data = pickle.dumps(data)
            self.socket.send(data)
        else:
            print(f"[ERROR] Message instead was {message}")

    def getCurrentBoardPosition(self):
        """Get the current board from the chessBoard object"""
        # print("[GETTING] Getting current board position")
        # send message to the server
        self.socket.send("GetBoardPosition".encode(self.format))
        # Get the boardPosition back
        boardPosition = self.socket.recv(1024)
        try:
            boardPosition = pickle.loads(boardPosition)
        except pickle.UnpicklingError:
            boardPosition = self.socket.recv(1024)
            boardPosition = pickle.loads(boardPosition)
            print(f"Other part = {boardPosition}")
            return boardPosition
        return boardPosition

    def getCurrentPossible(self):
        """Get the current possible moves from the chessBoard object"""
        print("[SENDING] Get Current Possible")
        # send message to the server
        self.socket.send("GetPossibleMoves".encode(self.format))
        # Get the board back
        board = self.receiveBoard()
        return board

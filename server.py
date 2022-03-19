import socket ## used for connecting users together ##
import threading ## used to manage each user in a seperate thread ##
import pickle ## used to transfer data across the internet, similar to JSON ##
from chess.layoutBoardObject import Board ## used to get Board class to get an object and save each game in a list ##

# used for server side of chess
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
totalConn = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    server.bind(ADDRESS)
except socket.error:
    str(socket.error)

# This will store all games, first term = game number, second = actual board
allChessGames = {}


def handle_client(conn, address, chessGame, gameNumber):
    global totalConn

    print(f"NEW CONNECTION {address}")
    # all games are full
    colourId = "b"
    if totalConn % 2 == 0:
        colourId = "w"

    # send what colour the player is
    conn.send(colourId.encode(FORMAT))
    # send board across socket by using pickle to "dump" it
    boardString = pickle.dumps(chessGame)
    conn.send(boardString)

    totalConn += 1
    connected = True

    while connected:
        d = conn.recv(942)
        try:
            data = d.decode("utf-8")
        except UnicodeDecodeError:
            print(f"Bytes data = {d}")
            print(f"Length of data = {len(d)}")
            print(pickle.loads(d))
        if not d:
            break
        if data == "":
            continue
        if data != "GetBoardPosition":
            print(f"[DATA] = {data}")
        if "Move" in data:
            # for moving pieces
            # "Move row column mousePos[0] mousePos[1]"

            fullData = data.split(" ")
            prevRow = int(fullData[1])
            prevCol = int(fullData[2])
            mousePosOne = int(fullData[3])
            mousePosTwo = int(fullData[4])
            mousePos = (mousePosOne, mousePosTwo)

            print(fullData, mousePosOne // 70, (mousePosTwo - 110) // 70)
            playerMoved = chessGame.movePossible(mousePos, prevCol, prevRow)
            playerMoved = str(playerMoved)

            conn.sendall(playerMoved.encode(FORMAT))

        elif "GetPossibleMoves" in data:
            # return the possible moves
            possibleMoves = chessGame.possible
            possibleMoves = pickle.dumps(possibleMoves)
            conn.sendall(possibleMoves)

        elif "GetBoardObject" in data:
            # return the current board object
            data = pickle.dumps(chessGame)
            conn.sendall(data)

        elif "SetPossible" in data:
            # send message to confirm
            conn.send("y".encode(FORMAT))
            # Set the possible moves
            print("[RECEIVED] Set Possible received")
            possibleMoves = conn.recv(1024)
            possibleMoves = pickle.loads(possibleMoves)
            print(possibleMoves)
            chessGame.possible = possibleMoves

        elif "GetBoardPosition" in data:
            # Return current board position
            boardPosition = chessGame.board
            boardPosition = pickle.dumps(boardPosition)
            conn.sendall(boardPosition)

        elif "CheckOtherPlayer" in data:
            # Return if the player with the black pieces is in the game
            # check if the total number of connections are even or odd
            otherPlayer = False
            if totalConn % 2 == 0:
                otherPlayer = True
            conn.send(otherPlayer)

    totalConn -= 1
    conn.close()


def start():
    global totalConn
    server.listen()
    print("[LISTENING] on " + SERVER)
    while True:
        conn, address = server.accept()
        print("[CONNECTED] PLAYER JOINED")
        totalConn = threading.activeCount() - 1
        # check if there is another game with only one player
        if totalConn % 2 == 0:
            # if not, add a new chess game to all chess games dictionary
            chessGame = Board()
            allChessGames[totalConn] = chessGame
        else:
            # chess game is the newest on the dictionary
            chessGame = allChessGames[totalConn - 1]

        thread = threading.Thread(target=handle_client, args=(conn, address, chessGame, totalConn))
        thread.start()
        print(f" \nACTIVE CONNECTIONS: {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()

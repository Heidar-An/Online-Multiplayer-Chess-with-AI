def check(row, column):
    """Check if position is valid"""
    if 0 <= row <= 7 and 0 <= column <= 7:
        return True
    return False


class Bishop: # class for bishop 
    def __init__(self, colour):
        self.colour = colour
        self.type = "b"
        # different attributes for different colours
        if colour == "w":
            self.image = "wb.svg"
            self.value = 30
        else:
            self.image = "bb.svg"
            self.value = -30

    def eval(self, i, j, AiTurn):
        """Get the evaluation of the piece at a certain position"""
        # used for AI, get the evaluation at different positions
        evalList = [
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
            [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
            [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
            [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
            [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
        ]
        if AiTurn:
            evalList.reverse() # reverse it if it is the other player's turn
        evaluation = evalList[i][j] # get evaluation
        return evaluation # return eval

    def possibleMoves(self, row, column, possibleMoves, boardPosition):
        """find all possible bishop moves at a certain position"""

        # check top left diagonal
        columnTemp = column
        for i in range(row - 1, -1, -1):
            columnTemp -= 1
            if check(row, columnTemp):
                if boardPosition[i][columnTemp] == "":
                    possibleMoves[i][columnTemp] = "green"
                elif boardPosition[i][columnTemp].colour != self.colour:
                    possibleMoves[i][columnTemp] = "green" # make position green
                    break
                else:
                    break

        # check bottom right diagonal
        columnTemp = column
        for i in range(row + 1, 8):
            columnTemp += 1
            if check(row, columnTemp):
                if boardPosition[i][columnTemp] == "":
                    possibleMoves[i][columnTemp] = "green"
                elif boardPosition[i][columnTemp].colour != self.colour:
                    possibleMoves[i][columnTemp] = "green" # make position green
                    break
                else:
                    break

        # check top right diagonal
        columnTemp = column
        for i in range(row - 1, -1, -1):
            columnTemp += 1
            if check(row, columnTemp):
                if boardPosition[i][columnTemp] == "":
                    possibleMoves[i][columnTemp] = "green" # bishopp can move here
                elif boardPosition[i][columnTemp].colour != self.colour:
                    possibleMoves[i][columnTemp] = "green" # piece can move here
                    break
                else:
                    break

        # check bottom left diagonal
        columnTemp = column
        for i in range(row + 1, 8):
            columnTemp -= 1
            if check(row, columnTemp):
                if boardPosition[i][columnTemp] == "":
                    possibleMoves[i][columnTemp] = "green" # bishop can move here
                elif boardPosition[i][columnTemp].colour != self.colour:
                    possibleMoves[i][columnTemp] = "green" # bishop can move here
                    break
                else:
                    break
        return possibleMoves # return where the bishop can move


class Pawn:
    def __init__(self, colour):
        self.colour = colour
        self.type = "p"
        # different attributes for different colours
        if colour == "w":
            self.image = "wp.svg"
            self.value = 10
        else:
            self.image = "bp.svg"
            self.value = -10

    def eval(self, i, j, AiTurn):
        """Get the evaluation of the piece at a certain position"""
        evalList = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
            [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
            [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
            [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
            [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
            [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]
        if AiTurn:
            evalList.reverse() # reverse it if it is the other player's turn
        evaluation = evalList[i][j] # get eval
        return evaluation # return eval

    def possibleMoves(self, row, column, possibleMoves, boardPosition):
        """Return all possible pawn moves"""

        if self.colour == "w":
            if check(row - 1, column):
                if boardPosition[row - 1][column] == "":
                    possibleMoves[row - 1][column] = "green"
            # if row == 6, pawn can move up two columns
            if row == 6:
                if boardPosition[row - 1][column] == "" and boardPosition[row - 2][column] == "":
                    possibleMoves[row - 2][column] = "green"
            # check for enemy to the top left and top right of pawn
            if check(row - 1, column - 1):
                if boardPosition[row - 1][column - 1] != "" and boardPosition[row - 1][column - 1].colour == "b":
                    possibleMoves[row - 1][column - 1] = "green"
            if check(row - 1, column + 1):
                if boardPosition[row - 1][column + 1] != "" and boardPosition[row - 1][column + 1].colour == "b":
                    possibleMoves[row - 1][column + 1] = "green"

        if self.colour == "b":
            if check(row + 1, column):
                if boardPosition[row + 1][column] == "":
                    possibleMoves[row + 1][column] = "green"
            # if row == 1, pawn can move up two columns
            if row == 1:
                if boardPosition[row + 1][column] == "" and boardPosition[row + 2][column] == "":
                    possibleMoves[row + 2][column] = "green"
            # check for enemy to the top left and top right of pawn
            if check(row + 1, column - 1):
                if boardPosition[row + 1][column - 1] != "" and boardPosition[row + 1][column - 1].colour == "w":
                    possibleMoves[row + 1][column - 1] = "green"
            if check(row + 1, column + 1):
                if boardPosition[row + 1][column + 1] != "" and boardPosition[row + 1][column + 1].colour == "w":
                    possibleMoves[row + 1][column + 1] = "green"
        return possibleMoves


class Knight:
    def __init__(self, colour):
        self.colour = colour
        self.type = "n"
        if colour == "w":
            self.image = "wn.svg"
            self.value = 30
        else:
            self.image = "bn.svg"
            self.value = -30

    def eval(self, i, j, AiTurn):
        """Get the evaluation of the piece at a certain position"""
        # used for AI, get the evaluation at different positions
        evalList = [
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
            [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
            [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
            [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
            [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
            [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
        ]
        if AiTurn:
            evalList.reverse() # reverse it if it is the other player's turn 
        evaluation = evalList[i][j] # get eval
        return evaluation # return eval

    def possibleMoves(self, row, column, possibleMoves, boardPosition):
        """return all possible knight moves"""
        for i in range(-2, 3):
            for j in range(-2, 3):
                # Use Pythagoras
                if i ** 2 + j ** 2 == 5:
                    if check(row + i, column + j):
                        if boardPosition[row + i][column + j] == "":
                            possibleMoves[row + i][column + j] = "green" # knight can move here
                        elif boardPosition[row + i][column + j].colour != self.colour:
                            possibleMoves[row + i][column + j] = "green" # knight can move here
        return possibleMoves


class Rook:
    def __init__(self, colour):
        self.colour = colour
        self.type = "r"
        self.moved = False
        # different attributes for different colours
        if colour == "w":
            self.image = "wr.svg"
            self.value = 50
        else:
            self.image = "br.svg"
            self.value = -50

    def eval(self, i, j, AiTurn):
        """Get the evaluation of the piece at a certain position"""
        # used for AI, get the evaluation at different positions
        evalList = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
        ]
        if AiTurn:
            evalList.reverse() # reverse it if it is the other player's turn 
        evaluation = evalList[i][j] # get eval
        return evaluation # return eval

    def possibleMoves(self, row, column, possibleMoves, boardPosition):
        """return all possible rook moves"""

        """check up direction"""
        for i in range(row - 1, -1, -1):
            if boardPosition[i][column] == "":
                possibleMoves[i][column] = "green"
            elif boardPosition[i][column].colour != self.colour:
                possibleMoves[i][column] = "green"
                break
            else:
                break

        """check down direction"""
        for i in range(row + 1, 8):
            if boardPosition[i][column] == "":
                possibleMoves[i][column] = "green"
            elif boardPosition[i][column].colour != self.colour:
                possibleMoves[i][column] = "green"
                break
            else:
                break

        """check right direction"""
        for i in range(column + 1, 8):
            if boardPosition[row][i] == "":
                possibleMoves[row][i] = "green"
            elif boardPosition[row][i].colour != self.colour:
                possibleMoves[row][i] = "green"
                break
            else:
                break

        """check left direction"""
        for i in range(column - 1, -1, -1):
            if boardPosition[row][i] == "":
                possibleMoves[row][i] = "green"
            elif boardPosition[row][i].colour != self.colour:
                possibleMoves[row][i] = "green"
                break
            else:
                break
        return possibleMoves


class King:
    def __init__(self, colour):
        self.colour = colour
        self.type = "k"
        self.moved = False
        if colour == "w":
            self.image = "wk.svg"
            self.value = 0
        else:
            self.image = "bk.svg"
            self.value = 0

    def eval(self, i, j, AiTurn):
        """Get the evaluation of the piece at a certain position"""
        # used for AI, get the evaluation at different positions
        evalList = [
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
            [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
        ]
        if AiTurn:
            evalList.reverse()
        evaluation = evalList[i][j]
        return evaluation

    def possibleMoves(self, row, column, possibleMoves, boardPosition):
        """return all possible king moves / castling ability"""

        """all king moves"""
        for i in range(-1, 2):
            for j in range(-1, 2):
                if check(row + i, column + j):
                    if boardPosition[row + i][column + j] == "":
                        possibleMoves[row + i][column + j] = "green"
                    elif boardPosition[row + i][column + j].colour != self.colour:
                        possibleMoves[row + i][column + j] = "green"

        """Castling"""
        if self.colour == "w":
            if row == 7 and column == 4:
                if self.moved is False:
                    # King Side Castling
                    if boardPosition[7][5] == "" and boardPosition[7][6] == "" and boardPosition[7][7] != "":
                        if boardPosition[7][7].type == "r":
                            if boardPosition[7][7].moved is False:
                                possibleMoves[7][6] = "green"
                                # kingWillMove = True
                    # Queen Side Castling
                    if boardPosition[7][3] == "" and boardPosition[7][2] == "" and boardPosition[7][1] == "" and \
                            boardPosition[7][0] != "":
                        if boardPosition[7][0].type == "r":
                            if boardPosition[7][0].moved is False:
                                possibleMoves[7][2] = "green"
                                # kingWillMove = True
        if self.colour == "b":
            if row == 0 and column == 4:
                if self.moved is False:
                    if boardPosition[0][5] == "" and boardPosition[0][6] == "" and boardPosition[0][7] != "":
                        if boardPosition[0][7].type == "r":
                            if boardPosition[0][7].moved is False:
                                possibleMoves[0][6] = "green"
                                # kingWillMove = True
                    if boardPosition[0][3] == "" and boardPosition[0][2] == "" and boardPosition[0][1] == "" and \
                            boardPosition[0][0] != "":
                        if boardPosition[0][0].type == "r":
                            if boardPosition[0][0].moved is False:
                                possibleMoves[0][2] = "green"
                                # kingWillMove = True

        return possibleMoves


class Queen:
    def __init__(self, colour):
        self.colour = colour
        self.type = "q"
        if colour == "w":
            self.image = "wq.svg"
            self.value = 90
        else:
            self.image = "bq.svg"
            self.value = -90

    def eval(self, i, j, AiTurn):
        """Get the evaluation of the piece at a certain position"""
        # used for AI, get the evaluation at different positions
        evalList = [
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ]
        if AiTurn:
            evalList.reverse() # reverse it if it is the other player's turn 
        evaluation = evalList[i][j] # get eval
        return evaluation # return eval

    def possibleMoves(self, row, column, possibleMoves, boardPosition):
        """Return all possible queen moves"""
        # queen moves is the same as the rook moves + bishop moves
        bishopMoves = Bishop(self.colour).possibleMoves(row, column, possibleMoves, boardPosition)
        queenMoves = Rook(self.colour).possibleMoves(row, column, bishopMoves, boardPosition)
        return queenMoves # return possible moves

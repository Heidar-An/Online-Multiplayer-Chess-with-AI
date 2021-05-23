class Piece:
    def __init__(self, colour, type, image, killable=False):
        self.colour = colour
        self.type = type
        self.killable = killable
        self.image = image


bp = Piece("b", "p", "bp.svg")
bk = Piece("b", "k", "bk.svg")
br = Piece("b", "r", "br.svg")
bb = Piece("b", "b", "bb.svg")
bq = Piece("b", "q", "bq.svg")
bn = Piece("b", "n", "bn.svg")

wp = Piece("w", "p", "wp.svg")
wk = Piece("w", "k", "wk.svg")
wr = Piece("w", "r", "wr.svg")
wb = Piece("w", "b", "wb.svg")
wq = Piece("w", "q", "wq.svg")
wn = Piece("w", "n", "wn.svg")

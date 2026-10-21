from enum import Enum


class Col(Enum):
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8


type_regular = ["Pawn", "Bishop", "Knight", "Rook", "Queen", "King"]
class Piece:
    def __init__(self, type_piece, col: Col, row, color):
        if (
                type_piece not in type_regular
                or not isinstance(col, Col)
                or row not in range(1, 9)
                or color not in ("B", "W")
        ):
            raise ValueError("Invalid piece")

        self.type_piece=type_piece
        self.col=col
        self.row=row
        self.color=color
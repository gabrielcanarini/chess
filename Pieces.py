type_regular = ["Pawn", "Bishop", "Knight", "Rook", "Queen", "King"]
class Piece:
    def __init__(self, type_piece, color):
        if (
                type_piece not in type_regular
                or color not in ("B", "W")
        ):
            raise ValueError("Invalid piece")

        self.type_piece=type_piece
        self.color=color


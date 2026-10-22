from Pieces import *
import tkinter as tk
from PIL import Image, ImageTk

def get_initial_state_pieces():
    piece = []

    # Torri
    piece.append(Piece(type_piece="Rook", color="W", col=Col.a, row=1))
    piece.append(Piece(type_piece="Rook", color="B", col=Col.a, row=8))
    piece.append(Piece(type_piece="Rook", color="W", col=Col.h, row=1))
    piece.append(Piece(type_piece="Rook", color="B", col=Col.h, row=8))

    # Cavalli
    piece.append(Piece(type_piece="Knight", color="W", col=Col.b, row=1))
    piece.append(Piece(type_piece="Knight", color="B", col=Col.b, row=8))
    piece.append(Piece(type_piece="Knight", color="W", col=Col.g, row=1))
    piece.append(Piece(type_piece="Knight", color="B", col=Col.g, row=8))

    # Alfieri
    piece.append(Piece(type_piece="Bishop", color="W", col=Col.c, row=1))
    piece.append(Piece(type_piece="Bishop", color="B", col=Col.c, row=8))
    piece.append(Piece(type_piece="Bishop", color="W", col=Col.f, row=1))
    piece.append(Piece(type_piece="Bishop", color="B", col=Col.f, row=8))

    # Donna
    piece.append(Piece(type_piece="Queen", color="W", col=Col.d, row=1))
    piece.append(Piece(type_piece="Queen", color="B", col=Col.d, row=8))

    # Re
    piece.append(Piece(type_piece="King", color="W", col=Col.e, row=1))
    piece.append(Piece(type_piece="King", color="B", col=Col.e, row=8))

    #PEZZO DI TEST
    piece.append(Piece(type_piece="King", color="B", col=Col.c, row=3))
    piece.append(Piece(type_piece="King", color="W", col=Col.c, row=6))


    # Pedoni
    for i in Col:
        piece.append(Piece(type_piece="Pawn", color="W", col=i, row=2))
        piece.append(Piece(type_piece="Pawn", color="B", col=i, row=7))
    return piece


class Game:
    pieces = []
    selected_piece: Piece | None = None
    legal_move: list[Cell] = []
    window = tk.Tk()
    images = {}
    marker = None
    main_frame = None

    def __init__(self):
        self.pieces = get_initial_state_pieces()
        self.selected_piece = None
        self.legal_move = []
        self.main_frame = None

        #Load asset
        self.images = {
        (color, piece): Image.open(
            f"./gui/asset/{color}_{piece}.png"
        ).convert("RGBA").resize((32,64))
        for color in ("W", "B")
        for piece in ("Pawn", "Rook", "Knight", "Bishop", "Queen", "King")
        }
        self.marker = Image.open("./gui/asset/marker.png").convert("RGBA").resize((21,21))



    def calc_legal_move(self):
        self.legal_move = []
        piece = self.selected_piece
        if piece is None:
            return


        if piece.type_piece == "Pawn":
            if piece.color == "W":
                #Mossa base, una casella avanti
                def x(p: Piece):
                    return p.row == piece.row+1 and p.col.value == piece.col.value

                nextPiece = next(filter(x, self.pieces), None)

                if nextPiece is None:
                    self.legal_move.append(Cell(row=piece.row+1, col=piece.col))

                #Controllo i lati se puó mangiare
                def x(p: Piece):
                    return p.row == piece.row + 1 and p.col.value == piece.col.value - 1 and p.color == "B"

                pezzo_laterale_sinistro =next(filter(x, self.pieces), None)

                if pezzo_laterale_sinistro is not None:
                    self.legal_move.append(Cell(row=piece.row+1, col=Col(piece.col.value - 1)))

                def x(p: Piece):
                    return p.row == piece.row + 1 and p.col.value == piece.col.value + 1 and p.color == "B"

                pezzo_laterale_destro =next(filter(x, self.pieces), None)

                if pezzo_laterale_destro is not None:
                    self.legal_move.append(Cell(row=piece.row+1, col=Col(piece.col.value+1)))

                #Controllo la prima mosso di 2 caselle avanti
                if piece.row == 2 and nextPiece is None:
                    def x(p: Piece):
                        return p.row == piece.row + 2 and p.col == piece.col
                    due_avvanti = next(filter(x, self.pieces), None)
                    if due_avvanti is None:
                        self.legal_move.append(Cell(row=piece.row + 2, col=piece.col))

            if piece.color == "B":
                # Mossa base, una casella avanti
                def x(p: Piece):
                    return p.row == piece.row - 1 and p.col.value == piece.col.value

                nextPiece = next(filter(x, self.pieces), None)

                if nextPiece is None:
                    self.legal_move.append(Cell(row=piece.row - 1, col=piece.col))

                # Controllo i lati se puó mangiare
                def x(p: Piece):
                    return p.row == piece.row - 1 and p.col.value == piece.col.value + 1 and p.color == "W"

                pezzo_laterale_sinistro = next(filter(x, self.pieces), None)

                if pezzo_laterale_sinistro is not None:
                    self.legal_move.append(Cell(row=piece.row - 1, col=Col(piece.col.value + 1)))

                def x(p: Piece):
                    return p.row == piece.row - 1 and p.col.value == piece.col.value - 1 and p.color == "W"

                pezzo_laterale_destro = next(filter(x, self.pieces), None)

                if pezzo_laterale_destro is not None:
                    self.legal_move.append(Cell(row=piece.row - 1, col=Col(piece.col.value - 1)))

                # Controllo la prima mosso di 2 caselle avanti
                if piece.row == 7 and nextPiece is None:
                    def x(p: Piece):
                        return p.row == piece.row - 2 and p.col == piece.col

                    due_avvanti = next(filter(x, self.pieces), None)
                    if due_avvanti is None:
                        self.legal_move.append(Cell(row=piece.row - 2, col=piece.col))






        print(f"{self.legal_move}")



    def select_piece(self, piece: Piece):
        if self.selected_piece is not None and self.selected_piece.col == piece.col and self.selected_piece.row == piece.row:
            return

        self.selected_piece = piece
        self.calc_legal_move()


        self.draw_board()


    def draw_board(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
        self.main_frame = tk.Frame(self.window)
        self.main_frame.grid()
        for r in range(1,9):
            for c in range(1,9):
                bg = "black" if (r + c) % 2 == 0 else "white"

                cella = tk.Frame(self.main_frame, width=100, height=100, bg=bg)
                cella.grid(row=8 - r, column=c - 1)
                cella.grid_propagate(False)

                def x(p: Piece) -> bool:
                    return r == p.row and c == p.col.value

                piece = next(filter(x, self.pieces), None)
                def y(c: Cell):
                    return c.col.value == c and c.row == r

                is_legal_move = any(
                    cell.row == r and cell.col.value == c
                    for cell in self.legal_move
                )

                if piece is not None and is_legal_move:
                    marker = self.marker.copy()
                    piece_img = self.images[(piece.color, piece.type_piece)].copy()
                    piece_img.alpha_composite(marker)
                    img = ImageTk.PhotoImage(piece_img)
                    label = tk.Label(cella, image=img, borderwidth=0, bg=bg)
                    label.image = img
                    label.place(rely=0.5,relx=0.5, anchor="center")
                    continue

                if piece is not None and not is_legal_move:
                    img = ImageTk.PhotoImage(self.images[(piece.color, piece.type_piece)])

                    label = tk.Label(cella, image=img, borderwidth=0, bg=bg)
                    label.image = img
                    label.bind("<Button-1>", lambda event, p=piece: self.select_piece(p))
                    label.place(rely=0.5,relx=0.5,anchor="center")
                    continue

                if is_legal_move:
                    img = ImageTk.PhotoImage(self.marker)
                    label = tk.Label(cella, image=img, borderwidth=0, bg=bg)
                    label.image = img
                    label.place(relx=0.5,rely=0.5,anchor="center")



    def start_game(self):
        self.window.title("Chess")
        self.window.resizable(False, False)



        self.draw_board()

        self.window.mainloop()
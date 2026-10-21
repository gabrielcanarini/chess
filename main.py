import tkinter as tk
from enum import Enum

import Pieces


def create_window(game: list[Pieces.Piece]):
    window = tk.Tk()
    window.title("Chess")
    window.resizable(False, False)

    main_frame = tk.Frame(window)
    main_frame.grid()

    ##Load asset
    images = {
        (color, piece): tk.PhotoImage(
            file=f"./gui/asset/{color}_{piece}.png"
        )
        for color in ("W", "B")
        for piece in ("Pawn", "Rook", "Knight", "Bishop", "Queen", "King")
    }

    pieces_by_position = {
        (p.row, p.col.value): p
        for p in game
    }

    for r in range(1,9):
        for c in range(1,9):
            bg = "white" if (r + c) % 2 == 0 else "black"

            cella = tk.Frame(main_frame, width=100,height=100, bg=bg)
            cella.grid(row=r-1, column=c-1)
            cella.grid_propagate(False)

            piece = pieces_by_position.get((r, c))

            if piece:
                img = images[(piece.color, piece.type_piece)]

                label = tk.Label(cella, image=img, bg=bg, borderwidth=0)
                label.place(relx=0.5,rely=0.5,anchor="center")

    window.mainloop()


def start_game():
    game = get_initial_game_list()
    create_window(game)


def get_initial_game_list():
    piece = []

    #Torri
    piece.append(Pieces.Piece(type_piece="Rook", color="W", col=Pieces.Col.a, row=1))
    piece.append(Pieces.Piece(type_piece="Rook", color="B", col=Pieces.Col.a, row=8))
    piece.append(Pieces.Piece(type_piece="Rook", color="W", col=Pieces.Col.h, row=1))
    piece.append(Pieces.Piece(type_piece="Rook", color="B", col=Pieces.Col.h, row=8))

    #Cavalli
    piece.append(Pieces.Piece(type_piece="Knight", color="W", col=Pieces.Col.b, row=1))
    piece.append(Pieces.Piece(type_piece="Knight", color="B", col=Pieces.Col.b, row=8))
    piece.append(Pieces.Piece(type_piece="Knight", color="W", col=Pieces.Col.g, row=1))
    piece.append(Pieces.Piece(type_piece="Knight", color="B", col=Pieces.Col.g, row=8))

    #Alfieri
    piece.append(Pieces.Piece(type_piece="Bishop", color="W", col=Pieces.Col.c, row=1))
    piece.append(Pieces.Piece(type_piece="Bishop", color="B", col=Pieces.Col.c, row=8))
    piece.append(Pieces.Piece(type_piece="Bishop", color="W", col=Pieces.Col.f, row=1))
    piece.append(Pieces.Piece(type_piece="Bishop", color="B", col=Pieces.Col.f, row=8))

    #Donna
    piece.append(Pieces.Piece(type_piece="Queen", color="W", col=Pieces.Col.d, row=1))
    piece.append(Pieces.Piece(type_piece="Queen", color="B", col=Pieces.Col.d, row=8))

    #Re
    piece.append(Pieces.Piece(type_piece="King", color="W", col=Pieces.Col.e, row=1))
    piece.append(Pieces.Piece(type_piece="King", color="B", col=Pieces.Col.e, row=8))

    #Pedoni
    for i in Pieces.Col:
        piece.append(Pieces.Piece(type_piece="Pawn", color="W", col=i, row=2))
        piece.append(Pieces.Piece(type_piece="Pawn", color="B", col=i, row=7))
    return piece

if __name__ == '__main__':
    start_game()





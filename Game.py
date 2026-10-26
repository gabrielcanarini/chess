from Pieces import *
import tkinter as tk
from PIL import Image, ImageTk

def get_initial_state_pieces():
    pieces: list[Piece | None] = [None] * 64

    # Pezzi neri
    pieces[56:64] = [
        Piece(type_piece="Rook", color="B"),
        Piece(type_piece="Knight", color="B"),
        Piece(type_piece="Bishop", color="B"),
        Piece(type_piece="Queen", color="B"),
        Piece(type_piece="King", color="B"),
        Piece(type_piece="Bishop", color="B"),
        Piece(type_piece="Knight", color="B"),
        Piece(type_piece="Rook", color="B"),
    ]

    # Pedoni neri
    for col in range(8):
        pieces[48 + col] = Piece(type_piece="Pawn", color="B")

    # Pedoni bianchi
    for col in range(8):
        pieces[8 + col] = Piece(type_piece="Pawn", color="W")

    # Pezzi bianchi
    pieces[0:8] = [
        Piece(type_piece="Rook", color="W"),
        Piece(type_piece="Knight", color="W"),
        Piece(type_piece="Bishop", color="W"),
        Piece(type_piece="Queen", color="W"),
        Piece(type_piece="King", color="W"),
        Piece(type_piece="Bishop", color="W"),
        Piece(type_piece="Knight", color="W"),
        Piece(type_piece="Rook", color="W"),
    ]

    #PEZZI TEST
    pieces[32] = Piece(type_piece="Knight", color="W")

    return pieces

def get_index_by_initial_position(pos: int, spostamento_row: int, spostamento_col: int):
    row = pos // 8
    col = pos % 8

    new_row = row + spostamento_row
    new_col = col + spostamento_col

    if not (0 <= new_row < 8 and 0 <= new_col < 8):
        return None

    return new_row * 8 + new_col
def get_row_by_index(pos: int):
    return pos // 8
def get_col_by_index(pos: int):
    return pos % 8

class Game:
    pieces: list[Piece | None] = []
    selected_piece: int | None = None
    legal_move: list[int] = []
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


    #funzione che da una casella ta dá l'index di una casella rispetto ad un movimento x/y dato

    def check_and_add_legal_move(self, i: int):
        # DA VEDERE SE LA MOSSA É EFFETTIVAMENTE LEGALE: non ho ancora verificato se la mossa porta la situazione di scacco.

        self.legal_move.append(i)


    def search_possible_move(self, pos: int):
        self.legal_move = []
        piece = self.pieces[pos]

        if piece is None:
            return


        if piece.type_piece == "Pawn":
            if piece.color == "W":
                #Mossa base, una casella avanti
                indice_casella_davanti = get_index_by_initial_position(pos, 1, 0)
                if self.pieces[indice_casella_davanti] is None:
                    self.check_and_add_legal_move(indice_casella_davanti)

                #Controllo i lati se puó mangiare
                indice_pezzo_laterale_sinistro = get_index_by_initial_position(pos, 1, 1)

                if self.pieces[indice_pezzo_laterale_sinistro] is not None and self.pieces[indice_pezzo_laterale_sinistro].color == "B":
                    self.check_and_add_legal_move(indice_pezzo_laterale_sinistro)

                indice_pezzo_laterale_destro = get_index_by_initial_position(pos, 1, -1)

                if self.pieces[indice_pezzo_laterale_destro] is not None and self.pieces[indice_pezzo_laterale_destro].color == "B":
                    self.check_and_add_legal_move(indice_pezzo_laterale_destro)

                #Controllo la prima mossa di 2 caselle avanti
                if self.pieces[indice_casella_davanti] is None and get_row_by_index(pos) == 2:
                    indice_due_caselle_avanti = get_index_by_initial_position(pos, 2, 0)
                    if \
                    self.pieces[indice_due_caselle_avanti] is None or self.pieces[indice_due_caselle_avanti].color == "B":
                        self.check_and_add_legal_move(indice_due_caselle_avanti)

            if piece.color == "B":
                #Mossa base, una casella avanti
                indice_casella_davanti = get_index_by_initial_position(pos, -1, 0)
                if self.pieces[indice_casella_davanti] is None:
                    self.check_and_add_legal_move(indice_casella_davanti)

                #Controllo i lati se puó mangiare
                indice_pezzo_laterale_sinistro = get_index_by_initial_position(pos, -1, 1)

                if self.pieces[indice_pezzo_laterale_sinistro] is not None and self.pieces[indice_pezzo_laterale_sinistro].color == "W":
                    self.check_and_add_legal_move(indice_pezzo_laterale_sinistro)

                indice_pezzo_laterale_destro = get_index_by_initial_position(pos, -1, -1)

                if self.pieces[indice_pezzo_laterale_destro] is not None and self.pieces[indice_pezzo_laterale_destro].color == "W":
                    self.check_and_add_legal_move(indice_pezzo_laterale_destro)

                #Controllo la prima mossa di 2 caselle avanti
                if self.pieces[indice_casella_davanti] is None and get_row_by_index(pos) == 7:
                    indice_due_caselle_avanti = get_index_by_initial_position(pos, -2, 0)
                    if \
                    self.pieces[indice_due_caselle_avanti] is None or self.pieces[indice_due_caselle_avanti].color == "B":
                        self.check_and_add_legal_move(indice_due_caselle_avanti)

        if piece.type_piece == "Bishop":
            #ciclo per un massimo di 7 volte (la massima distanza che puó percorrere) finche non trovo un ostacolo. In ogni direzione
            o_alto_destro = False
            o_alto_sinistro = False
            o_basso_destro = False
            o_basso_sinistro = False

            for i in range(1,8):
                #Alto destro
                index = get_index_by_initial_position(pos, i ,i)
                if not o_alto_destro and not index is None:
                    p_index = self.pieces[index]
                    if p_index is None:
                        self.check_and_add_legal_move(index)
                    elif p_index.color == piece:
                        o_alto_destro = True
                    elif p_index.color != piece.color:
                        self.check_and_add_legal_move(index)
                        o_alto_destro = True

                #alto sinistro
                index = get_index_by_initial_position(pos, i, -i)
                if not o_alto_sinistro and not index is None:
                    p_index = self.pieces[index]
                    if p_index is None:
                        self.check_and_add_legal_move(index)
                    elif p_index.color == piece:
                        o_alto_sinistro = True
                    elif p_index.color != piece.color:
                        self.check_and_add_legal_move(index)
                        o_alto_sinistro = True

                #basso destro
                index = get_index_by_initial_position(pos, -i, i)
                if not o_basso_destro and not index is None:
                    p_index = self.pieces[index]
                    if p_index is None:
                        self.check_and_add_legal_move(index)
                    elif p_index.color == piece:
                        o_basso_destro= True
                    elif p_index.color != piece.color:
                        self.check_and_add_legal_move(index)
                        o_basso_destro = True

                #basso sinistro
                index = get_index_by_initial_position(pos, -i, -i)
                if not o_basso_sinistro and not index is None:
                    p_index = self.pieces[index]
                    if p_index is None:
                        self.check_and_add_legal_move(index)
                    elif p_index.color == piece:
                        o_basso_sinistro = True
                    elif p_index.color != piece.color:
                        self.check_and_add_legal_move(index)
                        o_basso_sinistro = True

        if piece.type_piece == "Knight":
            return



        print(f"{self.legal_move}")



    def select_piece(self, position: int):
        if self.selected_piece is not None and self.selected_piece == position:
            return
        print(f"posizione: {position}, tipo: {self.pieces[position].type_piece}, colore: {self.pieces[position].color}")

        self.selected_piece = position
        self.search_possible_move(position)


        #Soluzione pessima, si vede un attimo di schermata bianca qunado aggiorna si deve trovare una soluzione migliore.
        self.draw_board()


    def draw_board(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
        self.main_frame = tk.Frame(self.window)
        self.main_frame.grid()
        for r in range(0, 64):
            bg = "white" if (get_row_by_index(r) + get_col_by_index(r)) % 2 != 0 else "black"

            cella = tk.Frame(self.main_frame, width=100, height=100, bg=bg)
            cella.grid(row=8-get_row_by_index(r), column=get_col_by_index(r))
            cella.grid_propagate(False)

            piece = self.pieces[r]

            is_legal_move = r in self.legal_move

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
                label.bind("<Button-1>", lambda event, position=r: self.select_piece(position))
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
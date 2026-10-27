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
    pieces[36] = Piece(type_piece="King", color="W")
    pieces[45] = Piece(type_piece="King", color="W")

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
    return pos // 8 + 1
def get_col_by_index(pos: int):
    return pos % 8 + 1

class Game:
    pieces: list[Piece | None] = []
    selected_piece: int | None = None
    legal_move: list[int] = []
    window = tk.Tk()
    images = {}
    marker = None
    main_frame = None
    turn = "W"

    def __init__(self):
        self.pieces = get_initial_state_pieces()
        self.selected_piece = None
        self.legal_move = []
        self.main_frame = None
        self.turn = "W"

        #Load asset
        self.images = {
        (color, piece): Image.open(
            f"./gui/asset/{color}_{piece}.png"
        ).convert("RGBA").resize((32,64))
        for color in ("W", "B")
        for piece in ("Pawn", "Rook", "Knight", "Bishop", "Queen", "King")
        }
        self.marker = Image.open("./gui/asset/marker.png").convert("RGBA").resize((21,21))



    def check_and_add_legal_move(self, i: int):
        # DA VEDERE SE LA MOSSA É EFFETTIVAMENTE LEGALE: non ho ancora verificato se la mossa porta la situazione di scacco.
        # OVVIAMENTE IL PEZZO MANGIATO NON PUÓ ESSERE UN RE, da verificare
        self.legal_move.append(i)


    def search_possible_move(self, pos: int):
        self.legal_move = []
        piece = self.pieces[pos]

        if piece is None:
            return

        def pawn_move():
            if piece.color == "W":
                #Mossa base, una casella avanti
                indice_casella_davanti = get_index_by_initial_position(pos, 1, 0)

                if not indice_casella_davanti is None and self.pieces[indice_casella_davanti] is None:
                    self.check_and_add_legal_move(indice_casella_davanti)

                #Controllo i lati se puó mangiare
                indice_pezzo_laterale_sinistro = get_index_by_initial_position(pos, 1, 1)

                if not indice_pezzo_laterale_sinistro is None and self.pieces[indice_pezzo_laterale_sinistro] is not None and self.pieces[indice_pezzo_laterale_sinistro].color == "B":
                    self.check_and_add_legal_move(indice_pezzo_laterale_sinistro)

                indice_pezzo_laterale_destro = get_index_by_initial_position(pos, 1, -1)

                if not indice_pezzo_laterale_destro is None and self.pieces[indice_pezzo_laterale_destro] is not None and self.pieces[indice_pezzo_laterale_destro].color == "B":
                    self.check_and_add_legal_move(indice_pezzo_laterale_destro)

                #Controllo la prima mossa di 2 caselle avanti
                if get_row_by_index(pos) == 2:
                    if not indice_casella_davanti is None and self.pieces[indice_casella_davanti] is None:
                        due_avanti = get_index_by_initial_position(pos, 2, 0)
                        if not due_avanti is None and self.pieces[due_avanti] is None:
                            self.check_and_add_legal_move(due_avanti)

            if piece.color == "B":
                #Mossa base, una casella avanti
                indice_casella_davanti = get_index_by_initial_position(pos, -1, 0)
                if not indice_casella_davanti is None and self.pieces[indice_casella_davanti] is None:
                    self.check_and_add_legal_move(indice_casella_davanti)

                #Controllo i lati se puó mangiare
                indice_pezzo_laterale_sinistro = get_index_by_initial_position(pos, -1, 1)

                if not indice_pezzo_laterale_sinistro is None and self.pieces[indice_pezzo_laterale_sinistro] is not None and self.pieces[indice_pezzo_laterale_sinistro].color == "W":
                    self.check_and_add_legal_move(indice_pezzo_laterale_sinistro)

                indice_pezzo_laterale_destro = get_index_by_initial_position(pos, -1, -1)

                if not indice_pezzo_laterale_destro is None and self.pieces[indice_pezzo_laterale_destro] is not None and self.pieces[indice_pezzo_laterale_destro].color == "W":
                    self.check_and_add_legal_move(indice_pezzo_laterale_destro)

                #Controllo la prima mossa di 2 caselle avanti
                if get_row_by_index(pos) == 7:
                    if not indice_casella_davanti is None and self.pieces[indice_casella_davanti] is None:
                        due_avanti = get_index_by_initial_position(pos, -2, 0)
                        if not due_avanti is None and self.pieces[due_avanti] is None:
                            self.check_and_add_legal_move(due_avanti)

        def bishop_move():
            # ciclo per un massimo di 7 volte (la massima distanza che puó percorrere) finche non trovo un ostacolo. In ogni direzione
            o_alto_destro = False
            o_alto_sinistro = False
            o_basso_destro = False
            o_basso_sinistro = False

            for i in range(1, 8):
                # Alto destro
                index = get_index_by_initial_position(pos, i, i)
                if not o_alto_destro and not index is None:
                    p_index = self.pieces[index]
                    if p_index is None:
                        self.check_and_add_legal_move(index)
                    elif p_index.color == piece:
                        o_alto_destro = True
                    elif p_index.color != piece.color:
                        self.check_and_add_legal_move(index)
                        o_alto_destro = True

                # alto sinistro
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

                # basso destro
                index = get_index_by_initial_position(pos, -i, i)
                if not o_basso_destro and not index is None:
                    p_index = self.pieces[index]
                    if p_index is None:
                        self.check_and_add_legal_move(index)
                    elif p_index.color == piece:
                        o_basso_destro = True
                    elif p_index.color != piece.color:
                        self.check_and_add_legal_move(index)
                        o_basso_destro = True

                # basso sinistro
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

        def knight_move():
            #MOVIMENTO CON L ROVESCIATA
            index_alto_destra = get_index_by_initial_position(pos, 1 , 2)
            index_alto_sinistra = get_index_by_initial_position(pos, 1, -2)
            index_basso_destra = get_index_by_initial_position(pos, -1, 2)
            index_basso_sinistra = get_index_by_initial_position(pos, -1, -2)

            if not index_alto_destra is None:
                p = self.pieces[index_alto_destra]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index_alto_destra)


            if not index_alto_sinistra is None:
                p = self.pieces[index_alto_sinistra]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index_alto_sinistra)


            if not index_basso_destra is None:
                p = self.pieces[index_basso_destra]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index_basso_destra)


            if not index_basso_sinistra is None:
                p = self.pieces[index_basso_sinistra]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index_basso_sinistra)


            #MOVIMENTI CON L NON ROVESCIATA
            index_alto_destra = get_index_by_initial_position(pos, 2 , 1)
            index_alto_sinistra = get_index_by_initial_position(pos, 2, -1)
            index_basso_destra = get_index_by_initial_position(pos, -2, 1)
            index_basso_sinistra = get_index_by_initial_position(pos, -2, -1)

            if not index_alto_destra is None:
                p = self.pieces[index_alto_destra]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index_alto_destra)


            if not index_alto_sinistra is None:
                p = self.pieces[index_alto_sinistra]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index_alto_sinistra)


            if not index_basso_destra is None:
                p = self.pieces[index_basso_destra]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index_basso_destra)


            if not index_basso_sinistra is None:
                p = self.pieces[index_basso_sinistra]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index_basso_sinistra)

        def rook_move():
            o_up = False
            o_down = False
            o_right = False
            o_left = False

            for i in range(1, 8):
                c_up = get_index_by_initial_position(pos, i, 0)
                c_down = get_index_by_initial_position(pos, -i, 0)
                c_right = get_index_by_initial_position(pos, 0, i)
                c_left = get_index_by_initial_position(pos, 0, -i)

                if not o_up and not c_up is None:
                    p = self.pieces[c_up]
                    if p is None:
                        self.check_and_add_legal_move(c_up)
                    elif p.color != piece.color:
                        self.check_and_add_legal_move(c_up)
                        o_up = True
                    else:
                        o_up = True

                if not o_down and not c_down is None:
                    p = self.pieces[c_down]
                    if p is None:
                        self.check_and_add_legal_move(c_down)
                    elif p.color != piece.color:
                        self.check_and_add_legal_move(c_down)
                        o_down = True
                    else:
                        o_down = True

                if not o_right and not c_right is None:
                    p = self.pieces[c_right]
                    if p is None:
                        self.check_and_add_legal_move(c_right)
                    elif p.color != piece.color:
                        self.check_and_add_legal_move(c_right)
                        o_right = True
                    else:
                        o_right = True

                if not o_left and not c_left is None:
                    p = self.pieces[c_left]
                    if p is None:
                        self.check_and_add_legal_move(c_left)
                    elif p.color != piece.color:
                        self.check_and_add_legal_move(c_left)
                        o_left = True
                    else:
                        o_left = True

        def queen_move():
            bishop_move()
            rook_move()

        def king_move():
            #Da definire arrocco
            index = get_index_by_initial_position(pos, 1, 0)
            if not index is None:
                p = self.pieces[index]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index)

            index = get_index_by_initial_position(pos, -1, 0)
            if not index is None:
                p = self.pieces[index]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index)

            index = get_index_by_initial_position(pos, 0, 1)
            if not index is None:
                p = self.pieces[index]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index)

            index = get_index_by_initial_position(pos, 0, -1)
            if not index is None:
                p = self.pieces[index]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index)

            index = get_index_by_initial_position(pos, 1, 1)
            if not index is None:
                p = self.pieces[index]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index)

            index = get_index_by_initial_position(pos, 1, -1)
            if not index is None:
                p = self.pieces[index]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index)

            index = get_index_by_initial_position(pos, 0, 1)
            if not index is None:
                p = self.pieces[index]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index)

            index = get_index_by_initial_position(pos, 0, -1)
            if not index is None:
                p = self.pieces[index]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index)

            index = get_index_by_initial_position(pos, -1, 1)
            if not index is None:
                p = self.pieces[index]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index)

            index = get_index_by_initial_position(pos, -1, -1)
            if not index is None:
                p = self.pieces[index]
                if p is None or p.color != piece.color:
                    self.check_and_add_legal_move(index)


        if piece.type_piece == "Pawn":
            pawn_move()

        if piece.type_piece == "Bishop":
            bishop_move()

        if piece.type_piece == "Knight":
            knight_move()

        if piece.type_piece == "Rook":
          rook_move()

        if piece.type_piece == "Queen":
            queen_move()

        if piece.type_piece == "King":
            king_move()

        print(f"{self.legal_move}")

    def switch_turn(self):
        self.turn = "W" if self.turn == "B" else "B"

    def move_piece(self, pos, new_pos):
        self.pieces[new_pos] = self.pieces[pos]
        self.pieces[pos] = None
        self.selected_piece = None
        self.switch_turn()

    def select_cell(self, position: int):
        p_s = self.pieces[position]

        # 1. Click sul pezzo già selezionato
        if position == self.selected_piece:
            return

        # 2. Nessun pezzo selezionato: provo a selezionarne uno
        if self.selected_piece is None:
            if p_s is not None and p_s.color == self.turn:
                self.selected_piece = position
                self.search_possible_move(position)
                self.draw_board()
            return

        # 3. Click su una destinazione valida: muovo il pezzo
        if position in self.legal_move:
            self.move_piece(self.selected_piece, position)

            self.selected_piece = None
            self.legal_move = []

            self.draw_board()
            return

        # 4. Click su un altro pezzo dello stesso colore: cambio selezione
        if p_s is not None and p_s.color == self.turn:
            self.selected_piece = position
            self.search_possible_move(position)
            self.draw_board()
            return

        # 5. Click su una casella non valida: deseleziono
        self.selected_piece = None
        self.legal_move = []
        self.draw_board()

    def draw_board(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
        self.main_frame = tk.Frame(self.window)
        self.main_frame.grid()
        for r in range(0, 64):
            bg = "white" if (get_row_by_index(r) + get_col_by_index(r)) % 2 != 0 else "black"

            cella = tk.Frame(self.main_frame, width=100, height=100, bg=bg)
            cella.bind("<Button-1>", lambda event, position=r: self.select_cell(position))
            cella.grid(row=8-get_row_by_index(r), column=get_col_by_index(r))
            cella.grid_propagate(False)

            piece = self.pieces[r]

            is_legal_move = r in self.legal_move

            if piece is not None and is_legal_move:
                marker = self.marker.copy()
                piece_img = self.images[(piece.color, piece.type_piece)].copy()

                x = (piece_img.width - marker.width) // 2
                y = (piece_img.height - marker.height) // 2

                piece_img.alpha_composite(marker, (x,y))
                img = ImageTk.PhotoImage(piece_img)
                label = tk.Label(cella, image=img, borderwidth=0, bg=bg)
                label.image = img
                label.place(rely=0.5,relx=0.5, anchor="center")
                continue

            if piece is not None and not is_legal_move:
                img = ImageTk.PhotoImage(self.images[(piece.color, piece.type_piece)])

                label = tk.Label(cella, image=img, borderwidth=0, bg=bg)
                label.image = img
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
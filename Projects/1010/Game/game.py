import random

from Game import Piece, Board, PIECES, SIZE, N_PIECES


class Game:
    board : Board
    score : int
    pieces : list[int]

    def __init__(self):
        self.board = Board()
        self.score = 0
        self.pieces = []

    def new_round(self) -> list[int]:
        if len([piece for piece in self.pieces if piece != -1]) > 0:
            return self.pieces
        
        self.pieces = random.choices(range(len(PIECES)), k=N_PIECES)
        return self.pieces

    def play(self, piece_index: int, row: int, col: int) -> tuple[list[int], list[int]]:
        piece: Piece = PIECES[piece_index]
        rows, cols = self.board.place(piece_index, row, col)

        points: int = piece.bits.bit_count()
        cleared: int = len(rows) + len(cols)
        points += cleared * (cleared + 1) * SIZE / 2
        self.score += points

        self.pieces[self.pieces.index(piece_index)] = -1
        return (rows, cols)
        

    def print(self) -> None:
        print(f"\nPontuação: {self.score}")
        print("\nTABULEIRO")
        self.board.print()
        print("\nPEÇAS:")
        for index in self.pieces:
            if index == -1: continue
            PIECES[index].print()
            print()

    def is_gameover(self) -> bool:
        if len([piece for piece in self.pieces if piece != -1]) == 0:
            self.new_round()

        for index in self.pieces:
            if len(self.board.get_valid_positions(index=index)) > 0:
                return False

        return True

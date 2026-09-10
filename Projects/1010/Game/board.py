from typing import Self

from Game import Piece, PIECES, SIZE


class Board:
    FULL_ROW: int = 0
    FULL_COL: int = 0
    bits: int = 0

    def __init__(self, bits: int = 0):
        self.bits = bits
        self.FULL_ROW = (1 << SIZE) - 1
        for row in range(SIZE):
            self.FULL_COL |= 1 << row * SIZE

    def copy(self) -> Self:
        return Board(self.bits)

    def can_place(self, index: int, row: int, col: int) -> bool:
        piece: Piece = PIECES[index]

        # Fora do tabuleiro
        if row < 0 or col < 0:
            return False
        if row + piece.height > SIZE:
            return False
        if col + piece.width > SIZE:
            return False

        # Colisão
        return not (self.bits & (piece.bits << (row * SIZE + col)))

    def place(self, index: int, row: int, col: int) -> tuple[list[int], list[int]]:
        piece: Piece = PIECES[index]

        if not self.can_place(index, row, col):
            raise ValueError("Jogada inválida")

        self.bits |= piece.bits << (row * SIZE + col)
        return self.clear_completed()

    def clear_completed(self) -> tuple[list[int], list[int]]:
        rows: list[int] = []
        cols: list[int] = []

        for row in range(SIZE):
            mask: int = self.FULL_ROW << (row * SIZE)
            if self.bits & mask == mask:
                rows.append(row)

        for col in range(SIZE):
            mask: int = self.FULL_COL << col
            if self.bits & mask == mask:
                cols.append(col)

        clear_mask: int = 0

        for row in rows:
            clear_mask |= self.FULL_ROW << (row * SIZE)

        for col in cols:
            clear_mask |= self.FULL_COL << col

        self.bits &= ~clear_mask
        return rows, cols

    def get_valid_positions(self, index: int) -> list[tuple[int, int]]:
        piece: Piece = PIECES[index]
        positions = []

        for row in range(SIZE - piece.height + 1):
            for col in range(SIZE - piece.width + 1):
                if self.can_place(index, row, col):
                    positions.append((row, col))

        return positions

    def is_empty(self, row: int, col: int) -> bool:
        position = row * SIZE + col
        return not (self.bits & (1 << position))

    def empty_cells(self) -> int:
        return SIZE * SIZE - self.bits.bit_count()

    def print(self) -> None:
        for row in range(SIZE):
            line = []
            for col in range(SIZE):
                line.append(
                    "X" if bool(self.bits & (1 << (row * SIZE + col))) else "."
                )
            print(" ".join(line))

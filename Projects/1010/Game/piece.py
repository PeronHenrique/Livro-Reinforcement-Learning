from Game import SIZE, bits_from_string

class Piece:
    def __init__(self, name: str, shape: str):
        self.name = name
        self.bits = bits_from_string(shape)

        positions = [
            i for i in range(self.bits.bit_length())
            if self.bits & (1 << i)
        ]

        rows = [pos // SIZE for pos in positions]
        cols = [pos % SIZE for pos in positions]

        self.width = max(cols) - min(cols) + 1
        self.height = max(rows) - min(rows) + 1

    def __repr__(self) -> str:
        piece_str = (
            f"Name: {self.name}\n"
            f"Dimentions: {self.width} x {self.height}" 
            )
        
        for row in range(self.height):
            line = []
            for col in range(self.width):
                line.append("X" if bool(self.bits & (1 << (row * SIZE + col))) else ".")
            piece_str = piece_str + f'\n{" ".join(line)}'

        return piece_str



    def print(self) -> None:
        for row in range(self.height):
            line = []
            for col in range(self.width):
                line.append("X" if bool(self.bits & (1 << (row * SIZE + col))) else ".")

            print(" ".join(line))
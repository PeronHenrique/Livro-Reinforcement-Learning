from Game import PIECES

class Move:
    def __init__(
        self,
        index: int,
        row: int,
        col: int,
    ):
        self.index: int = index
        self.row: int = row
        self.col: int = col

    def __repr__(self):
        return (
            f"Move("
            f"{PIECES[self.index].name}, "
            f"row={self.row}, "
            f"col={self.col}"
            f")"
        )
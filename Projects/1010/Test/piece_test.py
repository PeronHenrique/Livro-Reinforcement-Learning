from Game import PIECES


def test_pieces():
    assert len(PIECES) > 0

    for piece in PIECES:
        assert piece.name
        assert piece.bits > 0
        assert piece.width > 0
        assert piece.height > 0

def print_pieces() -> None:
	for piece in PIECES:
		print(piece, "\n")


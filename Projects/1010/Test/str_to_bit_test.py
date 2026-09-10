import pytest
from Game import Board, bits_from_string, SIZE

def test_board_line_too_large():
    with pytest.raises(ValueError):
        bits_from_string("""
            XXX...XXX.
            X.X...XXX
            X.X...XXX....
            X.X...XXX.
            X.X...XXX
            XXX...XXX
            ...XXX
            ...XXX
        """)

def test_board_too_many_lines():
    with pytest.raises(ValueError):
        bits_from_string("""
            XXX...XXX.
            X.X...XXX
            X.X...XXX.
            X.X...XXX.
            X.X...XXX
            XXX...XXX
            ...XXX
            ...XXX
            ...XXX
            ...XXX
            ...XXX
        """)
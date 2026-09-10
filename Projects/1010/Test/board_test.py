from Game import Board, PIECES, SIZE, bits_from_string

def test_create_board():
	# Board vazio
	bits = bits_from_string("")
	assert bits == 0

	board = Board(bits)
	assert board.empty_cells() == SIZE * SIZE

	board2 = Board()
	assert board2.bits == 0
	assert board2.empty_cells() == SIZE * SIZE

	# Board parcialmente definido
	board3 = Board(bits_from_string("""
		XXX...XXX.
		X.X...XXX
		X.X...XXX.
		X.X...XXX.
		X.X...XXX
		XXX...XXX
		...XXX
	"""))
    
	assert board3.bits != 0
	assert board3.empty_cells() < SIZE * SIZE
    


def test_place_piece():
    board = Board()
    index = 1  # square_2
    assert board.can_place(index, 0, 0)

    rows, cols = board.place(index, 0, 0)
    assert rows == []
    assert cols == []

    assert board.empty_cells() == SIZE * SIZE - 4
    assert not board.is_empty(0, 0)
    assert not board.is_empty(0, 1)
    assert not board.is_empty(1, 0)
    assert not board.is_empty(1, 1)


def test_collision():
    board = Board()
    index = 1  # square_2
    board.place(index, 0, 0)

    assert not board.can_place(index, 0, 0)
    assert not board.can_place(index, 1, 0)
    assert not board.can_place(index, 0, 1)
    assert not board.can_place(index, 1, 1)
    assert board.can_place(index, SIZE - 3, SIZE - 3)


def test_out_of_bounds():
    board = Board()
    index = 6  # horizontal_5

    assert board.can_place(index, 0, 5)
    assert not board.can_place(index, 0, 6)


def test_clear_row():
	board = Board()
	board.bits |= board.FULL_ROW
	assert board.empty_cells() == SIZE * (SIZE - 1)

	rows, cols = board.clear_completed()

	assert rows == [0]
	assert cols == []
	assert board.bits == 0


def test_clear_column():
	board = Board()
	board.bits |= board.FULL_COL
	assert board.empty_cells() == SIZE * (SIZE - 1)

	rows, cols = board.clear_completed()

	assert rows == []
	assert cols == [0]
	assert board.bits == 0


def test_multiple_lines():
	board = Board()
	board.bits |= board.FULL_ROW
	board.bits |= board.FULL_COL
      
	assert board.empty_cells() == (SIZE - 1) * (SIZE - 1)

	rows, cols = board.clear_completed()

	assert rows == [0]
	assert cols == [0]
	assert board.bits == 0

def test_get_positions():
	board = Board()

	for piece_index in range(len(PIECES)):
		count = len(board.get_valid_positions(piece_index))
		assert count == (SIZE - PIECES[piece_index].width + 1) * (SIZE - PIECES[piece_index].height + 1)
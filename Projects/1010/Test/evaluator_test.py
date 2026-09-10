from Game import Board, bits_from_string, SIZE
from Solvers import flood_fill, get_regions


def test_flood_fill():
	board = Board(bits_from_string("""
		XX........
		XX........
		..........
		..........
		..........
		..........
		..........
		..........
		..........
		..........
		"""))

	visited = set()
	area, perimeter = flood_fill(
		board,
		0,
		0,
		visited,
		empty=False
	)
	assert area == 4
	assert perimeter == 4

	board = Board(bits_from_string("""
		..........
		..........
		...X......
		...X...X..
		...XX..X..
		...XXXXX..
		.....XX...
		.....XX...
		..........
		..........
		"""))

	visited = set()
	area, perimeter = flood_fill(
		board,
		2,
		3,
		visited,
		empty=False
	)
	assert area == 15
	assert perimeter == 26

	visited = set()
	area, perimeter = flood_fill(
		board,
		0,
		0,
		visited,
		empty=True
	)
	assert area == SIZE * SIZE - 15
	assert perimeter == 26

def test_get_regions():

	board = Board(
		bits_from_string("""
		XX........
		XX........
		..........
		..........
		....XX....
		....XX....
		..........
		..........
		..........
		.........X
		""")
	)

	filled_regions = get_regions(board, empty=False)

	assert len(filled_regions) == 3
	assert filled_regions[0] == (4,4)
	assert filled_regions[1] == (4,8)
	assert filled_regions[2] == (1,2)

	empty_regions = get_regions(board, empty=True)

	assert len(empty_regions) == 1
	assert empty_regions[0] == (SIZE*SIZE-9, 14)
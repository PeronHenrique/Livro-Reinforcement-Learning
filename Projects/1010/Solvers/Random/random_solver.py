import random

from Game import Board
from Solvers import Move, Solution

def random_solve(board: Board, pieces: list[int]) -> Solution | None:
	board_copy = board.copy()
	moves: list[Move] = []
	for pieceindex in pieces:
		places = board_copy.get_valid_positions(pieceindex)
		if len(places) == 0:
			continue

		row, col = random.choice(places)
		moves.append(Move(index=pieceindex, row=row, col=col))
		board_copy.place(index=pieceindex, row=row, col=col)

	if len(moves) == 0: return None
	return Solution(moves=moves, board_bits=board_copy.bits, evaluation=0)
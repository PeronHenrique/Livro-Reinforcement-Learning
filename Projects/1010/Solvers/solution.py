from Solvers import Move

class Solution:
    moves: list[Move]
    board_bits: int
    evaluation: int
    
    def __init__(self, moves: list[Move], board_bits: int, evaluation: int):
        self.moves = moves
        self.board_bits = board_bits
        self.evaluation = evaluation

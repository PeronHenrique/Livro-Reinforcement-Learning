from typing import Callable

from Game import Board
from Solvers import Move, Solution

# muito lento para o jogo completo

def dfs_solve(board: Board, pieces: list[int], eval: Callable[[Board], int]) -> Solution | None:
    memo = {}
    solution = _dfs(board=board.copy(), pieces_left=pieces.copy(), memo=memo, eval=eval)
    print(len(memo))
    return solution
    

def _dfs(board: Board, pieces_left: list[int], memo: dict, eval: Callable[[Board], int]) -> Solution | None:
    # Estado equivalente:
    # mesma posição do tabuleiro + mesmas peças disponíveis
    key = board.bits
    if key in memo:
        return memo[key]

    # Não há mais peças para jogar
    if not pieces_left:
        solution = Solution(moves=[], board_bits=board.bits, evaluation=eval(board))
        memo[key] = solution
        return solution

    best_solution = None
    # Evita testar duas vezes peças iguais na mesma jogada
    used_pieces = set()

    for piece_index in pieces_left:
        if piece_index in used_pieces:
            continue
        used_pieces.add(piece_index)

        # Remove apenas uma ocorrência da peça
        remaining = pieces_left.copy()
        remaining.remove(piece_index)

        for row, col in board.get_valid_positions(piece_index):
            new_board = board.copy()
            new_board.place(piece_index, row, col)
            move = Move(index=piece_index, row=row, col=col)
            result: Solution = _dfs(board=new_board, pieces_left=remaining, memo=memo, eval=eval)
            if result is None:
                continue

            candidate = Solution(moves=[move, *result.moves], board_bits=result.board_bits, evaluation=result.evaluation)
            if (best_solution is None or candidate.evaluation > best_solution.evaluation):
                best_solution = candidate

    memo[key] = best_solution
    return best_solution
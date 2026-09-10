import pygame

from Game import Game, SIZE, PIECES
from Solvers import Move
from .colors import *
from .button import Button


class Renderer:

    piece_positions = [(560, 60), (560, 240), (560, 420)]

    def __init__(self, game: Game):
        self.game = game
        

        pygame.init()

        self.screen = pygame.display.set_mode((740, 590))
        self.restart_button = Button(330, 5, 200, 50, "RECOMEÇAR")
        
        pygame.display.set_caption("1010!")
        self.clock = pygame.time.Clock()
        self.clock.tick(60)

    def render(self):
        self.screen.fill(BACKGROUND)
        self.render_board()
        self.render_pieces()
        self.render_score()
        self.restart_button.draw(self.screen)
        if self.game.is_gameover():
            self.render_gameover()

        pygame.display.flip()

    def render_move(self, move: Move, progress: float):
        self.screen.fill(BACKGROUND)
        self.render_board()

        # peças normais
        pieces = [index for index in self.game.pieces]
        index_of_move = pieces.index(move.index)
        pieces[index_of_move] = -1
        self.render_pieces(pieces)
        # peça sendo movimentada
        self.render_moving_piece(move, index_of_move, progress)

        self.render_score()
        self.restart_button.draw(self.screen)

        pygame.display.flip()

    def render_board(self):
        board = self.game.board

        for row in range(SIZE):
            for col in range(SIZE):
                x = 30 + col * 50
                y = 60 + row * 50
                color = (EMPTY_COLOR if board.is_empty(row, col) else PIECE_COLOR)
                pygame.draw.rect(self.screen, color, (x, y, 48, 48), border_radius=5)

    def render_line_clear(self, rows, cols, progress):
        self.render_board()

        # Peças que não estão sendo apagadas
        for row in rows:
            for col in range(SIZE):
                self.draw_clear_cell(row, col, progress)

        for col in cols:
            for row in range(SIZE):
                if row not in rows:
                    self.draw_clear_cell(row, col, progress)

        self.render_pieces()
        self.render_score()
        self.restart_button.draw(self.screen)

        pygame.display.flip()

    def render_pieces(self, pieces: list[int] | None = None):
        if pieces is None:
            pieces = self.game.pieces
        for index, piece_index in enumerate(pieces):
            if piece_index == -1:
                continue

            piece = PIECES[piece_index]
            x, y = self.piece_positions[index]

            self.draw_piece(piece, x, y, 30)

    def render_moving_piece(self, move, index_of_move, progress):
        start_x, start_y = self.piece_positions[index_of_move]
        target_x = 30 + move.col * 50
        target_y = 60 + move.row * 50

        x = start_x + (target_x - start_x) * progress
        y = start_y + (target_y - start_y) * progress

        self.draw_piece(PIECES[move.index], x, y, 50)

    def draw_piece(self, piece, x, y, size):
        for row in range(piece.height):
            for col in range(piece.width):
                xi = x + col * size
                yi = y + row * size
                position = row * SIZE + col
                if piece.bits & (1 << position):
                    pygame.draw.rect( self.screen, PIECE_COLOR, (xi, yi, size-2, size-2), border_radius=5)

    def draw_clear_cell(self, row, col, progress):
        x = 30 + col * 50
        y = 60 + row * 50
        size = 48 * (1 - progress)

        offset = (48 - size) / 2
        pygame.draw.rect(self.screen, PIECE_COLOR,
            (x + offset, y + offset, size, size),
            border_radius= 5)

    def render_score(self):
        font = pygame.font.Font(None, 32)
        text = font.render(f"Score: {self.game.score}", True, TEXT_COLOR)
        self.screen.blit(text, (30, 20))

    def render_gameover(self):
        font = pygame.font.Font(None, 32)

        text = font.render("GAME OVER", True, TEXT_COLOR)
        self.screen.blit(text, (560, 20))
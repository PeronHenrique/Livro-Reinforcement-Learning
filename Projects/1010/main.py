import pygame

from Game import Game
from Solvers import Solution, random_solve
from Rendering import Renderer


def main():
	game = Game()
	game.new_round()
	renderer = Renderer(game)
	renderer.render()

	running = True
	solution = None
	move_index = 0
	last_move = 0
	move_delay = 200  # ms

	animation = None
	move_animation_duration = 360  # ms
	lines_animation_duration = 360  # ms

	while running:
		# Eventos do Pygame
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.MOUSEBUTTONDOWN and renderer.restart_button.clicked(event.pos):
				game = Game()
				game.new_round()
				renderer.game = game
				solution = None
				move_index = 0
				last_move = pygame.time.get_ticks()
				renderer.render()

		#Se game over continue
		if game.is_gameover(): 
			renderer.render()
			continue

		# Calcula uma nova solução
		if solution is None:
			left_pieces = [piece for piece in game.pieces if piece != -1]
			if len(left_pieces) == 0:
				game.new_round()
				renderer.render()
				last_move = pygame.time.get_ticks()
				left_pieces = game.pieces
			
			solution: Solution = random_solve(game.board, left_pieces)
			move_index = 0
			if not solution: continue

		now = pygame.time.get_ticks()
		if animation is None and now - last_move >= move_delay:
			move = solution.moves[move_index]
			animation = {"type": "move", "move": move, 
						 "start": now, "duration": move_animation_duration}

		if animation is not None and animation["type"] is "move":
			elapsed = now - animation["start"]
			progress = min(elapsed/animation["duration"], 1.0)
			renderer.render_move(animation["move"], progress)

			if progress >= 1.0:
				rows, cols = game.play(move.index, move.row, move.col)
				animation = None
				if len(rows) + len(cols) > 0:
					animation = {"type": "line", "rows": rows, "cols": cols, 
									"start": now, "duration": lines_animation_duration}
				move_index += 1
				last_move = now

		if animation is not None and animation["type"] is "line":
			elapsed = now - animation["start"]
			progress = min(elapsed/animation["duration"], 1.0)
			renderer.render_line_clear(animation["rows"], animation["cols"], progress)

			if progress >= 1.0:
				animation = None
				move_index += 1
				renderer.render()
				last_move = now

		if move_index >= len(solution.moves):
			solution = None
			move_index = 0

	pygame.quit()


if __name__ == "__main__":
    main()
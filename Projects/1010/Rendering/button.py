import pygame
from .colors import *


class Button:

    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 32)

    def draw(self, screen):
        pygame.draw.rect(screen, MEDIUM_GREY, self.rect, border_radius=8)
        text = self.font.render(self.text, True, BACKGROUND)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def clicked(self, position):
        return self.rect.collidepoint(position)
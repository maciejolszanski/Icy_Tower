import pygame
from pygame.sprite import Sprite
import settings

class Floor(Sprite):
    '''single floor'''

    def __init__(self,it_game,size):
        # size is x, y, width, height tuple
        super().__init__()
        self.it_game = it_game
        self.screen = it_game.screen
        self.settings = it_game.settings

        self.floor_color = self.settings.floor_color
        self.floor_border_color = self.settings.floor_border_color
        self.floor_rect_outer = pygame.Rect(size)
        self.floor_rect_inner = pygame.Rect(
            size[0] + self.settings.floor_border_width,
            size[1] + self.settings.floor_border_width,
            size[2] - 2*self.settings.floor_border_width,
            size[3] - 2*self.settings.floor_border_width
            )

    def blitme(self):
        pygame.draw.rect(self.it_game.screen, self.floor_border_color, self.floor_rect_outer)
        pygame.draw.rect(self.it_game.screen, self.floor_color, self.floor_rect_inner)

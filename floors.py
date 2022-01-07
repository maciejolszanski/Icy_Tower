import pygame
from pygame.sprite import Sprite
import settings

class Floor(Sprite):
    '''single floor'''

    def __init__(self,it_game,size):
        # size is (x, y, width, height) tuple
        super().__init__()
        self.it_game = it_game
        self.screen = it_game.screen
        self.settings = it_game.settings

        self.color = self.settings.floor_color
        self.border_color = self.settings.floor_border_color
        self.rect_outer = pygame.Rect(size)
        self.rect_inner = pygame.Rect(
            size[0] + self.settings.floor_border_width,
            size[1] + self.settings.floor_border_width,
            size[2] - 2*self.settings.floor_border_width,
            size[3] - 2*self.settings.floor_border_width
            )

    def move_down(self):
        '''scrolling the floor down'''
        self.rect_outer.y += self.settings.scroll_v
        self.rect_inner.y += self.settings.scroll_v

    def blitme(self):
        pygame.draw.rect(self.it_game.screen, self.border_color, self.rect_outer)
        pygame.draw.rect(self.it_game.screen, self.color, self.rect_inner)

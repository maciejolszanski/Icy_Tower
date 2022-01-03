import pygame, sys
from time import sleep

import settings
import floors

class IcyTower():
    '''
    General class to manage resources and control the game
    '''

    def __init__(self):
        '''initialize the game'''

        pygame.init()
        self.settings = settings.Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Icy_Tower")

        self.main_floor_size = (
            self.screen.get_rect().x,
            self.screen.get_rect().bottom - self.settings.floor_height - 20,
            self.screen.get_rect().width,
            self.settings.floor_height,
            )

        self.main_floor = floors.Floor(self,self.main_floor_size)

    def run_game(self):
        '''Starting the main loop of the game'''
        while True:
            # Waiting for the event to quit the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self._update_screen()

    def _update_screen(self):
        '''refreshing screen in each iteration'''
        self.screen.fill(self.settings.bg_color)
        self.main_floor.blitme()
        pygame.display.flip()



if __name__ == '__main__':
    icy_tower = IcyTower()
    icy_tower.run_game()
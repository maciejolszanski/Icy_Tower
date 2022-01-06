import pygame, sys
from time import sleep
import time
import random

import settings
import floors
import hero

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
        self.floors = pygame.sprite.Group()
        self._create_initial_floors()
        self.hero = hero.Hero(self)

    def run_game(self):
        '''Starting the main loop of the game'''
        while True:
            self._check_events()
            self.hero.update()
            self._update_screen()

    def _check_events(self):
        '''manage events of the game'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        '''check what key is pressed'''
        if event.key == pygame.K_LEFT:
            self.hero.moving_left = True
            self.hero.change_x_direction = True
        if event.key == pygame.K_RIGHT:
            self.hero.moving_right = True
            self.hero.change_x_direction = True
        if event.key == pygame.K_SPACE and not self.hero.in_air:
            self.hero.jump_start_time = time.time()
            self.hero.jump_start_y = self.hero.y
            self.hero.moving_up = True
            self.hero.in_air = True,
            self.hero.jump = True

    def _check_keyup_events(self,event):
        '''check what key is released'''
        if event.key == pygame.K_LEFT:
            self.hero.moving_left = False
        if event.key == pygame.K_RIGHT:
            self.hero.moving_right = False

    def _create_initial_floors(self):
        '''creating floors that are visible from the beggining of the game'''


        available_space = (self.settings.screen_height - 
        self.settings.floor_height)
        num_of_floors = available_space // self.settings.dist_between_floors + 1

        for num in range(num_of_floors):
            if num == 0:
                size = (
                    self.screen.get_rect().x,
                    (self.screen.get_rect().bottom - self.settings.floor_height 
                    -20),
                    self.screen.get_rect().width,
                    self.settings.floor_height,
                    )
                floor = floors.Floor(self,size)
                self.floors.add(floor)
            else:
                x_pos = random.randint(self.settings.floor_margin, self.settings.
                        screen_width - (self.settings.floor_max_width + 
                        self.settings.floor_margin))
                y_pos = (self.screen.get_rect().bottom - 
                        self.settings.floor_height - 20 - 
                        num*self.settings.dist_between_floors)
                width = random.randint(self.settings.floor_min_width, 
                        self.settings.floor_max_width)
                height = self.settings.floor_height
            
                size = (x_pos, y_pos, width, height)
               
                floor = floors.Floor(self,size)
                self.floors.add(floor)

    def _update_screen(self):
        '''refreshing screen in each iteration'''
        self.screen.fill(self.settings.bg_color)
        for floor in self.floors:
            floor.blitme()
        self.hero.blitme()
        pygame.display.flip() 


if __name__ == '__main__':
    icy_tower = IcyTower()
    icy_tower.run_game()
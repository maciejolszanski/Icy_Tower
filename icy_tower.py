import pygame, sys
from time import sleep
import time
import random

import settings
import floors
import hero
import menu

class IcyTower():
    '''
    General class to manage resources and control the game
    '''

    def __init__(self):
        '''initialize the game'''

        pygame.init()
        self.settings = settings.Settings()
        self.state = 'MENU'
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Icy_Tower")

        self._init_menu()
        self._init_gameplay()

    def _init_menu(self):
        '''init the game menu'''
        
        self.menu = menu.Menu(self)


    def _init_gameplay(self):
        '''init the gameplay screen elements'''
        self.floors = pygame.sprite.Group()
        self._create_initial_floors()
        self.hero = hero.Hero(self)

    def run_game(self):
        '''Starting the main loop of the game'''

        if self.state == "MENU":
            self._run_menu()
        elif self.state == 'PLAY':
            self._run_gameplay()
    
    def _run_menu(self):
        '''handling the menu'''
        while True:
            self._check_events()
            self._update_screen()
    
    def _run_gameplay(self):
        '''handling the gampeplay'''
        while True:
            self._check_events()
            if not self.hero.in_air:
                self.hero.check_falling(self.floors)
            # check if there is need to scroll the screen
            if self.hero.moving_up:
                self._scroll()
            self.hero.update()
            self._are_new_floors_needed()
            self._remove_unnecessary_floors()
            self._is_hero_fallen()
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
            if self.state == 'PLAY':
                self.hero.moving_left = True
                self.hero.change_x_direction = True
                self.hero.run_start_time = time.time()
        if event.key == pygame.K_RIGHT:
            if self.state == 'PLAY':
                self.hero.moving_right = True
                self.hero.change_x_direction = True     
                self.hero.run_start_time = time.time() 
        if event.key == pygame.K_DOWN:
            if self.state =='MENU':
                self.menu.active_button += 1
        if event.key == pygame.K_UP:
            if self.state =='MENU':
                self.menu.active_button -= 1
        if event.key == pygame.K_SPACE and not self.hero.in_air:
            if self.state == 'PLAY':
                self.hero.jump_start_time = time.time()
                self.hero.jump_start_y = self.hero.y
                self.hero.moving_up = True
                self.hero.jump = True
        if event.key == pygame.K_RETURN:
            self._change_state(
                self.settings.menu_buttons[self.menu.active_button])

    def _check_keyup_events(self,event):
        '''check what key is released'''
        if event.key == pygame.K_LEFT:
            if self.state == 'PLAY':
                self.hero.moving_left = False
                self.hero.run_speed = self.settings.run_speed
                self.hero.jump_power = self.settings.jump_power
        if event.key == pygame.K_RIGHT:
            if self.state == 'PLAY':
                self.hero.moving_right = False
                self.hero.run_speed = self.settings.run_speed
                self.hero.jump_power = self.settings.jump_power

    def _change_state(self, new_state):
        '''chenging the state of the game'''
        self.state = new_state
        self.run_game()

    def _create_initial_floors(self):
        '''creating floors that are visible from the beggining of the game'''

        # calculate availabe space and then number of initial floors to be drawn
        available_space = (self.settings.screen_height - 
        self.settings.floor_height)
        num_of_floors = available_space // self.settings.dist_between_floors + 1

        for num in range(num_of_floors):
            # first floor is the width of screen
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
            # rest of the floor is randomly sized and places
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

    def _scroll(self):
        '''scrolling the bakground while hero is moving up'''

        if self.hero.y < self.settings.screen_height/2:
            for floor in self.floors:
                floor.move_down()
            
            self.hero.do_scroll = True

    def _are_new_floors_needed(self):
        '''check if there is new floor needed and creating it'''
        
        # check what is the distance between the highest floor and the top of
        # the screen
        highest_floor = self.floors.sprites()[-1]
        dist = highest_floor.rect_outer.top
        
        if dist > self.settings.dist_between_floors/2:
            self._draw_normal_floor(highest_floor)

    def _draw_normal_floor(self, top_floor):
        '''drawing a new floor on the top''' 
        x_pos = random.randint(self.settings.floor_margin, self.settings.
                        screen_width - (self.settings.floor_max_width + 
                        self.settings.floor_margin))
        y_pos = (top_floor.rect_outer.top - 
                self.settings.dist_between_floors)
        width = random.randint(self.settings.floor_min_width, 
                self.settings.floor_max_width)
        height = self.settings.floor_height
    
        size = (x_pos, y_pos, width, height)

        floor = floors.Floor(self,size)
        self.floors.add(floor)

    def _remove_unnecessary_floors(self):
        '''remove floors which disappeared while hero was moving up'''

        for floor in self.floors:
            if (floor.rect_outer.top > self.settings.screen_height + 50):
                self.floors.remove(floor)

    def _is_hero_fallen(self):
        '''check if hero fell beyond the screen'''

        print(self.hero.rect.top > self.screen.get_rect().bottom)
        print(self.hero.rect.top)
        print(self.screen.get_rect().bottom)

        if self.hero.rect.top > self.screen.get_rect().bottom:
            
            for floor in self.floors:
                floor.kill()
            
            self._create_initial_floors()
            self.hero.spawn_on_the_base_floor(self.floors)
            self.hero.moving_down = False
            self.hero.in_air = False
            self.hero.jump = False
            self._change_state('MENU')

    def _update_screen(self):
        '''refreshing screen in each iteration'''
        self.screen.fill(self.settings.bg_color)
        if self.state == 'MENU':
            self.menu.update_menu()
            
        elif self.state == 'PLAY':
            for floor in self.floors:
                floor.blitme()
            self.hero.blitme()

        pygame.display.flip() 


if __name__ == '__main__':
    icy_tower = IcyTower()
    icy_tower.run_game()
from sys import settrace
import time
import pygame

class Hero():
    '''Class of the main character of the game'''

    def __init__(self, it_game):

        self.main_floor = it_game.main_floor
        self.screen = it_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = it_game.settings

        # Importing hero image and geting his rect
        self.image = pygame.image.load('images/hero.png')
        self.image = pygame.transform.scale(self.image, (90,80))
        self.rect = self.image.get_rect()
        self.rect.midbottom = it_game.main_floor.floor_rect_outer.midtop

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # attributes of moving the character
        self.moving_right = False
        self.moving_left = False
        self.change_x_direction = False

        self.jump = False
        self.in_air = False
        self.moving_up = False
        self.moving_down = False

        self.jump_start_time = 0
        self.jump_start_y = 0

    def update(self):
        '''moving the hero'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.run_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.run_speed
        if self.jump:
            self._fly()
        if self.change_x_direction:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.change_x_direction = False

        self.rect.x = self.x

    def _fly(self):
        '''control the flight of character'''
        
        # calculate the time of the flight
        self.flight_time = (time.time() - self.jump_start_time + 0.3) * 2
        self.flight_time = self.flight_time // 0.01 * 0.01
        
        # physics of the jump - actual y position
        self.y -= (self.settings.jump_v0*self.flight_time - 
                1/2*(self.settings.gravity*self.flight_time**2))
        
        # not allow to move down in first seconds
        if self.y > self.jump_start_y and self.flight_time < 0.1:
            self.y = self.jump_start_y


        if (self.rect.bottom > (self.main_floor.floor_rect_outer.top + 6) and 
            self.flight_time > 0.1): 
            # collision with main floor
            # if hero is slighly under top of the main floor, set its y to correct one  
            self.rect.bottom = self.main_floor.floor_rect_outer.top
            self.y = self.rect.top
            self.jump = False
            
        self.rect.y = self.y


    def blitme(self):
        '''displaying the hero on the screen'''
        self.screen.blit(self.image, self.rect)
        # print(self.rect.x)
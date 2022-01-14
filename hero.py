from sys import settrace
import time
import pygame

class Hero():
    '''Class of the main character of the game'''

    def __init__(self, it_game):

        self.it_game = it_game
        self.screen = it_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = it_game.settings

        # Importing hero image and getting his rect
        self.hero_size = (90,80)
        self.image = pygame.image.load('images/hero.png')
        self.image = pygame.transform.scale(self.image, self.hero_size)
        self.rect = self.image.get_rect()
        # spawn hero on the middle of the first floor
        for floor in it_game.floors:
            self.rect.midbottom = floor.rect_outer.midtop
            break

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
        self.drop_start_time = 0

        self.do_scroll = False

    def update(self):
        '''moving the hero'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.run_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.run_speed
        if self.jump:
            self._fly()
        # flipping the image to match the hero's direction
        if self.change_x_direction:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.change_x_direction = False

        # update the image x-pos
        self.rect.x = self.x

    def _fly(self):
        '''control the flight of character'''
        
        # calculate the time of the flight (+0.3 and *2 to give more dinamics 
        # at the beggining of the flight)
        self.flight_time = (time.time() - self.jump_start_time + 0.1) * 4.5
        # round the time to x.yz [s]
        self.flight_time = self.flight_time // 0.01 * 0.01

        self.drop_time = (time.time() - self.drop_start_time + 0.3) * 2
        self.drop_time = self.drop_time // 0.01 * 0.01

        '''First jump method'''
        # # physics of the jump - actual y position
        # self.y -= (self.settings.jump_v0*self.flight_time - 
        #         1/2*(self.settings.gravity*self.flight_time**2))
        
        # # not allow to move down in first seconds
        # if self.y > self.jump_start_y and self.flight_time < 0.1:
        #     self.y = self.jump_start_y
        
        '''Second jump method'''
        # at first calculate the max height of jump
        if not self.in_air:
            # calculate the h_max in meters
            self.h_max = self.settings.jump_v0**2 / (2*self.settings.gravity)
            # scale the meters to pixels based on the height of the hero - 1.5m
            self.h_max *= self.hero_size[0]/1.5
            # scale by a factor of the jump power
            self.h_max *= self.settings.jump_power
            self.in_air = True
        # then calculate the actual position of the hero
        else:
            # moving up is an uniform motion
            if self.moving_up:
                self.y -= self.settings.jump_v0 * self.flight_time
                if self.y <= self.jump_start_y - self.h_max:
                    self.moving_up = False
                    self.moving_down = True
                    self.drop_start_time = time.time()
                # lowering the hero while scrolling the screen
                if self.do_scroll:
                    self.scroll()
            # moving down is a free fall
            elif self.moving_down:
                self.y +=  1/2 * (self.settings.gravity * self.drop_time**2)
                self._check_collision(self.it_game.floors)
            
        # update the image y-pos    
        self.rect.y = self.y

    def _check_collision(self, floors):
        '''collision with floors'''

        for floor in floors:
            # check if the hero x position is inside any floor position
            if self.rect.centerx in range(floor.rect_outer.left, 
                                        floor.rect_outer.right):
                # then check if the y position of the hero is slightly beneath the 
                # floor
                if (self.rect.bottom > (floor.rect_outer.top)  
                    and self.rect.bottom < floor.rect_outer.top + 5
                    and self.flight_time > 0.1): 
                    self.rect.bottom = floor.rect_outer.top
                    self.y = self.rect.top
                    self.moving_down = False
                    self.in_air = False
                    self.jump = False
                    break
    
    def check_falling(self, floors):
        '''check if hero stepped out from a floor'''

        for floor in floors:
            # checking what floor is hero on
            # first check the y-position of hero and floors
            if self.rect.bottom in range(floor.rect_outer.top 
                - self.settings.dist_between_floors  + 20, floor.rect_outer.top + 10):
                # then check if hero is outside this floor
                if self.rect.centerx not in list(range(floor.rect_outer.left, 
                                        floor.rect_outer.right)):
                    self.moving_down = True
                    self.jump = True
                    self.in_air = True
                    self.drop_start_time = time.time()
                    self._fly()

    def scroll(self):
        '''moving hero down while scrolling floors'''
        self.y += self.settings.scroll_v/2
        # h_max has to be reduced while scrolling
        self.h_max -= self.settings.scroll_v
        if self.rect.y > self.settings.screen_height/2:
            self.do_scroll = False
        self.rect.y = self.y

    def blitme(self):
        '''displaying the hero on the screen'''
        self.screen.blit(self.image, self.rect)
        # print(self.rect.x)
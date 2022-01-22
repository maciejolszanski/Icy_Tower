import pygame
from pygame.sprite import Sprite

class Menu():
    '''This class creates a menu and handle navigating the menu'''

    def __init__(self, it_game):
        '''init the menu with any number of buttons'''
        self.settings = it_game.settings
        self.it_game = it_game
        self.screen = it_game.screen
        self.screen_rect = self.screen.get_rect()
        self.active_button = 0

        self.buttons = pygame.sprite.Group()
        self.but_width = self.settings.button_width
        self.but_height = self.settings.button_height

        self._generate_buttons()

    def _generate_buttons(self):
        '''generate buttons that creates a menu'''
        for text in self.settings.menu_buttons:
            size = (self.screen_rect.centerx - self.but_width/2, 
            300*self.settings.menu_buttons.index(text) + 100, self.but_width,self.
            but_height)
            button = Button(self.it_game, size, text)
            self.buttons.add(button)


    def update_menu(self):
        '''draw menu with updated active button'''

        for button in self.buttons:
            if list(self.buttons).index(button) == self.active_button:
                button.draw_activated()
            else:
                button.draw_deactivated()
    
    def draw_menu(self):
        '''displaying the menu'''

        for button in self.buttons:
            button.draw_button()


class Button(Sprite):
    '''create a single Button'''

    def __init__(self, it_game, size, text):
        '''create a Button'''
        super().__init__()
        self.screen = it_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = it_game.settings

        self.text = text
        self.font = self.settings.menu_font

        self.rect = pygame.Rect(size)
        self.draw_deactivated()

    def _prepare_text(self, activation):
        '''placing the text on the screen and centering on the button'''
        if activation:
            self.text_color = self.settings.font_col_act
            self.button_color = self.settings.button_color_act
        else:
            self.text_color = self.settings.font_col_deact
            self.button_color = self.settings.button_color_deact

        self.text_image = self.font.render(self.text, True, 
            self.text_color, self.button_color)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.center = self.rect.center


    def draw_deactivated(self):
        '''draw deactivated button'''

        self._prepare_text(False)
        self.draw_button()
    

    def draw_activated(self):
        '''draw deactivated button'''

        self._prepare_text(True)
        self.draw_button()

    def draw_button(self):
        '''displaying empty button and then a text on it'''
        pygame.draw.rect(self.screen,self.button_color,
         self.rect, 0, 10)
        pygame.draw.rect(self.screen,self.settings.button_border_color,
         self.rect, self.settings.button_border_width, 10)
        self.screen.blit(self.text_image,self.text_rect)
        
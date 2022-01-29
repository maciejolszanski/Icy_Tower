import pygame


class Settings():
    '''Class that stores all settings'''

    def __init__(self):

        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (76, 0, 153)

        # floor settings
        self.floor_height = 40
        self.floor_color = (153, 0, 153)
        self.floor_border_color = (102, 0, 102)
        self.floor_border_width = 4
        self.dist_between_floors = 160
        self.floor_margin = 20
        self.floor_min_width = 150
        self.floor_max_width = 300

        # game settings
        self.states = ['MENU', 'GAMEPLAY', ]

        # hero settings
        self.run_speed = 1.2
        self.jump_v0 = 1.4
        self.jump_power = 5.0
        self.dyn_run_factor = 1.05
        self.dyn_jump_factor = 1.35

        # physics settings
        self.gravity = 1
        self.scroll_v = 2

        # button settings
        self.menu_font = pygame.font.Font(
            r'suplemental_files\SnackerComic_PerosnalUseOnly.ttf', 72)
        self.font_col_act = (255, 255, 255)
        self.font_col_deact = (0, 0, 0)
        self.button_color_act = (255, 128, 0)
        self.button_color_deact = (210, 105, 0)
        self.button_border_color = (0, 0, 0)
        self.button_border_width = 4
        self.button_width = 350
        self.button_height = 150

        # menu settings
        self.menu_buttons = ['PLAY', 'SETTINGS']

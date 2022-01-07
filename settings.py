class Settings():
    '''Class that stores all settings'''

    def __init__(self):

        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (76,0,153)

        #floor settings
        self.floor_height = 40
        self.floor_color = (153, 0, 153)
        self.floor_border_color = (102, 0, 102)
        self.floor_border_width = 4
        self.dist_between_floors = 160
        self.floor_margin = 20
        self.floor_min_width = 150
        self.floor_max_width = 300

        self.scroll_v = 2

        # hero settings
        self.run_speed = 1.2
        self.jump_v0 = 1.3
        self.jump_power = 5.0

        # physics settings
        self.gravity = 1

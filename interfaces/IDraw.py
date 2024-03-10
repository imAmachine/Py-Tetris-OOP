class IDraw:
    def fill_screen(self, surface, color):
        raise NotImplementedError

    def draw_block(self, surface, color, rect):
        raise NotImplementedError

    def draw_text(self, surface, text, font, color):
        raise NotImplementedError

    def init_window(self, window_size):
        raise NotImplementedError

    def display_update(self, rect):
        raise NotImplementedError
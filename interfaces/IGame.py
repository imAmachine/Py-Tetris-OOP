class IGame:
    def process_events(self):
        raise NotImplementedError

    def game_loop(self, draw_engine):
        raise NotImplementedError
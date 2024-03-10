from engine.game_objects import Block


class DrawEngine:
    def __init__(self, window_size, window_title, background_color, drawing_layer):
        self.drawing_layer = drawing_layer
        self.screen = self.drawing_layer.init_window(window_title, window_size)
        self.background_color = background_color
        self.objects_to_draw = []

    def add_object(self, obj):
        if obj:
            self.objects_to_draw.append(obj)

    def remove_object(self, obj):
        if obj in self.objects_to_draw:
            self.objects_to_draw.remove(obj)

    def draw(self):
        self.drawing_layer.fill_screen(self.screen, self.background_color)
        for obj in self.objects_to_draw:
            if obj:
                obj.draw(self.screen, self.drawing_layer)
        self.drawing_layer.display_update()
        print(f"drawed elements: {len(self.objects_to_draw)}")

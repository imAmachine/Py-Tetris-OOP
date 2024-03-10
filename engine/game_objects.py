import random
from interfaces.IDrawable import IDrawable


class GameField(list, IDrawable):
    def __init__(self, field_size_blcks, field_size_px, default_color, isBordered, padding=(0, 0)):
        super().__init__()
        self.width = field_size_blcks[0]
        self.height = field_size_blcks[1]
        self.default_blocks_color = default_color
        self.isBordered = isBordered
        self.padding = padding
        self.real_size_px = field_size_px
        self.field_size_px = (field_size_px[0] - padding[0] * 2,
                              field_size_px[1] - padding[1] * 2)

    def _get_block_size_px(self):
        return min(self.field_size_px) / min((self.width, self.height))

    def initialize_field(self):
        self.clear()
        block_size_px = self._get_block_size_px()
        self.extend([[Block(block_size_px * j + self.padding[0],
                            block_size_px * i + self.padding[1],
                            block_size_px, self.isBordered)
                    for j in range(self.width)]
                    for i in range(self.height)])

    def check_lines(self, from_y, count):
        lines_found = 0
        for i in range(from_y, from_y + count):
            if all(block.isFixed for block in self[i]):
                self.shift_lines(i)
        return lines_found

    def shift_lines(self, to_y):
        for i in range(to_y, 0, -1):
            if all(not block.isFixed for block in self[i]):
                break
            for j in range(self.width):
                self[i][j].set_fixed(self[i-1][j].color)

    def draw(self, surface, layer):
        for line in self:
            for block in line:
                block.draw(surface, layer)

class Text(IDrawable):
    def __init__(self, text, x, y, width, height, color, font_name, hidden=False) -> None:
        self.text = text
        self.pos = (x, y)
        self.size = (width, height)
        self.color = color
        self.font_name = font_name
        self.hidden = hidden

    def draw(self, surface, drawing_layer):
        if not self.hidden:
            drawing_layer.draw_text(surface, self.text, self.pos[0], self.pos[1],
                            self.size[0], self.size[1], self.color, self.font_name)

class Block(IDrawable):
    def __init__(self, x=0.0, y=0.0, size=5.0, border=True) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.isFixed = False
        self.color = None
        self.border = True

    def set_fixed(self, color=None) -> None:
        self.isFixed = color != None
        self.color = color

    def draw(self, surface, layer):
        layer.draw_block(surface, self.color, self.x, self.y, self.size, self.size, self.border)


class Tetromino(IDrawable):
    SHAPES = {
        'I': [[1, 1, 1, 1]],
        'J': [[1, 0, 0], [1, 1, 1]],
        'L': [[0, 0, 1], [1, 1, 1]],
        'O': [[1, 1], [1, 1]],
        'S': [[0, 1, 1], [1, 1, 0]],
        'T': [[0, 1, 0], [1, 1, 1]],
        'Z': [[1, 1, 0], [0, 1, 1]]
    }

    COLORS = {
        'I': (0, 255, 255),  # Cyan
        'J': (0, 0, 255),    # Blue
        'L': (255, 165, 0),  # Orange
        'O': (255, 255, 0),  # Yellow
        'S': (0, 255, 0),    # Green
        'T': (128, 0, 128),  # Purple
        'Z': (255, 0, 0)     # Red
    }

    @staticmethod
    def get_random_tetromino(start_pos=(0, 0)):
        choice = random.choice(list(Tetromino.SHAPES.keys()))
        fg = Tetromino(start_pos[0], start_pos[1], choice)
        return fg

    def __init__(self, x, y, shape) -> None:
        self.x = x
        self.y = y
        self.shape = self.SHAPES[shape]
        self.color = self.COLORS[shape]
        self.blocks = None

    def rotate(self, to_right: bool):
        self.shape = [list(x) for x in zip(*self.shape)]
        if to_right:
            self.shape = self.shape[::-1]
        else:
            self.shape = [x[::-1] for x in self.shape]

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def fix(self):
        if self.blocks:
            for block in self.blocks:
                block.set_fixed(self.color)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface, layer):
        if self.blocks:
            for block in self.blocks:
                layer.draw_block(surface, self.color, block.x + 1, block.y + 1,
                                 block.size - 2, block.size - 2)
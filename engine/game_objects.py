import random
from interfaces.IDrawable import IDrawable


class GameField(list, IDrawable):
    def __init__(self, field_size_blcks, field_size_px, default_color, isGrid, padding=(0, 0)):
        super().__init__()
        self.width = field_size_blcks[0]
        self.height = field_size_blcks[1]
        self.default_blocks_color = default_color
        self.isGrid = isGrid
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
                            block_size_px)
                    for j in range(self.width)]
                    for i in range(self.height)])

    def check_lines(self, from_y, count):
        lines_found = 0
        for i in range(self.height):
            if all([block.isFixed for block in self[i]]):
                self.shift_lines(i)
        return lines_found
    
    def shift_lines(self, to_y):
        for i in range(to_y, 0, -1):
            print(f"shifted line {i}")
            cur_line = [block for block in self[i]]
            prev_line = [block for block in self[i-1]]
            for j in range(self.width):
                cur_line[j].set_fixed(prev_line[j].color)
    
    def draw(self, surface, layer):
        for line in self:
            for block in line:
                block.draw(surface, layer, self.isGrid)


class Block(IDrawable):
    def __init__(self, x=0.0, y=0.0, size=5.0) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.isFixed = False
        self.color = None

    def set_fixed(self, color=None) -> None:
        self.isFixed = color != None
        self.color = color

    def draw(self, surface, layer, border=False):
        layer.draw_block(surface, self.color, self.x, self.y, self.size, self.size)
        if border:
            layer.draw_block(surface, (155,155,155), self.x, self.y, self.size, self.size, 1)



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
    
    def get_random_tetromino(start_pos=(0, 0)):
        choice = random.choice(list(Tetromino.SHAPES.keys()))
        fg = Tetromino(start_pos[0], start_pos[1], choice)
        return fg

    def set_pos(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, surface, layer):
        if self.blocks:
            for block in self.blocks:
                layer.draw_block(surface, self.color, block.x + 1, block.y + 1, block.size - 2, block.size - 2)



class Text(IDrawable):
    def __init__(self, text, font, color=(255, 255, 255)):
        self.text = text
        self.font = font
        self.color = color

    def draw(self, surface, gp_draw):
        gp_draw.draw_text(surface, self.text, self.font, self.color)
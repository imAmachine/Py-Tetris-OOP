from engine.draw_engine import DrawEngine
from engine.game_engine import TetrisGame
from game_packet.DrawingLayer import DrawingLayer
from engine.game_objects import GameField

# параметры игровой логики
field_size_blcks = (10, 15) # размер поля в блоках
default_blocks_color = (255, 255, 255) # цвет заливки блока игрового поля по умолчанию
default_window_color = (155,155,155) # цвет заливки окна игры по умолчанию

# параметры движка
screen_size_px = (500, 800)
field_scaling_koef = 1
field_size_px = (screen_size_px[0] * field_scaling_koef,
                 screen_size_px[1] * field_scaling_koef) # размер игрового поля относительно окна в пикселях
game_title = "VLD`s TETROMINO"
game_field = GameField(field_size_blcks, field_size_px,
                       default_blocks_color, isGrid=True,
                       padding=(25 , 25))
drawing_engine = DrawEngine(screen_size_px, game_title, default_window_color, DrawingLayer()) # Инициализация движка отрисовки

if __name__ == "__main__":
    game = TetrisGame(drawing_engine, game_field)
    game.start_game()

from figgy.game_logic import Engine, Block

WIDTH = Block.block_size * Engine.scene_width
HEIGHT = Block.block_size * Engine.scene_height
TITLE = "Figgy"

engine = Engine(clock)


def draw():
    screen.fill((255, 255, 255))
    engine.draw()


def on_key_down():
    if keyboard.n:
        engine.start_game()
    elif keyboard.left:
        engine.move_left()
    elif keyboard.right:
        engine.move_right()
    elif keyboard.up:
        engine.rotate()
    elif keyboard.down:
        engine.drop()

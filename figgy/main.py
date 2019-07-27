from figgy.game_logic import Engine, Block

WIDTH = Block.block_size * Engine.scene_width
HEIGHT = Block.block_size * Engine.scene_height
TITLE = "Figgy"

engine = Engine(clock)


def draw():
    screen.fill((255, 255, 255))
    engine.draw()
    if not engine.is_running:
        screen.draw.text(
            "Press N key to start game!",
            centerx=0.5 * WIDTH,
            centery=0.5 * HEIGHT,
            shadow=(0.5, 0.5),
            color=(0, 200, 0),
        )


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

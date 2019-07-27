import os

import pytest
import pygame
from pgzero.loaders import set_root

import figgy
from figgy.game_logic import Block, Engine


@pytest.fixture
def pygame_setup():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_mode(
        (Block.block_size * Engine.scene_width, Block.block_size * Engine.scene_height)
    )
    set_root(os.path.dirname(os.path.abspath(figgy.__file__)))
    yield None
    pygame.display.quit()

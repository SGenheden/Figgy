import pytest
from figgy.game_logic import Block


@pytest.fixture
def new_block(pygame_setup):
    def wrapper(x=0, y=0):
        return Block("pastel1_0", {"x": x, "y": y})

    return wrapper


def test_move(new_block):
    block = new_block(0, 0)
    old_gridpos = block.grid_pos
    old_pos = block.pos

    block.move(+1, +1)

    assert old_gridpos[0] - block.grid_pos[0] == -1
    assert old_gridpos[1] - block.grid_pos[1] == -1
    assert old_pos[0] - block.pos[0] == -Block.block_size
    assert old_pos[1] - block.pos[1] == -Block.block_size


def test_rotate(new_block):
    block = new_block(0, 1)
    old_gridpos = block.grid_pos
    old_origin = block.origin

    block.rotate()

    assert old_gridpos[0] - block.grid_pos[0] == 1
    assert old_gridpos[1] - block.grid_pos[1] == 1
    assert old_origin[0] - block.origin[0] == 1
    assert old_origin[1] - block.origin[1] == 1

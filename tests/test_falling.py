import pytest

from figgy.game_logic import FallingObject, FallFailure, Engine


@pytest.fixture
def new_object(pygame_setup):
    # Create a square-shaped object
    templates = [
        [{"x": 0, "y": 1}, {"x": 1, "y": 1}, {"x": 0, "y": 0}, {"x": 1, "y": 0}]
    ]
    images = ["pastel1_0.png"]
    return FallingObject(templates, images)


def test_move_down(new_object):
    old_pos = list(new_object.to_dict().keys())

    new_object.move_down({})

    new_pos = list(new_object.to_dict().keys())
    for pos1, pos2 in zip(old_pos, new_pos):
        assert pos1[0] - pos2[0] == 0
        assert pos1[1] - pos2[1] == -1


def test_move_down_onto_block(new_object):
    fake_blocks = {(7, 3): None, (6, 3): None}

    with pytest.raises(FallFailure):
        new_object.move_down(fake_blocks)


def test_move_to_bottom(new_object):
    for _ in range(Engine.scene_height - 3):
        new_object.move_down({})

    with pytest.raises(FallFailure):
        new_object.move_down({})


def test_move_left(new_object):
    new_object.move_down({})
    old_pos = list(new_object.to_dict().keys())

    new_object.move_left({})

    new_pos = list(new_object.to_dict().keys())
    for pos1, pos2 in zip(old_pos, new_pos):
        assert pos1[0] - pos2[0] == 1
        assert pos1[1] - pos2[1] == 0


def test_move_left_onto_block(new_object):
    new_object.move_down({})
    old_pos = list(new_object.to_dict().keys())
    fake_blocks = {(5, 2): None}

    new_object.move_left(fake_blocks)

    new_pos = list(new_object.to_dict().keys())
    for pos1, pos2 in zip(old_pos, new_pos):
        assert pos1[0] - pos2[0] == 0
        assert pos1[1] - pos2[1] == 0


def test_move_right(new_object):
    new_object.move_down({})
    old_pos = list(new_object.to_dict().keys())

    new_object.move_right({})

    new_pos = list(new_object.to_dict().keys())
    for pos1, pos2 in zip(old_pos, new_pos):
        assert pos1[0] - pos2[0] == -1
        assert pos1[1] - pos2[1] == 0


def test_move_right_onto_block(new_object):
    new_object.move_down({})
    old_pos = list(new_object.to_dict().keys())
    fake_blocks = {(8, 2): None}

    new_object.move_right(fake_blocks)

    new_pos = list(new_object.to_dict().keys())
    for pos1, pos2 in zip(old_pos, new_pos):
        assert pos1[0] - pos2[0] == 0
        assert pos1[1] - pos2[1] == 0

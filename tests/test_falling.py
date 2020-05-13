import pytest

from figgy.game_logic import FallingObject, FallFailure, Engine


@pytest.fixture
def new_object(pygame_setup):
    def wrapper(template=None):
        # Create a square-shaped object
        if template:
            templates = [template]
        else:
            templates = [
                [{"x": 0, "y": 1}, {"x": 1, "y": 1}, {"x": 0, "y": 0}, {"x": 1, "y": 0}]
            ]
        images = ["pastel1_0.png"]
        return FallingObject(templates, images)

    return wrapper


def test_move_down(new_object):
    object_ = new_object()
    old_pos = list(object_.to_dict().keys())

    object_.move_down({})

    new_pos = list(object_.to_dict().keys())
    for pos1, pos2 in zip(old_pos, new_pos):
        assert pos1[0] - pos2[0] == 0
        assert pos1[1] - pos2[1] == -1


def test_move_down_onto_block(new_object):
    object_ = new_object()
    fake_blocks = {(7, 3): None, (6, 3): None}

    with pytest.raises(FallFailure):
        object_.move_down(fake_blocks)


def test_move_to_bottom(new_object):
    object_ = new_object()
    for _ in range(Engine.scene_height - 3):
        object_.move_down({})

    with pytest.raises(FallFailure):
        object_.move_down({})


def test_move_left(new_object):
    object_ = new_object()
    object_.move_down({})
    old_pos = list(object_.to_dict().keys())

    object_.move_left({})

    new_pos = list(object_.to_dict().keys())
    for pos1, pos2 in zip(old_pos, new_pos):
        assert pos1[0] - pos2[0] == 1
        assert pos1[1] - pos2[1] == 0


def test_move_left_onto_block(new_object):
    object_ = new_object()
    object_.move_down({})
    old_pos = list(object_.to_dict().keys())
    fake_blocks = {(5, 2): None}

    object_.move_left(fake_blocks)

    new_pos = list(object_.to_dict().keys())
    for pos1, pos2 in zip(old_pos, new_pos):
        assert pos1[0] - pos2[0] == 0
        assert pos1[1] - pos2[1] == 0


def test_move_right(new_object):
    object_ = new_object()
    object_.move_down({})
    old_pos = list(object_.to_dict().keys())

    object_.move_right({})

    new_pos = list(object_.to_dict().keys())
    for pos1, pos2 in zip(old_pos, new_pos):
        assert pos1[0] - pos2[0] == -1
        assert pos1[1] - pos2[1] == 0


def test_move_right_onto_block(new_object):
    object_ = new_object()
    object_.move_down({})
    old_pos = list(object_.to_dict().keys())
    fake_blocks = {(8, 2): None}

    object_.move_right(fake_blocks)

    new_pos = list(object_.to_dict().keys())
    for pos1, pos2 in zip(old_pos, new_pos):
        assert pos1[0] - pos2[0] == 0
        assert pos1[1] - pos2[1] == 0


def test_rotate(new_object):
    object_ = new_object(
        [{"x": 0, "y": 2}, {"x": 0, "y": 1}, {"x": 0, "y": 0}, {"x": 0, "y": -1}]
    )  # Create an I shape
    old_pos = list(object_.to_dict().keys())

    object_.rotate({})

    new_pos = list(object_.to_dict().keys())
    for idx, (pos1, pos2) in enumerate(zip(old_pos, new_pos)):
        if idx != 2:
            assert pos1[0] != pos2[0]
            assert pos1[1] != pos2[1]
        else:
            assert pos1[0] == pos2[0]
            assert pos1[1] == pos2[1]


def test_rotate_blocked_by_boundary(new_object):
    object_ = new_object(
        [{"x": 0, "y": 2}, {"x": 0, "y": 1}, {"x": 0, "y": 0}, {"x": 0, "y": -1}]
    )  # Create an I shape
    object_.move_down({})
    object_.move_down({})
    for _ in range(6):
        object_.move_left({})
    old_pos = list(object_.to_dict().keys())

    object_.rotate({})

    new_pos = list(object_.to_dict().keys())
    for pos1, pos2 in zip(old_pos, new_pos):
        assert pos1[0] == pos2[0]
        assert pos1[1] == pos2[1]


def test_rotate_blocked_by_block(new_object):
    object_ = new_object(
        [{"x": 0, "y": 2}, {"x": 0, "y": 1}, {"x": 0, "y": 0}, {"x": 0, "y": -1}]
    )  # Create an I shape
    old_pos = list(object_.to_dict().keys())
    fake_blocks = {(7, 3): None, (7, 2): None, (7, 1): None, (7, 0): None}

    object_.rotate(fake_blocks)

    new_pos = list(object_.to_dict().keys())
    for pos1, pos2 in zip(old_pos, new_pos):
        assert pos1[0] == pos2[0]
        assert pos1[1] == pos2[1]

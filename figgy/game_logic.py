import glob
import json
import math
import os
import random

from pgzero.actor import Actor


class Block(Actor):
    """
    Class that represent a single block, a piece of a falling object or a fixed block

    The block will be placed at the top of the scene

    Parameters
    ----------
    image: str
        the name of an image resource that will be loaded
    origin: dict int
        the origin of this block on which it will be rotated
    """

    block_size = 32

    def __init__(self, image, origin):
        pos = (origin["x"] + 6, origin["y"] + 1)
        real_pos = pos[0] * self.block_size, pos[1] * self.block_size
        super().__init__(image, real_pos, (0, 0))
        self.grid_pos = pos
        self.origin = (origin["x"], origin["y"])

    def move(self, dx, dy):
        """
        Move the block on the scene. Repositions the image.

        Parameters
        ----------
        dx: int
            the delta in x
        dy: int
            the delta in y
        """
        self.grid_pos = (self.grid_pos[0] + dx, self.grid_pos[1] + dy)
        self.pos = self.grid_pos[0] * self.block_size, self.grid_pos[1] * self.block_size

    def rotate(self):
        """
        Rotates the block about a origin
        """
        angle = 0.5 * math.pi
        tempx = round(
            self.origin[0] * math.cos(angle) - self.origin[1] * math.sin(angle)
        )
        tempy = round(
            self.origin[0] * math.sin(angle) + self.origin[1] * math.cos(angle)
        )
        self.grid_pos = (
            tempx + (self.grid_pos[0] - self.origin[0]),
            tempy + (self.grid_pos[1] - self.origin[1]),
        )
        self.origin = (tempx, tempy)
        self.pos = self.grid_pos[0] * self.block_size, self.grid_pos[1] * self.block_size


class FallFailure(Exception):
    """ A class to signal a failure to move a falling object downwards"""

    pass


class FallingObject:
    """
    A collection of blocks that are falling

    Parameters
    ----------
    object_templates: list
        a list of object templates to choose the shape of the object from
    images: list
        a list of images to choose the image for all blocks from
    """

    def __init__(self, object_templates, images):
        filename = random.choice(images)
        name = os.path.splitext(filename)[0]

        object_ = random.choice(object_templates)
        self._kind = object_templates.index(object_)
        self._blocks = [Block(name, origo) for origo in object_]
        self._hidden = False
        self._fallen = False

    @property
    def fallen(self):
        return self._fallen

    def draw(self):
        """ Draw all blocks on the scene
        """
        if self._hidden:
            return

        for block in self._blocks:
            block.draw()

    def move_down(self, fixed_blocks):
        """
        Move the object downwards if it is possible

        Parameters
        ----------
        fixed_blocks: dict
            a dictionary of fixed blocks

        Raises
        ------
        FallFailure
            if it is not possible to move downwards
        """
        if self._can_fall(fixed_blocks):
            for block in self._blocks:
                block.move(0, 1)
            self._fallen = True
        else:
            raise FallFailure

    def move_left(self, fixed_blocks):
        """
        Move the object to the left if it is possible

        Parameters
        ----------
        fixed_blocks: dict
            a dictionary of fixed blocks
        """
        if self._top_most() > 1 and self._can_move_left(fixed_blocks):
            for block in self._blocks:
                block.move(-1, 0)

    def move_right(self, fixed_blocks):
        """
        Move the object to the right if it is possible

        Parameters
        ----------
        fixed_blocks: dict
            a dictionary of fixed blocks
        """
        if self._top_most() > 1 and self._can_move_right(fixed_blocks):
            for block in self._blocks:
                block.move(+1, 0)

    def rotate(self, fixed_blocks):
        """
        Rotate the object if it is possible

        Parameters
        ----------
        fixed_blocks: dict
            a dictionary of fixed blocks
        """
        if self._kind == 0:  # Don't rotate the square box
            return
        if self._can_rotate(fixed_blocks):
            for block in self._blocks:
                block.rotate()

    def to_dict(self):
        """
        Creates a dictionary of this object with the positions as keys and the Block objects as values

        Returns
        -------
        dict:
            the dictionary representation of this object
        """
        return {(block.grid_pos[0], block.grid_pos[1]): block for block in self._blocks}

    def _bottom_most(self):
        return max([block.grid_pos[1] for block in self._blocks])

    def _can_fall(self, fixed_blocks):
        for block in self._blocks:
            query_pos = (block.grid_pos[0], block.grid_pos[1] + 1)
            if block.grid_pos[1] == Engine.scene_height - 1 or query_pos in fixed_blocks:
                return False
        return True

    def _can_move_left(self, fixed_blocks):
        for block in self._blocks:
            query_pos = (block.grid_pos[0] - 1, block.grid_pos[1])
            if block.grid_pos[0] == 0 or query_pos in fixed_blocks:
                return False
        return True

    def _can_move_right(self, fixed_blocks):
        for block in self._blocks:
            query_pos = (block.grid_pos[0] + 1, block.grid_pos[1])
            if block.grid_pos[0] == Engine.scene_width - 1 or query_pos in fixed_blocks:
                return False
        return True

    def _can_rotate(self, fixed_blocks):
        self._hidden = True
        for block in self._blocks:
            block.rotate()
        invalid = self._is_outside()
        for block in self._blocks:
            if block.grid_pos in fixed_blocks:
                invalid = True
                break
        for _ in range(3):
            for block in self._blocks:
                block.rotate()
        self._hidden = False
        return not invalid

    def _is_outside(self):
        return (
            self._left_most() < 0
            or self._right_most() >= Engine.scene_width
            or self._top_most() < 0
            or self._bottom_most() >= Engine.scene_height
        )

    def _left_most(self):
        return min([block.grid_pos[0] for block in self._blocks])

    def _right_most(self):
        return max([block.grid_pos[0] for block in self._blocks])

    def _top_most(self):
        return min([block.grid_pos[1] for block in self._blocks])


class Engine:
    """
    Represents the game engine, the public API

    Parameters
    ----------
    clock: pgzero.clock.Clock
        the master clock
    """

    scene_height = 25
    scene_width = 12
    default_tick_interval = 1.25

    def __init__(self, clock):
        self._current = None
        self._blocks = {}
        self.is_running = False
        self._is_dropping = False
        self._clock = clock
        self._tick_interval = self.default_tick_interval
        self._completed_lines = 0

        figgy_path = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(figgy_path, "templates.json")
        with open(filename, "r") as fileobj:
            self._object_templates = json.load(fileobj)

        self._images = glob.glob(os.path.join(figgy_path, "images", "*.png"))

    def draw(self):
        """ Draw all blocks and falling objects on the scene
        """
        if not self.is_running:
            return

        for _, block in self._blocks.items():
            block.draw()
        self._current.draw()

    def drop(self):
        """ Drop the currently falling object
        """
        if not self.is_running:
            return
        self._is_dropping = True
        self._clock.unschedule(self._tick)
        self._clock.schedule_interval(self._tick, 0.01)

    def move_left(self):
        """ Move the currently falling object to the left
        """
        if not self.is_running or self._is_dropping:
            return
        self._current.move_left(self._blocks)

    def move_right(self):
        """ Move the currently falling object to the right
        """
        if not self.is_running or self._is_dropping:
            return
        self._current.move_right(self._blocks)

    def rotate(self):
        """ Rotate the currently falling object
        """
        if not self.is_running or self._is_dropping:
            return
        self._current.rotate(self._blocks)

    def start_game(self):
        """ Starts a new game
        """
        self._blocks = {}
        self.is_running = True
        self._tick_interval = self.default_tick_interval
        self._completed_lines = 0
        self._new_falling_object()

    def _check_lines(self):
        for line in range(self.scene_height):
            if all((col, line) in self._blocks for col in range(self.scene_width)):
                self._remove_line(line)
                self._completed_lines += 1
                if self._completed_lines % 4 == 0:
                    self._tick_interval = max(0.02, self._tick_interval-0.1)

    def _handle_fall_failure(self):
        self._is_dropping = False
        self._clock.unschedule(self._tick)
        if not self._current.fallen:  # Stop game
            self.is_running = False
        else:
            self._blocks.update(self._current.to_dict())
            self._check_lines()
            self._new_falling_object()

    def _new_falling_object(self):
        self._current = FallingObject(
            object_templates=self._object_templates, images=self._images
        )
        self._clock.schedule_interval(self._tick, self._tick_interval)

    def _remove_line(self, line_to_remove):
        for col in range(self.scene_width):
            del self._blocks[(col, line_to_remove)]

        # Move every block above the removed line, one step down
        for line in range(line_to_remove - 1, -1, -1):
            for col in range(self.scene_width):
                if (col, line) not in self._blocks:
                    continue
                block = self._blocks[(col, line)]
                block.move(0, +1)
                self._blocks[(col, line + 1)] = block
                del self._blocks[(col, line)]

    def _tick(self):
        try:
            self._current.move_down(self._blocks)
        except FallFailure:
            self._handle_fall_failure()

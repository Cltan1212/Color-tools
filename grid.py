from __future__ import annotations
from layer_store import *
from data_structures.referential_array import *
from layer_store import *


class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        # check condition
        if draw_style not in Grid.DRAW_STYLE_OPTIONS:
            raise Exception("Not in DRAW_STYLE_OPTIONS")

        # initialise the brush size to the default
        self.brush_size = Grid.DEFAULT_BRUSH_SIZE

        # dimension
        self.x = x
        self.y = y

        # set up grid with 2D array
        self.grid = ArrayR(x)
        for i in range(x):
            self.grid[i] = ArrayR(y)

        # create one instance of the LayerStore for each grid square
        for i in range(x):
            for j in range(y):
                if draw_style == Grid.DRAW_STYLE_SET:
                    self.grid[i][j] = SetLayerStore()

                elif draw_style == Grid.DRAW_STYLE_ADD:
                    self.grid[i][j] = AdditiveLayerStore()

                else:
                    self.grid[i][j] = SequenceLayerStore()

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        if self.brush_size < Grid.MAX_BRUSH:
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.brush_size > Grid.MIN_BRUSH:
            self.brush_size -= 1

    def special(self):
        """
        Activate the special effect on all grid squares.
        """
        for row in self.grid:
            for layer_store in row:
                layer_store.special()

    def __getitem__(self, x):
        """
        Return each layerStore inside grid squares.
        """
        return self.grid[x]

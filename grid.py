from __future__ import annotations

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
        - draw_style (String):
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y (int) : The dimensions of the grid.

        Should also initialise the brush size to the DEFAULT provided as a class variable.

        Raise:
        - Exception: if the draw style is not in draw_style_options

        Time Complexity:
        - Worst Case: O(x * y * capacity): if the draw_style is additive layer (based on the __init__ complexity)
        - Best Case: O(x * y): if the draw_style is set layer (the time complexity of __init__ in set layer is O(1)

        Explanation of time complexity:
        line 48: O(len(draw_style_option)) -> O(constant) -> O(1)
        line 52 - 56: O(1) for all operation (assignment and raise Exception)
        line 59: O(x) create an array with size x
        line 60: O(x) -> loop through the array of size x
        line 61: O(y) -> create an array with size y
        line 64-73 : O(x * y) -> loop through each layerStore inside the grid (other are assignment that is constant)
        """
        # raise Exception to ensure the draw style inside the enumerations
        if draw_style not in Grid.DRAW_STYLE_OPTIONS:
            raise Exception("Not in DRAW_STYLE_OPTIONS")

        # initialise the brush size to the default
        self.brush_size = Grid.DEFAULT_BRUSH_SIZE

        # dimension of the grid
        self.x = x
        self.y = y

        # set up grid with 2D array
        self.grid = ArrayR(x)
        for i in range(x):
            self.grid[i] = ArrayR(y)

        # create one instance of the LayerStore for each grid square
        for i in range(x):
            for j in range(y):
                if draw_style == Grid.DRAW_STYLE_SET:  # create layer store based on draw style
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

        Time Complexity:
        - Worst Case: O(1) since all the operation are constant (comparison, assignment and operation)
        - Best Case: same as Worst Case

        Explanation of time complexity:
        line 89: O(1) - comparison is constant
        line 90: O(1) - operation is constant
        """
        if self.brush_size < Grid.MAX_BRUSH:
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.

        Time Complexity:
        - Worst case: O(1) since all the operation are constant (comparison, assignment and operation)
        - Best case: same as Worst Case

        Explanation of time complexity:
        line 106: O(1) - comparison is constant
        line 107: O(1) -operation is constant
        """
        if self.brush_size > Grid.MIN_BRUSH:
            self.brush_size -= 1

    def special(self):
        """
        Activate the special effect on all grid squares.

        Time Complexity:
        - Worst Case: O(x * y * special): where x and y is the dimensions of the grid and special is the complexity of each layerStore
        - Best Case: O(x * y * special): same as worst case

        Explanation of time complexity:
        line 123: O(len(self.grid)) - where len(self.grid) is the dimension x of the grid
        line 124: O(row) - where row is the size of dimension y
        line 125: O(special) where special is the function of the special that depends on the layer_store
        line 123 - 125: O(x * y * special)
        """
        for row in self.grid:
            for layer_store in row:
                layer_store.special()

    def __getitem__(self, x):
        """
        Return each layerStore inside grid squares.

        Time Complexity:
        - O(1): get item in a particular place in array

        Explanation:
        line 137: O(1) access array is constant
        """
        return self.grid[x]

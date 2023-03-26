from __future__ import annotations
from action import PaintAction
from grid import Grid

from data_structures.stack_adt import *


class UndoTracker:
    """
    Attributes:
        capacity (int): the number of actions
        actions (ArrayStack): a stack that store all the actions
        undone_actions (ArrayStack): a stack that all the undone actions

    Methods:
        add_action: add PaintAction into the actionStore
        undo: undo an operation, and apply the relevant action to the grid.
        redo: Redo an operation that was previously undone.
    """

    def __init__(self):
        """
        Time complexity:
            O(1): constant.
        """
        self.capacity = 10000  # the maximum number of actions does not exceed 10000
        self.actions = ArrayStack(self.capacity)
        self.undone_actions = ArrayStack(self.capacity)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.

        Parameter:
            action (PaintAction): The PaintAction that should be added into the actionStore

        Time Complexity:
            O(1): the method is_full and push are all constant
        """

        # push the action if the collection is not full
        if not self.actions.is_full():
            self.actions.push(action)

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        Parameter:
            grid (Grid): the grid to be applied the undo action

        Return:
            The action that was undone, or None.

        Time Complexity:
            Best Case: O(1) when there is no action in the collection
        """
        if self.actions.is_empty():
            return None

        else:
            current_action = self.actions.pop()
            current_action.undo_apply(grid)
            self.undone_actions.push(current_action)  # add to undone actions for redo
            return current_action

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        Parameter:
            grid (Grid): the grid to be applied the redo action

        Return:
            The action that was redone, or None.

        Time Complexity:
            Best Case: O(1) if there is no action inside undoneActions
            Worse Case: O()
        """
        if self.undone_actions.is_empty():
            return None

        else:
            current_action = self.undone_actions.pop()
            current_action.redo_apply(grid)
            self.actions.push(current_action)  # add to actions for undo
            return current_action

    def reset_redo(self):
        """
        Reset the undone_actions.

        Time Complexity:
            O(1): constant
        """
        self.undone_actions = ArrayStack(self.capacity)
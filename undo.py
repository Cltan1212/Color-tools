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
            O(capacity): where capacity is the size to create array stack

        Explanation of time complexity:
            line 30, 31: the time complexity of creating an arrayStack depends on the capacity
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

        Explanation of time complexity:
            line 52: the time complexity of is_full and comparison are constant
            line 53: the time complexity of pushing an item into the stack is constant
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
            Worst Case: O(undo_apply) where undo depended on the time complexity of method undo apply
            (which is the size of paint step inside paint action)
            Best Case: O(1) if the actions is empty

        Explanation of time complexity:
            line 77: the time complexity of comparison is constant
            line 77, 82, 86: the time complexity of is_empty, pop and push in stack ADT are all constant
            line 83: the time complexity of undo_apply depends on the function undo_apply
            line 78, 87: the time complexity of return statements are constant
        """
        if self.actions.is_empty():
            return None

        else:
            # get the action from the stack and undo the action
            current_action = self.actions.pop()
            current_action.undo_apply(grid)

            # add to undone actions for redo
            self.undone_actions.push(current_action)
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
            Worst Case: O(redo) where redo depended on the time complexity of method redo apply
            (which is the size of paint step inside paint action)
            Best Case: O(1) if the size of undone action is empty

        Explanation of time complexity:
            line 111: the time complexity of comparison is constant
            line 111, 116, 120: the time complexity of is_empty, pop and push in stack ADT are all constant
            line 117: the time complexity of undo_apply depends on the function redo_apply
            line 112, 121: the time complexity of return statements are constant
        """
        if self.undone_actions.is_empty():
            return None

        else:
            # get the action from the stack and redo the action
            current_action = self.undone_actions.pop()
            current_action.redo_apply(grid)

            # add to actions for undo
            self.actions.push(current_action)
            return current_action

    def reset_redo(self):
        """
        Reset the undone_actions.

        Time Complexity:
            O(1): constant since clear method is constant

        Explanation of time complexity:
            line 133: the time complexity of clear a stack is constant
        """
        self.undone_actions.clear()
from __future__ import annotations
from action import PaintAction
from grid import Grid

from data_structures.stack_adt import *


class UndoTracker:

    def __init__(self):
        self.capacity = 10000
        self.actions = ArrayStack(self.capacity)
        self.undone_actions = ArrayStack(self.capacity)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        if not self.actions.is_full():
            self.actions.push(action)

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        if self.actions.is_empty():
            return None

        else:
            current_action = self.actions.pop()
            current_action.undo_apply(grid)
            self.undone_actions.push(current_action)
            return current_action

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if self.undone_actions.is_empty():
            return None

        else:
            current_action = self.undone_actions.pop()
            current_action.redo_apply(grid)
            self.actions.push(current_action)
            return current_action

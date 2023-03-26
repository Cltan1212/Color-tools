from __future__ import annotations
from action import PaintAction
from grid import Grid

from data_structures.queue_adt import *


class ReplayTracker:
    """
    Attributes:
        capacity (int): the number of actions
        actions (CircularQueue): the queue that stored all the actions
        start (bool): Keep track when called replay.

    Methods:
        start_replay: Called whenever we should stop taking actions, and start playing them back.
        add_action: Adds an action to the replay.
        play_next_action: Plays the next replay action on the grid.
    """

    def __init__(self):
        """
        Time Complexity：
            O(1): Constant for all operation
        """
        self.capacity = 10000
        self.actions = CircularQueue(self.capacity)
        self.start = False

    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.

        Time Complexity:
            O(1): constant
        """
        self.start = True

    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.

        Parameters:
            action (PaintAction): The paintAction to be added.
            is_undo (bool): specifies whether the action was an undo action or not.
                            Special, Redo, and Draw all have this is False.

        Time Complexity:
            O(1): constant
        """
        self.actions.append((action, is_undo))

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.

        Parameter:
            grid (Grid): the grid to be applied the current action

        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.

        Time Complexity:
            Best Case: O(1) if nothing to be replayed
            Worse Case:
        """
        # when not calling the replay
        if not self.start:
            return True

        # when all the action is finished
        elif self.actions.is_empty():
            self.start = False
            return True

        else:
            action, is_undo = self.actions.serve()

            # undo if the action is undo
            if is_undo:
                action.undo_apply(grid)

            # redo
            else:
                action.redo_apply(grid)

            return False


if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)


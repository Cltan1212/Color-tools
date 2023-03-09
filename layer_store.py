from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from layers import *

class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        super().__init__()
        self.layer = None
        self.previous_layer = None

    def add(self, layer: Layer) -> bool:
        if self.layer != layer:
            self.layer = layer
            return True
        return False
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.layer is None:
            return start

        # always applies an inversion of the colours after the layer has been applied
        elif self.previous_layer is not None:
            start = self.previous_layer.apply(start, timestamp, x, y)

        return self.layer.apply(start, timestamp, x, y)

    def erase(self, layer: Layer) -> bool:
        if self.layer != layer:
            self.layer = None
            return True
        return False

    def special(self):
        # if layer is invert, means apply two invert will result the same effect
        # -> only apply the previous layer
        if self.layer is invert:
            self.layer = self.previous_layer
            self.previous_layer = None
            return

        # always applies an inversion of the colours after the layer has been applied
        elif self.previous_layer is None:
            self.previous_layer = self.layer
            self.layer = invert

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    pass

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    pass

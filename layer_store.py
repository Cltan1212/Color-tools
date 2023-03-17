from __future__ import annotations
from abc import ABC, abstractmethod
import math

import layer_util
from layer_util import Layer
from layers import *
from data_structures.stack_adt import *
from data_structures.queue_adt import *
from data_structures.array_sorted_list import *

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
        self.special_effect = False

    def add(self, layer: Layer) -> bool:
        if self.layer != layer:
            self.layer = layer
            return True
        return False
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.layer is None:
            color = start
        else:
            color = self.layer.apply(start, timestamp, x, y)

        if self.special_effect:
            color = invert.apply(color, timestamp, x, y)
        return color

    def erase(self, layer: Layer) -> bool:
        if self.layer is None:
            return False
        self.layer = None
        return True

    def special(self):
        if self.special_effect is True:
            self.special_effect = False
        else:
            self.special_effect = True


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:
        super().__init__()
        self.capacity = 100
        self.layers = CircularQueue(self.capacity)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        if self.layers.is_full():
            return False

        self.layers.append(layer)
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        color = start

        if not self.layers.is_empty():
            iteration = len(self.layers)

            for i in range(iteration):
                item = self.layers.serve()
                color = item.apply(color, timestamp, x, y)
                self.layers.append(item)

        return color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        if self.layers.serve() != layer:
            return True
        return False

    def special(self):
        """
        Special mode. Different for each store implementation.
        """

        # each time called the special method should reverse the queue
        self.reverse_queue()

    def reverse_queue(self):

        capacity = len(self.layers)
        stack = ArrayStack(capacity)

        while not self.layers.is_empty():
            stack.push(self.layers.serve())

        while not stack.is_empty():
            self.layers.append(stack.pop())


class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:
        super().__init__()

        self.layers = layer_util.get_layers()
        self.special_effect = False

        # create a Array for the applying status
        self.status = ArraySortedList(len(layer_util.LAYERS))
        for i, layer in enumerate(layer_util.LAYERS):
            self.status[i] = ListItem[i, "not applying"]

        # Lexicographic order for special method
        self.lexiLayers = ArraySortedList(len(layer_util.LAYERS))

    def add(self, layer: Layer) -> bool:

        self.status[layer.index] = ListItem[layer.index, "applying"]
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        color = start
        for i in range(len(self.layers)):
            if self.status[i] == ListItem[i, "applying"]:
                color = self.layers[i].apply(color, timestamp, x, y)
        return color

    def erase(self, layer: Layer) -> bool:
        self.status[layer.index] = ListItem[layer.index, "not applying"]
        return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        for index in range(len(layer_util.LAYERS)):
            if self.status[index] == ListItem[index, "applying"]:
                self.lexiLayers.add(ListItem(self.layers[index], self.layers[index].name[0]))

        if len(self.lexiLayers) % 2 == 0:
            median = len(self.lexiLayers)//2 - 1
        else:
            median = math.floor(len(self.lexiLayers)/2)
        self.erase(self.lexiLayers[median].value)
        self.lexiLayers.clear()


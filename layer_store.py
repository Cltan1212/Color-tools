from __future__ import annotations
from abc import ABC, abstractmethod

import layer_util
from layer_util import *
from layers import *
from data_structures.stack_adt import *
from data_structures.queue_adt import *
from data_structures.array_sorted_list import *
from data_structures.bset import *


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

    Attributes:
        layer (Layer): Layer that be stored for apply.
        special_effect (bool): Keep track when called special method.

    Methods:
        add: Set the single layer.
        erase: Remove the single layer. Ignore what is currently selected.
        special: Invert the colour output.
    """

    def __init__(self) -> None:
        """
        Initialise the attributes of SetLayerStore.

        Time Complexity:
            O(1): since there is nothing in parent class's constructor and assignments
        """

        super().__init__()
        self.layer = None
        self.special_effect = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.

        Parameter:
            layer (Layer): Layer that need to be stored.

        Return:
            boolean: Returns true if the layer was actually added.

        Time Complexity:
            O(1): comparison and assignment
        """

        if self.layer != layer:  # simply check if the layer is already stored
            self.layer = layer
            return True
        return False
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layer.

        Parameter:
            start (tuple): the initial color that provided to be applied.
            timestamp (int): used by some layers for dynamic effects.
            x,y (int): the position on the screen.

        Return:
            color (tuple): the colour this square should show.

        Time Complexity:
            Best Case: O(1) if there is no layer to be applied
            Worse Case: O(N) where N depends on the function of layer that should be applied.
        """

        color = start

        # only apply if there is a layer
        if self.layer is not None:
            color = self.layer.apply(start, timestamp, x, y)

        # always applies an inversion if activate special effect
        if self.special_effect:
            color = invert.apply(color, timestamp, x, y)

        return color

    def erase(self, layer: Layer) -> bool:
        """
        Erase the layer from the store.

        Parameter:
            layer (Layer): Layer that need to be removed.

        Return:
            boolean: Returns true if the layer was actually removed.

        Time Complexity:
            O(1): Constant since there is only comparison, assignment and return statement.
        """

        if self.layer is None:  # simply check if the layer is empty
            return False
        self.layer = None
        return True

    def special(self):
        """
        Special mode tracker. Change special effect status whenever call the special method.

        Time Complexity:
            O(1): Constant for all operations.
        """
        if self.special_effect:
            self.special_effect = False
        else:
            self.special_effect = True


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.

    Attributes:
        capacity (int): maximum number of layers to be stored
        layers (CircularQueue): storage for the layers to be applied

    Methods:
        add: Add a new layer to be added last.
        erase: Remove the first layer that was added. Ignore what is currently selected.
        special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:
        """
         Initialise the attributes of AdditiveLayerStore.

        Time Complexity:
        - O(N): while N is the capacity of the Circular Queue.
        """
        super().__init__()
        self.capacity = 100  # the capacity of the store at least 100 times the number of layers.
        self.layers = CircularQueue(self.capacity)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.

        Parameter:
            layer (Layer): Layer that need to be stored.

        Return:
            Boolean: Returns true if the LayerStore was actually changed.

        Time Complexity:
            O(1): since the time complexity of is_full, append is O(1),
            therefore the overall time complexity should be constant as well.
        """

        # only append if the layerStore is not full
        if self.layers.is_full():
            return False

        self.layers.append(layer)
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Parameter:
            start (tuple): the initial color that provided to be applied.
            timestamp (int): used by some layers for dynamic effects.
            x,y (int): the position on the screen.

        Return:
            color (tuple): the colour this square should show.

        Time Complexity:
            Best Case: O(1) if the layerStore is empty.
            Worse Case: O(N * comp+) where N is the number of layers in LayerStore and
            comp+ is depended on the function of the layer applied.
        """
        color = start

        # only apply the layer if there is a layer in layerStore
        if not self.layers.is_empty():
            iteration = len(self.layers)

            # apply each layer in the queue
            for i in range(iteration):
                item = self.layers.serve()
                color = item.apply(color, timestamp, x, y)
                self.layers.append(item)

        return color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer.

        Parameter:
            layer (Layer): Layer that need to be removed.

        Return:
            boolean: Returns true if the layer was actually removed.

        Time Complexity:
            O(1): Constant since the method is_empty and serve are both constant.
        """

        # only applied if there is a layer inside layerStore
        if not self.layers.is_empty() and self.layers.serve() != layer:
            return True
        return False

    def special(self):
        """
        Special mode. Reverse the order of current layers.

        Time Complexity:
            Best Case: O(1) when there is no layers inside layerStore.
            Worse Case: O(N) where N is the layers inside layerStore.
        """

        # each time called the special method should reverse the queue
        stack_capacity = len(self.layers)
        stack = ArrayStack(stack_capacity)  # temp stack for reversing

        # push all the layer to stack
        while not self.layers.is_empty():
            stack.push(self.layers.serve())

        # append to layerStore with the reverse order
        while not stack.is_empty():
            self.layers.append(stack.pop())


class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.

    Class Variable:
        CAPACITY (int): the number of total layers register

    Attributes:
        get_layers (ArrayR): Array that stored all the registered layers.
        seq_layers (BSet): Storage for the layers to be applied

    Methods:
        add: Ensure this layer type is applied.
        erase: Ensure this layer type is not applied.
        special:
            Of all currently applied layers, remove the one with median `name`.
            In the event of two layers being the median names, pick the lexicographically smaller one.
    """
    CAPACITY = layer_util.cur_layer_index

    def __init__(self) -> None:
        """
        Initialise the attributes of SequenceLayerStore.

        Time Complexity:
            - O(N) where N is the number of layers registered.
        """
        super().__init__()
        self.get_layers = layer_util.get_layers()
        self.seq_layers = BSet()

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.

        Parameter:
            layer (Layer): Layer that need to be stored.

        Return:
            Boolean: Returns true if the LayerStore was actually changed.

        Time Complexity:
            O(1): since all the operation are constant.
        """

        # simply add the layer into layerStore if it is not inside it
        if layer.index+1 not in self.seq_layers:  # use layer.index+1 because set is not accepted '0' as an integer
            self.seq_layers.add(layer.index + 1)
            return True
        return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Parameter:
            start (tuple): the initial color that provided to be applied.
            timestamp (int): used by some layers for dynamic effects.
            x,y (int): the position on the screen.

        Return:
            color (tuple): the colour this square should show.

        Time Complexity:
            Best Case: O(1) if the layerStore is empty.
            Worse Case: O(N) where N is depended on the layer to be applied.
        """
        color = start

        # apply the color if there is layer store in layerStore
        # use the range to compare to check integer is inside the set since the set is not iterable
        if not self.seq_layers.is_empty():
            for i in range(SequenceLayerStore.CAPACITY):
                if i+1 in self.seq_layers:  # set is not accept '0' as an integer
                    color = self.get_layers[i].apply(color, timestamp, x, y)

        return color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer.

        Parameter:
            layer (Layer): Layer that need to be removed.

        Return:
            boolean: Returns true if the layer was actually removed.

        Time Complexity:
            O(1): Constant since the method is_empty and serve are both constant.
        """

        # only remove if the layer is inside layerStore
        if layer.index+1 in self.seq_layers:
            self.seq_layers.remove(layer.index + 1)
            return True
        return False

    def special(self):
        """
        Special mode. Of all currently applied layers, remove the one with median `name`.

        Time Complexity:
            Best Case: O(1) when there is nothing inside layerStore
            Worse Case: O(X * log(Y)) where X is the size of the lexi_layers(since we have to resize the array)
            and Y is the total layers to be added into ArraySortedList
        """
        # an ArraySortedList that stored the applied layers in lexicographically ordered
        lexi_layers = ArraySortedList(SequenceLayerStore.CAPACITY)

        if not self.seq_layers.is_empty():

            # add the layer as ListItem into lexi_layers(ArraySortedList)
            # ListItem: value: Layer (Layer) , key: Layer's name (String)
            for i in range(SequenceLayerStore.CAPACITY):
                if i+1 in self.seq_layers:
                    lexi_layers.add(ListItem(self.get_layers[i], self.get_layers[i].name))

            # find the median to erase the layer
            if len(lexi_layers) % 2 == 0:
                median = len(lexi_layers)//2 - 1
            else:
                median = len(lexi_layers)//2

            # erase the layer inside layerStore (therefore the layer will not be applied)
            self.erase(lexi_layers[median].value)



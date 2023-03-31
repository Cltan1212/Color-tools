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
    Set layer store. A single layer can be stored at a time (or nothing at all). Inherited from LayerStore Class.

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
            Worst Case: O(1) since there is nothing in parent class's constructor and assignments
            Best Case: O(1) same as Worst Case
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
            Worst Case: O(1) constant since there are comparison and assignment
            Best Case: O(1) same as worst case

        Explanation of time complexity:
            line 96: the time complexity of comparison is constant
            line 97: the time complexity of assignment is constant
            line 98,99: the time complexity of return is constant
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
            timestamp (int): parameter is used to calculate the hue component of the output color.
            x,y (int): the position on the screen.

        Return:
            color (tuple): the colour this square should show.

        Time Complexity:
            Worst Case: O(apply) where apply is the time complexity of the apply method (layer in layerStore and invert)
            Best Case: O(1) if there is no layer to be applied and no special effect

        Explanation of time complexity:
            line 124: the time complexity of assignment is constant
            line 127, 131: the time complexity of comparison is constant
            line 128, 132: the time complexity is apply where apply is the function inside the layers.py files
            line 34: the time complexity of return is constant
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
            Worse Case: O(1) Constant since there is only comparison, assignment and return statement.
            Best Case: same as Worst Case

        Explanation of time complexity:
            line 155, 159: the time complexity of comparison is constant
            line 156, 160: the time complexity of return is constant
        """
        # simply check if the layer is empty
        if self.layer is None:
            return False

        # clear the layer inside layerStore
        self.layer = None
        return True

    def special(self):
        """
        Special mode tracker. Change special effect status whenever call the special method.

        Time Complexity:
            Worst Case: O(1) Constant for all operations.
            Best Case: Same as Worst Case

        Explanation of time complexity:
            line 174: the time complexity of comparison is constant
            line 175, 177: the time complexity of assignment is constant
        """
        if self.special_effect:
            self.special_effect = False
        else:
            self.special_effect = True


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones. v

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
        - O(capacity): while capacity is the capacity of the Circular Queue.

        Explanation of time complexity:
            line 208: the time complexity of get_layers is O(get_layers)
            where get_layers is the time complexity of get_layers method
            line 209: the time complexity of layers is depends on the capacity (since the time complexity of creating
            a circular queue depends on the size of capacity)
        """
        super().__init__()
        self.capacity = len(get_layers()) * 100  # the capacity of the store at least 100 times the number of layers.
        self.layers = CircularQueue(self.capacity)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.

        Parameter:
            layer (Layer): Layer that need to be stored.

        Return:
            Boolean: Returns true if the LayerStore was actually changed.

        Time Complexity:
            Worst Case: O(1) since the time complexity of is_full, append is O(1),
            Best Case: same as worst case

        Explanation of time complexity:
            line 232: the time complexity of is_full is constant
            line 236: the time complexity of append (circular queue) is constant
            line 233, 237: the time complexity of return a statement is constant
        """

        # only append if the layerStore is not full
        if self.layers.is_full():
            return False

        # add layer to the layerStore
        self.layers.append(layer)
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Parameter:
            start (tuple): the initial color that provided to be applied.
            timestamp (int): parameter is used to calculate the hue component of the output color.
            x,y (int): the position on the screen.

        Return:
            color (tuple): the colour this square should show.

        Time Complexity:
            Worse Case: O(N * apply) where N is the number of layers in LayerStore and apply is the time complexity of
            apply method (serve and append are all O(1))
            Best Case: O(1) if the layers is empty

        Explanation of time complexity:
            line 263: the time complexity of assignment is constant
            line 266, 271, 273: the time complexity of is_empty, serve and append in circular queue is constant
            line 272: the time complexity of apply is depended on the function apply()
            line 275: the time complexity of return statements is constant
            line 270 - 273: the time complexity of looping through the layer in each layer in layerStore is N times
        """
        color = start

        # only apply the layer if there is a layer in layerStore
        if not self.layers.is_empty():
            iteration = len(self.layers)

            # apply each layer in the queue
            for i in range(iteration):
                item = self.layers.serve()  # layer that need to be applied
                color = item.apply(color, timestamp, x, y)
                self.layers.append(item)  # append again since will need to apply for the next time

        return color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer.

        Parameter:
            layer (Layer): Layer that need to be removed.

        Return:
            boolean: Returns true if the layer was actually removed.

        Time Complexity:
            Worst Case: O(1) Constant since the method is_empty and serve are both constant.
            Best Case: same as worst case

        Explanation of time complexity:
            line 297: the time complexity of is_empty and serve and comparison is all constant
            line 298, 299: the time complexity of return statements is constant
        """

        # only applied if there is a layer inside layerStore
        if not self.layers.is_empty() and self.layers.serve() != layer:
            return True
        return False

    def special(self):
        """
        Special mode. Reverse the order of current layers.

        Time Complexity:
            Worst Case: O(N) where N is the layers inside layerStore.
            Best Case: same as worst case

        Explanation of time complexity:
            line 317: create an array stack depends on the size of layerStore -> O(len(self.layers))
            line 320,321, 324,325: while loop depends on the time complexity of the size of layerStore
            line 320 -325: the time complexity of is_empty, push, pop and append is constant
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

    Attributes:
        capacity (int): counter for iteration to check whether the layer.index inside the layerStore
        get_layers (ArrayR): Array that stored all the registered layers.
        seq_layers (BSet): Storage for the layers to be applied

    Methods:
        add: Ensure this layer type is applied.
        erase: Ensure this layer type is not applied.
        special:
            Of all currently applied layers, remove the one with median `name`.
            In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:
        """
        Initialise the attributes of SequenceLayerStore. Inherited from LayerStore Class.

        Time Complexity:
            Worst Case: O(get_layers) where get_layers is the time complexity of the method
            Best Case: same as worst case

        Explanation of time complexity:
            line 360: the time complexity of get_layers
            line 364 - 368: the time complexity if the length of get_layers (we need to loop through all layer inside)
            line 363, 366, 367: the time complexity of assignment, comparison and arithmetic operation are constant
            line 370: create a set is constant (here it creates an array size of 1 -> min_capacity)
        """
        super().__init__()
        self.get_layers = get_layers()

        # calculate the number of available layers inside get_layers
        self.capacity = 0
        for layer in self.get_layers:
            if layer is not None:
                self.capacity += 1
            else:
                break

        self.seq_layers = BSet()

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.

        Parameter:
            layer (Layer): Layer that need to be stored.

        Return:
            Boolean: Returns true if the LayerStore was actually changed.

        Time Complexity:
            Worst Case: O(1) since all the operation are constant (including contains and add method in set).
            Best Case: same as worst case

        Explanation of time complexity:
            line 393: time complexity of contains in set is constant
            line 394: time complexity of add in set is constant
            line 395, 396: time complexity of return statements is constant
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
            timestamp (int): parameter is used to calculate the hue component of the output color.
            x,y (int): the position on the screen.

        Return:
            color (tuple): the colour this square should show.

        Time Complexity:
            Worst Case: O(capacity * apply) since always iterate the same time (capacity is a constant)
            Best Case: O(1) if the seq_layer is empty

        Explanation of time complexity:
            line 421: the time complexity of assignment is constant
            line 425: the time complexity of is_empty is constant
            line 426: the time complexity of for loop depends on the size of capacity
            line 427: the time complexity of contains in set is constant
            line 428: the time complexity depends on the method apply(), accessing the set is constant
        """
        color = start

        # apply the color if there is layer store in layerStore
        # use the range to compare to check integer is inside the set since the set is not iterable
        if not self.seq_layers.is_empty():
            for i in range(self.capacity):
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
            Worst Case: O(1) Constant since the method contains and remove in set are both constant.
            Best Case: O(1) same as worst case

        Explanation of time complexity:
            line 452, 453: the time complexity of contains and remove in set is constant
            line 454, 455: the time complexity of return statements is constant
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
            Worst Case: O(capacity * add) where capacity is the CAPACITY of sequence layer store, add is the method
            of adding elements into array sorted list (basically the time complexity is O(log(n)) -> binary search)
            Best Case: O(1) if the seq_layer is empty

        Explanation of time complexity:
            line 474: the time complexity of create an arraySortedList depends on the size of capacity
            line 480: the time complexity for loop depends on the number of looping, which is O(capacity)
            line 482: the time complexity of adding a ListItem into the list is basically O(log(n)) -> use binary search
            line 484 - 488: the time complexity of comparison, arithmetic operation are all constant
            line 491: the time complexity of erase is constant
        """
        # an ArraySortedList that stored the applied layers in lexicographically ordered
        lexi_layers = ArraySortedList(self.capacity)

        if not self.seq_layers.is_empty():

            # add the layer as ListItem into lexi_layers(ArraySortedList)
            # ListItem: value: Layer (Layer) , key: Layer's name (String)
            for i in range(self.capacity):
                if i+1 in self.seq_layers:
                    lexi_layers.add(ListItem(self.get_layers[i], self.get_layers[i].name))

            # find the median to erase the layer
            if len(lexi_layers) % 2 == 0:  # even number
                median = len(lexi_layers)//2 - 1
            else:  # odd number
                median = len(lexi_layers)//2

            # erase the layer inside layerStore (therefore the layer will not be applied)
            self.erase(lexi_layers[median].value)



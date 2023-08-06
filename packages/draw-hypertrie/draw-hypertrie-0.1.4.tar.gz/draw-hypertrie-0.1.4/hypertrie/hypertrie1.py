from hypertrie.hypertrie_commons import *

from collections import defaultdict
from typing import List, Tuple, DefaultDict, Dict, Union, Optional, Set

from hypertrie.hypertrie_commons import next_slice_key

ht1_children_t = Union[Tuple[Dict[HTKeyPart, SliceKey], ...],  # uncompressed node depth > 1
                       Tuple[Set[HTKeyPart]]]  # uncompressed node depth == 1


class Hypertrie1Node:
    def __init__(self, children: ht1_children_t, size=1, count: int = 1):
        self.children: ht1_children_t = children
        self.size = size
        self.count = count

    @property
    def n_dim(self):
        return len(self.children)

    def inc(self):
        self.count += 1


class Hypertrie1Context:
    def __init__(self, max_depth: int = 3):
        self._max_depth: int = max_depth
        self._storage: Tuple[Dict[SliceKey, Hypertrie1Node], ...] = tuple(dict() for _ in range(max_depth))
        self._call_once = False

    @property
    def max_depth(self):
        return self._max_depth

    @property
    def storage(self):
        return self._storage

    def create_hypertrie(self, keys: List[HTKey], depth=3, slice_key: Optional[SliceKey] = None) -> SliceKey:
        if self._call_once:
            raise ValueError("v1 hypertrie context can only hold a single hypertrie.")

        # not supported in this simplified version
        assert len(keys) >= 1

        if slice_key is None:
            keys.sort()
            slice_key: SliceKey = (None,) * depth

        if slice_key in self._storage[depth - 1]:
            self._storage[depth - 1][slice_key].inc()
        else:
            if depth == 1:
                children: ht1_children_t = (set(key[0] for key in keys),)
            else:
                children: ht1_children_t = tuple(dict() for _ in range(depth))

                for pos in range(depth):
                    # sort with key_part at pos as major
                    keys.sort(key=lambda x: (x[pos],) + x[:pos] + x[pos + 1:])
                    slices: DefaultDict[HTKeyPart, List[HTKey]] = defaultdict(list)
                    for key in keys:
                        slices[key[pos]].append(key[:pos] + key[pos + 1:])

                    for slice_key_part, next_slice in slices.items():
                        next_slicekey = next_slice_key(slice_key, pos, slice_key_part)
                        self.create_hypertrie(next_slice, depth - 1, next_slicekey)
                        children[pos][slice_key_part] = next_slicekey
            self._storage[depth - 1][slice_key] = Hypertrie1Node(children, len(keys))
        return slice_key

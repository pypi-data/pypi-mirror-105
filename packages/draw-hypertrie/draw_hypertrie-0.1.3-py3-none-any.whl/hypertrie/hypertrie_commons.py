from typing import Tuple, Optional

HTKeyPart = int

HTKey = Tuple[HTKeyPart, ...]

SliceKey = Tuple[Optional[HTKeyPart], ...]


def slice_key2str(slice_key: SliceKey) -> str:
    return "⟨{}⟩".format(", ".join(str(entry) if entry is not None else ": " for entry in slice_key))


def next_slice_key(old_slice_key: SliceKey, pos: int, key_part: HTKeyPart) -> SliceKey:
    tmp_key = list(old_slice_key)
    no_slices = tmp_key.count(None)
    curr_pos = 0
    for i in range(len(tmp_key)):
        if tmp_key[i] is None:
            if pos == curr_pos:
                tmp_key[i] = key_part
                break
            else:
                curr_pos += 1
    return tuple(tmp_key)

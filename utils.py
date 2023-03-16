import hashlib
import collections

# hashlib.sha256("test".encode()).hexdigest()

def sorted_dict_by_key(unsorted_dict):
    return collections.OrderedDict(
        sorted(unsorted_dict.items(), key=lambda d:d[0])
    )
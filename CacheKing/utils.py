def make_hashable(arg):
    """
    Recursively convert argument to a hashable type.
    """
    if isinstance(arg, (tuple, list)):
        return tuple(make_hashable(e) for e in arg)
    elif isinstance(arg, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in arg.items()))
    elif isinstance(arg, set):
        return frozenset(arg)
    elif is_hashable(arg):
        return arg
    else:
        raise TypeError(f"Unhashable type: {type(arg)}")
    

def is_hashable(arg):
    """
    Check if argument is hashable.
    """
    try:
        hash(arg)
        return True
    except TypeError:
        return False
def public(view):
    """
    Decorator that flags a view as completely available to the public.
    It passes its decorated function unchanged.
    It's only used for semantic purposes, to make code reading easier.
    """
    return view

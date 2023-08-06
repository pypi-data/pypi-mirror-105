def value_type(d, k):
    return ((v := d[k]), type(v)) if k in d else (None, type(None))


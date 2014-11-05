def func_a():
    return '1'

def func_b():
    return '2'

class simple:
    def __init__(self, choice):
        if choice:
            self.func = func_a
        else:
            self.func = func_b
def greet(name):
    return 'Hello {}!'.format(name)

# test
def _test():
    assert(greet('Josip') == 'Hello Josip!')

if __name__ == 'main':
    _test()
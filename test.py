import traceback

try:
    print('running')
    raise KeyError
except KeyError:
    traceback.print_tb(e.__traceback__)
    print(e)


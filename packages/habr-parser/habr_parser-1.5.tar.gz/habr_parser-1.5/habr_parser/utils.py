from threading import Thread


class ThreadWithReturnValue(Thread):
    """ Add-on over the thread so that it returns the result of a function """

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def convert_str_to_number(x: str) -> int:
    """ convert numbers fron human-readable format (like -21k) to int """
    total_stars = 0
    num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    x = x.replace(',', '.')
    if '–' not in x:
        if x.isdigit():
            total_stars = int(x)
        else:
            if len(x) > 2:
                print(x)
                total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    else:
        x = x[1:]
        if x.isdigit():
            total_stars = -int(x)
        else:
            if len(x) > 1:
                total_stars = -float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)

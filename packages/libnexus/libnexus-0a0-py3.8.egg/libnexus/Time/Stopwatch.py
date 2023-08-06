from _thread import start_new_thread
from time import sleep

class Stopwatch:

    @staticmethod
    def time(function, *args, **kwargs):

        t = Stopwatch()
        t.start()
        function(*args, **kwargs)
        t.stop()
        return t

    def __init__(self):

        self.__run__ = False
        self.__time__ = 0

    def __tick__(self):

        while self.__run__:

            sleep(.001)

            self.__time__ += 1

    def start(self):

        if not self.__run__:

            self.__run__ = True

            start_new_thread(self.__tick__, ())

            return True

        else:

            return False

    def stop(self):

        self.__run__ = False

        return self

    def reset(self):

        self.__time__ = 0

    def restart(self):

        self.stop()
        self.reset()
        self.start()

    @property
    def ticks(self): return self.__time__

    @property
    def ms(self): return self.ticks

    @property
    def s(self): return self.ticks / 100

    @property
    def m(self): return self.s / 60

    @property
    def h(self): return self.m / 60
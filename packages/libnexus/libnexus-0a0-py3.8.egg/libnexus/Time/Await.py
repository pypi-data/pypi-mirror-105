from _thread import start_new_thread
from time import sleep

class Await:

    @staticmethod
    def ing(checks, returns, pass_ctx=False, check_interval=0.001, returns_in=False, returns_is=False,
            returns_custom=None):

        def collect_function(function):
            return Await(checks, returns, function, pass_ctx, check_interval, returns_in, returns_is, returns_custom)

        return collect_function

    @staticmethod
    def literal(literal):

        def r():
            return literal

        return r

    def __init__(self, checks, returns, results, pass_ctx, check_interval=0.001, returns_in=False, returns_is=False,
                 returns_custom=None):

        self.checks = checks
        self.returns = returns
        self.results = results
        self.pass_ctx = pass_ctx
        self.check_interval = check_interval

        self.returns_in = returns_in
        self.returns_is = returns_is
        self.returns_custom = returns_custom

    def __main__(self):

        c = True

        r = None

        while c:

            sleep(self.check_interval)

            r = self.checks()

            r = (r in self.returns()) if self.returns_in else (r is self.returns()) if self.returns_is else (
                self.returns_custom(r, self.returns())) if self.returns_custom else (r == self.returns())

            c = False if r else True

        if self.pass_ctx:
            self.results(r)

        else:
            self.results()

    def start(self):

        start_new_thread(self.__main__, ())

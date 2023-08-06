class Writeout:

    s = None

    @classmethod
    def write(cls, safe=False, delete=True):

        if cls.s or not safe:

            print(cls.s)

            cls.s = None if delete else cls.s

        else:

            pass


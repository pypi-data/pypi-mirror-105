class DynamicVariable:

    @staticmethod
    def wraps(function):

        return DynamicVariable(function)

    def __repr__(self):

        return f"""{self.l}""" if not self.__frozen__ else self.__frozen_val__

    def __init__(self, function):

        self.__function__ = function

        self.__frozen__ = False

        self.__frozen_val__ = None
        self.__frozen_l__ = None

    def freeze(self):

        if self.__frozen__:

            return False

        else:

            v = self.l

            self.__frozen_val__ = f"""{v}"""
            self.__frozen_l__ = v

            self.__frozen__ = True

            return True

    def unfreeze(self):

        if self.__frozen__:

            self.__frozen__ = False

            return True

        else:

            return False

    @property
    def literal(self):

        return self.__function__() if not self.__frozen__ else self.__frozen_l__

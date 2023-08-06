class Except:

    ERROR = '%e%'
    OBJECT = '%o%'
    OBJECT_NAME = '%on%'
    ARGS = '%a%'
    KWARGS = '%kwa%'
    LINE = '%l%'


    cached_exceptions = []

    @classmethod
    def s(cls, exception, replace_message=None, exit=False, returns=False):

        def handle_exception(function):

            def execute_function(*args, **kwargs):

                try:

                    function(*args, **kwargs)

                except exception as e:

                    if replace_message:

                        r = replace_message.replace(cls.ERROR, f'{e}')
                        r = r.replace(cls.OBJECT, f'{function}')
                        r = r.replace(cls.OBJECT_NAME, f'{getattr(function, "__name__")}')
                        r = r.replace(cls.ARGS, f'{args}')
                        r = r.replace(cls.KWARGS, f'{kwargs}')
                        r = r.replace(cls.LINE, f'{e.__traceback__.tb_lineno}')




                        print(r)

                    if exit: quit()

                    cls.cached_exceptions.append({e, exception, replace_message, exit})

            return execute_function

        return handle_exception

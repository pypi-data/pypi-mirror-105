class Format:

    ESCAPE = None
    NULL = False

    @classmethod
    def s(cls, string, sub_string, replace_string, max_times=None, escape_character=None):

        escape_character = cls.ESCAPE if escape_character is None else escape_character

        char = 0
        new_string = ''
        times = 0

        while char < len(string):

            if string[char] == escape_character:

                try:

                    if len(string[char:]) > 1:

                        if string[char - 1] == escape_character and string[char - 1] != escape_character:

                            new_string += escape_character
                            char += 2

                        else:

                            new_string += string[char + 1]
                            char += 2

                except IndexError:

                    new_string += string[char]
                    char += 1

            else:

                if string[char:].startswith(sub_string):

                    if (max_times and times < max_times) or not max_times:

                        times += 1
                        char += len(sub_string)
                        new_string += f'{replace_string}'

                else:

                    new_string += f'{string[char]}'
                    char += 1

        if cls.NULL:

            return string

        return new_string

    def __call__(self, string, max_times=None, escape_character=None):

        for catch, replace in self.format_group.items():

            string = Format.s(string, catch, replace, max_times, escape_character)

        return string

    def __init__(self, format_group):

        self.format_group = format_group

mc_group = {}

format_group = {
    "r": "0",  # Reset
    "l": "1",  # Bold
    "n": "2",  # Underline
    "0": "30",  # Black
    "4": "31",  # Red
    "2": "32",  # Green
    "6": "33",  # Yellow
    "1": "34",  # Blue
    "5": "35",  # Purple
    "3": "36",  # Cyan
    "f": "37",  # White
}

format_group = {f'&{x}': f'\033[{y}m' for x, y in format_group.items()}
mc_group.update(format_group)

MinecraftFormat = Format(mc_group)

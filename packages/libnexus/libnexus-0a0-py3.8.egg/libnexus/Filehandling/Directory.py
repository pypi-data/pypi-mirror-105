import os
from libnexus.Filehandling.File import File
import subprocess

class Directory:

    def __contains__(self, item):

        return item in self.list_names or item in self.name or item in self.list or (True in [item in n for n in self.list_names])

    def __repr__(self):

        return f"""<Directory Type Object of (name={self.name}, path={self.path}, files={self.size})>"""

    def __getitem__(self, item):

        if type(item) == str:

            return self.files[item]

        elif type(item) == int:

            return self.list[item]

    def __init__(self, path):

        self.path = path
        self.files = {}
        self.directory_name = lambda: os.path.basename(self.abs_path)
        self.parent = None

        self.isdir = lambda: True
        self.isfile = lambda: False

    def append(self, file, overwrite=True):

        if file.name not in self.files or overwrite:

            file.parent = self
            self.files[file.name] = file

        else:

            print(f'Filename {file.name} already exists.')
            quit()

    def __check_dir__(self, a):

        # TODO: where a is an array, return list with wanted attribute or something

        pass

    def findall(self, named=None, startswith=None, endswith=None, contains=None):

        found = []

        for f in self.list:

            if type(f) == Directory:

                [found.append(e) for e in f.findall(named, startswith, endswith, contains)]

            elif type(f) == File:

                # TODO: Fix this so that you can be more picky with what it finds

                if named and f.name == named: found.append(f)

                if startswith and f.name.startswith(startswith): found.append(f)

                if endswith and f.name.endswith(endswith): found.append(f)

                if contains and contains in f.name: found.append(f)

        return found

    def tree(self, _indent=1, _flags=None, _dir='\-', _file='|-', _thread='|'):

        string = ""

        _flags = {} if _flags is None else _flags
        flags = {
            "__init__.py": "(Python Module)",
            "__pycache__": "(Python Cache)",
            "__lstruct__.lb": "(Libnexus Struct)",
            ".cfg": "(Config)",
            "Log": ".log",
        }
        _flags.update(flags)

        for f in self.list:

            if type(f) == Directory:

                extras = ''

                for flag, alert in _flags.items():

                    extras += ' ' + alert if flag in f else ''

                string += f"{f'{_thread}    ' * _indent}{_dir} {f.name}{extras}\n{f.tree(_indent + 1)}"

            else:

                string += f"{f'{_thread}    ' * _indent}{_file} {f.name}\n"

        return string

    def get_parent(self):

        # {f', parent={self.parent}' if self.parent else ''}

        return self.parent

    def open(self):

        subprocess.Popen(r'explorer /select,"%s"' % self.abs_path)

    @property
    def size(self):

        return len(self.files)

    @property
    def list(self):

        return [self.files[file] for file in self.files]

    @property
    def list_names(self):

        return [file.name for file in self.list]

    @property
    def abs_path(self):

        return os.path.abspath(self.path)

    @property
    def name(self):

        return self.directory_name()


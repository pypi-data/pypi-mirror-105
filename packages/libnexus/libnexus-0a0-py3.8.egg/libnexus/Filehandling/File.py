import os
import subprocess

class File:

    def __contains__(self, item):

        return item in self.read() or item in self.name

    def __repr__(self):

        return f"""<File Type Object of (parent={self.parent}, name={self.name})>"""

    def __init__(self, path, __on=None):

        if __on:

            self.file_name = lambda: __on
            self.parent = None
            self.path = './'
            self.isdir = lambda: False
            self.isfile = lambda: False

        else:

            self.parent = None
            self.path = path
            self.file_name = lambda: os.path.basename(self.abs_path)
            self.isdir = lambda: False
            self.isfile = lambda: True

    def open(self, mode): return open(self.abs_path, mode)

    def read(self): return open(self.abs_path, 'r').read()

    def write(self, string): open(self.abs_path, 'w').write(string)

    def append(self, string): open(self.abs_path, 'a').write(string)

    def _assert(self): open(self.abs_path, 'a')

    def explore(self): subprocess.Popen(r'explorer /select,"%s"' % self.abs_path)

    @property
    def name(self): return self.file_name()

    @property
    def abs_path(self): return os.path.abspath(self.path)
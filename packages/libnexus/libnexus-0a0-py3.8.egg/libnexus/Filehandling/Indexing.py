import os

from libnexus.Filehandling.File import File
from libnexus.Filehandling.Directory import Directory

class Indexer:

    Cached_Directories = None
    Cached_Files = None

    @staticmethod
    def investigate_dir(path):

        dirs = os.listdir(path)

        index = []

        for d in dirs:

            npath = f'{path}/{d}'

            indexed_files = []

            if os.path.isdir(npath):

                indexed_files.append(Indexer.investigate_dir(npath))

            elif os.path.isfile(npath):

                indexed_files.append(npath)

            # THEN

            if len(indexed_files) > 1:

                index.append(indexed_files)

            else:

                index.append(indexed_files[0])

        return index

    id = investigate_dir

    @classmethod
    def practical_investigate_dir(cls, path, complexity=9999):

        dirs = os.listdir(path)
        index = Directory(path)

        if complexity > 0:

            for d in dirs:

                npath = f'{path}/{d}'

                indexed_files = Directory(npath)

                try:

                    if os.path.isdir(npath):

                        indexed_files.append(Indexer.practical_investigate_dir(npath, complexity - 1))

                    elif os.path.isfile(npath):

                        indexed_files.append(
                            File(npath)
                        )

                    # THEN

                    if indexed_files.size > 1:

                        index.append(indexed_files)

                    else:

                        index.append(indexed_files[0])

                except PermissionError:

                    index.append(
                        File(None, f'<NoPermission: Can\'t enter directory! (path={npath})>')
                    )

            return index

        else:

            return index

    pid = practical_investigate_dir

from abc import ABC

import package
from setuptools import setup, find_namespace_packages
import distutils.cmd
import os
import shutil

ROOTDIR = os.path.dirname(os.path.abspath(__file__))
FILES_CLEAN = ['build', 'dist', '{name}.egg-info'.format(name=package.name), '.cache']
WALK_FILES_EXT_CLEAN = ['.pyc']
WALK_DIRS_CLEAN = ['__pycache__']


class CleanCommand(distutils.cmd.Command, ABC):
    description = 'Project Clean'

    def run(self) -> None:
        for filename in FILES_CLEAN:
            if os.path.exists(filename):
                shutil.rmtree(filename)
        for dirpath, dirnames, filenames in os.walk(ROOTDIR):
            for filename in filenames:
                for extension in WALK_FILES_EXT_CLEAN:
                    if filename.endswith(extension):
                        path = os.path.join(dirpath, filename)
                        os.unlink(path)
            for dirname in dirnames:
                if dirname in WALK_DIRS_CLEAN:
                    path = os.path.join(dirpath, dirname)
                    shutil.rmtree(path, ignore_errors=True)


def main():
    args_setuptools = dict(
        keywords=', '.join([keyword for keyword in package.keywords])
    )

    metadata = dict(
        name=package.name,
        version=package.version,
        description=package.description,
        long_description=package.long_description,
        author=','.join([author['name'] for author in package.authors]),
        author_email=','.join([author['email'] for author in package.authors]),
        packages=find_namespace_packages(),
        cmdclass={
            'clean': CleanCommand
                 },
        **args_setuptools
    )

    setup(**metadata)


if __name__ == '__main__':
    main()

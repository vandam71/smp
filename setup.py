from abc import ABC

import package
import distutils.cmd
import os
import shutil

ROOTDIR = os.path.dirname(os.path.abspath(__file__))
FILES_CLEAN = ['build', 'dist', '{name}.egg-info'.format(name=package.name), '.cache']
WALK_FILES_EXT_CLEAN = ['.pyc', '.smp']
WALK_DIRS_CLEAN = ['__pycache__']


class CleanCommand(distutils.cmd.Command):
    description = 'Project Clean'
    user_options = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

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
    try: 
        from setuptools import setup
        args_setuptools = dict(
            keywords =', '.join([keyword for keyword in package.keywords])
        )
    except ImportError:
        from distutils.core import setup
        args_setuptools = dict()

    metadata = dict(
        name=package.name,
        version=package.version,
        description=package.description,
        long_description=package.long_description,
        author=','.join([author['name'] for author in package.authors]),
        author_email=','.join([author['email'] for author in package.authors]),
        packages=package.modules,
        cmdclass={
            'clean': CleanCommand
                 },
        **args_setuptools
    )

    setup(**metadata)


if __name__ == '__main__':
    main()

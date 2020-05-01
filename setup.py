import package
from setuptools import setup, find_namespace_packages
import distutils.cmd


class PrintCommand(distutils.cmd.Command):
    description = 'Simple Test Command'

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        print("I am Here!")


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
            'test': PrintCommand
                 },
        **args_setuptools
    )

    setup(**metadata)


if __name__ == '__main__':
    main()

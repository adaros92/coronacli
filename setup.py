import pathlib
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ["--cov", "coronacli"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    description='COVID-19 stats in your terminal',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Adams Rosales (https://github.com/arlovesdata)',
    url='https://github.com/adaros92/coronacli',
    author_email='adams.rosales.92@gmail.com',
    version='0.1.6',
    install_requires=['requests', 'sqlalchemy', 'pandas', 'tabulate'],
    tests_require=['pytest', 'pytest-cov'],
    license="MIT",
    classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
        ],
    cmdclass={'test': PyTest},
    packages=find_packages(exclude=("test",)),
    name='coronacli',
    python_requires='>=3.5',
    entry_points={
            'console_scripts': [
                    'coronacli = coronacli.cli:main'
                ]
        }
)

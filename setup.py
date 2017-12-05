#!/usr/bin/env python
from setuptools import setup, find_packages, Command
import os


class PyTest(Command):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import pytest
        pytest.main('')


def generate_console_scripts(location):
    yield '[console_scripts]'
    files = os.listdir(location)
    checks = filter(lambda x: x.endswith('.py'),
                    files)
    for check_name in checks:
        simple_name = check_name[:-len('.py')]
        line = "%s=kapacitor_plugins.%s:main" % (check_name, simple_name)
        yield line

setup(name="kapacitor_plugins",
      version="1.0",
      description="kapacitor plugins in python",
      author="Dmitry Ryobrishkin",
      author_email="dr@servers.com",
      url="http://fillmeplease",
      packages=find_packages(),
      install_requires=['requests',
                        'regex'],
      entry_points="\n".join(generate_console_scripts('kapacitor_plugins')),
      cmdclass={'test': PyTest})

from setuptools import setup, find_packages

setup(
    name='commands',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Checksumdir'
    ],
    entry_points={
        'console_scripts': [
            'init = commands.init:init',
            'add = commands.add:add',
            'commit = commands.commit:commit',
            'log = commands.log:log',
            'reset = commands.reset:reset'
        ],
    },
)

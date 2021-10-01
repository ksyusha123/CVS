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
            'init = commands.init:cli',
            'add = commands.add:cli',
            'commit = commands.commit:cli',
            'log = commands.log:log',
            'reset = commands.reset:cli'
        ],
    },
)

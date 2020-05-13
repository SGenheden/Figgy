from setuptools import setup

setup (
    name='Figgy',
    version="0.0.2",
    description='Tetris-like game',
    long_description=open('README.md').read(),
    url='https://github.com/sgenheden/Figgy',
    author='Samuel Genheden',
    author_email='samuel.genheden@gmail.com',
    license='GNU General Public Licence',

    packages=['figgy', 'figgy/utils', 'figgy/images'],
    package_data= {
        "": ["*.png", "*.json"]
    },
    install_requires=['pgzero', 'matplotlib', 'black',],
    entry_points={'console_scripts': ['figgy = figgy.utils.runner:main', ]},
)
from setuptools import setup
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='portest',
    version='0.1.0',
    author=['HavivV'],
    author_email=['HavivV1305@gmail.com'],
    license='LICENSE',
    platforms='linux',
    description='Check port throw firewall to your attack server',
    long_description=read('README.md'),
    packages=['.',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'portest = main:main',
        ]
    },
    install_requires=[
        "scapy",
        "colorlog",
        "click==6.7",
        "requests",
        "netifaces",
    ]
)


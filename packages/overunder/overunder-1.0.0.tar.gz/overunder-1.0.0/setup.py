# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['overunder']
entry_points = \
{'console_scripts': ['overunder = overunder:main']}

setup_kwargs = {
    'name': 'overunder',
    'version': '1.0.0',
    'description': "An interpreted programming language in Python that could receive as rules basic weaving instructions 'over' and 'under' and apply a pattern onto text.",
    'long_description': '# overunder\n\nCommands:\n\nload - loads the input text\nshow - shows which line you are currently working on\nover + int(x) - keeps the corresponding x characters intact\nunder + int(x) - replaces the corresponding x characters with a symbol\npattern - generates the pattern created so far\nsave - saves the pattern in a text file\nenter/return - moves to the next line of text\nquit - quits the program\n\nSee more here: https://pzwiki.wdka.nl/mediadesign/User:Alice/Special_Issue_V\n',
    'author': 'anxiouspeanut',
    'author_email': 'alice.strt@gmail.com',
    'maintainer': 'anxiouspeanut',
    'maintainer_email': 'alice.strt@gmail.com',
    'url': 'https://git.vvvvvvaria.org/alicestrt/overunder.git',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

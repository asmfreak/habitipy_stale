"""habitipy_stale - cache calls to habitipy and execute them after"""
import sys
from setuptools import setup

INSTALL_REQUIRES = [
    'plumbum',
    'habitipy'
]
if sys.version_info < (3, 5):
    INSTALL_REQUIRES.append('typing')

setup(
    name='habitipy_stale',
    version='0.1.0',
    author='Pavel Pletenev',
    author_email='cpp.create@gmail.com',
    url='https://github.com/ASMfreaK/habitipy',
    license='GNU GPL v3.0',
    description='cache calls to habitipy and execute them after',
    packages=['habitipy_stale'],
    install_requires=INSTALL_REQUIRES,
    package_data={
        'habitipy_stale': [
            'i18n/*/LC_MESSAGES/*.mo'
        ]
    },
    entry_points={
        'console_scripts': [
            'habitipy_stale = habitipy_stale.cli:Stale',
        ],
    },
    classifiers=[  # add more here from 'https://pypi.python.org/pypi?%3Aaction=list_classifiers'
        'License :: OSI Approved :: MIT License',
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
    ],
)

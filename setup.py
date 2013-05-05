import os
from setuptools import setup, find_packages


def read(fname):
    '''Read a file's contents'''
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="morpheus",
    version="0.0.1",
    author="Ziad Sawalha",
    author_email="ziad@sawalha.com",
    description="Dict schema helper for schema-free projects",
    license="Apache 2.0",
    keywords="schema NoSQL validation migration",
    url="http://github.com/ziadsawalha/morpheus",
    packages=find_packages(exclude=['*.tests']),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        'Natural Language :: English',
        "Topic :: Utilities",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
    ],
)

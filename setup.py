#!/usr/bin/env -S python3

from setuptools import setup, find_packages

setup(
    name = "vparser",
    version = "1.0.0",
    description = "Vector parser",
    author = "Vitold Sedyshev",
    author_email = "vit1251@gmail.com",
    url = "https://github.com/vit1251/vparser",
    install_requires = ['wheel'],
    package_dir = {'': 'src'},
    packages = find_packages('src'),
    test_suite = "tests",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Testing :: BDD',
        'Topic :: Text Processing',
    ],
)
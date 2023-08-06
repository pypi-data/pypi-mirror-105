#!/usr/bin/env python
import io
import os

from setuptools import setup, find_packages

__doc__ = ("Custom user model app for Django featuring email as username and"
           " class-based views for authentication.")


def read(fname):
    return io.open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8").read()


install_requires = [
    'Django>=1.11',
]
setup(
    # Patch from 1.7.0 and update to resolve some python3 syntax
    name='django-authtools-py3',
    packages=["authtools", "authtools.migrations"],
    version='1.7.5',
    author='Fusionbox, Inc.',
    author_email='programmers@fusionbox.com',
    description=__doc__,
    long_description='\n\n'.join([read('README.rst'), read('CHANGES.rst')]),
    url='https://github.com/nguyencg/django-authtools',
    license='BSD',
    install_requires=install_requires,
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)

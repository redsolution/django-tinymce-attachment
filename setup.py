# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

# Utility function to read the README file.  
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="grandma.django-tinymce-attachment",
    version="0.1.0",
    description=("Django tinymce attachment" +
        " with GrandmaCMS integration"),
    license="LGPL",
    keywords="django tinymce attachment",

    author="Alexander Ivanov",
    author_email="alexander.ivanov@redsolution.ru",

    maintainer='Alexander Ivanov',
    maintainer_email='alexander.ivanov@redsolution.ru',

    url="http://packages.python.org/django-tinymce-attachment",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Natural Language :: Russian',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.5',
        'Topic :: Software Development :: Version Control',
    ],
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    long_description=open('README').read(),
    entry_points={
        'grandma_setup': ['attachment = attachment.grandma_setup', ],
    }
)

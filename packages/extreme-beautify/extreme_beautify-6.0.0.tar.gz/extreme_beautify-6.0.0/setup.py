import os
from setuptools import setup, find_packages

DESCRIPTION = 'simple tool for beautifying the appearance of the application in the terminal.'
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(name='extreme_beautify',
    version='6.0.0',
    packages = find_packages(),
    include_package_data=True,
    description=DESCRIPTION,
    long_description = README,
    author='Exso Kamabay',
    author_email='<lexyong66@gmail.com>',
    url='https://github.com/ExsoKamabay/terminal-banner',
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    install_requires=['bs4', 'art', 'url64','string-color','requests'],
    keywords = ['python', 'color', 'text', 'font', 'beautifull', 'terminal'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)

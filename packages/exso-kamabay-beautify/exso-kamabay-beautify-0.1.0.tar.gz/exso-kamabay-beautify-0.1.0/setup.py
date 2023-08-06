import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(name='exso-kamabay-beautify',
    version='0.1.0',
    packages = find_packages(),
    include_package_data=True,
    description='beautify the appearance of the application on the terminal.',
    long_description = README,
    author='Exso Kamabay',
    url='https://github.com/ExsoKamabay/terminal-banner',
    license='Apache License 2.0',
    install_requires=['url64', 'string-color', 'bs4','requests','art'],
    keywords = ['beautify', 'terminal color', 'color', 'font', 'style', 'terminal'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Fonts',
        'Topic :: Text Processing :: General',
        'Topic :: Multimedia',
        'Topic :: Utilities',
    ],
)

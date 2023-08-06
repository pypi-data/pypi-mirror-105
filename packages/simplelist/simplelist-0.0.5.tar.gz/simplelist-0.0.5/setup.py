from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='simplelist',
    version='0.0.5',
    description='A Simple List Maker',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='Neil Shah',
    author_email='neil@insight3d.tech',
    license='MIT',
    classifiers=classifiers,
    keywords='lists',
    packages=find_packages(),
    install_requires=['']
)
from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='simplelist',
    version='0.0.3',
    description='A Simple List Maker',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Neil Shah',
    author_email='neil@insight3d.tech',
    license='MIT',
    classifiers=classifiers,
    keywords='lists',
    packages=find_packages(),
    install_requires=['']
)
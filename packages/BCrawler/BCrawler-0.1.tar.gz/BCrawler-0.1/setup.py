from setuptools import setup, find_packages

classiefiers = [
    'Developement Status :: 5 - Production/Stable',
    'Intended Auidence :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10 :: Linux',
    'Licence :: OSI Approved :: MIT Lience',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'BCrawler',
    version = 'V0.1',
    description = 'A folder crawler which crwls a folder and returns every file name available inside folder',
    Long_description = open('README.txt').read(),
    url = 'https://github.com/back-2-hack',
    author = 'B2h',
    author_email = 'back2hacck@gmail.com',
    License = 'MIT',
    classiefiers = classiefiers,
    keywords = 'crawler',
    packages = find_packages(),
    install_requires = []
)
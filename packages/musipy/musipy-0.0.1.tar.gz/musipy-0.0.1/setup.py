from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Python package to analyse songs'
LONG_DESCRIPTION = 'This python package helps analyse songs'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="musipy", 
        version=VERSION,
        author="Anirudh Prabhakaran",
        author_email="anirudhprabhakaran3@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that needs to be installed along with your package.
)
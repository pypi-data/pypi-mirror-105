from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'Make buttons in pygame with pyg_btn!'
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
# Setting up
setup(
    name="pygbtn",
    version=VERSION,
    author="SATAN01 (Shourya sinha)",
    author_email="<shouryasinha001@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'pygame','buttons','game-development'],
    classifiers=classifiers
)
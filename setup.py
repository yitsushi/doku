from setuptools import setup, find_packages
from doku import __version__


with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='doku',
      version=__version__,
      packages=find_packages(),
      author="Balazs Nadasdi",
      author_email="balazs.nadasdi@cheppers.com",
      long_description=long_description,
      url="https://github.com/yitsushi/doku",
      zip_safe=True,
      include_package_data=True,
      install_requires=['click'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
          "Operating System :: OS Independent",
      ],
      entry_points="""
      [console_scripts]
      doku = doku.main:cli
      """)

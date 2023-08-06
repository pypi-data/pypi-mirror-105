# Copyright (C) 2021 Avery
#
# This file is part of py18n.
#
# py18n is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# py18n is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with py18n.  If not, see <http://www.gnu.org/licenses/>.


from os import path
from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='tribi',
      version='1.0.0',
      description='Prettier error handling for Python',
      author='starsflower',
      url='https://github.com/starsflower/python-tri',
      license="MIT",
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
      ],
      packages=['tri'],
      package_dir={'tri': './tri'},

      # Description
      long_description=long_description,
      long_description_content_type='text/markdown')

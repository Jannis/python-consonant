#!/bin/bash

set -e

sudo apt-get install cmake

cd ~
&& git clone --depth=1 -b master https://github.com/libgit2/libgit2.git
&& ls .
&& cd libgit2
&& mkdir build
&& cd build
&& cmake .. -DCMAKE_INSTALL_PREFIX=../_install -DBUILD_CLAR=OFF
&& cmake --build . --target install
&& ls ..

pip install pygit2

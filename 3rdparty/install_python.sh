#!/bin/bash

# Set this an aboslute path when not running from this folder
INSTALL_DIR=$PWD
INSTALL_TARGET=$PWD/python
FW_PYTHON="$INSTALL_TARGET/bin/python"

set -e

# Install Python

cd $INSTALL_DIR
if [ ! -d "Python-2.7.2" ]; then
        tar xzf $INSTALL_DIR/Python-2.7.2.tgz
fi

cd $INSTALL_DIR/Python-2.7.2
./configure --enable-framework=$INSTALL_TARGET --enable-universalsdk=/Developer/SDKs/MacOSX10.5.sdk --prefix=$INSTALL_TARGET --with-universal-archs="32-bit"

make -j 4 && make install


#!/bin/sh
cd sip-4.12.3 && ../python/bin/python configure.py --sdk=MacOSX10.5.sdk --arch i386 && make -j 2 && make install

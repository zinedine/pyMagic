#!/bin/sh
cd PyQt-mac-gpl-4.8.4 && ../python/bin/python configure.py --verbose --use-arch i386 && make -j 5 && make install

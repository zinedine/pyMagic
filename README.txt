Running the PyMagic Code
========================

Firstly; go and *read* the README.txt in 3rdparty - it's required to ensure your dev environment is set up correctly.

General Tips
============

if you need to; install setup tools, go find PyPi (the python package index) and download setuptools-0.6.xxxx - its a shell script that is self extracting.

for coverage analysis you'll need to install figleaf:
    /usr/local/filewave/python/Python.framework/Versions/2.7/bin/easy_install http://darcs.idyll.org/~t/projects/figleaf-latest.tar.gz

Other things to consider:

pyuic4 among other usefuly python binaries will be in:
    <path to python>/python/Python.framework/Versions/Current/bin

Build QT .ui/qrc moc files with (this does not happen automatically):
    $ cd pymagic
    $ ./make_uic.sh

Making the gui.py find the lib module

1. You can add the lib to the python path folder as described in http://docs.python.org/tutorial/modules.html,
    Or just make a sym link in the ui folder.

    $ cd ui
    $ ln -s ../lib lib
    $ python main.py

2. or You can run the gui like this:
    $ PYTHONPATH=. python gui.py




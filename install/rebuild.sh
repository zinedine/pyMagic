#!/bin/bash

if [ ! -f PyMagic.spec ] ; then
        pushd . > /dev/null
        ../pyinstaller-1.5/Makespec.py -n PyMagic ../gui.py
        cat assets/spec-adjustment >> PyMagic.spec
        popd
fi

../pyinstaller-1.5/Build.py -y PyMagic.spec || exit 5
cp assets/Info.plist MacPyMagic.app/Contents/
cp -r dist/PyMagic/* ./MacPyMagic.app/Contents/MacOS
mkdir ./MacPyMagic.app/Contents/Resources > /dev/null
cp -r assets/qt_menu.nib ./MacPyMagic.app/Contents/Resources
cp assets/fwadmin.icns ./MacPyMagic.app/Contents/Resources

function rewrite_qt4name() {
        ORIG="$1"
        REPL="$2" 
        INP="$3"
        echo /usr/bin/install_name_tool -change "$ORIG" "$REPL" "$INP"
        /usr/bin/install_name_tool -change "$ORIG" "$REPL" "$INP"
}

function rewrite_qt4id() {
        ORIG="$1"
        INP="$2"
        echo /usr/bin/install_name_tool -id "$ORIG" "$INP"
        /usr/bin/install_name_tool -id "$ORIG" "$INP"
}

INSTALL=$PWD

function fixSOFiles() {
        PATH="$1"
        NAME="$2"
        shift
        shift
        COMPS="$*"
        echo "Replacing $COMPS in $NAME"
        for COMP in $COMPS; do
                rewrite_qt4name "$PREFIX/lib/$COMP.framework/Versions/4/$COMP" "$COMP" "$PATH/$NAME"
        done

        #echo "**** fixSOFiles: AFTER ****"
        #/usr/bin/otool -L "$PATH/$NAME"
}

function fixFiles() {
        ALL="$*"

        PATH="$1"
        NAME="$2"
        shift
        shift
        COMP="$NAME"
 
        rewrite_qt4id "$COMP" "$PATH/$NAME"
        
        fixSOFiles $ALL
}

function fixPlugin() {
        PATH="$1"
        PLUGIN="$2"
        shift
        shift
        COMPS="$*"
        fixSOFiles $PATH $PLUGIN.dylib $COMPS
        fixSOFiles $PATH ${PLUGIN}_debug.dylib $COMPS
}

# adjust the internal name of all the libs
which qmake
if [ $? -ne 0 ]; then
        echo "Cannot find qmake, put it in your path and run this script again..."       
        exit 3
else
        PREFIX=`qmake -query QT_INSTALL_PREFIX`

        fixSOFiles "./MacPyMagic.app/Contents/MacOS" "PyQt4.QtCore.so" QtCore
        fixSOFiles "./MacPyMagic.app/Contents/MacOS" "PyQt4.QtXml.so" QtXml QtCore
        fixSOFiles "./MacPyMagic.app/Contents/MacOS" "PyQt4.QtGui.so" QtGui QtCore
        fixSOFiles "./MacPyMagic.app/Contents/MacOS" "PyQt4.QtSql.so" QtSql QtCore QtGui
        fixSOFiles "./MacPyMagic.app/Contents/MacOS" "PyQt4.QtTest.so" QtTest QtCore QtGui
        fixSOFiles "./MacPyMagic.app/Contents/MacOS" "PyQt4.QtNetwork.so" QtNetwork QtCore QtGui
        fixSOFiles "./MacPyMagic.app/Contents/MacOS" "PyQt4.QtSvg.so" QtSvg QtCore QtGui
        fixSOFiles "./MacPyMagic.app/Contents/MacOS" "PyQt4.QtOpenGL.so" QtOpenGL QtCore QtGui

        fixFiles "./MacPyMagic.app/Contents/MacOS" QtCore QtCore
        fixFiles "./MacPyMagic.app/Contents/MacOS" QtXml QtXml QtCore
        fixFiles "./MacPyMagic.app/Contents/MacOS" QtGui QtGui QtCore
        fixFiles "./MacPyMagic.app/Contents/MacOS" QtSql QtSql QtCore QtGui
        fixFiles "./MacPyMagic.app/Contents/MacOS" QtTest QtTest QtCore QtGui
        fixFiles "./MacPyMagic.app/Contents/MacOS" QtNetwork QtNetwork QtCore QtGui
        fixFiles "./MacPyMagic.app/Contents/MacOS" QtSvg QtSvg QtCore QtGui
        fixFiles "./MacPyMagic.app/Contents/MacOS" QtOpenGL QtOpenGL QtCore QtGui

        # plugins
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/accessible" libqtaccessiblewidgets QtCore QtGui
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/codecs" libqcncodecs QtCore
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/codecs" libqjpcodecs QtCore 
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/codecs" libqkrcodecs QtCore 
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/codecs" libqtwcodecs QtCore 
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/iconengines" libqsvgicon QtCore QtXml QtSvg QtGui
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/imageformats" libqgif QtCore QtGui
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/imageformats" libqsvg QtCore QtGui
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/imageformats" libqico QtCore QtGui
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/imageformats" libqjpeg QtCore QtGui
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/imageformats" libqtiff QtCore QtGui
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/imageformats" libqmng QtCore QtGui
        fixPlugin "./MacPyMagic.app/Contents/MacOS/qt4_plugins/sqldrivers" libqsqlite QtCore QtSql

        /bin/rm MacPyMagic.app.zip > /dev/null
        /usr/bin/zip -yr MacPyMagic.app.zip MacPyMagic.app
fi


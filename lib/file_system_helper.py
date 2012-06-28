import os
from string import replace
from lib.platform import Platform

class FileSystemHelper:

    @staticmethod
    def isDriveSpec(path):
        if Platform.isWindows:
            drive, therest = os.path.splitdrive(path)
            return drive == path
        return path == u"/"

    @staticmethod
    def driveOnlyPortion(path):
        if Platform.isWindows:
            return os.path.splitdrive(path)[0]
        return u"/"

    @staticmethod
    def convertedPath(path_with_forward_slashes):
        """Takes something like a/b/c and produces the right path for the platform for it, e.g. c:\\a\\b\\c"""
        if Platform.isMac:
            return path_with_forward_slashes
        return replace(path_with_forward_slashes, '/', '\\')

    @staticmethod
    def splitPath(path):
        """
        Splits a drive path (regardless of platform) into its component parts, separated by both the drive and pathSep
        Returns a list of the parts, where the driveOnlyPortion is the first element of the list, the original path can be
        rebuilt by appending all the element and DirectoryScanner.pathSep()
        """
        res = []

        # remove the drive portion
        res += FileSystemHelper.driveOnlyPortion(path)

        # split up the remainder according to the drive separator
        remaining = path[len(res[0]):]
        if len(remaining) > 0:
            res += remaining.split(os.path.sep)

        return res

    @staticmethod
    def attachedExternalDriveNames():
        """
        Returns a list of the attached disks on this computer.  Works for both Win32 and Mac
        """
        if Platform.isWindows:
            import win32api
            return list(win32api.GetLogicalDriveStrings().split('\x00'))
        elif Platform.isMac:
            drives = []
            for dir in os.listdir('/Volumes'):
                drives.append( (dir, os.path.ismount(os.path.join('/Volumes', dir))) )
            return drives


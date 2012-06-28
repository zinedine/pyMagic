import sys
import logging
logger = logging.getLogger(__name__)

class Platform:
    """
    Provides some simple constants that make checking the platform a lot easier to read.
    """
    isWindows = sys.platform.startswith("win")
    isMac = sys.platform.startswith("darwin")

if Platform.isWindows:
    # We want to elevate privs to be able to create symlinks - this requires SeCreateSymbolicLinkPrivilege
    import jaraco.windows.privilege

    status = jaraco.windows.privilege.enable_symlink_privilege()
    if not status:
        logger.critical("FAILED to elevate our privileges to be able to construct SymLinks")

    # path the os routines to use jaraco.windows
    import jaraco.windows.filesystem as fs; fs.patch_os_module()
    # uncomment to dump privs to debug console
    # jaraco.windows.privilege.report_privilege_information()

# EASY-INSTALL-ENTRY-SCRIPT: 'figleaf==0.6.1','console_scripts','figleaf2html'
__requires__ = 'figleaf==0.6.1'
import sys
from pkg_resources import load_entry_point

sys.exit(
   load_entry_point('figleaf==0.6.1', 'console_scripts', 'figleaf2html')()
)

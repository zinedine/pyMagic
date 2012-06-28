__author__ = 'john'

import figleaf, sys
figleaf_started = None

if sys.gettrace() is None:
    figleaf.start()
    figleaf_started = True
else:
    print "Warning: NOT RUNNING COVERAGE, because the debugger seems to be active"

def stopCoverage():
    if figleaf_started is not None:
        figleaf.stop()
        figleaf.write_coverage('.figleaf')
        print "Figleaf stats were written to .figleaf"
    else:
        print "Warning: NO coverage written as the debugger was active"

from gui import run_app

run_app()
stopCoverage()
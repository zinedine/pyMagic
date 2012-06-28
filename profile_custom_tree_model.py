
import cProfile
import sys
from spike.custom_tree_widget import run_ui
cProfile.run( 'run_ui([])', 'profile_custom_tree_model.txt' )

import pstats
p = pstats.Stats('profile_custom_tree_model.txt')
p.sort_stats('time').print_stats(80)

"""
Module for running the interpretator on files
Usage: python3 run.py <filename>
"""

import subprocess
import sys

subprocess.run('python3 lib/parser.py ' + sys.argv[1], shell=True, check=False)
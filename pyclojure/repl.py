#!/usr/bin/env python

import re
import sys

from pyclojure.lexer import PyClojureLex
from pyclojure.parser import PyClojureParse
from pyclojure.core import evaluate, tostring, GlobalScope

try:
    import readline
except ImportError:
    pass
else:
    import os
    histfile = os.path.join(os.path.expanduser("~"), ".pyclojurehist")
    try:
        readline.read_history_file(histfile)
    except IOError:
        # Pass here as there isn't any history file, so one will be
        # written by atexit
        pass
    import atexit
    atexit.register(readline.write_history_file, histfile)

lexer = PyClojureLex().build()
parser = PyClojureParse().build()

def main():
    global_scope = GlobalScope()
    scopechain = [global_scope]
    while True:
        try:
            txt = raw_input("pylisp> ")
            if re.search('^\s*$', txt):
                continue
            else:
                print(tostring(evaluate(
                            parser.parse(txt, lexer=lexer), scopechain)))
        except EOFError:
            break
        except KeyboardInterrupt:
            print  # Give user a newline after Cntrl-C for readability
            break
        except Exception, e:
            print e
            return 1

if __name__ == "__main__":
    exit_code = main()
    if exit_code:
        sys.exit(exit_code)

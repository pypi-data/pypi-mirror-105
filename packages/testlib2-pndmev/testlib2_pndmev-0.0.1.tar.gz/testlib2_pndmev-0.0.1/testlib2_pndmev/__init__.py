import subprocess
subprocess.call(['pip', 'install', 'testlib_pndmev'])

import testlib_pndmev as mylib

def calc(a, b):
    return mylib.add(a, b), mylib.mul(a, b), mylib.sqr(mylib.sqrt(a))
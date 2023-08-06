import os
import stat

def add_xu(f):
    os.chmod(f, os.stat(f).st_mode | stat.S_IXUSR)


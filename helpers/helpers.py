import json
import os
import tempfile

def load_json(fname):
    ret = None
    try:
        f = open(fname)
        ret = json.load(f)
    except OSError:
        print(f"Failed to open {fname}")
    finally:
        f.close()
    return ret


tmpdir = tempfile.gettempdir()
pid_filename = os.path.join(tmpdir, 'crawler.pid')

def get_lock():
    """attempt to get a lock
    """
    print(f"writing pid to {pid_filename}")
    if os.path.isfile(pid_filename):
        return False

    f = open(pid_filename, 'w')
    f.write(f"{os.getpid()}")
    f.close()
    return True

def release_lock():
    """release the lock file
    """
    if os.path.isfile(pid_filename):
        os.unlink(pid_filename)
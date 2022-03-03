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

def get_lock(lockId = 0):
    """attempt to get a lock
    """
    # print(f"writing pid to {pid_filename}")
    real_pid_filename = f"{pid_filename}-{lockId}"
    if os.path.isfile(real_pid_filename):
        return False

    f = open(real_pid_filename, 'w')
    f.write(f"{os.getpid()}")
    f.close()
    return True

def release_lock(lockId = 0):
    """release the lock file
    """
    real_pid_filename = f"{pid_filename}-{lockId}"
    if os.path.isfile(real_pid_filename):
        os.unlink(real_pid_filename)
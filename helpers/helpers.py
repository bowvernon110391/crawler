import json

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

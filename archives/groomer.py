

from misc import setDefaultInMap

CLUSTER="cluster"
ARCHIVES="archives"
DISABLED="disabled"
BASE_DIR="base_dir"

def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], ARCHIVES, {})
    setDefaultInMap(model[CLUSTER][ARCHIVES], DISABLED, False)
    if model[CLUSTER][ARCHIVES][DISABLED]:
        return False
    else:
        setDefaultInMap(model[CLUSTER][ARCHIVES], BASE_DIR, "/data/archives_repo")
        setDefaultInMap(model[CLUSTER][ARCHIVES], ARCHIVES, [])
        return True







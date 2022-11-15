

from misc import setDefaultInMap

CLUSTER="cluster"
ARCHIVES_REPO="archives_repo"
DISABLED="disabled"
BASE_DIR="base_dir"
ARCHIVES="archives"

def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], ARCHIVES_REPO, {})
    setDefaultInMap(model[CLUSTER][ARCHIVES_REPO], DISABLED, False)
    setDefaultInMap(model[CLUSTER][ARCHIVES_REPO], BASE_DIR, "/data/archives_repo")
    setDefaultInMap(model[CLUSTER][ARCHIVES_REPO], ARCHIVES, [])
    if model[CLUSTER][ARCHIVES_REPO][DISABLED]:
        return False
    else:
        return True






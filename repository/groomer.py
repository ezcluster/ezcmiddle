

from misc import setDefaultInMap

CLUSTER="cluster"
REPOSITORY="repository"
ARCHIVES="archives"
DISABLED="disabled"
BASE_DIR="base_dir"
APT_CACHER="apt_cacher"
ALLOWED_HOSTS="allowed_hosts"

def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], REPOSITORY, {})
    setDefaultInMap(model[CLUSTER][REPOSITORY], DISABLED, False)
    if model[CLUSTER][REPOSITORY][DISABLED]:
        return False
    else:
        setDefaultInMap(model[CLUSTER][REPOSITORY], ARCHIVES, {})
        setDefaultInMap(model[CLUSTER][REPOSITORY][ARCHIVES], DISABLED, False)
        setDefaultInMap(model[CLUSTER][REPOSITORY][ARCHIVES], BASE_DIR, "/data/archives_repo")
        setDefaultInMap(model[CLUSTER][REPOSITORY][ARCHIVES], ARCHIVES, [])
        setDefaultInMap(model[CLUSTER][REPOSITORY], APT_CACHER, {})
        setDefaultInMap(model[CLUSTER][REPOSITORY][APT_CACHER], DISABLED, False)
        setDefaultInMap(model[CLUSTER][REPOSITORY][APT_CACHER], ALLOWED_HOSTS, "*")
        return True







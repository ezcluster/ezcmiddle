

from misc import setDefaultInMap

CLUSTER="cluster"
DISABLED="disabled"
BASE_DIR="base_dir"
APT_CACHER="apt_cacher"
ALLOWED_HOSTS="allowed_hosts"

def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], APT_CACHER, {})
    setDefaultInMap(model[CLUSTER][APT_CACHER], DISABLED, False)
    if model[CLUSTER][APT_CACHER][DISABLED]:
        return False
    else:
        setDefaultInMap(model[CLUSTER][APT_CACHER], ALLOWED_HOSTS, "*")
        return True







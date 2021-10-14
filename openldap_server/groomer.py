# Copyright (C) 2018 BROADSoftware
#
# This file is part of EzCluster
#
# EzCluster is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EzCluster is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with EzCluster.  If not, see <http://www.gnu.org/licenses/lgpl-3.0.html>.

import os
from misc import setDefaultInMap, ERROR, appendPath

CLUSTER="cluster"
OPENLDAP_SERVER="openldap_server"
DISABLED="disabled"
SSL_CERT_PATH="ssl_cert_path"
SSL_KEY_PATH="ssl_key_path"
DATA="data"
SOURCE_FILE_DIR="sourceFileDir"

def groom(plugin, model):
    setDefaultInMap(model[CLUSTER][OPENLDAP_SERVER], DISABLED, False)
    if model[CLUSTER][OPENLDAP_SERVER][DISABLED]:
        return False
    else:
        if (SSL_CERT_PATH in model[CLUSTER][OPENLDAP_SERVER]) ^ (SSL_KEY_PATH in model[CLUSTER][OPENLDAP_SERVER]):
            ERROR("'ssl_cert_path' and 'ssl_key_path' must be defined together or none")
        if SSL_CERT_PATH in model[CLUSTER][OPENLDAP_SERVER]:
            model[CLUSTER][OPENLDAP_SERVER][SSL_CERT_PATH] = appendPath(model[DATA][SOURCE_FILE_DIR], model[CLUSTER][OPENLDAP_SERVER][SSL_CERT_PATH])
            model[CLUSTER][OPENLDAP_SERVER][SSL_KEY_PATH] = appendPath(model[DATA][SOURCE_FILE_DIR], model[CLUSTER][OPENLDAP_SERVER][SSL_KEY_PATH])
        if SSL_CERT_PATH in model[CLUSTER][OPENLDAP_SERVER]:
            fn = model[CLUSTER][OPENLDAP_SERVER][SSL_CERT_PATH]
            if not os.path.isfile(fn):
                ERROR("Unable to find '{}'!".format(fn))
            fn = model[CLUSTER][OPENLDAP_SERVER][SSL_KEY_PATH]
            if not os.path.isfile(fn):
                ERROR("Unable to find '{}'!".format(fn))
        
        return True

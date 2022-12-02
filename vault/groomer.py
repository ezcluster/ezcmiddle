# Copyright (C) 2022 BROADSoftware
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

from misc import setDefaultInMap,lookupRepository,appendPath,ERROR
import os
import shutil

VAULT = "vault"
CLUSTER = "cluster"
DISABLED = "disabled"
REPO_ID="repo_id"
SSL_CERT_SRC="ssl_cert_src"
SSL_KEY_SRC="ssl_key_src"
SSL_CA_SRC="ssl_key_src"
DATA="data"
SCHEME="scheme"
SOURCE_FILE_DIR="sourceFileDir"
PORT="port"
TEMP_CERT_FOLDER="temp_cert_folder"
ENDPOINT_FQDN="endpoint_fqdn"
FQDN="fqdn"
_FQDN="_fqdn"
NODES="nodes"

def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], VAULT, {})
    setDefaultInMap(model[CLUSTER][VAULT], DISABLED, False)
    if model[CLUSTER][VAULT][DISABLED]:
        return False
    else:
        setDefaultInMap(model[CLUSTER][VAULT], SCHEME, "https")
        setDefaultInMap(model[CLUSTER][VAULT], PORT, 8200)
        setDefaultInMap(model[DATA], VAULT, {})

        lookupRepository(model, VAULT, repoId = model[CLUSTER][VAULT][REPO_ID])
        if model[CLUSTER][VAULT][SCHEME] == "https":
            if SSL_KEY_SRC not in model[CLUSTER][VAULT] or SSL_CERT_SRC not in model[CLUSTER][VAULT] or SSL_CA_SRC not in model[CLUSTER][VAULT]:
                ERROR("If 'scheme' == 'https', then 'ssl_cert_src', 'ssl_key_src' and 'ssl_ca_src' must be defined")
            model[CLUSTER][VAULT][SSL_CERT_SRC] = appendPath(model[DATA][SOURCE_FILE_DIR], model[CLUSTER][VAULT][SSL_CERT_SRC])
            if not os.path.isfile( model[CLUSTER][VAULT][SSL_CERT_SRC]):
                ERROR("Unable to find '{}'!".format( model[CLUSTER][VAULT][SSL_CERT_SRC]))
            model[CLUSTER][VAULT][SSL_KEY_SRC] = appendPath(model[DATA][SOURCE_FILE_DIR], model[CLUSTER][VAULT][SSL_KEY_SRC])
            if not os.path.isfile( model[CLUSTER][VAULT][SSL_KEY_SRC]):
                ERROR("Unable to find '{}'!".format( model[CLUSTER][VAULT][SSL_KEY_SRC]))
            model[CLUSTER][VAULT][SSL_CA_SRC] = appendPath(model[DATA][SOURCE_FILE_DIR], model[CLUSTER][VAULT][SSL_CA_SRC])
            if not os.path.isfile(model[CLUSTER][VAULT][SSL_CA_SRC]):
                ERROR("Unable to find '{}'!".format(model[CLUSTER][VAULT][SSL_CA_SRC]))
            # Must copy in a temp location, as the playbook require all tree in same folder.
            temp_cert_folder = appendPath(model[DATA][SOURCE_FILE_DIR], "build/notzombie/cert")
            os.makedirs(temp_cert_folder, exist_ok=True)
            shutil.copy(model[CLUSTER][VAULT][SSL_CERT_SRC], temp_cert_folder + "/tls.crt")
            shutil.copy(model[CLUSTER][VAULT][SSL_KEY_SRC], temp_cert_folder + "/tls.key")
            shutil.copy(model[CLUSTER][VAULT][SSL_CA_SRC], temp_cert_folder + "/ca.crt")
            model[DATA][VAULT][TEMP_CERT_FOLDER] = temp_cert_folder
        if ENDPOINT_FQDN in model[CLUSTER][VAULT]:
            model[DATA][VAULT][ENDPOINT_FQDN] = model[CLUSTER][VAULT][ENDPOINT_FQDN]
        else:
            ## Default to the fqdn of the first node
            if _FQDN in model[CLUSTER][NODES][0]:
                model[DATA][VAULT][ENDPOINT_FQDN] = model[CLUSTER][NODES][0][_FQDN]
            else:
                model[DATA][VAULT][ENDPOINT_FQDN] = model[CLUSTER][NODES][0][FQDN]
        return True

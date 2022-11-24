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

from misc import setDefaultInMap, ERROR

CLUSTER = "cluster"
SQUID="squid"
DISABLED = "disabled"
DISK_SPACE_GB = "disk_space_gb"
CACHE_DIR="cache_dir"
ACLS="acls"
NAME="name"
ACL="acl"
RULES="rules"



def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], SQUID, {})
    setDefaultInMap(model[CLUSTER][SQUID], DISABLED, False)
    if model[CLUSTER][SQUID][DISABLED]:
        return False
    else:
        if CACHE_DIR in model[CLUSTER][SQUID] and DISK_SPACE_GB in model[CLUSTER][SQUID]:
            ERROR("squid.cache_dir and squid.disk_space_gb can't be both defined")
        setDefaultInMap(model[CLUSTER][SQUID], DISK_SPACE_GB, 10)
        setDefaultInMap(model[CLUSTER][SQUID], ACLS, [])
        setDefaultInMap(model[CLUSTER][SQUID], RULES, [])
        acl_by_name = {}
        for acl in model[CLUSTER][SQUID][ACLS]:
            acl_by_name[acl[NAME]] = acl

        for idx, rule in enumerate(model[CLUSTER][SQUID][RULES]):
            if rule[ACL] not in acl_by_name:
                ERROR("Rule[{}] refer to an unknow acl:{}".format(idx, rule[ACL]))

        if not CACHE_DIR in model[CLUSTER][SQUID]:
            model[CLUSTER][SQUID][CACHE_DIR] = "aufs /var/spool/squid {} 16 256".format(model[CLUSTER][SQUID][DISK_SPACE_GB] * 1024)

        return True

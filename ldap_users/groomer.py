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

from misc import setDefaultInMap,ERROR

CLUSTER="cluster"
LDAP_USERS="ldap_users"
DISABLED="disabled"
DATA="data"
USERS="users"
LDAP="ldap"
POSIX_USERS="posixUsers"
PERSON_USERS="personUsers"
CLASS="class"
POSIX="posix"
PERSON="person"
ATTRIBUTES="attributes"
DN="dn"
NAME="name"
VALUE="value"
CN="cn"
PASSWORD="password"
RELAY_HOST="relay_host"
LDAP_URL="ldap_url"
ADMIN_BIND_DN="admin_bind_dn"
USERS_OU="users_ou"
GROUPS_OU="groups_ou"
SN="sn"
PASSWORDS="passwords"
GROUPS="groups"
GID_NUMBER="gidNumber"
POSIX_GROUPS="posixGroups"
LDAP_GROUPS="ldapGroups"
UID="uid"
MEMBERSHIPS="memberships"
DOMAINS="domains"

posix_mandatory = {CN, UID, "uidNumber", "gidNumber", "homeDirectory"}

userByUid = {}
userByDN = {}
userByCN = {}   # Just to check duplicated

def lookupUserByUid(str):
    if str in userByUid:
        return userByUid[str]
    return None

def lookupUserByDN(str):
    if str in userByDN:
        return userByDN[str]
    return None


def groom(plugin, model):
    setDefaultInMap(model[CLUSTER][LDAP_USERS], DISABLED, False)
    if model[CLUSTER][LDAP_USERS][DISABLED]:
        return False
    else:
        setDefaultInMap(model[CLUSTER][LDAP_USERS], RELAY_HOST, "ldap_server[0]")
        setDefaultInMap(model[CLUSTER][LDAP_USERS], LDAP_URL, "ldapi:///")
        setDefaultInMap(model[CLUSTER][LDAP_USERS], DOMAINS, [])
        setDefaultInMap(model[DATA], LDAP, {})
        setDefaultInMap(model[DATA][LDAP], POSIX_USERS, [])
        setDefaultInMap(model[DATA][LDAP], PERSON_USERS, [])
        setDefaultInMap(model[DATA][LDAP], POSIX_GROUPS, [])
        setDefaultInMap(model[DATA][LDAP], LDAP_GROUPS, [])
        setDefaultInMap(model[DATA][LDAP], ATTRIBUTES, [])
        setDefaultInMap(model[DATA][LDAP], PASSWORDS, [])
        setDefaultInMap(model[DATA][LDAP], MEMBERSHIPS, [])
        if USERS in model[CLUSTER][LDAP_USERS]:
            for user in model[CLUSTER][LDAP_USERS][USERS]:
                if CLASS not in user:
                    ERROR("Missing 'class' attribute for user '{}'".format(user))
                if user[CLASS] == POSIX:
                    user2 = {}
                    # Special handling for mandatory and immutable attributes
                    for attr in posix_mandatory:
                        if attr not in user:
                            ERROR("Missing attribute '{}' for posix user '{}'. This attribute is required for a user of class 'posix'".format(attr, user))
                        user2[attr] = user[attr]
                    if SN not in user:
                        ERROR("Missing attribute 'sn' for user '{}'. This attribute is required.".format(user))
                    user2[SN] = user[SN]    # SN will also be left in optional attributes, to allow its modification
                    dn = user2[DN] = "uid={},{}".format(user['uid'], model[CLUSTER][LDAP_USERS][USERS_OU])
                    model[DATA][LDAP][POSIX_USERS].append(user2)
                    # Optional attributes
                    for attr in user:
                        if attr not in posix_mandatory and attr != "password" and attr != "class" :
                            attr2 = {}
                            attr2[DN] = user2[DN]
                            attr2[NAME] = attr
                            attr2[VALUE] = user[attr]
                            model[DATA][LDAP][ATTRIBUTES].append(attr2)
                elif user[CLASS] == PERSON:
                    if CN not in user:
                        ERROR("Missing attribute 'cn' for user '{}'. This attribute is required.".format(user))
                    if SN not in user:
                        ERROR("Missing attribute 'sn' for user '{}'. This attribute is required.".format(user))
                    user2 = {}
                    user2[CN] = user[CN]
                    user2[SN] = user[SN]  # SN will also be left in optional attributes, to allow its modification
                    if UID in user:
                        user2[UID] = user[UID]
                        dn = user2[DN] = "uid={},{}".format(user[UID], model[CLUSTER][LDAP_USERS][USERS_OU])
                    else:
                        dn = user2[DN] = "cn={},{}".format(user[CN], model[CLUSTER][LDAP_USERS][USERS_OU])
                    model[DATA][LDAP][PERSON_USERS].append(user2)
                    # Optional attributes
                    for attr in user:
                        if attr != CN and attr != "password" and attr != "class" :
                            attr2 = {}
                            attr2[DN] = user2[DN]
                            attr2[NAME] = attr
                            attr2[VALUE] = user[attr]
                            model[DATA][LDAP][ATTRIBUTES].append(attr2)
                else:
                    ERROR("Invalid 'class' value for user '{}'. Must be 'posix' or 'person'".format(user))
                if PASSWORD in user:
                    model[DATA][LDAP][PASSWORDS].append({ 'dn': dn, 'password': user[PASSWORD] })
                if CN in user2:
                    if user2[CN] in userByCN:
                        ERROR("Duplicated CN: '{}' and '{}'".format(user2, userByCN[user2[CN]]))
                    userByCN[user2[CN]] = user2                    
                if UID in user2:
                    if user2[UID] in userByUid:
                        ERROR("Duplicated Uid: '{}' and '{}'".format(user2, userByUid[user2[UID]]))
                    userByUid[user2[UID]] = user2
                userByDN[user2[DN]] = user2
        if GROUPS in model[CLUSTER][LDAP_USERS]:
            for group in model[CLUSTER][LDAP_USERS][GROUPS]:
                if CLASS not in group:
                    ERROR("Missing 'class' attribute for group '{}'".format(group))
                if CN not in group:
                    ERROR("Missing 'cn' attribute for group '{}'".format(group))
                group2 = {}
                dn = group2[DN] = "cn={},{}".format(group[CN], model[CLUSTER][LDAP_USERS][GROUPS_OU])
                group2[CN] = group[CN]
                for attr in group:
                    if attr != CN and attr != CLASS and (attr != GID_NUMBER or group[CLASS] != POSIX) and attr != USERS:
                        attr2 = {}
                        attr2[DN] = dn
                        attr2[NAME] = attr
                        attr2[VALUE] = group[attr]
                        model[DATA][LDAP][ATTRIBUTES].append(attr2)
                if group[CLASS] == POSIX:
                    if GID_NUMBER not in group:
                        ERROR("Missing 'gidNumber' attribute for posix group '{}'".format(group))
                    group2[GID_NUMBER] = group[GID_NUMBER]
                    model[DATA][LDAP][POSIX_GROUPS].append(group2)
                elif group[CLASS] == LDAP:
                    model[DATA][LDAP][LDAP_GROUPS].append(group2)
                else:
                    ERROR("Invalid 'class' value for group '{}'. Must be 'posix' or 'ldap'".format(group))
                # Now, handle group membership 
                if USERS in group:
                    for uname in group[USERS]:
                        attr = {}
                        attr[DN] = dn
                        if group[CLASS] == POSIX:
                            user = lookupUserByUid(uname)
                            if user == None:
                                ERROR("Unable to lookup a user of uid '{}' (Group:'{}')".format(uname, group[CN]))
                            attr[NAME] = "memberUid"
                            attr[VALUE] = user[UID]
                        else:
                            user = lookupUserByDN(uname)
                            if user == None:
                                ERROR("Unable to lookup a user of dn '{}' (Group:'{}')".format(uname, group[CN]))
                            attr[NAME] = "member"
                            attr[VALUE] = user[DN]
                        model[DATA][LDAP][MEMBERSHIPS].append(attr)
                        # And set the reverse 'memberOf' attribute on the user
                        #attr2 = {}
                        #attr2[DN] = user[DN]
                        #attr2[NAME] = "memberOf"
                        #attr2[VALUE] = dn
                        #model[DATA][LDAP][MEMBERSHIPS].append(attr2)
        return True

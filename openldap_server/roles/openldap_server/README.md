OpenLDAP Ansible Role
=====================
This role installs openldap and loads some example data. Intended for development and tests purposes, not to be used as production server

Original code: https://github.com/capitanh/openldap-ansible-role

SergeAlexandre modification:
- Add handler and notification
- Add TLS certificates
- Create ldap_admin_bind_dn (!= ldap_basedn)
- Rename ldap_bind_pw to ldap_admin_bind_password 


Requirements
------------
None

Role Variables
--------------
This role requires the following variables to be defined elsewhere in the playbook that uses it:
```yaml
ldap_basedn:              dc=mydomain,dc=net         # Base DN
ldap_server_uri:          ldap://localhost:389       # LDAP server URI
ldap_admin_bind_password: secret                     # bind password
ldap_admin_bind_dn:       cn=Manager,dc=mydomain,dc=net
```

Additionally, to load users and groups, you should define the following structure
```yaml
ldap_users:
  user_id1:
    cn: Name1 Surname1
    givenname: Name1
    sn: Surname1
    mail: userid1@mydomain.net
    userpassword: password
  user_id2:
    cn: Name2 Surname2
    givenname: Name2
    sn: Surname2
    mail: userid2@mydomain.net
    userpassword: password
ldap_groups:
  - name: group1
    members:
      - user_id1
  - name: group2
    members:
      - user_id1
      - user_id2
```

Dependencies
------------
None

Example Playbook
----------------
Register the role in requirements.yml:
```yaml
- src: capitanh.openldap-ansible-role
  name: openldap
```
Include it in your playbooks:
```yaml
- hosts: servers
  roles:
  - openldap
```

License
-------

BSD



Role from: https://github.com/robertdebock/ansible-role-squid


To test:
From a VM without Internet access

curl -x "http://repo1.ops.scw01:3128" -i -O -L -X GET  https://github.com/derailed/k9s/releases/download/v0.26.7/k9s_Linux_x86_64.tar.gz


sudo apt install python3-pip

pip install openshift==0.13.1

pip --proxy "http://repo1.ops.scw01:3128" install openshift==0.13.1


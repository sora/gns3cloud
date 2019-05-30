## Quick start

```bash
$ cd deploy-gns3vm

# atach the external IP address from pysical interace to br0
# example config file: 50-cloud-init.yaml.sample
$ vim /etc/netplan/50-cloud-init.yaml
$ sudo netplan apply

# install all packages and remove virbr0
$ sudo bash ./setup.bash

# edit config file: site.yaml
$ cp site.yaml.sample site.yaml
$ vim site.yaml

# delete all GNS3 vms and re-deploy all vms
$ python3 ./deploy.py

$ virsh list
```


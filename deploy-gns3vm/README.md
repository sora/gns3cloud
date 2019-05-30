## Quick start

```bash
$ cd deploy-gns3vm

# atach the external IP address from pysical interace to br0
# example config file: 50-cloud-init.yaml.sample
$ vim /etc/netplan/50-cloud-init.yaml

# check and install all packages
$ sudo bash ./setup.bash

# edit config file: site.yaml
$ cp site.yaml.sample site.yaml

# delete all GNS3 vms and re-deploy all vms
$ python3 ./deploy.py
```


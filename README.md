## Environment

* VMM: 1 host
  - OS: ubuntu 18.04
  - KVM (need Nested VM feature)
* GNS3 resource Manager: 1 host
  - OS: ubuntu 20.04
  - services:
    - apt-cacher-ng server
      - port: 3142
    - GNS3 resource server :Todo
      - port: 443
* VM: 1~ hosts
  - OS: ubuntu 20.04
  - services:
    - GNS3 server
      - port: 3080

## Quick start

### VM manager

```bash
$ sudo add-apt-repository universe
$ sudo apt install apt-cacher-ng

# Firewall setting: enable TCP 3142 port from VMs

$ sudo systemctl status apt-cacher-ng
```

### VMM

```bash
$ sudo apt update
$ sudo apt upgrade

$ git clone https://github.com/sora/gns3cloud.git
$ cd gns3cloud/deploy-gns3vm

# atach the external IP address from pysical interace to br0
# example config file: 50-cloud-init.yaml.sample
$ vim /etc/netplan/50-cloud-init.yaml
$ sudo netplan apply

# install all packages and remove virbr0
$ sudo bash ./setup.bash

# reboot and check the nested VM support
$ sudo shutdown -r now
$ cat /sys/module/kvm_intel/parameters/nested
Y

# edit config file: site.yaml
# Should edit vcpu, memory, IP address and ubuntu and gns3 user password
$ cp site.yaml.sample site.yaml
$ vim site.yaml

# delete all GNS3 vms and re-deploy all vms
$ python3 ./deploy.py

$ virsh list
```


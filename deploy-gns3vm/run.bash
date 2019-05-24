rm -f config.img
rm -f ubuntu.qcow2

bash scripts/download.bash
bash scripts/convert_ubntimg2qcow2.bash
bash scripts/cloud-localds.bash

sudo virsh destroy gns3-1
sudo virsh undefine gns3-1
sudo virsh define virt/gns3-1.xml
sudo virsh start gns3-1

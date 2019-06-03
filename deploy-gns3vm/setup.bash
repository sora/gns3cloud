# packages
echo "Install all packages for GNS3cloud"
apt install -y qemu-kvm libvirt-bin virtinst bridge-utils libosinfo-bin libguestfs-tools virt-top libvirt-dev
apt install -y unzip cloud-image-utils cloud-init 
apt install -y python3-jinja2 python3-libvirt python3-yaml

# delete default bridge device
echo "Remove default bridge device: virbr0
virsh net-autostart default --disable
virsh net-destroy default



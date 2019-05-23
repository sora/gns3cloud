GNS3VERSION="2.1.18"

#vmzip="GNS3.VM.VMware.ESXI.${GNS3VERSION}.zip"
vmzip="GNS3.VM.VMware.Workstation.${GNS3VERSION}.zip"
vmova="GNS3 VM.ova"
vmovf="GNS3 VM.ovf"
vmmf="GNS3 VM.mf"
vmvmdk1="GNS3_VM-disk1.vmdk"
vmvmdk2="GNS3_VM-disk2.vmdk"

if [ ! -e "${vmzip}" ]; then
	echo "Downloading ${vmzip}"
	wget "https://github.com/GNS3/gns3-gui/releases/download/v${GNS3VERSION}/${vmzip}"
fi

if [ ! -e "${vmova}" ]; then
	unzip "${vmzip}"
fi
tar xf "${vmova}"

echo "qemu-img convert vm image from vmdk to qcow2"
qemu-img convert -f vmdk -O qcow2 "${vmvmdk1}" "${vmvmdk2}" "GNS3-${GNS3VERSION}.qcow2"
#qemu-img convert -f vmdk -O qcow2 "${vmvmdk1}" "GNS3-${GNS3VERSION}.qcow2"

echo "remove immediate files"
rm -f "${vmmf}"
rm -f "${vmovf}"
rm -f "${vmvmdk1}"
rm -f "${vmvmdk2}"

rm -f "${vmova}"

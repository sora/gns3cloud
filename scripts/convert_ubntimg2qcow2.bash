outdir="/home/user/wrk"
imgdir="/home/user/wrk/img"

#vmimg="${imgdir}/ubuntu-18.04-minimal-cloudimg-amd64.img"
vmimg="${imgdir}/ubuntu-18.04-server-cloudimg-amd64.img"
vmqcow2="${outdir}/ubuntu.qcow2"

if [ ! -e "${vmimg}" ]; then
	echo "Downloading ${vmimg}"
	exit 1
fi

echo "qemu-img convert vm image from img to qcow2"
qemu-img convert -O qcow2 ${vmimg} ${vmqcow2}
qemu-img resize ${vmqcow2} 60G


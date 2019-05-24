outdir="img"

# vm OS
target="ubuntu-18.04-server-cloudimg-amd64.img"
url="https://cloud-images.ubuntu.com/releases/18.04/release/${target}"
if [ ! -e ${outdir}/${target} ]; then
	echo "Downloading"
	wget -O ${outdir}/${target} ${url}
fi

# VyOS
target="empty8G.qcow2"
url="https://downloads.sourceforge.net/project/gns-3/Empty%20Qemu%20disk/${target}"
if [ ! -e ${outdir}/${target} ]; then
	echo "Downloading"
	wget -O ${outdir}/${target} ${url}
fi

target="vyos-1.1.8-amd64.iso"
url="http://packages.vyos.net/iso/release/1.1.8/${target}"
if [ ! -e ${outdir}/${target} ]; then
	echo "Downloading"
	wget -O ${outdir}/${target} ${url}
fi

echo "Done"

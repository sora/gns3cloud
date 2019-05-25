import yaml, os, sys, time
import shutil

from jinja2 import Template, Environment, FileSystemLoader

def make_work_dir(work_dir):
    try:
        print(work_dir)
        os.mkdir(work_dir)
    except Exception as e:
        print("cannot make the working directory")
        print(e)
        sys.exit(1)

def remove_work_dir(work_dir):
    try:
        shutil.rmtree(work_dir)
    except:
        print("cannot remove the working directory")
        sys.exit(1)

def build_virt_xml(work_dir, tmpl_file, vmid, config):
    print("vm_id: %s" % (vmid))

    env = Environment(loader = FileSystemLoader('.'))
    template = env.get_template(tmpl_file)
    output = template.render(config)
    with open(work_dir + '/' + vmid + '.xml', 'w') as f:
        f.write(output)



def main():
    working_dir = '/tmp/gns3cloud-%d-%f' % (os.getpid(), time.time())

    make_work_dir(working_dir)

    vm = dict()

    with open("site.yaml", "r") as site_file:
        site_data = yaml.safe_load(site_file)
        vm = site_data['vm_list']

    for vm_id, vm_config in vm.items():
        build_virt_xml(working_dir, 'virt/gns3-1.xml', vm_id, vm_config)
        #build_cloud-init_base(working_dir, 'virt/gns3-1.xml', vm_id, vm_config)
        #build_cloud-init_net(working_dir, 'virt/gns3-1.xml', vm_id, vm_config)

    #remove_work_dir(working_dir)

if __name__ == "__main__":
    main()


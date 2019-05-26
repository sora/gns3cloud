import yaml, os, sys, time
import shutil

from jinja2 import Template, Environment, FileSystemLoader

config_file = 'site.yaml'

virt_xml = 'gns3.xml'
cloud_init_base = 'base.yaml'
cloud_init_network = 'network.yaml'

template_virt_dir = 'virt'
template_cloud_init_dir = 'cloud-init'


def make_work_dir(work_dir):
    try:
        os.mkdir(work_dir)
    except Exception as e:
        print("cannot make the working directory")
        print(e)
        sys.exit(1)

def make_output_dir(out_dir):
    try:
        os.mkdir(out_dir)
    except Exception as e:
        print("cannot make the output directory")
        print(e)
        sys.exit(1)

def remove_work_dir(work_dir):
    try:
        shutil.rmtree(work_dir)
    except:
        print("cannot remove the working directory")
        sys.exit(1)

def build_deploy_file(work_dir, input_dir, input_file, config):
    env = Environment(loader = FileSystemLoader('.'))
    template = env.get_template("%s/%s" % (input_dir, input_file))
    output = template.render(config)
    with open("%s/%s" % (work_dir, input_file), 'w') as f:
        f.write(output)

def main():
    working_dir = '/tmp/gns3cloud-%d-%f' % (os.getpid(), time.time())

    make_work_dir(working_dir)

    vm = dict()

    with open(config_file, "r") as site_file:
        site_data = yaml.safe_load(site_file)
        vm = site_data['vm_list']

    for vm_id, vm_config in vm.items():
        output_dir = "%s/%s" % (working_dir, vm_id)

        make_output_dir(output_dir)
        build_deploy_file(output_dir, template_virt_dir, virt_xml, vm_config)
        build_deploy_file(output_dir, template_cloud_init_dir, cloud_init_base, vm_config)
        build_deploy_file(output_dir, template_cloud_init_dir, cloud_init_network, vm_config)

    #remove_work_dir(working_dir)

if __name__ == "__main__":
    main()


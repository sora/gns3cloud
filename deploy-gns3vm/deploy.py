import os, sys, time
import subprocess
import shutil

from jinja2 import Template, Environment, FileSystemLoader
import yaml

class Config:
    def __init__(self):
        #self.working_dir = '/tmp/gns3cloud-%d-%f' % (os.getpid(), time.time())
        self.working_dir = './run'
        print(self.working_dir)

    def open(self, config_file='site.yaml'):
        vm_list = dict()
        with open(config_file, 'r') as site_file:
            site_data = yaml.safe_load(site_file)
            vm_list = site_data['vm_list']
        return vm_list

    def make_work_dir(self, work_dir=''):
        if work_dir == '':
            work_dir = self.working_dir
        try:
            os.mkdir(work_dir)
        except Exception as e:
            print("cannot make the working directory")
            print(e)
            sys.exit(1)

    def make_output_dir(self, vmid):
        out_dir = "%s/%s" % (self.working_dir, vmid)
        try:
            os.mkdir(out_dir)
        except Exception as e:
            print("cannot make the output directory")
            print(e)
            sys.exit(1)
        return out_dir

    # tsukattenai
    def remove_work_dir(self):
        try:
            shutil.rmtree(self.working_dir)
        except:
            print("cannot remove the working directory")
            sys.exit(1)

    def build_deploy_file(self, out_dir, settings):
        env = Environment(loader = FileSystemLoader('.'))
        template = env.get_template("%s/%s" % (settings['dir'], settings['file']))
        output = template.render(settings['setting'])
        with open("%s/%s" % (out_dir, settings['file']), 'w') as f:
            f.write(output)

    def build_deploy_file_all(self, vm_list):
        for vm_id, vm_config in vm_list.items():
            output_dir = self.make_output_dir(vm_id)
            for config in vm_config.items():
                config_name = config[0]
                settings = config[1]
                if config_name == 'qemu':
                    self.build_deploy_qemu(output_dir, settings)
                else:
                    self.build_deploy_file(output_dir, settings)

    def build_deploy_qemu(self, out_dir, settings):
        print('qemu')

        os_img_path = settings['setting']['os_image_path']
        qcow2_disk = settings['setting']['qcow2_disk_name']
        disk_size = settings['setting']['disk_gb']

        if os.path.isfile(os_img_path):
            print("os image file doesn't exist: " + os_img_path)
            sys.exit(1)

        # command
        out_path = "%s/%s" % (out_dir, qcow2_disk)
        try:
            result = subprocess.check_call([
                "qemu-img",
                "convert",
                "-O qcow2",
                os_img_path,
                out_path ])
        except:
            print("command faild: qemu-img convert")
            sys.exit(1)

        # command
        try:
            result = subprocess.check_call([
                "qemu-img",
                "resize",
                out_path,
                disk_size ])
        except:
            print("command faild: qemu-img resize")
            sys.exit(1)

def main():
    config = Config()
    config.make_work_dir()

    vm_list = config.open('site.yaml')

    config.build_deploy_file_all(vm_list)


if __name__ == "__main__":
    main()


import os, sys, time
import subprocess
import pathlib
import shutil

from jinja2 import Template, Environment, FileSystemLoader, DebugUndefined
import yaml

class GNS3_deploy:
    def __init__(self):
        self.working_dir = ''
        self.download_list = dict()

    def open(self, config_file='site.yaml'):
        vm_list = dict()
        with open(config_file, 'r') as site_file:
            site_data = yaml.safe_load(site_file)
            vm_list = site_data['vm_list']
            temp_path = pathlib.Path(site_data['deploy_dir'])
            self.working_dir = str(temp_path.resolve())
            print(self.working_dir)
            self.download_list = site_data['download_images']
        return vm_list

    def is_work_dir(self):
        if os.path.isdir(self.working_dir):
            return 1
        else:
            return 0

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

    def get_output_dir(self, vmid):
        return "%s/%s" % (self.working_dir, vmid)

    def remove_output_dir_all(self, vm_list):
        for vm_id, vm_config in vm_list.items():
            output_dir = self.get_output_dir(vm_id)
            if os.path.isdir(output_dir):
                try:
                    shutil.rmtree(output_dir)
                except:
                    print("cannot remove the output directory")
                    sys.exit(1)

    # tsukattenai
    def remove_work_dir(self):
        try:
            shutil.rmtree(self.working_dir)
        except:
            print("cannot remove the working directory")
            sys.exit(1)

    def cmd_run(self, cmd):
        try:
            result = subprocess.check_call(cmd)
        except:
            print("command faild:", cmd[0])
            sys.exit(1)
        return result

    def download_images(self):
        output_dir = "%s/%s" % (self.working_dir, self.download_list['output_dir'])
        if not os.path.isdir(output_dir):
            try:
                os.mkdir(output_dir)
            except Exception as e:
                print("cannot make the download_images directory")
                print(e)
                sys.exit(1)

        for t in self.download_list['targets'].items():
            target = t[1]
            output_path = "%s/%s" % (output_dir, target['file_name'])
            url_full = "%s/%s" % (target['url'], target['file_name'])

            if not os.path.isfile(output_path):
                cmd = ["wget", "-O", output_path, url_full]
                result = self.cmd_run(cmd)
            else:
                print("File exists:", target['file_name'])

    def build_deploy_file(self, out_dir, settings):
        env = Environment(loader = FileSystemLoader('.'))
        template = env.get_template("%s/%s" % (settings['dir'], settings['file']))
        tmp = settings['setting']
        tmp.update({ 'output_dir': out_dir })
        output = template.render(tmp)
        with open("%s/%s" % (out_dir, settings['file']), 'w') as f:
            f.write(output)

    def build_deploy_qemu(self, out_dir, settings):
        os_img_path = "%s/%s/%s" % (self.working_dir, self.download_list['output_dir'],
                settings['setting']['os_image_file'])
        qcow2_disk = settings['setting']['qcow2_disk_file']
        disk_size = settings['setting']['disk_gb']

        if not os.path.isfile(os_img_path):
            print("os image file doesn't exist: " + os_img_path)
            sys.exit(1)

        out_path = "%s/%s" % (out_dir, qcow2_disk)

        cmd = ["qemu-img", "convert", "-O", "qcow2", os_img_path, out_path]
        result = self.cmd_run(cmd)

        cmd = ["qemu-img", "resize", out_path, disk_size]
        result = self.cmd_run(cmd)

    def build_deploy_cloud_init_config_img(self, out_dir, settings):
        network_file = "%s/%s" % (out_dir, settings['setting']['cloud_init_network_file'])
        base_file = "%s/%s" % (out_dir, settings['setting']['cloud_init_base_file'])
        config_img_file = "%s/%s" % (out_dir, settings['setting']['config_img_file'])

        cmd = ["cloud-localds", "-N", network_file, config_img_file, base_file]
        result = self.cmd_run(cmd)

    def make_output_dir_all(self, vm_list):
        for vm_id, vm_config in vm_list.items():
            output_dir = self.make_output_dir(vm_id)

    def build_deploy_file_all(self, vm_list):
        for vm_id, vm_config in vm_list.items():
            output_dir = self.get_output_dir(vm_id)
            for config in vm_config.items():
                config_name = config[0]  # tsukattenai
                # print(config_name)
                settings = config[1]
                config_type = settings['type']
                if config_type == "command":
                    continue
                elif config_type == "file":
                    self.build_deploy_file(output_dir, settings)
                else:
                    print("unknown config_type: ", config_type)
                    sys.exit(1)

    def deploy_all(self, vm_list):
        for vm_id, vm_config in vm_list.items():
            output_dir = self.get_output_dir(vm_id)
            for config in vm_config.items():
                config_name = config[0]
                settings = config[1]
                config_type = settings['type']
                if config_type == "command":
                    if config_name == 'qemu':
                        self.build_deploy_qemu(output_dir, settings)
                    elif config_name == 'cloud_init_config_img':
                        self.build_deploy_cloud_init_config_img(output_dir, settings)
                elif config_type == "file":
                    continue
                else:
                    print("unknown config_type: ", config_type)
                    sys.exit(1)


def main():
    gns3 = GNS3_deploy()
    vm_list = gns3.open('site.yaml')

    if not gns3.is_work_dir():
        print("Make working directory ...")
        gns3.make_work_dir()

    print("Downloading images ...")
    gns3.download_images()

    print("Remove output directory ...")
    gns3.remove_output_dir_all(vm_list)

    print("Make output directory ...")
    gns3.make_output_dir_all(vm_list)

    print("Make config files ...")
    gns3.build_deploy_file_all(vm_list)

    print("Run deploy commands ...")
    gns3.deploy_all(vm_list)

if __name__ == "__main__":
    main()


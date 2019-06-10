import time

import GNS3_deploy

def main():
    config_name = 'site.yaml'

    gns3 = GNS3_deploy.GNS3_deploy()

    vm_list = gns3.open(config_name)

    if not gns3.is_work_dir():
        print("Make working directory ...")
        gns3.make_work_dir()

    print("Downloading images ...")
    gns3.download_images()

    for vm_id, vm_config in vm_list.items():
        gns3.delete_vm(vm_id, vm_config)
        gns3.remove_output_dir(vm_id, vm_config)
        gns3.make_output_dir(vm_id)
        gns3.build_deploy_file(vm_id, vm_config)
        gns3.build_vm_image(vm_id, vm_config)
        gns3.deploy_vm(vm_id, vm_config)

        time.sleep(180)

if __name__ == "__main__":
    main()


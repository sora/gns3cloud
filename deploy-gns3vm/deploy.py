import GNS3_deploy

def main():
    gns3 = GNS3_deploy.GNS3_deploy()

    vm_list = gns3.open('site.yaml')

    if not gns3.is_work_dir():
        print("Make working directory ...")
        gns3.make_work_dir()

    #print("Downloading images ...")
    #gns3.download_images()

    #print("Delete all running VMs ...")
    #gns3.delete_vm_all(vm_list)

    #print("Remove output directory ...")
    #gns3.remove_output_dir_all(vm_list)

    #print("Make output directory ...")
    #gns3.make_output_dir_all(vm_list)

    #print("Build config files ...")
    #gns3.build_deploy_file_all(vm_list)

    #print("Build vm images ...")
    #gns3.build_vm_image_all(vm_list)

    #print("Deploy all VMs ...")
    #gns3.deploy_vm_all(vm_list)

if __name__ == "__main__":
    main()


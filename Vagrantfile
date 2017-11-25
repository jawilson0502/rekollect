# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
    # Name of the machine according to Vagrant
    config.vm.define "web-rekollect"

    # Hostname
    config.vm.hostname = "web-rekollect"

    # This Vagrant development is based on Ubuntu 16.04
    config.vm.box = "ubuntu/xenial64"

    # Create a public network, or bridged network
    config.vm.network "public_network"

    # VirtualBox-specific configuration
    config.vm.provider "virutalbox" do |vb|
        vb.name = "web-rekollect"
    
        # Specify RAM and CPUs
        vb.customize ['modifyvm', :id, '--memory', 2048]
        vb.customize ['modifyvm', :id, '--cpus', 2]
    end 
    # Fix bogus error "ttyname failed Inappropriate ioctl for device"
    # Ref: https://bugs.launchpad.net/ubuntu/+source/xen-3.1/+bug/1167281
    config.vm.provision "ttyname_failed_fixup", type: "shell" do |s|
      s.inline = "sed -i -e 's/mesg n/tty -s \\&\\& mesg n/' /root/.profile; echo 'Ignore the previous error.  It is fixed now.'"
    end

    # Sync shared folder
    # config.vm.synced_folder "./", "~/rekollect"

    # Configure VM as necessary
    config.vm.provision "shell", path: "vagrantSetup.sh", privileged: false

    # Disable the default /vagrant share
    config.vm.synced_folder '.', "/vargrant", disabled: true
end

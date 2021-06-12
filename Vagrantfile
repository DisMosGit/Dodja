# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "0.0.0.0"
  config.vm.synced_folder ".", "/vagrant", type: "rsync",
    rsync__exclude: ".git/", "dodja-spa/"

  # config.vm.synced_folder ".", "/app"
  # config.vbguest.auto_update = false
  config.vm.provider "virtualbox" do |v|
    # v.name = "dodja-vm-centos-7"
    v.check_guest_additions = false
    v.memory = 1024
    v.cpus = 2
  end
  config.vm.provision :ansible do |ansible|
    ansible.playbook = "prepare_vm.yml"
    ansible.become = true
    ansible.verbose = "true"
  end
end
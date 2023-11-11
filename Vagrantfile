Vagrant.configure("2") do |config|
  config.vm.box = "debian/bullseye64"
  config.vm.provider :virtualbox do |vb|
    vb.memory = 1024
    vb.cpus = 1
  end

  config.vm.define "master" do |master|
    master.vm.hostname = "master"
    master.vm.provision "shell", inline: <<-SHELL
        mkdir /home/vagrant/stacosys
    SHELL
  end
end
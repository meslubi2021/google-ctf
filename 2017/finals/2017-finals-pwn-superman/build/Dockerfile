FROM pwntools/pwntools:dev


RUN sudo sed -i -E 's|# deb-src|deb-src|' /etc/apt/sources.list

RUN sudo apt-get update
RUN sudo apt-get --no-install-recommends install -y apt-utils ca-certificates apt-transport-https gcc-arm-linux-gnueabi
RUN sudo apt-get build-dep -y qemu
RUN git clone -b v2.9.1 --single-branch --depth 1 git://git.qemu-project.org/qemu.git

RUN sudo mkdir /shared


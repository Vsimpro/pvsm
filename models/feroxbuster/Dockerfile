FROM ubuntu:22.04

WORKDIR /root

# Update
RUN apt -y update && apt -y dist-upgrade && apt -y autoremove && apt clean
RUN apt install --reinstall coreutils
RUN apt -y install golang-go python3 python3-pip git wget unzip file zip grep coreutils


# Install Feroxbuster
RUN wget https://github.com/epi052/feroxbuster/releases/latest/download/feroxbuster_amd64.deb.zip
RUN unzip feroxbuster_amd64.deb.zip
RUN apt install ./feroxbuster_*_amd64.deb

# Install SecLists
RUN wget -c https://github.com/danielmiessler/SecLists/archive/master.zip -O SecList.zip
RUN unzip SecList.zip
RUN mkdir /usr/share/seclists
RUN mv SecLists-master/* /usr/share/seclists


# Set default command to Nuclei
ENTRYPOINT ["feroxbuster", "--url"]
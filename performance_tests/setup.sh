
dnf update -y

dnf -y install dnf-plugins-core

dnf config-manager \
    --add-repo \
    https://download.docker.com/linux/fedora/docker-ce.repo

dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose git vim

systemctl start docker

# git clone https://github.com/linnit/xasd.git

# cd xasd/performance_tests/

docker-compose -f docker-compose.yml build
# docker-compose -f docker-compose.yml up


# Use Fedora 38 as the base image
FROM fedora:38

# Build arguments
ARG OMNIA_VERSION=staging

# Update the system and install Python 3.11
RUN dnf -y install python3.11 python3.11-pip git git-lfs openssh-server \
    iproute systemd passwd openssl jq createrepo yum-utils \
    wget unzip tar dnf-plugins-core rsync iputils nano && \
    dnf clean all

RUN dnf install --setopt=install_weak_deps=False ipcalc -y

# Verify Python version
RUN python3 --version

# Install/sync python packages using the uv.lock
RUN pip3 install uv
COPY pyproject.toml uv.lock ./
ENV UV_PROJECT_ENVIRONMENT="/usr"
RUN uv sync --locked

# Allow root login by enabling it in the SSH configuration
RUN sed -i 's/^#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose port 22 for SSH
RUN sed -i 's/^#Port 22/Port 2222/' /etc/ssh/sshd_config
EXPOSE 2222

# Generate host keys if they don't exist
RUN ssh-keygen -A

# Configure workdir for ssh
RUN echo "cd /omnia" >> /root/.bashrc

# Create the /tmp/omnia_core directory
RUN mkdir -p /tmp/omnia_core

# Create the pulp config directory
RUN mkdir -p /root/.config/pulp

# Dynamically create the Ansible Galaxy requirements file
RUN echo "collections:" > /tmp/omnia_core/galaxy_requirements.yml && \
    echo "  - name: ansible.utils" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 5.1.1" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "  - name: community.crypto" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 2.23.0" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "  - name: community.docker" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 3.12.1" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "  - name: community.general" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 10.3.0" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "  - name: community.grafana" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 2.1.0" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "  - name: community.mysql" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 3.10.3" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "  - name: dellemc.os10" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 1.1.1" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "  - name: dellemc.openmanage" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 9.6.0" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "  - name: ansible.posix" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 2.0.0" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "  - name: containers.podman" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 1.16.2" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "  - name: community.postgresql" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 3.10.2" >> /tmp/omnia_core/galaxy_requirements.yml  && \
    echo "  - name: kubernetes.core" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 5.2.0" >> /tmp/omnia_core/galaxy_requirements.yml  && \
    echo "  - name: community.kubernetes" >> /tmp/omnia_core/galaxy_requirements.yml && \
    echo "    version: 2.0.1" >> /tmp/omnia_core/galaxy_requirements.yml

# Install a specific version of Ansible
RUN pip install --no-cache-dir "ansible-core==2.16.14rc1"

# Install ansible-galaxy collections from galaxy_requirements.yml
RUN ansible-galaxy collection install -r /tmp/omnia_core/galaxy_requirements.yml

# Git clone omnia repository
RUN git clone https://github.com/dell/omnia.git -b ${OMNIA_VERSION}

# Copy the entrypoint script to / and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Configure workdir for podman
WORKDIR /omnia

# Copy pulp certificate to core container's trust
COPY cert-copy.sh /cert-copy.sh
RUN chmod +x /cert-copy.sh

# Set the entrypoint script as the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

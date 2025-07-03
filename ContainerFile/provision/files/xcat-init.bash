#!/bin/bash

# Check if the OS is Ubuntu
echo "Checking if the operating system is Ubuntu..."
is_ubuntu=$(test -f /etc/debian_version && echo Y)
[[ -z ${is_ubuntu} ]] && logadm="root:" || logadm="syslog:adm"
echo "Log ownership will be set to: ${logadm}"

# Change ownership of xCAT logs
echo "Changing ownership of /var/log/xcat/ to ${logadm}..."
chown -R ${logadm} /var/log/xcat/

# Source xCAT environment variables
echo "Sourcing xCAT environment variables..."
. /etc/profile.d/xcat.sh

# Apply patches
echo "Applying patch to /opt/xcat/bin/pgsqlsetup..."
patch /opt/xcat/bin/pgsqlsetup < /patch/pgsqlsetup.patch

echo "Applying patch to /opt/xcat/lib/perl/xCAT_plugin/ddns.pm..."
patch /opt/xcat/lib/perl/xCAT_plugin/ddns.pm < /patch/ddns.patch

# Display running processes
echo "Listing running processes..."
ps -ax

# Check if xCAT needs initialization
if [[ -d "/xcatdata.NEEDINIT" ]]; then
    echo "xCAT data initialization directory found."

    if [ ! -f "/xcatdata/.init-finished" ]; then
        echo "First initialization detected. Copying template data..."
        rsync -a /xcatdata.NEEDINIT/ /xcatdata
        rsync -a /xcatdata.install/ /install
        rsync -a /xcatdata.tftpboot/ /tftpboot
        echo "Template data copied successfully."

        # Uncomment the database initialization if needed
        echo "Initializing database..."
        xcatconfig --database

        echo "Marking initialization as finished..."
        touch /xcatdata/.init-finished
    fi

    echo "Updating install table..."
    xcatconfig --updateinstall

    echo "Updating xCAT site table with xcatdport value..."
    XCATBYPASS=1 chtab key=xcatdport site.value=3001

    echo "Initializing loop devices..."
    for i in {0..7}; do
        if ! test -b /dev/loop$i; then
            echo "Creating loop device /dev/loop$i..."
            mknod /dev/loop$i -m0660 b 7 $i
        else
            echo "Loop device /dev/loop$i already exists."
        fi
    done

    echo "Creating symbolic link for switch_macmap workaround..."
    ln -sf /opt/xcat/bin/xcatclient /opt/xcat/probe/subcmds/bin/switchprobe

    echo "Renaming /xcatdata.NEEDINIT to /xcatdata.orig..."
    mv /xcatdata.NEEDINIT /xcatdata.orig
    mv /xcatdata.install /xcatdata.install.orig
    mv /xcatdata.tftpboot /xcatdata.tftpboot.orig
fi

echo "Applying patch to /install/postscripts/configeth ..."
# --forward  Ignore patches that appear to be reversed or already applied
patch --forward /install/postscripts/configeth < /patch/configeth.patch

# Restart xCAT service
echo "Restarting xCAT service..."
systemctl restart --no-block xcatd

echo "Copying mlnxofed_ib_install postscripts"
cp /opt/xcat/share/xcat/ib/scripts/Mellanox/mlnxofed_ib_install /install/postscripts/mlnxofed_ib_install

# Modify rpcbind.socket if it exists
rpcbind_socket="/usr/lib/systemd/system/rpcbind.socket"
if [ -f "$rpcbind_socket" ]; then
    echo "Modifying rpcbind.socket to use port 2240 instead of 111..."
    sed -i 's/111/2240/g' "$rpcbind_socket"
fi

# Reload and restart rpcbind.socket
echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Stopping rpcbind.socket..."
systemctl stop rpcbind.socket

echo "Starting rpcbind.socket..."
systemctl start rpcbind.socket

echo "Starting rsyslog..."
systemctl start rsyslog

# Set ownership for PostgreSQL data
echo "Changing ownership of PostgreSQL data directory to postgres:postgres..."
chown -R postgres:postgres /var/lib/pgsql/data

# Display the environment variable
# echo "Environment Variable XCATPGPW: $XCATPGPW"

# # Run PostgreSQL setup
# echo "Initializing PostgreSQL database with pgsqlsetup..."
# pgsqlsetup -i -V

# Define PostgreSQL data directory
PGSQL_DATA_DIR="/var/lib/pgsql/data"

# Check if the directory is not empty
if [ -d "$PGSQL_DATA_DIR" ] && [ "$(ls -A $PGSQL_DATA_DIR)" ]; then
    # Start PostgreSQL service if the data directory is not empty
    echo "PostgreSQL data directory is not empty. Starting PostgreSQL service..."
    systemctl start postgresql.service

    # Loop for 30s checking if both Postgres and xCAT are running, if so remake the DHCP configuration.
    for i in {1..6}; do
	    if (systemctl is-active --quiet postgresql.service) && (systemctl is-active --quiet xcatd.service); then
  		    echo "Both Postgres and xCAT are running, remaking the DHCP configuration."
  		    makedhcp -nl
	            makedhcp -a
		    break
	    fi
	    sleep 5
    done

    if ! (systemctl is-active --quiet postgresql.service) || ! (systemctl is-active --quiet xcatd.service); then
	    echo "WARN: Postgres or xCAT is not running, could not remake the DHCP configuration file."
    fi
else
    echo "PostgreSQL data directory is empty or does not exist. PostgreSQL service will not be started."
fi

# Remove nologin files
echo "Removing /etc/nologin and /var/run/nologin files..."
rm -f /etc/nologin /var/run/nologin

echo "xCAT initialization finished."
touch "/xcat-init.finished"

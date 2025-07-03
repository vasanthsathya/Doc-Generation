#!/bin/bash

# Start the corosync service
/usr/sbin/corosync start &
pid=$(pidof corosync)
if [ "$?" -ne 0 ]; then
    # If corosync fails to start, print an error message and exit
    echo "startup of corosync failed"
    exit 1
fi

# Create the /var/run directory if it doesn't exist
mkdir -p /var/run

# Start the pacemakerd service in the background
/usr/sbin/pacemakerd &
pid=$(pidof pacemakerd)
if [ "$?" -ne 0 ]; then
    # If pacemakerd fails to start, print an error message and exit
    echo "startup of pacemaker failed"
    exit 1
fi

# Check if the pcs-start.sh script exists and run it if it does
if [ -f "/opt/omnia/pcs/pcs-start.sh" ]; then
  # Run the pcs-start.sh script and redirect output to a log file
  /bin/bash -c '/opt/omnia/pcs/pcs-start.sh >> /var/log/pcs-start.log 2>&1'
else
  # Print a message if the script is not found
  echo "Script /opt/omnia/pcs/pcs-start.sh not found"
fi

tail -f /dev/null

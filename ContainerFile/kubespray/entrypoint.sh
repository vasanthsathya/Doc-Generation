#!/bin/bash

# Generate host keys
ssh-keygen -A

# Start SSH daemon
/usr/sbin/sshd -D

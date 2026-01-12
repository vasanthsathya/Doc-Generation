Host the RPMS on the Apache server
=========================================

**Prerequisites**

Make sure the server on which you want to host the repository is accessible from the OIM.

1. Update system packages ::
    
        dnf update -y

2. Install Apache (https) ::

         dnf install -y httpd

3. Install createrepo ::

        dnf install createrepo

4. Start and enable Apache ::

        systemctl start httpd
        systemctl enable httpd

5. Verify the HTTP status ::

        systemctl status httpd

The status should be Active.

6. Copy the RPMs to ``/var/www/html/``, then navigate to that directory and run the command ``“createrepo .”,`` as shown in the image below.

.. image:: ../../../images/host_rpm.png

.. image:: ../../../images/host_rpm_1.png
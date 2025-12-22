Collect Telemetry Data from OpenManage Enterprise to Kafka
==========================================================

This section describes how to configure OpenManage Enterprise to securely stream metrics into the Service Kubernetes clusters using mutual TLS (mTLS).

Prerequisites
--------------

- Ensure that the ``telemetry.yml`` file has been executed.

Steps
-----

1. Retrieve the Kafka LoadBalancer external IP by running the following command::

      kubectl get svc -n telemetry kafka-kafka-external-bootstrap -o wide

   Sample output:

   .. image:: ../../../images/external_ip_loadbalances.png

   .. note::

      Record the Kafka LoadBalancer external IP. This IP address will be used by the OpenManage Enterprise to connect to Kafka.

2. Extract the required server certificate for mTLS authentication by running the following command::

      kubectl get secret kafka-cluster-ca-cert -n telemetry -o jsonpath='{.data.ca\.crt}' | base64 -d > ca.crt

3. Extract the required client certificate for mTLS authentication using the following commands::

      kubectl get secret kafkapump -n telemetry -o jsonpath='{.data.user\.crt}' | base64 -d > user.crt
      kubectl get secret kafkapump -n telemetry -o jsonpath='{.data.user\.key}' | base64 -d > user.key

4. Create a certificate in ``.pfx`` format by running the following command. Provide a passphrase when prompted::

      openssl pkcs12 -export -out user.pfx -inkey user.key -in user.crt

5. In OpenManage Enterprise, navigate to **Configuration > Remote Connectivity**, and select **Enable**.

6. In the Kafka Connectivity wizard, select the **Enable Kafka Connectivity** check box to turn on Kafka integration.

7. In the **OME Identifier** field, enter a unique identifier to be used as the topic prefix for publishing OpenManage Enterprise metrics.

8. In the **Kafka Bootstrap Server** field, enter the external LoadBalancer IP identified in Step 1, along with the port number.

   Example::

      <Kafka LoadBalancer External IP>:<Port Number>

9. From the **Authentication Mode** list, select **SSL**.

10. Under **Server Certificate Validation**, select the **Enable Server Certificate Validation** check box, and upload the server certificate extracted in Step 2.

11. Under **Client Certificate Configuration**, select the **Enable Client Certificate for mTLS** check box, and upload the client certificate (``.pfx`` format) generated in Step 4.  
    Enter the password or passphrase used to generate the certificate, and click **Next**.

12. On the **Data Configuration** page, select the metrics to stream to the Omnia Kubernetes Service cluster, and click **Next**.

13. On the **Group Configuration** page, select the devices and device groups from which metrics should be collected, and click **Next**.

14. Navigate to **Configuration > Remote Connectivity** and verify the following:

    - Under **Connectivity**, a green check mark next to **Connected since** indicates successful connectivity between OpenManage Enterprise and the Omnia Service Kubernetes cluster.
    - Under **Transfer status**, green check marks next to each metric indicate that the selected metrics are being successfully transmitted without errors.

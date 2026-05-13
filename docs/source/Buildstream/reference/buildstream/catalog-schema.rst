.. _catalog-schema-reference:

Catalog Schema Reference
=========================

Reference documentation for the BuildStream catalog schema, including structure, validation rules, and field definitions.

.. contents:: On This Page
   :local:
   :depth: 2

Overview
--------

The BuildStream catalog schema defines the structure and validation rules for catalog files used to specify build requirements. The catalog file (``catalog_rhel.json``) contains the definitions for images, packages, and deployment targets.

* **Schema Version**: 1.1
* **File Format**: JSON
* **Default File**: ``catalog_rhel.json``
* **Location**: GitLab project repository

Catalog Structure
-----------------

The catalog file follows this top-level structure:

.. code-block:: json

    {
      "schema_version": "1.1",
      "catalog_name": "string",
      "description": "string",
      "image_groups": [
        {
          "image_group_id": "string",
          "functional_group_name": "string",
          "architecture": "string",
          "os_type": "string",
          "os_version": "string",
          "constituent_images": [
            {
              "image_name": "string",
              "image_type": "string",
              "packages": [
                {
                  "package_name": "string",
                  "package_type": "string",
                  "version": "string"
                }
              ]
            }
          ]
        }
      ]
    }

Schema Fields
-------------

Top-Level Fields
~~~~~~~~~~~~~~~~

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ``schema_version`` | string | Yes | Schema version (must be "1.1") |
| ``catalog_name`` | string | Yes | Human-readable name for the catalog |
| ``description`` | string | No | Description of the catalog purpose |
| ``image_groups`` | array | Yes | Array of image group definitions |

Image Group Fields
~~~~~~~~~~~~~~~~~

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ``image_group_id`` | string | Yes | Unique identifier for the image group |
| ``functional_group_name`` | string | Yes | Target functional group for deployment |
| ``architecture`` | string | Yes | CPU architecture (x86_64, aarch64) |
| ``os_type`` | string | Yes | Operating system type (RHEL) |
| ``os_version`` | string | Yes | OS version (10.0) |
| ``constituent_images`` | array | Yes | Array of constituent image definitions |

Constituent Image Fields
~~~~~~~~~~~~~~~~~~~~~~~~

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ``image_name`` | string | Yes | Name of the constituent image |
| ``image_type`` | string | Yes | Type of image (rpm, rpm_repo, image, iso, tarball, pip_module, git, manifest) |
| ``packages`` | array | No | Array of package definitions |

Package Fields
~~~~~~~~~~~~~~

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| ``package_name`` | string | Yes | Name of the package |
| ``package_type`` | string | Yes | Type of package (rpm, rpm_repo, pip_module, git) |
| ``version`` | string | No | Specific version of the package |

Supported Values
----------------

Functional Group Names
~~~~~~~~~~~~~~~~~~~~~~

* ``service_kube_control_plane_x86_64``
* ``service_kube_node_x86_64``
* ``slurm_control_node_x86_64``
* ``slurm_node_x86_64``
* ``slurm_node_aarch64``
* ``login_node_x86_64``
* ``login_node_aarch64``
* ``login_compiler_node_x86_64``
* ``login_compiler_node_aarch64``

Architecture Types
~~~~~~~~~~~~~~~~~~

* ``x86_64``
* ``aarch64``

OS Types
~~~~~~~~

* ``RHEL``

OS Versions
~~~~~~~~~~~

* ``10.0``

Package Types
~~~~~~~~~~~~~

* ``rpm``
* ``rpm_repo``
* ``image``
* ``iso``
* ``tarball``
* ``pip_module``
* ``git``
* ``manifest``

ApplicableFunctionalLayers
~~~~~~~~~~~~~~~~~~~~~~~~~~

The schema supports functional layer filtering through the ``ApplicableFunctionalLayers`` field, which allows specifying which functional layers the catalog applies to.

Validation Rules
----------------

* All required fields must be present
* ``schema_version`` must be exactly "1.1"
* Functional group names must match predefined values
* Architecture types must be supported values
* OS types and versions must be supported combinations
* Package types must be valid for the specified image type
* ``image_group_id`` must be unique within the catalog
* JSON syntax must be valid

Example Catalog
---------------

.. code-block:: json

    {
      "schema_version": "1.1",
      "catalog_name": "RHEL 10.0 HPC Catalog",
      "description": "Catalog for RHEL 10.0 HPC deployment",
      "image_groups": [
        {
          "image_group_id": "slurm-control-x86_64-v1",
          "functional_group_name": "slurm_control_node_x86_64",
          "architecture": "x86_64",
          "os_type": "RHEL",
          "os_version": "10.0",
          "constituent_images": [
            {
              "image_name": "slurm-control-base",
              "image_type": "image",
              "packages": [
                {
                  "package_name": "slurm",
                  "package_type": "rpm",
                  "version": "23.02.1"
                }
              ]
            }
          ]
        }
      ]
    }

Related Topics
--------------

* :doc:`../build/executing-build-pipeline` - Execute Build Pipeline
* :doc:`../deploy/executing-deploy-pipeline` - Execute Deploy Pipeline
* :doc:`upload-validation-rules` - Upload Validation Rules
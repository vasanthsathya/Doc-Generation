.. _upload-validation-rules:

Upload Validation Rules Reference
===================================

Reference documentation for BuildStream upload validation rules, including file size limits, archive restrictions, and entry count constraints.

.. contents:: On This Page
   :local:
   :depth: 2

Overview
--------

BuildStream enforces validation rules on catalog file uploads to ensure system stability and performance. These rules prevent excessively large uploads that could impact pipeline execution.

* **File Size Limits**: Maximum size for individual files
* **Archive Size Limits**: Maximum size for archive files
* **Entry Count Limits**: Maximum number of entries in catalog definitions

Validation Rules
----------------

File Size Limits
~~~~~~~~~~~~~~~~

| Resource Type | Maximum Size | Description |
|---------------|--------------|-------------|
| Individual Files | 5 MB | Maximum size for any single file uploaded to BuildStream |
| Catalog Files | 5 MB | Maximum size for catalog JSON files |
| Package Files | 5 MB | Maximum size for individual package files |

Archive Size Limits
~~~~~~~~~~~~~~~~~~~

| Resource Type | Maximum Size | Description |
|---------------|--------------|-------------|
| Archive Files | 50 MB | Maximum size for archive files (tar, zip, etc.) |
| Repository Archives | 50 MB | Maximum size for repository archive uploads |

Entry Count Limits
~~~~~~~~~~~~~~~~~~

| Resource Type | Maximum Count | Description |
|---------------|---------------|-------------|
| Catalog Entries | 500 | Maximum number of entries in a single catalog file |
| Image Groups | 500 | Maximum number of image groups in a catalog |
| Package Definitions | 500 | Maximum number of package definitions per image group |

Validation Process
------------------

When uploading catalog files or resources to BuildStream, the system performs the following validation checks:

#. **File Size Check**: Verifies individual files do not exceed 5 MB limit
#. **Archive Size Check**: Verifies archive files do not exceed 50 MB limit
#. **Entry Count Check**: Verifies catalog entries do not exceed 500 limit
#. **Schema Validation**: Verifies JSON structure matches catalog schema
#. **Content Validation**: Verifies field values match supported types and ranges

If any validation check fails, the upload is rejected with an error message indicating the specific validation rule that was violated.

Error Messages
---------------

Common validation error messages:

* **File size exceeds limit**: "Uploaded file exceeds maximum size of 5 MB"
* **Archive size exceeds limit**: "Archive file exceeds maximum size of 50 MB"
* **Entry count exceeds limit**: "Catalog contains more than 500 entries"
* **Schema validation failed**: "Catalog JSON does not match required schema"
* **Invalid field value**: "Field contains unsupported value"

Best Practices
--------------

To avoid validation errors when uploading catalog files:

* **Split Large Catalogs**: If you need more than 500 entries, split into multiple catalog files
* **Compress Archives**: Use efficient compression to keep archives under 50 MB
* **Optimize Package Lists**: Remove unnecessary package definitions to reduce entry count
* **Validate Locally**: Use JSON schema validators to check catalog files before upload
* **Monitor File Sizes**: Check file sizes before uploading to BuildStream

Troubleshooting
---------------

**Upload fails with size limit error**:
* Check the size of the file being uploaded
* Split large files into smaller chunks
* Remove unnecessary content from the file
* Verify you are not uploading compressed archives when individual files are expected

**Upload fails with entry count error**:
* Count the number of image groups in your catalog
* Split catalog into multiple files if exceeding 500 entries
* Remove duplicate or unused image group definitions
* Consider consolidating similar image groups

**Validation fails with schema error**:
* Use a JSON validator to check syntax
* Compare against the catalog schema reference
* Verify all required fields are present
* Check field values against supported values

Related Topics
--------------

* :doc:`catalog-schema` - Catalog Schema Reference
* :doc:`../build/executing-build-pipeline` - Execute Build Pipeline
* :doc:`../../troubleshooting/buildstream/common-pipeline-issues` - Troubleshooting Guide
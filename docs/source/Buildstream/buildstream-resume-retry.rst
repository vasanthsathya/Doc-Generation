.. _buildstream-resume-retry:

BuildStream Resume and Retry
===========================

BuildStream introduces intelligent execution management through Resume and Retry capabilities. This feature allows failed stages to be retried and deploy stages to be re-executed with changed inputs, eliminating the need for complete job restarts and enabling flexible deployment management.

What Is Resume and Retry?
--------------------------

Resume and Retry is a capability that enables intelligent execution management for BuildStream pipelines. It provides:

- **Retry after failure** - Failed stages can be retried without restarting the entire job
- **Smart resume** - Build stages skip already-completed work on retry
- **Re-run after success** - Deploy stages can be re-executed with changed inputs
- **Audit trail** - Complete attempt history and log preservation

**Stage Execution Patterns:**

BuildStream classifies stages into two execution patterns:

| Stage Type | Retry After Failure | Re-run After Success | Example Stages |C:\Working Folder\TOK\TOK\source
|------------|---------------------|---------------------|----------------|
| **Build Stages** | ✅ Yes (smart resume) | ❌ No (immutable) | parse-catalog, generate-input-files, create-local-repository, build-image |
| **Deploy Stages** | ✅ Yes (simple retry) | ✅ Yes (inputs can change) | deploy, restart, validate |

Why Resume and Retry Matters
----------------------------

**Operational Efficiency**

   - Save time by skipping already-completed work during retries
   - Reduce resource consumption by avoiding redundant operations
   - Enable faster recovery from transient failures

**Deployment Flexibility**

   - Re-run deploy stages when infrastructure changes (e.g., adding nodes)
   - Update configurations without rebuilding images
   - Support iterative deployment processes

**Improved Reliability**

   - Automatic recovery from transient network or storage failures
   - Complete audit trail of all execution attempts
   - Better debugging with attempt-numbered log files

**Resource Optimization**

   - Build stages skip successfully built images on retry
   - Deploy stages use input hash tracking to detect changes
   - Automated cleanup prevents resource accumulation

How Resume and Retry Works
--------------------------

Stage Guard Decision Logic
~~~~~~~~~~~~~~~~~~~~~~~~~~

BuildStream enforces stage execution rules through guard logic that determines whether a stage can be executed based on its current state.

**Build Stage Guard Logic:**

```
IF status == PENDING → Allow (Initial execution)
IF status == FAILED → Allow (Retry with resume)
IF status == COMPLETED → Reject (409 Conflict - Images are immutable)
IF status == RUNNING → Reject (409 Conflict - Already running)
```

**Deploy Stage Guard Logic:**

```
IF status == PENDING → Allow (Initial execution)
IF status == FAILED → Allow (Retry)
IF status == COMPLETED → Allow (Re-run with new inputs)
IF status == RUNNING → Reject (409 Conflict - Already running)
```

**Stage Guard Decision Tree:**

.. graph::
   Start([Stage Execution Request]) --> CheckStage{Which Stage?}
   CheckStage -->|Build Stage| BuildCheck{Current Status?}
   CheckStage -->|Deploy Stage| DeployCheck{Current Status?}
   
   BuildCheck -->|PENDING| AllowBuild[✅ Allow Execution<br/>Type: Initial]
   BuildCheck -->|FAILED| AllowRetry[✅ Allow Execution<br/>Type: Retry/Resume]
   BuildCheck -->|COMPLETED| RejectBuild[❌ Reject 409 Conflict<br/>Images are immutable]
   BuildCheck -->|RUNNING| RejectRunning1[❌ Reject 409 Conflict<br/>Already running]
   
   DeployCheck -->|PENDING| AllowDeploy[✅ Allow Execution<br/>Type: Initial]
   DeployCheck -->|FAILED| AllowDeployRetry[✅ Allow Execution<br/>Type: Retry]
   DeployCheck -->|COMPLETED| AllowRerun[✅ Allow Execution<br/>Type: Re-run]
   DeployCheck -->|RUNNING| RejectRunning2[❌ Reject 409 Conflict<br/>Already running]
   
   AllowBuild --> Execute[Execute Playbook]
   AllowRetry --> Execute
   AllowDeploy --> Execute
   AllowDeployRetry --> Execute
   AllowRerun --> Execute
   
   style AllowBuild fill:#90EE90
   style AllowRetry fill:#90EE90
   style AllowDeploy fill:#90EE90
   style AllowDeployRetry fill:#90EE90
   style AllowRerun fill:#90EE90
   style RejectBuild fill:#FFB6C1
   style RejectRunning1 fill:#FFB6C1
   style RejectRunning2 fill:#FFB6C1

Build Stage Resume Logic
~~~~~~~~~~~~~~~~~~~~~~~

Build stages implement intelligent resume to skip already-completed work:

**Resume Process:**

1. Retrieve catalog → List of images to build
2. For each image:
   - Check if image file exists in NFS storage
   - If exists → Skip (log: "Already built")
   - If not exists → Build image
3. Save successful builds to NFS storage
4. Mark stage:
   - ``COMPLETED`` if all images built
   - ``FAILED`` if any image failed (can retry)

**Build Stage Resume Flow:**

.. graph::
   Start([build_image Playbook Starts]) --> GetImages[Get list of images to build<br/>from catalog]
   GetImages --> Loop{For each image}
   
   Loop -->|Next image| CheckExists{Does image file<br/>exist in NFS?}
   
   CheckExists -->|Yes| Skip[Skip this image<br/>Log: Already built]
   CheckExists -->|No| Build[Build this image]
   
   Skip --> Loop
   Build --> BuildSuccess{Build<br/>successful?}
   
   BuildSuccess -->|Yes| SaveImage[Save image to NFS]
   BuildSuccess -->|No| MarkFailed[Mark image as failed]
   
   SaveImage --> Loop
   MarkFailed --> Loop
   
   Loop -->|All done| CheckResults{Any images<br/>failed?}
   
   CheckResults -->|No| Success[Stage status: COMPLETED]
   CheckResults -->|Yes| Failed[Stage status: FAILED<br/>Can be retried]
   
   style CheckExists fill:#FFF4E1
   style Skip fill:#E1FFE1
   style Build fill:#E1F5FF
   style Success fill:#90EE90
   style Failed fill:#FFB6C1

**Resume Example:**

| Image | Attempt 1 | Attempt 2 | Result |
|-------|-----------|-----------|--------|
| image-1 | ✅ Built | ⏭️ Skipped | Reused |
| image-2 | ✅ Built | ⏭️ Skipped | Reused |
| image-3 | ❌ Failed | ✅ Built | New |
| image-4 | ⏸️ Not started | ✅ Built | New |

**Time Savings:** 50% (2 of 4 images reused)

Deploy Stage Re-run Logic
~~~~~~~~~~~~~~~~~~~~~~~

Deploy stages track input changes via hash to enable re-execution:

**Re-run Process:**

1. Calculate input hash from PXE mapping + configuration
2. Store hash in ``result_detail`` JSON field
3. On re-run:
   - Compare new hash with previous
   - Execute regardless (inputs may have changed)
   - Track new hash for audit

**Use Case:** Add nodes to cluster

- Initial: 2 nodes deployed
- Re-run: 4 nodes deployed (PXE mapping updated)
- Result: No rebuild required

Attempt Number Tracking
~~~~~~~~~~~~~~~~~~~~~~

BuildStream maintains a complete audit trail of stage executions through attempt number tracking:

**Database Schema:**

   - ``job_stages`` table with single record per stage
   - ``attempt_number`` field tracks execution count
   - ``started_at`` records first execution start time
   - ``last_attempt_at`` records most recent execution time
   - ``result_detail`` JSONB stores execution metadata

**Log File Naming:**

Pattern: ``<stage_name>_<job_id>_attempt<attempt_number>.log``

Examples:
- ``build_image_018f3c4b_attempt1.log`` (Attempt 1)
- ``build_image_018f3c4b_attempt2.log`` (Attempt 2)
- ``deploy_018f3c4b_attempt1.log`` (Initial)
- ``deploy_018f3c4b_attempt2.log`` (Re-run)

**Audit Trail Visualization:**

.. graph::
   subgraph Job["Job ID: 018f3c4b-7b5b"]
       direction TB
       
       subgraph BuildStage["build_image Stage (Single Record)"]
           E1["id: stage-001<br/>status: COMPLETED<br/>attempt_number: 2<br/>started: 10:20<br/>last_attempt: 10:20"]
       end
       
       subgraph DeployStage["deploy Stage (Single Record)"]
           D1["id: deploy-001<br/>status: COMPLETED<br/>attempt_number: 2<br/>input_hash: def456<br/>nodes: 4<br/>started: 12:00<br/>last_attempt: 12:00"]
       end
       
       subgraph ValidateStage["validate Stage (Single Record)"]
           V1["id: val-001<br/>status: COMPLETED<br/>attempt_number: 2<br/>started: 13:30<br/>last_attempt: 13:30"]
       end
   end
   
   subgraph Logs["NFS Logs Directory (All Attempts Preserved)"]
       L1["build_image_018f3c4b_attempt1.log"]
       L2["build_image_018f3c4b_attempt2.log"]
       L3["deploy_018f3c4b_attempt1.log"]
       L4["deploy_018f3c4b_attempt2.log"]
       L5["validate_018f3c4b_attempt1.log"]
       L6["validate_018f3c4b_attempt2.log"]
   end
   
   E1 -.->|Attempt 1| L1
   E1 -.->|Attempt 2| L2
   D1 -.->|Attempt 1| L3
   D1 -.->|Attempt 2| L4
   V1 -.->|Attempt 1| L5
   V1 -.->|Attempt 2| L6
   
   style E1 fill:#E1FFE1
   style D1 fill:#E1FFE1
   style V1 fill:#E1FFE1

**Key Points:**

- Each stage has one record in ``job_stages`` table
- ``attempt_number`` tracks execution count
- Logs are numbered by attempt and map to database
- Single record updated on retry/re-run, not new records
- Complete audit trail preserved in attempt-numbered logs

Usage Examples
---------------

Retry Failed Build Stage
~~~~~~~~~~~~~~~~~~~~~~~~

**Scenario:** Build image stage fails (2 of 5 images built successfully)

**Initial Execution:**

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/build-image \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

**Response (FAILED):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "build-image",
     "status": "failed",
     "attempt_number": 1,
     "result_detail": {
       "images_built": 2,
       "images_failed": 3,
       "failed_images": ["image-3", "image-4", "image-5"]
     }
   }

**Retry Execution:**

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/build-image \
     -H "Authorization: Bearer <jwt_token>" \
     -H "X-Client-Id: gitlab-ci"

**Response (COMPLETED with Resume):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "build-image",
     "status": "completed",
     "attempt_number": 2,
     "result_detail": {
       "images_built": 5,
       "images_skipped": 2,
       "images_rebuilt": 3
     }
   }

**Result:** Successfully built 3 new images, skipped 2 existing images

Re-run Deploy Stage
~~~~~~~~~~~~~~~~~

**Scenario:** Add 2 nodes to existing 4-node deployment

**Initial Deployment (4 nodes):**

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/deploy \
     -H "Authorization: Bearer <jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{"image_group_id": "image-build19"}'

**Response (COMPLETED):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "deploy",
     "status": "completed",
     "attempt_number": 1,
     "result_detail": {
       "nodes_deployed": 4,
       "input_hash": "abc123"
     }
   }

**Update PXE Mapping (6 nodes total)**

Update ``pxe_mapping_file.csv`` to include 2 new nodes.

**Re-run Deploy Stage:**

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/deploy \
     -H "Authorization: Bearer <jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{"image_group_id": "image-build19"}'

**Response (COMPLETED with Re-run):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "deploy",
     "status": "completed",
     "attempt_number": 2,
     "result_detail": {
       "nodes_deployed": 6,
       "nodes_added": 2,
       "input_hash": "def456"
     }
   }

**Result:** Deployed 2 additional nodes without rebuilding images

Retry Failed Validation
~~~~~~~~~~~~~~~~~~~~

**Scenario:** Validation tests fail

**Initial Validation (FAILED):**

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/validate \
     -H "Authorization: Bearer <jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{"test_suite": "basic", "timeout": 600}'

**Response (FAILED):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "validate",
     "status": "failed",
     "attempt_number": 1,
     "result_detail": {
       "tests_passed": 8,
       "tests_failed": 2,
       "failed_tests": ["network_connectivity", "service_availability"]
     }
   }

**Retry Validation:**

.. code-block:: bash

   curl -X POST https://<buildstream-host>:5001/api/v1/jobs/{job_id}/stages/validate \
     -H "Authorization: Bearer <jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{"test_suite": "basic", "timeout": 600}'

**Response (COMPLETED):**

.. code-block:: json

   {
     "job_id": "018f3c4b-7b5b-4c4e-9c4e-3b5b4c4e9c4e",
     "stage": "validate",
     "status": "completed",
     "attempt_number": 2,
     "result_detail": {
       "tests_passed": 10,
       "tests_failed": 0
     }
   }

**Result:** All tests passed on retry

Error Handling and Constraints
-----------------------------

Immutability Constraints
~~~~~~~~~~~~~~~~~~~~~~

**Build Stages:**

   - Once ``COMPLETED``, build stages cannot be re-run
   - Images are considered immutable after successful build
   - To rebuild images, create a new Job

**Deploy Stages:**

   - Can be re-run after ``COMPLETED`` (inputs may change)
   - Useful for adding nodes or updating configurations
   - Input hash tracking detects configuration changes

State Precondition Checks
~~~~~~~~~~~~~~~~~~~~~~

**Deploy Stage Precondition:**

   - Image Group must be in ``BUILT`` state or intermediate states (``DEPLOYING``, ``DEPLOYED``, ``RESTARTING``, ``RESTARTED``, ``VALIDATING``, ``FAILED``)
   - ``PASSED`` and ``CLEANED`` states block deploy (require fresh build)

**Restart Stage Precondition:**

   - Image Group must be in ``DEPLOYED`` state
   - PXE mapping file must exist

**Validate Stage Precondition:**

   - Image Group must be in ``RESTARTED`` state
   - Molecule framework must be configured

Attempt Limits
~~~~~~~~~~~~

BuildStream does not enforce hard limits on retry attempts. However:

   - Image retention limit: Maximum 50 non-CLEANED Image Groups
   - Automated cleanup: Validation-failed images cleaned up after 24 hours
   - Log storage: Attempt-numbered logs preserved until Job cleanup

Log Preservation
~~~~~~~~~~~~~~

All attempt logs are preserved until Job cleanup:

   - Log location: ``/opt/omnia/build_stream_root/artifacts/{job_id}/``
   - Naming pattern: ``<stage_name>_<job_id>_attempt<attempt_number>.log``
   - Complete history available for debugging
   - Logs included in cleanup artifact deletion

Benefits and Best Practices
---------------------------

**Benefits:**

   - **Time Savings:** Smart resume skips completed work, reducing build times by 30-50%
   - **Resource Efficiency:** Avoid redundant image builds and deployments
   - **Operational Flexibility:** Re-run deploy stages without rebuilding images
   - **Complete Audit Trail:** Attempt-numbered logs provide complete execution history
   - **Better Debugging:** Separate logs per attempt simplify troubleshooting

**Best Practices:**

1. **Monitor Attempt Numbers:** High attempt counts may indicate underlying issues
2. **Review Log Files:** Check attempt-specific logs for failure patterns
3. **Clean Up Old Jobs:** Use CleanUp pipeline to remove failed artifacts
4. **Validate Before Re-run:** Ensure configuration changes are intentional
5. **Use Input Hash Tracking:** Leverage deploy stage re-run for infrastructure changes

**When to Retry vs. Create New Job:**

   - **Retry:** Transient failures, network issues, partial build failures
   - **New Job:** Fundamental configuration changes, catalog updates, architecture changes

Related Topics
--------------

* :doc:`buildstream-architecture`
* :doc:`buildstream-api-reference`
* :doc:`buildstream-pipelines`
* :doc:`buildstream_troubleshooting`

.. note::
   Resume and Retry capabilities are automatically available in BuildStream. No special configuration required. For pipeline execution procedures, see :doc:`buildstream-pipelines`. For troubleshooting, see :doc:`buildstream_troubleshooting`.

.. [SME VALIDATION REQUIRED: Verify all resume and retry logic, stage guard rules, and attempt tracking against actual BuildStream implementation]

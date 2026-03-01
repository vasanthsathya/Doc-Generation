.. _buildstream-index:

BuildStreaM Documentation
==========================

.. note::
   This topic is pending SME validation. Content may change before publication.

BuildStreaM is a build and validation automation solution that provides a catalog-driven, policy-enforced lifecycle to build, validate, and promote Omnia-compatible images. This documentation covers BuildStreaM architecture, setup, configuration, and operational procedures.

.. contents:: On This Page
   :local:
   :depth: 2

Overview
--------

BuildStreaM implements a modular monolith architecture that integrates with Omnia for automated build and validation workflows. The system provides:

- **Catalog-driven builds**: Define roles, packages, and validation dependencies in YAML catalogs
- **Stage-gated workflows**: Enforce proper build sequence with validation at each stage
- **GitLab integration**: Automated pipeline triggering and monitoring
- **API access**: RESTful API for integration with CI/CD systems
- **Policy enforcement**: Automated validation and promotion procedures

BuildStreaM represents a separate workflow from traditional Omnia deployment, focusing on automated image build and validation rather than manual cluster provisioning.

Key Features
------------

**Automation**
- Eliminates manual build and validation processes
- Automated pipeline triggering based on catalog changes
- Consistent build procedures across all environments

**Integration**
- Seamless integration with existing Omnia deployments
- GitLab-based source control and pipeline management
- RESTful API for CI/CD integration

**Validation**
- Comprehensive validation at each build stage
- Automated testing and verification procedures
- Detailed reporting and audit trails

**Scalability**
- Support for multiple concurrent build operations
- Efficient resource utilization and management
- Artifact repository integration for build storage

Architecture
-----------

BuildStreaM consists of several key components:

**API Facade**
- Single external entry point with OAuth 2.0 authentication
- Request validation and routing to internal modules
- Rate limiting and access control

**Workflow Orchestrator**
- Central coordination of build stages
- Stage gating and dependency management
- Error handling and recovery procedures

**Core Modules**
- **Catalog Manager**: Catalog parsing and validation
- **Build Module**: Omnia build workflow orchestration
- **Validate Module**: Test execution and validation
- **Promote Module**: Image promotion and baseline management

**Data Plane**
- **Artifact Repository**: Immutable storage for build artifacts
- **Metadata Store**: Job tracking and state management
- **Cache**: Performance optimization for repeated operations

Getting Started
---------------

To start using BuildStreaM:

1. **Review prerequisites**: Ensure Omnia 2.1+ and required system resources
2. **Enable BuildStreaM**: Configure Omnia to start BuildStreaM services
3. **Set up authentication**: Configure OAuth 2.0 for API access
4. **Create catalogs**: Define your build requirements in YAML catalogs
5. **Submit builds**: Use API or GitLab integration to start builds

For detailed setup instructions, see :doc:`how-to-get-started`.

Configuration
-------------

BuildStreaM requires several configuration components:

**Catalogs**
- Define roles, packages, and validation dependencies
- Support for complex build requirements
- Version control and change tracking

**GitLab Integration**
- Automated pipeline triggering
- Build monitoring and status tracking
- Collaboration and change management

**API Access**
- RESTful endpoints for all operations
- OAuth 2.0 authentication
- Comprehensive error handling

For configuration details, see:
- :doc:`how-to-configure-catalogs`
- :doc:`how-to-gitlab-integration`

Operations
----------

BuildStreaM operations include:

**Build Management**
- Submit and monitor build jobs
- Handle build failures and retries
- Manage build artifacts and results

**Pipeline Monitoring**
- Track build progress through GitLab
- Analyze build logs and error messages
- Optimize build performance

**System Maintenance**
- Service health monitoring
- Database and storage management
- Performance tuning and scaling

For operational guidance, see :doc:`../troubleshooting/buildstream-issues`.

API Reference
-------------

The BuildStreaM API provides comprehensive access to all system functions:

**Jobs API**
- Submit and manage build jobs
- Monitor job status and progress
- Control job execution and cancellation

**Catalog API**
- Validate catalog files
- Retrieve catalog schemas
- Analyze catalog dependencies

**System API**
- Health checks and system status
- Configuration and capabilities
- Metrics and performance data

For complete API documentation, see :doc:`../reference/api/buildstream`.

Limitations
-----------

BuildStreaM has several limitations to consider:

**Single-User Support**
- Baseline supports one client/user
- No role-based access control
- Multi-tenant support planned for future releases

**Performance Constraints**
- Default limit of 1 concurrent build
- No queueing for overflow requests
- Performance depends on external capacity

**Operational Constraints**
- No high availability guarantees
- No disaster recovery features
- Build and validation only (no deployment)

For detailed limitations, see :doc:`concept-architecture`.

Support and Troubleshooting
---------------------------

For help with BuildStreaM:

**Documentation**
- Review relevant topics in this documentation
- Check API reference for integration details
- Consult troubleshooting guides for common issues

**Diagnostics**
- Use built-in health check endpoints
- Analyze service logs and metrics
- Run diagnostic scripts for system analysis

**Community Support**
- Report issues through appropriate channels
- Share diagnostic information for faster resolution
- Contribute to documentation and improvements

For troubleshooting assistance, see :doc:`../troubleshooting/buildstream-issues`.

BuildStreaM Topics
------------------

.. toctree::
   :maxdepth: 2
   
   concept-architecture
   how-to-get-started
   how-to-configure-catalogs
   how-to-gitlab-integration

Related Topics
--------------

* :doc:`../reference/api/buildstream`
* :doc:`../troubleshooting/buildstream-issues`
* :doc:`../Overview/Architecture/index`

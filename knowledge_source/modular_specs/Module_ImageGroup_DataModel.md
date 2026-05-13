# Module Specification — ImageGroup Data Model

| | |
|---|---|
| **Document ID** | MSPEC-BS-DATAMODEL-2026-001 |
| **Current Version** | 1.0 |
| **Date** | 04/07/2026 |
| **Author** | Rajeshkumar S |
| **Team** | Dell Omnia — BuildStream |
| **Document Type** | Module Specification |
| **SDD Phase** | 5b — Module Specification |
| **Parent Component Spec** | CSPEC-BS-C1 (Build Pipeline API), CSPEC-BS-C2-2026-001 (Deploy Pipeline API) |
| **Implementation Task** | S1-3 (data model portion) |
| **Owner** | SD-1 (primary), SD-2 (review) |

---

**Dell Confidential - Internal Use Only**

Copyright 2026 Dell Inc. or its subsidiaries. All Rights Reserved.

---

## Revision History

| Version | Date | Description | Author(s) |
|---------|------|-------------|-----------|
| 1.0 | 04/07/2026 | Initial module spec — ImageGroup/Image data model, ORM models, enums, Alembic migration, domain entities, repository interfaces, DI registration | Dell Omnia Team |

---

## Table of Contents

- [1 References](#1-references)
- [2 Purpose & Scope](#2-purpose--scope)
- [3 Current State Analysis](#3-current-state-analysis)
- [4 ORM Model Changes](#4-orm-model-changes)
  - [4.1 ImageGroupModel (Modified)](#41-imagegroupmodel-modified)
  - [4.2 ImageModel (New)](#42-imagemodel-new)
  - [4.3 JobModel (Modified)](#43-jobmodel-modified)
  - [4.4 StageModel (Modified)](#44-stagemodel-modified)
- [5 Enum Additions](#5-enum-additions)
  - [5.1 ImageGroupStatus](#51-imagegroupstatus)
  - [5.2 PipelinePhase](#52-pipelinephase)
  - [5.3 StageType Extensions](#53-stagetype-extensions)
- [6 Alembic Migration](#6-alembic-migration)
- [7 Domain Layer Additions](#7-domain-layer-additions)
  - [7.1 File Layout](#71-file-layout)
  - [7.2 Value Objects](#72-value-objects)
  - [7.3 Domain Entity — ImageGroup](#73-domain-entity--imagegroup)
  - [7.4 Domain Entity — Image](#74-domain-entity--image)
  - [7.5 Repository Interfaces](#75-repository-interfaces)
  - [7.6 Domain Exceptions](#76-domain-exceptions)
  - [7.7 State Machine — Guard Functions](#77-state-machine--guard-functions)
- [8 Infrastructure Layer — SQL Repository](#8-infrastructure-layer--sql-repository)
- [9 Infrastructure Layer — In-Memory Repository](#9-infrastructure-layer--in-memory-repository)
- [10 Infrastructure Layer — ORM Mapper](#10-infrastructure-layer--orm-mapper)
- [11 DI Container Registration](#11-di-container-registration)
- [12 Traceability](#12-traceability)

---

## 1. References

| Source | ID | Description |
|--------|----|-------------|
| Engineering Spec (HLD) | BuildStream_Engineering_Spec(HLD).md v0.6, Section 4.1.3.3 | DB schema: `image_groups`, `images` tables, column definitions, constraints |
| Implementation Plan | BuildStream_Implementation_Plan.md, S1-3 | Task definition: ORM model creation |
| Component Spec (C2) | CSPEC-BS-C2-2026-001, Section 4.1-4.2 | ORM models, deploy-lifecycle status transitions |
| API Specification | API_Spec.md v2.0, Section 8.2 | ImageGroup data model, state machine |
| Codebase | `build_stream/infra/db/models.py` | Existing ORM models (current state) |
| Codebase | `build_stream/core/jobs/value_objects.py` | Existing enums and value objects |

---

## 2. Purpose & Scope

This module specification defines the **foundational data model** for Release 2: the `ImageGroup` and `Image` ORM models, associated enums, domain entities, repository interfaces, and Alembic migration. This data model is consumed by **all** other Sprint 1 tasks:

| Consumer | How It Uses the Data Model |
|----------|---------------------------|
| S1-3 (parse-catalog enhancement) | Creates ImageGroup placeholder, validates uniqueness |
| S1-4 (build-image DB changes) | Updates ImageGroup to BUILT, inserts Image records |
| S1-5 (Images API) | Queries ImageGroup + Image via JOIN |
| S1-6 (Deploy stage) | Guard checks on ImageGroup status, state transitions |

**This spec covers:**
- Modifications to existing `ImageGroupModel` ORM (currently incomplete)
- New `ImageModel` ORM
- New enums: `ImageGroupStatus`, `PipelinePhase`
- Extensions to existing `StageType` enum
- Modifications to existing `JobModel` and `StageModel`
- Alembic migration for schema changes
- New domain layer: entities, value objects, repository interfaces, exceptions
- SQL and in-memory repository implementations
- DI container registration

**This spec does NOT cover:**
- How these models are used by specific API endpoints (covered in Module_APIEnhancements.md and Module_Images_API.md)
- Business logic for guard checks beyond the state machine definition
- Playbook invocation patterns

---

## 3. Current State Analysis

The existing codebase has a **partial** `ImageGroupModel` in `infra/db/models.py`. The following gaps need to be addressed:

| Aspect | Current State | Required State (HLD) | Change |
|--------|--------------|---------------------|--------|
| `ImageGroupModel.id` | `String(36)` (UUID format) | `String(128)` — catalog ImageGroupID, not a UUID | **Modify** column type |
| `ImageGroupModel.job_id` | Regular FK + index (not unique) | UNIQUE FK — enforces 1:1 Job-to-ImageGroup mapping | **Add** UNIQUE constraint |
| `ImageGroupModel.image_key` | Exists as separate column | Redundant — HLD uses `id` as the image group identifier from catalog | **Remove** column (merge with `id`) |
| `ImageGroupModel.status` | Raw `String(20)` with check constraint | Should align with `ImageGroupStatus` enum | **Update** check constraint values |
| Status check constraint | `BOOTING`, `BOOTED` | `RESTARTING`, `RESTARTED`, `CLEANED` | **Update** allowed values |
| `ImageModel` | Does not exist | Required for constituent images per role | **Create** new table |
| `ImageGroup.images` relationship | Does not exist | `relationship("ImageModel")` with cascade | **Add** relationship |
| `JobModel.image_groups` | Plural relationship (list) | Should be singular 1:1 (`uselist=False`) | **Modify** to `image_group` (singular) |
| `JobModel.pipeline_phase` | Does not exist | `PipelinePhase` enum column, nullable | **Add** column |
| `StageModel.result_detail` | Does not exist | JSONB column for validation results | **Add** column |
| `StageType` enum | 6 values (build pipeline only) | 9 values (add deploy, pxe_boot, validate) | **Extend** enum |
| `StageName.MAX_LENGTH` | 30 characters | Sufficient for new stage names | No change needed |

---

## 4. ORM Model Changes

All ORM models reside in `build_stream/infra/db/models.py` (centralized, per existing convention).

### 4.1 ImageGroupModel (Modified)

```python
# build_stream/infra/db/models.py — ImageGroupModel (MODIFIED)

class ImageGroupModel(Base):
    """ORM model for image_groups table.

    Tracks the lifecycle of built images independently of transient Job states.
    Enforces a 1:1 mapping between Job and ImageGroup via UNIQUE constraint on job_id.

    The primary key 'id' is the ImageGroupID extracted from the catalog JSON
    during parse-catalog (not a UUID — it is a human-readable identifier like
    'omnia-cluster-v1.2').
    """

    __tablename__ = "image_groups"

    # Primary key — ImageGroupID from catalog (NOT a UUID)
    id = Column(String(128), primary_key=True, nullable=False)

    # Foreign key to jobs table — UNIQUE enforces 1:1 mapping
    job_id = Column(
        String(36),
        ForeignKey("jobs.job_id", ondelete="CASCADE"),
        unique=True,          # <-- CRITICAL: 1:1 Job-to-ImageGroup mapping
        nullable=False,
        index=True,
    )

    # Business attributes
    status = Column(String(20), nullable=False, default="BUILT", index=True)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    job = relationship("JobModel", back_populates="image_group", uselist=False)
    images = relationship(
        "ImageModel",
        back_populates="image_group",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # Indexes and constraints
    __table_args__ = (
        Index("idx_image_groups_job_id", "job_id", unique=True),
        Index("idx_image_groups_status", "status"),
        CheckConstraint(
            "status IN ('BUILT', 'DEPLOYING', 'DEPLOYED', 'RESTARTING', "
            "'RESTARTED', 'VALIDATING', 'PASSED', 'FAILED', 'CLEANED')",
            name="ck_image_groups_status",
        ),
    )
```

**Key changes from current code:**
1. `id` column: `String(36)` -> `String(128)` — accommodates catalog ImageGroupID strings
2. `job_id` column: added `unique=True` — enforces 1:1 mapping
3. Removed `image_key` column — redundant with `id` (the ImageGroupID IS the image key)
4. Updated status check constraint: `BOOTING`/`BOOTED` -> `RESTARTING`/`RESTARTED`, added `CLEANED`
5. Changed `job` relationship: added `uselist=False` for 1:1
6. Added `images` relationship to new `ImageModel`

### 4.2 ImageModel (New)

```python
# build_stream/infra/db/models.py — ImageModel (NEW)

class ImageModel(Base):
    """ORM model for images table.

    Stores constituent images within an Image Group, identified by
    functional role (e.g., slurm_node, kube_control_plane).

    Each Image Group contains one image per role, enforced by the
    UNIQUE constraint on (image_group_id, role).
    """

    __tablename__ = "images"

    # Primary key — UUID
    id = Column(String(36), primary_key=True, nullable=False)

    # Foreign key to image_groups table
    image_group_id = Column(
        String(128),
        ForeignKey("image_groups.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Business attributes
    role = Column(String(128), nullable=False)        # e.g., slurm_node
    image_name = Column(String(256), nullable=False)  # e.g., slurm_node.img

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    image_group = relationship("ImageGroupModel", back_populates="images")

    # Constraints
    __table_args__ = (
        Index("idx_images_image_group_id", "image_group_id"),
        Index(
            "uq_images_image_group_id_role",
            "image_group_id",
            "role",
            unique=True,
        ),
    )
```

### 4.3 JobModel (Modified)

```python
# build_stream/infra/db/models.py — JobModel changes

class JobModel(Base):
    # ... existing columns unchanged ...

    # NEW: Pipeline phase (nullable — NULL for direct invocation)
    pipeline_phase = Column(String(10), nullable=True)

    # MODIFIED: singular 1:1 relationship (was plural list)
    image_group = relationship(
        "ImageGroupModel",
        back_populates="job",
        uselist=False,           # <-- 1:1, not a list
        cascade="all, delete-orphan",
        lazy="selectin",
    )
```

**Changes:**
1. Add `pipeline_phase` column: `String(10)`, nullable (values: `BUILD`, `DEPLOY`, or `NULL`)
2. Rename relationship from `image_groups` (plural, list) to `image_group` (singular, `uselist=False`)

### 4.4 StageModel (Modified)

```python
# build_stream/infra/db/models.py — StageModel changes

class StageModel(Base):
    # ... existing columns unchanged ...

    # NEW: Result detail JSONB for validation results
    result_detail = Column(JSONB, nullable=True)
```

**Changes:**
1. Add `result_detail` column: `JSONB`, nullable — used by validate stage to persist structured test results

---

## 5. Enum Additions

### 5.1 ImageGroupStatus

```python
# build_stream/core/image_group/value_objects.py (NEW FILE)

from enum import Enum


class ImageGroupStatus(str, Enum):
    """ImageGroup lifecycle states.

    State machine for image group lifecycle through build and deploy pipelines.
    Terminal states: PASSED, FAILED, CLEANED.
    """

    BUILT = "BUILT"
    DEPLOYING = "DEPLOYING"
    DEPLOYED = "DEPLOYED"
    RESTARTING = "RESTARTING"
    RESTARTED = "RESTARTED"
    VALIDATING = "VALIDATING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    CLEANED = "CLEANED"

    def is_terminal(self) -> bool:
        """Check if status is terminal (no further transitions)."""
        return self in {
            ImageGroupStatus.PASSED,
            ImageGroupStatus.FAILED,
            ImageGroupStatus.CLEANED,
        }
```

### 5.2 PipelinePhase

```python
# build_stream/core/image_group/value_objects.py (same file as above)

class PipelinePhase(str, Enum):
    """Pipeline execution context.

    Optional — NULL/None indicates direct invocation (context-agnostic).
    """

    BUILD = "BUILD"
    DEPLOY = "DEPLOY"
```

### 5.3 StageType Extensions

```python
# build_stream/core/jobs/value_objects.py — StageType (MODIFIED)

class StageType(str, Enum):
    """Canonical stage types for BuildStreaM workflow."""

    # Existing (Release 1)
    PARSE_CATALOG = "parse-catalog"
    GENERATE_INPUT_FILES = "generate-input-files"
    CREATE_LOCAL_REPOSITORY = "create-local-repository"
    BUILD_IMAGE_X86_64 = "build-image-x86_64"
    BUILD_IMAGE_AARCH64 = "build-image-aarch64"
    VALIDATE_IMAGE_ON_TEST = "validate-image-on-test"  # Legacy, kept for R1

    # New (Release 2 — Deploy Pipeline)
    DEPLOY = "deploy"
    PXE_BOOT = "pxe_boot"
    VALIDATE = "validate"
```

**Impact on StageName value object:** The `StageName.__post_init__` validation uses `StageType(self.value)`. Adding new enum members automatically makes new stage names valid. No change to `StageName` class needed, but `MAX_LENGTH = 30` is sufficient for all new values (longest: `validate-image-on-test` = 24 chars).

---

## 6. Alembic Migration

```python
# build_stream/infra/db/alembic/versions/007_release2_image_groups_images.py

"""Release 2: Modify image_groups, create images, modify jobs and job_stages.

Revision ID: 007
Revises: 006
Create Date: 2026-04-07
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


revision = "007"
down_revision = "006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ─── 1. Modify image_groups table ───
    # Drop existing check constraint (outdated status values)
    op.drop_constraint("ck_image_groups_status", "image_groups", type_="check")

    # Change id column type from String(36) to String(128)
    op.alter_column(
        "image_groups", "id",
        existing_type=sa.String(36),
        type_=sa.String(128),
        existing_nullable=False,
    )

    # Remove image_key column (redundant with id)
    op.drop_index("idx_image_groups_image_key", table_name="image_groups")
    op.drop_column("image_groups", "image_key")

    # Add UNIQUE constraint on job_id (1:1 mapping)
    op.drop_index("idx_image_groups_job_id", table_name="image_groups")
    op.create_index(
        "idx_image_groups_job_id", "image_groups", ["job_id"], unique=True
    )

    # Add updated check constraint with correct status values
    op.create_check_constraint(
        "ck_image_groups_status",
        "image_groups",
        "status IN ('BUILT', 'DEPLOYING', 'DEPLOYED', 'RESTARTING', "
        "'RESTARTED', 'VALIDATING', 'PASSED', 'FAILED', 'CLEANED')",
    )

    # ─── 2. Create images table ───
    op.create_table(
        "images",
        sa.Column("id", sa.String(36), primary_key=True, nullable=False),
        sa.Column(
            "image_group_id",
            sa.String(128),
            sa.ForeignKey("image_groups.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("role", sa.String(128), nullable=False),
        sa.Column("image_name", sa.String(256), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("idx_images_image_group_id", "images", ["image_group_id"])
    op.create_index(
        "uq_images_image_group_id_role",
        "images",
        ["image_group_id", "role"],
        unique=True,
    )

    # ─── 3. Modify jobs table — add pipeline_phase ───
    op.add_column(
        "jobs",
        sa.Column("pipeline_phase", sa.String(10), nullable=True),
    )

    # ─── 4. Modify job_stages table — add result_detail JSONB ───
    op.add_column(
        "job_stages",
        sa.Column("result_detail", JSONB, nullable=True),
    )


def downgrade() -> None:
    # Remove result_detail from job_stages
    op.drop_column("job_stages", "result_detail")

    # Remove pipeline_phase from jobs
    op.drop_column("jobs", "pipeline_phase")

    # Drop images table
    op.drop_index("uq_images_image_group_id_role", table_name="images")
    op.drop_index("idx_images_image_group_id", table_name="images")
    op.drop_table("images")

    # Revert image_groups changes
    op.drop_constraint("ck_image_groups_status", "image_groups", type_="check")
    op.drop_index("idx_image_groups_job_id", table_name="image_groups")
    op.create_index("idx_image_groups_job_id", "image_groups", ["job_id"])
    op.add_column(
        "image_groups",
        sa.Column("image_key", sa.String(256), nullable=False, server_default=""),
    )
    op.create_index(
        "idx_image_groups_image_key", "image_groups", ["image_key"]
    )
    op.alter_column(
        "image_groups", "id",
        existing_type=sa.String(128),
        type_=sa.String(36),
        existing_nullable=False,
    )
    op.create_check_constraint(
        "ck_image_groups_status",
        "image_groups",
        "status IN ('BUILT', 'DEPLOYING', 'DEPLOYED', 'BOOTING', "
        "'BOOTED', 'VALIDATING', 'PASSED', 'FAILED')",
    )
```

---

## 7. Domain Layer Additions

### 7.1 File Layout

```
build_stream/core/image_group/          # NEW domain module
├── __init__.py
├── entities.py                          # ImageGroup, Image domain entities
├── value_objects.py                     # ImageGroupId, ImageGroupStatus, PipelinePhase
├── repositories.py                      # ImageGroupRepository interface (abstract)
├── exceptions.py                        # Domain exceptions
└── state_machine.py                     # Guard functions, allowed transitions
```

### 7.2 Value Objects

```python
# build_stream/core/image_group/value_objects.py

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


@dataclass(frozen=True)
class ImageGroupId:
    """ImageGroup identifier from catalog.

    Unlike JobId (UUID), this is a human-readable string from the catalog
    payload (e.g., 'omnia-cluster-v1.2').

    Attributes:
        value: ImageGroup identifier string (1-128 characters).
    """

    value: str

    MIN_LENGTH: ClassVar[int] = 1
    MAX_LENGTH: ClassVar[int] = 128

    def __post_init__(self) -> None:
        """Validate identifier format and length."""
        if not self.value or not self.value.strip():
            raise ValueError("ImageGroupId cannot be empty")
        if len(self.value) > self.MAX_LENGTH:
            raise ValueError(
                f"ImageGroupId length cannot exceed {self.MAX_LENGTH} "
                f"characters, got {len(self.value)}"
            )

    def __str__(self) -> str:
        return self.value


class ImageGroupStatus(str, Enum):
    """ImageGroup lifecycle states — see Section 5.1."""
    BUILT = "BUILT"
    DEPLOYING = "DEPLOYING"
    DEPLOYED = "DEPLOYED"
    RESTARTING = "RESTARTING"
    RESTARTED = "RESTARTED"
    VALIDATING = "VALIDATING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    CLEANED = "CLEANED"

    def is_terminal(self) -> bool:
        return self in {
            ImageGroupStatus.PASSED,
            ImageGroupStatus.FAILED,
            ImageGroupStatus.CLEANED,
        }


class PipelinePhase(str, Enum):
    """Pipeline execution context — see Section 5.2."""
    BUILD = "BUILD"
    DEPLOY = "DEPLOY"
```

### 7.3 Domain Entity — ImageGroup

```python
# build_stream/core/image_group/entities.py

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from build_stream.core.image_group.value_objects import (
    ImageGroupId,
    ImageGroupStatus,
)
from build_stream.core.jobs.value_objects import JobId


@dataclass
class ImageGroup:
    """ImageGroup domain entity.

    Tracks the lifecycle of a built image group from catalog parsing
    through deploy, restart, validate, and cleanup.

    The 1:1 relationship with Job is enforced at the DB level via
    UNIQUE constraint on job_id.
    """

    id: ImageGroupId               # Catalog ImageGroupID
    job_id: JobId                  # Associated job (1:1)
    status: ImageGroupStatus       # Current lifecycle status
    images: List["Image"] = field(default_factory=list)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def transition_status(self, new_status: ImageGroupStatus) -> None:
        """Transition to a new status and update timestamp."""
        self.status = new_status
        self.updated_at = datetime.now(timezone.utc)


@dataclass(frozen=True)
class Image:
    """Constituent image within an ImageGroup.

    Each image is identified by its functional role (e.g., slurm_node)
    and the generated image file name (e.g., slurm_node.img).
    """

    id: str                        # UUID
    image_group_id: str            # FK to ImageGroup
    role: str                      # Functional role name
    image_name: str                # Generated image file name
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
```

### 7.4 Domain Entity — Image

See `Image` dataclass in Section 7.3 above (co-located with `ImageGroup` in the same file).

### 7.5 Repository Interfaces

```python
# build_stream/core/image_group/repositories.py

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from build_stream.core.image_group.entities import ImageGroup, Image
from build_stream.core.image_group.value_objects import (
    ImageGroupId,
    ImageGroupStatus,
)
from build_stream.core.jobs.value_objects import JobId


class ImageGroupRepository(ABC):
    """Abstract repository for ImageGroup persistence.

    Implementations: SqlImageGroupRepository (prod), InMemoryImageGroupRepository (dev).
    """

    @abstractmethod
    def save(self, image_group: ImageGroup) -> None:
        """Persist a new ImageGroup record."""
        ...

    @abstractmethod
    def find_by_id(self, image_group_id: ImageGroupId) -> Optional[ImageGroup]:
        """Find ImageGroup by its catalog ID."""
        ...

    @abstractmethod
    def find_by_job_id(self, job_id: JobId) -> Optional[ImageGroup]:
        """Find ImageGroup by associated Job ID (1:1 mapping)."""
        ...

    @abstractmethod
    def find_by_job_id_for_update(self, job_id: JobId) -> Optional[ImageGroup]:
        """Find ImageGroup with row-level lock (SELECT FOR UPDATE).

        Used by deploy/restart/validate stages to prevent concurrent
        status transitions.
        """
        ...

    @abstractmethod
    def update_status(
        self, image_group_id: ImageGroupId, new_status: ImageGroupStatus
    ) -> None:
        """Update ImageGroup status and updated_at timestamp."""
        ...

    @abstractmethod
    def list_by_status(
        self,
        status: ImageGroupStatus,
        limit: int,
        offset: int,
    ) -> Tuple[List[ImageGroup], int]:
        """List ImageGroups by status with pagination.

        Returns: (image_groups_with_images, total_count)
        """
        ...

    @abstractmethod
    def exists(self, image_group_id: ImageGroupId) -> bool:
        """Check if an ImageGroup with the given ID exists."""
        ...


class ImageRepository(ABC):
    """Abstract repository for Image persistence."""

    @abstractmethod
    def save_batch(self, images: List[Image]) -> None:
        """Persist multiple Image records in a single operation."""
        ...

    @abstractmethod
    def find_by_image_group_id(
        self, image_group_id: ImageGroupId
    ) -> List[Image]:
        """Find all Images belonging to an ImageGroup."""
        ...
```

### 7.6 Domain Exceptions

```python
# build_stream/core/image_group/exceptions.py

class DuplicateImageGroupError(Exception):
    """Raised when an ImageGroup with the same ID already exists.

    Maps to HTTP 409 Conflict.
    """

    def __init__(self, image_group_id: str):
        self.image_group_id = image_group_id
        super().__init__(
            f"Image Group '{image_group_id}' already exists. "
            f"Each catalog can only be built once."
        )


class ImageGroupNotFoundError(Exception):
    """Raised when no ImageGroup is associated with a Job.

    Maps to HTTP 404 Not Found.
    """

    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(
            f"No Image Group associated with Job '{job_id}'"
        )


class ImageGroupMismatchError(Exception):
    """Raised when supplied image_group_id doesn't match Job's ImageGroup.

    Maps to HTTP 409 Conflict.
    """

    def __init__(self, supplied: str, expected: str):
        self.supplied = supplied
        self.expected = expected
        super().__init__(
            f"Supplied image_group_id '{supplied}' does not match "
            f"expected '{expected}'"
        )


class InvalidStateTransitionError(Exception):
    """Raised when ImageGroup is not in the required status for an operation.

    Maps to HTTP 412 Precondition Failed.
    """

    def __init__(self, current: str, required: set):
        self.current = current
        self.required = required
        super().__init__(
            f"ImageGroup status is '{current}', "
            f"required: {sorted(required)}"
        )
```

### 7.7 State Machine — Guard Functions

```python
# build_stream/core/image_group/state_machine.py

from build_stream.core.image_group.value_objects import ImageGroupStatus
from build_stream.core.image_group.exceptions import (
    ImageGroupNotFoundError,
    ImageGroupMismatchError,
    InvalidStateTransitionError,
)


# Allowed status transitions per stage
ALLOWED_TRANSITIONS = {
    "deploy": {ImageGroupStatus.BUILT},
    "restart": {ImageGroupStatus.DEPLOYED},
    "validate": {ImageGroupStatus.RESTARTED},
    "cleanup": {
        ImageGroupStatus.BUILT,
        ImageGroupStatus.PASSED,
        ImageGroupStatus.FAILED,
    },
}

# Status flow per stage (on_start, on_success, on_failure)
STATUS_FLOW = {
    "deploy": (
        ImageGroupStatus.DEPLOYING,
        ImageGroupStatus.DEPLOYED,
        ImageGroupStatus.FAILED,
    ),
    "restart": (
        ImageGroupStatus.RESTARTING,
        ImageGroupStatus.RESTARTED,
        ImageGroupStatus.FAILED,
    ),
    "validate": (
        ImageGroupStatus.VALIDATING,
        ImageGroupStatus.PASSED,
        ImageGroupStatus.FAILED,
    ),
}


def guard_check(
    image_group,
    stage_name: str,
    requested_image_group_id: str = None,
) -> None:
    """Validate preconditions for a stage execution.

    Args:
        image_group: The ImageGroup entity (or None if not found).
        stage_name: The stage being executed (deploy, restart, validate).
        requested_image_group_id: For deploy stage only — must match.

    Raises:
        ImageGroupNotFoundError: No ImageGroup for this Job (404).
        ImageGroupMismatchError: ID mismatch on deploy (409).
        InvalidStateTransitionError: Wrong status (412).
    """
    if image_group is None:
        raise ImageGroupNotFoundError("unknown")

    # Deploy stage: verify ID match (1:1 mapping)
    if requested_image_group_id is not None:
        if str(image_group.id) != requested_image_group_id:
            raise ImageGroupMismatchError(
                supplied=requested_image_group_id,
                expected=str(image_group.id),
            )

    # Status precondition check
    required = ALLOWED_TRANSITIONS.get(stage_name, set())
    if image_group.status not in required:
        raise InvalidStateTransitionError(
            current=image_group.status.value,
            required={s.value for s in required},
        )
```

---

## 8. Infrastructure Layer — SQL Repository

```python
# build_stream/infra/db/repositories.py — additions to existing file

class SqlImageGroupRepository(ImageGroupRepository):
    """SQL implementation of ImageGroupRepository.

    Uses synchronous SQLAlchemy Session (per existing codebase convention).
    """

    def __init__(self, session: Session):
        self.session = session

    def save(self, image_group: ImageGroup) -> None:
        model = ImageGroupMapper.to_orm(image_group)
        self.session.add(model)
        self.session.flush()

    def find_by_id(self, image_group_id: ImageGroupId) -> Optional[ImageGroup]:
        model = self.session.get(ImageGroupModel, str(image_group_id))
        if model is None:
            return None
        return ImageGroupMapper.to_domain(model)

    def find_by_job_id(self, job_id: JobId) -> Optional[ImageGroup]:
        stmt = (
            select(ImageGroupModel)
            .where(ImageGroupModel.job_id == str(job_id))
            .options(selectinload(ImageGroupModel.images))
        )
        result = self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return ImageGroupMapper.to_domain(model)

    def find_by_job_id_for_update(self, job_id: JobId) -> Optional[ImageGroup]:
        """SELECT FOR UPDATE — holds row lock for transaction duration."""
        stmt = (
            select(ImageGroupModel)
            .where(ImageGroupModel.job_id == str(job_id))
            .with_for_update()
            .options(selectinload(ImageGroupModel.images))
        )
        result = self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return ImageGroupMapper.to_domain(model)

    def update_status(
        self, image_group_id: ImageGroupId, new_status: ImageGroupStatus
    ) -> None:
        model = self.session.get(ImageGroupModel, str(image_group_id))
        if model:
            model.status = new_status.value
            model.updated_at = datetime.now(timezone.utc)
            self.session.flush()

    def list_by_status(
        self, status: ImageGroupStatus, limit: int, offset: int
    ) -> Tuple[List[ImageGroup], int]:
        # Count query
        count_stmt = (
            select(func.count())
            .select_from(ImageGroupModel)
            .where(ImageGroupModel.status == status.value)
        )
        total_count = self.session.execute(count_stmt).scalar()

        # Data query with eager-loaded images
        data_stmt = (
            select(ImageGroupModel)
            .where(ImageGroupModel.status == status.value)
            .options(selectinload(ImageGroupModel.images))
            .order_by(ImageGroupModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = self.session.execute(data_stmt)
        models = result.scalars().unique().all()

        return [ImageGroupMapper.to_domain(m) for m in models], total_count

    def exists(self, image_group_id: ImageGroupId) -> bool:
        stmt = select(
            select(ImageGroupModel.id)
            .where(ImageGroupModel.id == str(image_group_id))
            .exists()
        )
        return self.session.execute(stmt).scalar()


class SqlImageRepository(ImageRepository):
    """SQL implementation of ImageRepository."""

    def __init__(self, session: Session):
        self.session = session

    def save_batch(self, images: List[Image]) -> None:
        for img in images:
            model = ImageMapper.to_orm(img)
            self.session.add(model)
        self.session.flush()

    def find_by_image_group_id(
        self, image_group_id: ImageGroupId
    ) -> List[Image]:
        stmt = (
            select(ImageModel)
            .where(ImageModel.image_group_id == str(image_group_id))
        )
        result = self.session.execute(stmt)
        return [ImageMapper.to_domain(m) for m in result.scalars().all()]
```

---

## 9. Infrastructure Layer — In-Memory Repository

```python
# build_stream/infra/repositories/in_memory.py — additions

class InMemoryImageGroupRepository(ImageGroupRepository):
    """In-memory implementation for development/testing."""

    def __init__(self):
        self._store: Dict[str, ImageGroup] = {}

    def save(self, image_group: ImageGroup) -> None:
        self._store[str(image_group.id)] = image_group

    def find_by_id(self, image_group_id: ImageGroupId) -> Optional[ImageGroup]:
        return self._store.get(str(image_group_id))

    def find_by_job_id(self, job_id: JobId) -> Optional[ImageGroup]:
        for ig in self._store.values():
            if str(ig.job_id) == str(job_id):
                return ig
        return None

    def find_by_job_id_for_update(self, job_id: JobId) -> Optional[ImageGroup]:
        return self.find_by_job_id(job_id)  # No locking in memory

    def update_status(
        self, image_group_id: ImageGroupId, new_status: ImageGroupStatus
    ) -> None:
        ig = self._store.get(str(image_group_id))
        if ig:
            ig.transition_status(new_status)

    def list_by_status(
        self, status: ImageGroupStatus, limit: int, offset: int
    ) -> Tuple[List[ImageGroup], int]:
        filtered = [
            ig for ig in self._store.values()
            if ig.status == status
        ]
        filtered.sort(key=lambda x: x.created_at, reverse=True)
        total = len(filtered)
        page = filtered[offset:offset + limit]
        return page, total

    def exists(self, image_group_id: ImageGroupId) -> bool:
        return str(image_group_id) in self._store


class InMemoryImageRepository(ImageRepository):
    """In-memory implementation for development/testing."""

    def __init__(self):
        self._store: List[Image] = []

    def save_batch(self, images: List[Image]) -> None:
        self._store.extend(images)

    def find_by_image_group_id(
        self, image_group_id: ImageGroupId
    ) -> List[Image]:
        return [
            img for img in self._store
            if img.image_group_id == str(image_group_id)
        ]
```

---

## 10. Infrastructure Layer — ORM Mapper

```python
# build_stream/infra/db/mappers.py — additions

class ImageGroupMapper:
    """Maps between ImageGroup domain entity and ImageGroupModel ORM."""

    @staticmethod
    def to_orm(entity: ImageGroup) -> ImageGroupModel:
        return ImageGroupModel(
            id=str(entity.id),
            job_id=str(entity.job_id),
            status=entity.status.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_domain(model: ImageGroupModel) -> ImageGroup:
        images = [ImageMapper.to_domain(img) for img in model.images]
        return ImageGroup(
            id=ImageGroupId(model.id),
            job_id=JobId(model.job_id),
            status=ImageGroupStatus(model.status),
            images=images,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )


class ImageMapper:
    """Maps between Image domain entity and ImageModel ORM."""

    @staticmethod
    def to_orm(entity: Image) -> ImageModel:
        return ImageModel(
            id=entity.id,
            image_group_id=entity.image_group_id,
            role=entity.role,
            image_name=entity.image_name,
            created_at=entity.created_at,
        )

    @staticmethod
    def to_domain(model: ImageModel) -> Image:
        return Image(
            id=model.id,
            image_group_id=model.image_group_id,
            role=model.role,
            image_name=model.image_name,
            created_at=model.created_at,
        )
```

---

## 11. DI Container Registration

```python
# build_stream/container.py — additions

# In DevContainer:
image_group_repository = providers.Singleton(InMemoryImageGroupRepository)
image_repository = providers.Singleton(InMemoryImageRepository)

# In ProdContainer: (not directly registered — created via dependency functions)
# SqlImageGroupRepository and SqlImageRepository are instantiated in
# api/*/dependencies.py with the shared DB session, following the existing
# pattern used by SqlJobRepository and SqlStageRepository.
```

**Dependency function pattern** (in `api/dependencies.py`):

```python
# build_stream/api/dependencies.py — additions

def _create_sql_image_group_repo(session: Session):
    from infra.db.repositories import SqlImageGroupRepository
    return SqlImageGroupRepository(session=session)

def _create_sql_image_repo(session: Session):
    from infra.db.repositories import SqlImageRepository
    return SqlImageRepository(session=session)
```

---

## 12. Traceability

| Implementation Item | Spec Section | HLD Section | Task |
|---------------------|-------------|-------------|------|
| ImageGroupModel ORM | [4.1](#41-imagegroupmodel-modified) | 4.1.3.3 | S1-3 |
| ImageModel ORM | [4.2](#42-imagemodel-new) | 4.1.3.3 | S1-3 |
| JobModel.pipeline_phase | [4.3](#43-jobmodel-modified) | 4.1.3.3 | S1-3 |
| StageModel.result_detail | [4.4](#44-stagemodel-modified) | 4.1.3.3 | S1-3 |
| ImageGroupStatus enum | [5.1](#51-imagegroupstatus) | 4.1.3.3 | S1-3 |
| PipelinePhase enum | [5.2](#52-pipelinephase) | 4.1.3.3 | S1-3 |
| StageType extensions | [5.3](#53-stagetype-extensions) | 4.1.3.3 | S1-3 |
| Alembic migration | [6](#6-alembic-migration) | 4.1.3.6 (U1) | S1-3 |
| Domain entities | [7.3-7.4](#73-domain-entity--imagegroup) | 4.1.3.3 | S1-3 |
| Repository interfaces | [7.5](#75-repository-interfaces) | — | S1-3 |
| Guard functions | [7.7](#77-state-machine--guard-functions) | 3.3.1 | S1-3 |
| SQL repositories | [8](#8-infrastructure-layer--sql-repository) | — | S1-3 |
| In-memory repositories | [9](#9-infrastructure-layer--in-memory-repository) | — | S1-3 |
| ORM mappers | [10](#10-infrastructure-layer--orm-mapper) | — | S1-3 |
| DI container | [11](#11-di-container-registration) | — | S1-3 |

---

*END OF DOCUMENT*

*Document Owner: Dell Omnia Team*
*Team: Dell Omnia — BuildStream*
*Classification: Dell Confidential - Internal Use Only*

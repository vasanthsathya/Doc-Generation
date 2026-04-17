# Content Plan: Minimal OS Functional Groups Documentation Updates

**Generated:** 2026-04-16  
**Source Documents Analyzed:** Behavior Specification (BSpec), Functional Specification (FSPEC), Component Specification (CSPEC), Manual Inputs  
**Phase:** COLLECT - Information gathering and planning  
**Target Implementation:** BUILD phase  
**Approach:** Update existing documentation rather than creating new topics (per updated skill guidance)

---

## Analysis Summary

**Existing Documentation Found:**
- Functional groups documentation exists in `OmniaInstallGuide/RHEL_new/composable_roles.rst`
- Supporting data in `Tables/omnia_roles.csv` 
- Comprehensive functional groups section with current groups listed

**Gap Identified:**
- New Minimal OS functional groups (`os_x86_64`, `os_aarch64`) are not documented in existing functional groups section
- Current documentation lists existing functional groups but missing the new Minimal OS variants
- Software recommendations table needs updates for Minimal OS groups

**Decision:** Update existing functional groups documentation to include Minimal OS groups rather than creating separate new topics.

---

### Update Functional Groups Documentation

| Field | Details |
|-------|---------|
| **Topic Type** | Update Existing Topic |
| **Status** | Update Existing Topic |
| **Target Audience** | Infrastructure/HPC Administrator |
| **Source Traceability** | BSpec §6.1, FSPEC §3, CSPEC §4.1-4.2 |
| **RST File** | `/docs/source/OmniaInstallGuide/RHEL_new/composable_roles.rst` |
| **Content Type** | Update to existing installation guide |

**Customer Workflow Context:**
Administrators using the existing functional groups documentation need to see the new Minimal OS groups alongside existing groups to make informed decisions about node assignment. This is part of the standard node configuration workflow.

**Content Requirements:**
- Add Minimal OS functional groups to the existing functional groups section
- Update the software recommendations table with Minimal OS package mappings
- Add explanatory notes about Minimal OS groups and their use cases
- Update sample mapping file examples to include Minimal OS entries

**Configuration Artifacts:**
- Functional group names: `os_x86_64`, `os_aarch64`
- Layer classification: compute layer
- Recommended software: `default_packages.json`, `ldms.json`
- Optional software: `additional_packages.json`

**Cross-References:**
- No new cross-references needed (maintaining existing structure)

**Build Agent Instructions:**
- Update the existing `omnia_roles.csv` file to add Minimal OS functional groups
- Update the "Recommended Software by Functional Groups" table in `composable_roles.rst`
- Add Minimal OS entries to the sample mapping file examples
- Add explanatory note about Minimal OS groups use cases
- Do not create new files - only update existing ones
- Flag for SME validation: functional group accuracy and software mappings

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [x] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if additional demo transcripts needed
- [ ] Flag if additional unit tests needed
- [ ] Flag if SME interviews required
- [ ] Flag if user feedback collection needed
- [ ] Flag if HLD clarification required
- [ ] Flag if engineering notes clarification required

---

### Update Supporting CSV Data

| Field | Details |
|-------|---------|
| **Topic Type** | Update Existing Data File |
| **Status** | Update Existing Topic |
| **Target Audience** | Infrastructure/HPC Administrator |
| **Source Traceability** | BSpec §6.1, FSPEC §3, Manual Inputs |
| **RST File** | `/docs/source/Tables/omnia_roles.csv` |
| **Content Type** | Update to existing data file |

**Customer Workflow Context:**
The CSV file provides the data source for the functional groups table in the documentation. It must include Minimal OS groups to appear in the generated documentation.

**Content Requirements:**
- Add two new rows for `os_x86_64` and `os_aarch64` functional groups
- Include appropriate layer classification (Compute)
- Include detailed descriptions explaining Minimal OS purpose and use cases
- Follow existing CSV format and structure

**Configuration Artifacts:**
- CSV rows for Minimal OS functional groups with proper formatting
- Layer classification: Compute
- Detailed descriptions for downstream platform use cases

**Cross-References:**
- No cross-references needed (data file)

**Build Agent Instructions:**
- Add two new rows to the existing CSV file following the current format
- Use the exact functional group names: `os_x86_64`, `os_aarch64`
- Include comprehensive descriptions explaining the Minimal OS concept
- Maintain CSV formatting consistency with existing entries
- Flag for SME validation: functional group descriptions accuracy

**Gap Analysis:**
- [x] User workflows and use cases identified
- [x] Real-world examples and scenarios available
- [ ] Common mistakes and gotchas documented
- [ ] Performance characteristics covered
- [x] Integration examples provided
- [ ] Troubleshooting scenarios included
- [x] Prerequisites and dependencies listed
- [x] Security and compliance considerations addressed

**Additional Source Requirements:**
- [ ] Flag if additional demo transcripts needed
- [ ] Flag if additional unit tests needed
- [ ] Flag if SME interviews required
- [ ] Flag if user feedback collection needed
- [ ] Flag if HLD clarification required
- [ ] Flag if engineering notes clarification required

---

## Implementation Priority

**High Priority:**
1. Update `omnia_roles.csv` - Add Minimal OS functional groups data
2. Update `composable_roles.rst` - Add Minimal OS groups to software recommendations table

**Medium Priority:**
3. Update sample mapping file examples to include Minimal OS entries
4. Add explanatory notes about Minimal OS use cases

---

## Build Agent Coordination Notes

**Update-Only Approach:**
- No new files to be created
- All changes are updates to existing documentation
- Maintain current documentation structure and formatting
- Preserve existing cross-references and navigation

**Consistency Requirements:**
- Use exact functional group names from source documents
- Maintain existing table formatting and structure
- Follow current note and warning conventions
- Keep consistent tone and voice with existing content

**SME Validation Requirements:**
- Functional group descriptions and classifications
- Software package recommendations for Minimal OS groups
- Sample mapping file format and examples
- Explanatory notes accuracy and completeness

---

## Phase Transition Readiness

This COLLECT phase plan provides sufficient detail for the BUILD phase to implement all documentation updates. The Build Agent should be able to:

1. Update the existing CSV file with new Minimal OS functional groups
2. Update the existing RST file with new software recommendations
3. Add Minimal OS examples to existing mapping file samples
4. Maintain consistency with existing documentation structure
5. Apply proper SME validation flags

**No additional source gathering required** - the analyzed source documents provide comprehensive information for updating the existing functional groups documentation with Minimal OS content.

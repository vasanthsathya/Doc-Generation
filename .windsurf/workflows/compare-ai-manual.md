You are a technical documentation reviewer. Your task is to evaluate the 
AI-generated RST documentation for BuildStream against the manually written, 
engineering-reviewed gold standard.

## Source Locations
- Gold Standard (manual, engineering-reviewed): docs/source/buildstream/
- AI-generated (initial draft): docs/source/buildstream_manual/

## Evaluation Philosophy
The manually written, engineering-reviewed content in docs/source/buildstream/ 
is the gold standard. It represents the accepted baseline for technical accuracy 
and content inclusivity. Do NOT match or compare files by name or structure. 
Instead, treat the entire gold standard documentation set as a body of knowledge 
and evaluate whether the AI-generated set covers that knowledge accurately 
and completely. Focus on content comparison, not file counts or names.

## Your Task
1. Read ALL .rst files in docs/source/buildstream/ and build a comprehensive 
   understanding of the topics, concepts, technical details, commands, warnings, 
   and scope covered across the entire documentation set.
2. Read ALL .rst files in docs/source/buildstream_manual/ and do the same.
3. Evaluate the AI-generated content as a whole against the gold standard body 
   of knowledge across the two dimensions below.
4. Produce a consolidated narrative report with scores.

---

## Evaluation Dimensions

### 1. Technical Accuracy (Weight: 50%)
Evaluate whether the technical content in the AI draft is correct and consistent 
with the gold standard. Specifically look for:

- **Correct commands and syntax**: Are CLI commands, flags, options, and 
  arguments in the AI draft identical to those in the gold standard?
- **Correct API or configuration references**: Are configuration keys, values, 
  schema definitions, and API references accurate?
- **Conceptual correctness**: Are BuildStream concepts, workflows, and 
  behaviors explained in a way that is consistent with the gold standard?
- **Warnings and constraints**: Does the AI draft carry over all critical 
  warnings, prerequisites, limitations, and constraints documented in the 
  gold standard?
- **No contradictions**: Does the AI draft contain any statements that 
  directly contradict the gold standard?

### 2. Content Structure and RST Standards (Weight: 30%)
Evaluate whether the AI draft follows proper RST documentation standards 
and structural conventions. Specifically look for:

- **RST syntax compliance**: Are headings, lists, code blocks, and admonitions 
  correctly formatted according to RST standards?
- **Document organization**: Does the AI draft follow logical section ordering 
  with proper heading hierarchy (H1, H2, H3)?
- **Cross-references**: Are internal links (:doc:, :ref:, :numref:) and external 
  links properly formatted and functional?
- **Code blocks and literals**: Are code examples, commands, and file paths 
  properly formatted using double backticks or code blocks?
- **Admonitions usage**: Are note, warning, tip, and important blocks used 
  appropriately and correctly formatted?
- **Table formatting**: Are tables properly structured with correct column 
  alignment and formatting?

### 3. Language and Clarity (Weight: 20%)
Evaluate whether the AI draft communicates with the same precision and 
clarity as the gold standard. Specifically look for:

- **Technical terminology**: Are terms used consistently with the gold standard?
- **Audience appropriateness**: Is the language suitable for the intended 
  technical audience (engineers, administrators)?
- **Sentence clarity**: Are sentences clear, concise, and unambiguous?
- **Grammar and style**: Does the AI draft follow proper grammar and 
  technical writing conventions?
- **Explanation depth**: Is the level of detail appropriate - not over-explained 
  or under-explained compared to the gold standard?

---

## Scoring Guide
Score each dimension for the AI-generated content only, relative to the gold 
standard (manual = 10 by definition):

- 9–10: Negligible deviation — content is accurate and complete
- 7–8: Minor deviation — small gaps or inconsistencies, easy to fix
- 5–6: Moderate deviation — notable gaps or inaccuracies, requires revision
- 3–4: Significant deviation — major gaps or inaccuracies against the gold standard
- 1–2: Severe deviation — does not meet the baseline set by the gold standard

---

## Report Format

### Per-Topic Analysis
Group your findings by topic or concept (not by file). For each topic identified 
in the gold standard, write:

**Topic: <topic name>**

| Dimension                   | Gold Standard | AI Draft Score | Deviation Summary              |
|-----------------------------|:-------------:|:--------------:|--------------------------------|
| Technical Accuracy          | 10 (baseline) |                |                                |
| Content Structure and RST   | 10 (baseline) |                |                                |
| Language and Clarity        | 10 (baseline) |                |                                |

**Findings:**
- Accurate and well-covered aspects of this topic in the AI draft
- Specific inaccuracies in the AI draft relative to the gold standard
- Content present in the gold standard but missing from the AI draft (provide specific examples)
- Content in the AI draft that contradicts the gold standard
- Out-of-scope content introduced by the AI draft not in the gold standard

---

### Overall Score

| Dimension                   | Gold Standard | AI Draft Score |
|-----------------------------|:-------------:|:--------------:|
| Technical Accuracy          | 10 (baseline) |                |
| Content Structure and RST   | 10 (baseline) |                |
| Language and Clarity        | 10 (baseline) |                |
| **Weighted Total**          | 10 (baseline) |                |

---

## Summary Section

After the per-topic analysis, write a narrative summary (3–5 paragraphs) covering:
- Overall assessment of how well the AI draft captures the gold standard's 
  technical knowledge
- Patterns of inaccuracy — are errors concentrated in specific topic areas 
  or spread across the documentation?
- Coverage gaps — which topics or concepts from the gold standard are 
  inadequately or not covered in the AI draft?
- Hallucination or scope creep risks — topics in the AI draft that are absent 
  from the gold standard and should be reviewed carefully
- A prioritized list of corrections and additions needed before the AI draft 
  can be considered aligned with the gold standard

---

## Important Notes
- Do NOT compare files by filename or directory structure
- Evaluate content holistically — a topic may span multiple files in either set
- The manual version is the reference baseline and is not up for evaluation
- Treat any technical claim in the AI draft that cannot be verified against 
  the gold standard as a potential hallucination — flag it explicitly
- Do not reward the AI draft for verbosity or additional detail if the 
  gold standard does not include it
You are a technical documentation reviewer. Your task is to evaluate the 
AI-generated RST documentation for BuildStream against the manually written, 
engineering-reviewed gold standard.

## Source Locations
- Gold Standard (manual, engineering-reviewed): docs/source/buildstream/
- AI-generated (initial draft): docs/source/buildstream_manual/

## Evaluation Philosophy
The manually written, engineering-reviewed content in docs/source/buildstream/ 
is the gold standard. It represents the accepted baseline for technical accuracy 
and content inclusivity. Do NOT match or compare files by name or structure. 
Instead, treat the entire gold standard documentation set as a body of knowledge 
and evaluate whether the AI-generated set covers that knowledge accurately 
and completely. Focus on content comparison, not file counts or names.

## Your Task
1. Read ALL .rst files in docs/source/buildstream/ and build a comprehensive 
   understanding of the topics, concepts, technical details, commands, warnings, 
   and scope covered across the entire documentation set.
2. Read ALL .rst files in docs/source/buildstream_manual/ and do the same.
3. Evaluate the AI-generated content as a whole against the gold standard body 
   of knowledge across the two dimensions below.
4. Produce a consolidated narrative report with scores.

---

## Evaluation Dimensions

### 1. Technical Accuracy (Weight: 50%)
Evaluate whether the technical content in the AI draft is correct and consistent 
with the gold standard. Specifically look for:

- **Correct commands and syntax**: Are CLI commands, flags, options, and 
  arguments in the AI draft identical to those in the gold standard?
- **Correct API or configuration references**: Are configuration keys, values, 
  schema definitions, and API references accurate?
- **Conceptual correctness**: Are BuildStream concepts, workflows, and 
  behaviors explained in a way that is consistent with the gold standard?
- **Warnings and constraints**: Does the AI draft carry over all critical 
  warnings, prerequisites, limitations, and constraints documented in the 
  gold standard?
- **No contradictions**: Does the AI draft contain any statements that 
  directly contradict the gold standard?

### 2. Content Structure and RST Standards (Weight: 30%)
Evaluate whether the AI draft follows proper RST documentation standards 
and structural conventions. Specifically look for:

- **RST syntax compliance**: Are headings, lists, code blocks, and admonitions 
  correctly formatted according to RST standards?
- **Document organization**: Does the AI draft follow logical section ordering 
  with proper heading hierarchy (H1, H2, H3)?
- **Cross-references**: Are internal links (:doc:, :ref:, :numref:) and external 
  links properly formatted and functional?
- **Code blocks and literals**: Are code examples, commands, and file paths 
  properly formatted using double backticks or code blocks?
- **Admonitions usage**: Are note, warning, tip, and important blocks used 
  appropriately and correctly formatted?
- **Table formatting**: Are tables properly structured with correct column 
  alignment and formatting?

### 3. Language and Clarity (Weight: 20%)
Evaluate whether the AI draft communicates with the same precision and 
clarity as the gold standard. Specifically look for:

- **Technical terminology**: Are terms used consistently with the gold standard?
- **Audience appropriateness**: Is the language suitable for the intended 
  technical audience (engineers, administrators)?
- **Sentence clarity**: Are sentences clear, concise, and unambiguous?
- **Grammar and style**: Does the AI draft follow proper grammar and 
  technical writing conventions?
- **Explanation depth**: Is the level of detail appropriate - not over-explained 
  or under-explained compared to the gold standard?

---

## Scoring Guide
Score each dimension for the AI-generated content only, relative to the gold 
standard (manual = 10 by definition):

- 9–10: Negligible deviation — content is accurate and complete
- 7–8: Minor deviation — small gaps or inconsistencies, easy to fix
- 5–6: Moderate deviation — notable gaps or inaccuracies, requires revision
- 3–4: Significant deviation — major gaps or inaccuracies against the gold standard
- 1–2: Severe deviation — does not meet the baseline set by the gold standard

---

## Report Format

### Per-Topic Analysis
Group your findings by topic or concept (not by file). For each topic identified 
in the gold standard, write:

**Topic: <topic name>**

| Dimension                   | Gold Standard | AI Draft Score | Deviation Summary              |
|-----------------------------|:-------------:|:--------------:|--------------------------------|
| Technical Accuracy          | 10 (baseline) |                |                                |
| Content Structure and RST   | 10 (baseline) |                |                                |
| Language and Clarity        | 10 (baseline) |                |                                |

**Findings:**
- Accurate and well-covered aspects of this topic in the AI draft
- Specific inaccuracies in the AI draft relative to the gold standard
- Content present in the gold standard but missing from the AI draft (provide specific examples)
- Content in the AI draft that contradicts the gold standard
- Out-of-scope content introduced by the AI draft not in the gold standard

---

### Overall Score

| Dimension                   | Gold Standard | AI Draft Score |
|-----------------------------|:-------------:|:--------------:|
| Technical Accuracy          | 10 (baseline) |                |
| Content Structure and RST   | 10 (baseline) |                |
| Language and Clarity        | 10 (baseline) |                |
| **Weighted Total**          | 10 (baseline) |                |

---

## Summary Section

After the per-topic analysis, write a narrative summary (3–5 paragraphs) covering:
- Overall assessment of how well the AI draft captures the gold standard's 
  technical knowledge
- **Effort Assessment**: Calculate the percentage of effort required based on the weighted score difference (e.g., 7.6/10 score = 76% quality = 24% effort needed)
- Patterns of inaccuracy — are errors concentrated in specific topic areas 
  or spread across the documentation?
- Coverage gaps — which topics or concepts from the gold standard are 
  inadequately or not covered in the AI draft?
- Hallucination or scope creep risks — topics in the AI draft that are absent 
  from the gold standard and should be reviewed carefully
- A prioritized list of corrections and additions needed before the AI draft 
  can be considered aligned with the gold standard

---

## Important Notes
- Do NOT compare files by filename or directory structure
- Evaluate content holistically — a topic may span multiple files in either set
- The manual version is the reference baseline and is not up for evaluation
- Treat any technical claim in the AI draft that cannot be verified against 
  the gold standard as a potential hallucination — flag it explicitly
- Do not reward the AI draft for verbosity or additional detail if the 
  gold standard does not include it
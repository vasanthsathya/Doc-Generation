# Dell Technologies Unified Style Guide v1.0

***

## Table of Contents

- [Introduction](#introduction)
- [Voice and Tone](#voice-and-tone)
- [Grammar and Style](#grammar-and-style)
- [Punctuation](#punctuation)
- [Numbers and Measurement Units](#numbers-and-measurement-units)
- [Document Components](#document-components)
- [Writing About the UI](#writing-about-the-ui)
- [UI Components](#ui-components)
- [Minimalism](#minimalism)
- [Topic-Based Authoring](#topic-based-authoring)
- [Writing for Accessibility](#writing-for-accessibility)
- [Writing for Localization](#writing-for-localization)

***

## Introduction

The **Dell Technologies Unified Style Guide (USG)** is a set of style standards for content
creators who work across Dell and across the full range of Dell's product lines. Whether you
create technical content or you write or design for the UI, the USG is your style guide.

This guide replaces:

- Technical Writers Style Guide
- APEX Style Guide
- Content guidance contained within the Dell Digital Design System 2.0
- Content guidance contained within the Experience Design Group (EDG) ISG Design System 1.0

### Other Resources (Order of Precedence)

1. The Chicago Manual of Style
2. Microsoft Writing Style Guide
3. The IBM Style Guide
4. Merriam-Webster's Collegiate Dictionary

> **Note:** `[TBD]` indicates missing information and, in a few cases, a missing topic.

***

## Voice and Tone

### Conversational vs. Formal Tone

| Audience             | Tone          |
|----------------------|---------------|
| CSG Client customers | Conversational|
| ISG Enterprise customers | Formal    |
| APEX UI              | Conversational|

### Brand Voice Principles

Dell Technologies voice is defined by **four brand principles**:

1. **Collaborative** — Positive, action-oriented, open to change, intentional and sensitive
2. **Authentic** — Plain-spoken, inclusive, gender-neutral, honest, accessible
3. **Reliable** — Connects ideas to actions and results, backs claims with examples, writes for
current functionality
4. **Bold** — Supports and empowers people, responsive to feedback, anticipates user needs

### Tone Guidelines

The Dell Technologies tone is **friendly, calm, candid, conversational, neutral, and
respectful** in most cases. Tone adjusts by context:

| Message Type                          | Tonal Characteristics     |
|---------------------------------------|---------------------------|
| Task completion & form instructions   | Concise & conversational  |
| Notifications, getting started, billing | Neutral                 |
| Confirmations                         | Concise                   |
| Errors                                | Concise & serious         |
| Onboarding documentation              | Detailed & conversational |
| Support documentation                 | Detailed                  |
| Disclaimers                           | Detailed & serious        |

### Writing-Style Guidelines Summary

- Keep content **clear and easy to read** (also easy to listen to for screen readers)
- Keep sentences **≤ 25 words**
- Keep paragraphs **≤ 5 sentences**
- Use **active voice** (except to emphasize action over subject)
- Write in **present tense**
- Use **indicative and imperative moods**
- Make titles and headings **unique and informative**
- Begin action sentences with the **objective** (e.g., *To do X, do Y*)
- **Conversational writing:** Use contractions
- **Formal writing:** Do not use contractions

**Contractions examples:**

- ❌ Formal: We cannot process your request at this time.
- ✅ Casual: We can't process your request right now.
- ❌ Casual: We can't process your request right now.
- ✅ Formal: Your request cannot be processed.

**Additional principles:**

- Be **friendly, but not funny**
- Make content **scannable** and concise
- Use **personal language** (second person, imperative)
- Use **familiar and simple terms**
- Be **straightforward** and **reduce bias**
- Be **consistent** across similar messages

***

## Grammar and Style

### Abbreviations

- **Never abbreviate** Brand-approved Dell product names
- **Spell out** abbreviations on first use per topic/page/component; use abbreviated form after
- **Do not** spell out abbreviations that are common knowledge (e.g., XML, HTML)
- **Do not** use Latin abbreviations (e.g., use *for example* instead of *e.g.*)
- Add **lowercase** `s` for plural abbreviations — no apostrophe (e.g., `LANs`, not `LAN's`)
- **Do not** use abbreviations as verbs:
  - ❌ FTP a file
  - ✅ Transfer a file using FTP

### Active and Passive Voice

Prefer **active voice** — it is more straightforward, less wordy, and easier to translate.

| Active Voice                          | Passive Voice                            |
|---------------------------------------|------------------------------------------|
| Subject → Verb → Object               | Object → Verb → Subject                  |
| Identifies who does the action first  | Entity receiving action is named first   |
| More concise                          | Heavier cognitive load                   |

- ❌ Passive: Active voice is recommended.
- ✅ Active: Use the active voice.
- ❌ Passive: The operating system for the server must be selected.
- ✅ Active: Select the operating system for the server.

**Exception — use passive voice for Dell recommendations:**

- ❌ Dell recommends that you remove the hard drive before removing the fan.
- ✅ It is recommended that you remove the hard drive before removing the fan.

### Anthropomorphism

Avoid attributing human characteristics to inanimate objects.

- ❌ If the system sees a new device...
- ✅ If the system detects a new device...
- ❌ The hard drive remembers data...
- ✅ The hard drive stores data...

### Capitalization

| Component          | Case           | Examples                                         |
|--------------------|----------------|--------------------------------------------------|
| Document title     | Title case     | *SupportAssist for Business PCs User's Guide*    |
| UI/web page H1     | Title case     | *Identity Management*                            |
| Button labels      | Title case     | *Submit Order*                                   |
| Navigation menus   | Title case     | *Site Management*                                |
| Chapter titles     | Sentence case  | *Configuring alert and event settings*           |
| Topic titles       | Sentence case  | *Device credentials and credential profiles*     |
| Table/figure titles| Sentence case  | *Types of email notifications*                   |
| Body text, H2+     | Sentence case  | —                                                |

### Colloquialisms, Idioms, and Jargon

- ❌ My computer crashed.
- ✅ My computer stopped responding.
- ❌ Consult with your admin.
- ✅ Consult with your network administrator.

### Spelling

Use **American English** spelling:

| American   | British    |
|------------|------------|
| center     | centre     |
| color      | colour     |
| analyze    | analyse    |
| specialize | specialise |
| fulfill    | fulfil     |
| catalog    | catalogue  |

### Verb Tense

Use **simple present tense** wherever possible.

- ❌ If the network did not connect, run the troubleshooting wizard.
- ✅ If the network does not connect, run the troubleshooting wizard.

### Pronouns & Point of View

- Write directly to the audience using **second person** (you, imperative mood)
- **Avoid first person** (I, we) with exceptions for blogs and white papers
- **Never** use gendered third-person pronouns (he/she)

**UI-specific exceptions:**

- First person for user acknowledgement: *"I have read and agree to the Terms and Conditions."*
- Proper names: *My Account*, *My Dashboard*
- Second person for messages: *"Forgot your password?"*

### Sentences

- Keep sentences **short and to the point**
- State **purpose before action**:
  - ❌ See the VMware website for more information about ESXi.
  - ✅ For more information about ESXi, see the VMware website.

***

## Punctuation

### Quick Reference

| Symbol                  | Guideline                                                        |
|-------------------------|------------------------------------------------------------------|
| **Ampersand (&)**       | Do not use except in brand names                                 |
| **Angle brackets (<>)** | Do not use in text; OK for math notation and variables           |
| **Colons (:)**          | Introduce lists, separate title/subtitle, time, ratios           |
| **Commas (,)**          | Use serial (Oxford) comma; use after introductory words          |
| **Em dash (—)**         | Set off parenthetical expressions; no spaces                     |
| **En dash (–)**         | Number ranges in tables; minus sign                              |
| **Ellipses (…)**        | Avoid in documentation; OK for progress indicators               |
| **Exclamation marks (!)** | Do not use except in coding statements                         |
| **Hashtags (#)**        | Do not use as substitute for "number"                            |
| **Hyphens (-)**         | Compound modifiers; not after `-ly` adverbs                      |
| **Parentheses ()**      | Introduce acronyms; measurement equivalents                      |
| **Percent (%)**         | Use symbol with numerals, no space: `70%`                        |
| **Periods (.)**         | End all sentences; one space after                               |
| **Pipes (\|)**          | Space before and after                                           |
| **Question marks (?)**  | Use sparingly                                                    |
| **Quotation marks ("")**| Spoken words only; not for emphasis                              |
| **Semicolons (;)**      | Avoid; break into simpler sentences                              |
| **Slashes (/)**         | Do not use for alternatives; OK for common terms (read/write)    |

### Commas — Key Rules

- ✅ Serial comma: The ROC feature allows the user to delete, edit, and filter devices.
- ✅ Introductory: However, do not turn off the server while this process is in progress.
- ✅ Independent clauses: The software checks each component, and the wizard displays the results.
- ❌ Compound predicate: Enter your name in the field, and click Enter.
- ✅ Compound predicate: Enter your name in the field and click Enter.

### Hyphens — Key Rules

- ✅ read-only memory
- ✅ 8-port switch
- ✅ a highly unstable configuration (no hyphen after -ly adverb)
- ✅ non-Windows (hyphen before proper noun)
- ✅ preinstalled (no hyphen with common prefixes)
- ✅ re-create (hyphen to distinguish meaning)
- ❌ email → Do not hyphenate (email, ecommerce, website)

***

## Numbers and Measurement Units

### General Number Use

| Rule                               | Example                      |
|------------------------------------|------------------------------|
| Words for 0–9                      | *four hard drives*           |
| Numerals for 10+                   | *10 hard drives*             |
| Numerals for units of measure      | *2 ft*, *5 GB*               |
| Numerals for modifiers             | *8-port switch*              |
| Numerals for currency always       | *$8*                         |
| Spell out numbers starting a sentence | *Fifteen infrastructure nodes...* |
| Large numbers: numeral + word      | *1 million*, *100 million*   |
| Commas for 4+ digits               | *1,000*, *10,000*            |

### Currency

- ✅ $8
- ✅ $5.20
- ✅ $0.40
- ✅ $1,000
- ✅ USD 300
- ❌ $300 USD
- ❌ USD$300

### Dates

| Form       | Example      | Use Case                                  |
|------------|--------------|-------------------------------------------|
| Long       | July 18, 1958 | Emails, block quotes, cards, inline copy |
| Abbreviated| Jul 18, 1958 | Compact spaces (tables)                   |
| Short      | 7/18/1958    | UI inputs, date pickers                   |
| ISO 8601   | 2014-05-25   | File naming                               |

- Always use **4-digit year**
- Use **cardinal numbers** (October 21, not October 21st)
- Avoid referring to **seasons**; use months or quarters

### Time

- Use **AM/PM** (capitalized, no periods, with space): `1:00 PM`
- Use year-round time zone abbreviations: `CT` not `CST`
- Use **noon** and **midnight** instead of 12:00 PM/AM
- Separate date and time with **at**: `December 26, 2024 at 1:00 PM CT`

### Units of Measurement

- Always use **numerals** with units: `5 GB` not `Five GB`
- **Space** between value and unit (except %, °, px, U)
- **Do not pluralize** abbreviated units: `5 cm` not `5 cms`
- Spell out **time units** when possible: `3 years` not `3 y`
- Three-dimensional format: `10" x 12" x 20"` (height × width × depth)

**Common Abbreviations:**

| Unit                | Abbreviation |
|---------------------|--------------|
| Gigabyte            | GB           |
| Terabyte            | TB           |
| Megabits per second | Mbps         |
| Gigahertz           | GHz          |
| Kilowatt-hour       | kWh          |
| Centimeter          | cm           |
| Inch                | in.          |
| Degrees Celsius     | °C           |
| Degrees Fahrenheit  | °F           |

***

## Document Components

### Title Page Requirements

- Document title in **title case**
- Do not use a sentence as a title
- Include regulatory model number only if required
- Include copyright statement and month/year (`yyyy-mm` format)

### Titles, Headings, and Headers

| Component             | Capitalization | Examples                                     |
|-----------------------|----------------|----------------------------------------------|
| Document/book title   | Title case     | *Latitude 7350 Owner's Manual*               |
| Chapter title         | Sentence case  | *Configuring alert and event settings*       |
| Topic title           | Sentence case  | *Device credentials and credential profiles* |
| Heading within page   | Sentence case  | *About this task*                            |
| Table/figure title    | Sentence case  | *Types of email notifications*               |

**Guidelines:**

- Accurately describe the content
- Be brief
- Do not end with period or colon
- Avoid widowed headings (successive headings without intervening text)
- Task topics: start with **imperatives**, not gerunds:
  - ❌ Installing Dell devices
  - ✅ Install Dell devices

### Steps in a Procedure

- Limit to **7–9 numbered steps** (preferably fewer)
- Each step is a **complete sentence** ending with a period
- Start each step with an **imperative verb**
- State **purpose/condition before action**
- Optional steps: add `(Optional)` at end
- Single-step procedures: use a **bullet** instead of a number

### Lists

- **Unordered** — when sequence doesn't matter
- **Ordered** — when sequence matters
- **Definition** — to explain terms
- Use **parallel construction**
- Minimum **2 items**, maximum **9 items**
- Avoid nesting beyond **2 levels**
- Use a **colon** at the end of introductory sentences

### Tables

- Precede with an **explanatory paragraph**
- Avoid more than **4–5 columns**
- Repeat **column headings** on subsequent pages
- Avoid **footnotes** in tables (use parenthetical phrases instead)
- Use **sentence case** for titles and cell text

### Warnings, Cautions, and Notes

| Type        | Purpose                                    | Placement                    |
|-------------|--------------------------------------------|------------------------------|
| **Warning** | Potential property damage, injury, or death| Before related content       |
| **Caution** | Potential hardware damage or data loss     | Before related content       |
| **Note**    | Important supplemental information         | Before or after related content |

**Order of severity:** Warnings → Cautions → Notes

### References to External Content

- Visible link text should be **human-readable** (page title, not URL)
- Keep external links at a **high level** (pages change frequently)
- Use **see** for informational references
- Use **go to** for action-oriented references
- Use **from** for downloads:
  - ✅ For more information, see Dell Technologies Training and Certification.
  - ✅ Download the product video from the Dell Support Site.

### Trademarks

- Do **not** use trademarks or trademark symbols in the body of technical content

***

## Writing About the UI

### General Guidelines

- **Match** capitalization, spelling, and wording of UI components as they appear
- Use **bold** for actionable UI text in documentation
- Do **not** tag generic nouns/verbs as UI elements
- Do **not** include trailing punctuation from UI labels (except `?`):
  - ❌ Click OK to close the Edit VM dialog box.
  - ✅ Click **OK** to close the **Edit VM** dialog box.

### Mouse Actions

| Verb            | Usage                                        |
|-----------------|----------------------------------------------|
| **Click**       | Buttons, dialogs, menus, tabs, hyperlinks    |
| **Double-click**| Opening files, etc.                          |
| **Right-click** | Context menus                                |
| **Hover over**  | Resting pointer to see tooltip/definition    |

> Do **not** use "click on" — just "click"

### Keyboard Actions

- Use **press** for keys: `Press Enter`
- Use **enter** for values: `Enter Y`
- Simultaneous keys: `Press Ctrl+Alt+Delete`
- Key sequences: `Press Alt, A`
- Do **not** use hit, punch, push, or strike

### Common UI Verbs

| Verb       | Usage                                                        |
|------------|--------------------------------------------------------------|
| **Clear**  | Remove check mark (not *deselect* or *uncheck*)              |
| **Click**  | Buttons, dialogs, menus, tabs, links                         |
| **Close**  | Windows, tabs, pages, dialog boxes                           |
| **Drag**   | Select and move (not *click and drag*)                       |
| **Enter**  | Text in a field (not *type*, *input*, *key in*)              |
| **Open**   | Windows, pages, dialogs, documents                           |
| **Select** | Items from a list, checkboxes (not *choose*, *tick*, *pick*) |
| **Tap**    | Touch devices only                                           |

***

## UI Components

### Buttons

- **Title case** for button labels
- Keep to **1–3 words** (max 22 characters)
- Use **verbs** rather than *Yes* or *No*
- Avoid brand names, prepositions, articles, and punctuation
- Use `OK` (not *Okay* or *Ok*)

### Checkboxes

- **No default selections** (implement unselected state)
- **Sentence case** with no period (exception: confirmation statements like *"I accept."*)
- Use **positive language**: *"I want to receive..."* not *"I don't want to..."*
- For terms acceptance: *"I agree to the terms and conditions."*

### Dropdown Menus

- **Sentence case** for labels and items
- Write **clear, succinct** label text
- Avoid multiple lines; use **ellipsis (…)** for overflow with tooltip

### Radio Buttons

- **Title case** for group labels
- **No default selection**
- Use **positive tone** (affirmation over negation)
- Options must **not overlap**
- Avoid punctuation unless description is a complete sentence

### Toggle Switches

- Label: **Title case**, 1–2 words (nouns preferred)
- Label **does not change** when toggled
- Use **mutually exclusive states** only:
  - ✅ On | Off
  - ✅ Enabled | Disabled
  - ❌ Monday | Tuesday

### Tabs

- **Sentence case**
- Keep labels to **1–2 words**
- No punctuation on tab labels

### Tooltips

- **Sentence case**
- Do **not** use for error/status messages, long text, images, or interactive content
- Avoid adding **essential information** in tooltips

### Navigation

- **Title case** for navigation menu labels
- Match **page titles** to navigation labels
- Keep labels **short enough** to avoid text wrapping
- Use **icons** for primary levels only

### Notifications, Errors, and Alerts

- Write in **active voice** and **sentence case**
- Be **specific and concise**
- Provide **logical next steps**
- Avoid "Something went wrong" — describe **what specifically happened**
- Limit body copy to **1–3 sentences**
- Avoid including error codes in **titles** (put in body copy):
  - ❌ Error 500
  - ✅ We're experiencing server downtime.
  - ❌ Something went wrong.
  - ✅ We're experiencing server downtime. Try reloading the page.

### Success Messages (Toasts)

- **Avoid** "Success!" or "successfully" in titles
- Include **reason for success** — confirm what action was completed
- Keep to **1–2 sentences**
- **Sentence case**, no periods in titles
- **No exclamation marks**

### Empty State Messages

Four common types:

1. **First use** — New product/service with nothing to show yet
2. **User cleared** — User completed all tasks (e.g., cleared inbox)
3. **No results** — Search returned no results
4. **No data** — Information not yet available to populate

***

## Minimalism

### Principles

Writing based on minimalism is **action-oriented**, **succinct**, and **directed toward a
well-defined audience**.

### Key Guidelines

- Know your audience
- Do not explain the obvious
- Write **task-oriented** topics focused on **user goals**
- Use **active voice**
- Avoid **glue text** (*"This section describes…"*)
- Remove words that add no value
- Avoid **nominalization** (use *change* instead of *make a change*)

### Minimalist Language Quick Reference

| Instead of...        | Use...        |
|----------------------|---------------|
| in order to          | to            |
| due to the fact that | due to        |
| in the event that    | if, when      |
| for the purpose of   | to, for       |
| utilize              | use           |
| whether or not       | whether       |
| make a change to     | change        |
| end result           | result        |
| still remains        | remains       |
| very important       | important     |
| type in              | type          |
| combine together     | combine       |
| create a new folder  | create a folder|

***

## Topic-Based Authoring

### DITA Topic Types

| Topic Type                  | Title Phrase        | Examples                                               |
|-----------------------------|---------------------|--------------------------------------------------------|
| **Concept** (overview)      | Noun phrase         | *Network management*, *NDMP overview*                  |
| **Concept** (intro to tasks)| Gerund (-ing)       | *Creating quotas*, *Managing quotas*                   |
| **Reference**               | Noun phrase         | *Internal network settings*, *Quota report components* |
| **Task**                    | Imperative verb     | *Create an accounting quota*, *Connect the power cables* |

### Short Descriptions

- Required for DITA content (with exceptions)
- Must **stand alone** at the start of a topic
- Do **not** start with glue text: *"This topic describes…"*
- **Task** short descriptions: answer *why*, *when*, *who*, *what it accomplishes*
- **Concept** short descriptions: answer *what is this*, *why do I care*
- **Reference** short descriptions: answer *what are the items*, *what do they do*

### Task Topics

- **One task per topic**
- **Max 9 main steps**; restructure if more
- Use **imperative verbs** in steps
- Avoid screenshots (use diagrams for complex flows)
- Include **one action per step** (exception: short steps in same location)
- Write a **short introduction** explaining *why* or *when*

***

## Writing for Accessibility

### Overview

> With **20% of the world's population** estimated to have a disability, writing accessible
> content is not only the right thing to do, but it makes good business sense.

### Elements Requiring Accessibility

| Element            | Requirement                                                              |
|--------------------|--------------------------------------------------------------------------|
| **Headings/titles**| Logical hierarchy; descriptive; meaningful H1                            |
| **Images**         | Alt text (concise, descriptive); null alt text for decorative images     |
| **Tables**         | Title; column headings; never leave top-left cell empty; avoid merged cells |
| **Links**          | Human-readable link text; avoid "click here"                             |
| **Lists**          | Properly tagged (`<ul>`, `<ol>`)                                         |
| **Audio/video**    | Transcripts; captions                                                    |
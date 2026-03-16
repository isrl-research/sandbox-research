---
name: isrl-zenodo-prep
description: >
  Prepares Zenodo upload packages for iSRL research outputs — reports, datasets,
  or working documents. Use this skill whenever Lalitha asks to "prep a Zenodo upload",
  "write a Zenodo description", "package this for Zenodo", or "get this ready to publish".
  Creates a folder named {title_slug}_zenodo/ containing a _zenodo.md metadata file
  and organised subfolders for attached files. Understands iSRL brand tone and will
  flag messy or incomplete data before proceeding.
---

# iSRL — Zenodo Upload Prep Skill

You are preparing a Zenodo upload package on behalf of **iSRL (Interdisciplinary Systems Research Lab)**. Your job is to write metadata that is accurate, precise, and consistent with iSRL's institutional voice — and to organise the files that need to go up correctly before anything is submitted.

Read this skill fully before doing anything.

---

## Step 0 — Clarify Before You Build

Before creating any files, confirm the following. If any are missing from the prompt, ask — do not assume:

1. **What is being uploaded?** Report, dataset, working document, encyclopedia entry, or something else?
2. **What files need to be attached?** Get the full list. If files are mentioned but not provided, note them as placeholders.
3. **Is this preliminary / a working version?** If yes, what caveat applies — v0.1, pilot dataset, pre-peer-review, living document?
4. **Is there a related DOI or prior iSRL output this should reference?**
5. **What is the iSRL project code?** (e.g. iSRL-26-03-R-Allergen, iSRL-26-06-0x-R-Metadata)

If the data or files provided look incomplete, inconsistent, or too messy to publish without cleaning, **say so clearly and specifically** before building the package. Name exactly what the problem is (e.g. "The dataset has inconsistent column headers across sheets", "Three of the listed files don't appear to exist", "The description references a methodology that isn't in the attached report"). Suggest what cleaning or completion is needed. Do not package and flag later — flag first.

---

## Output Structure

When ready to build, create a folder named:

```
{title_slug}_zenodo/
├── _zenodo.md           ← metadata file (see format below)
├── report/              ← final report PDF and/or HTML (if applicable)
└── data/                ← datasets, CSVs, supporting files (if applicable)
```

`title_slug` = lowercase, hyphenated short form of the title. Example: `emf-triaxial-model_zenodo/`

If only a report is being uploaded (no dataset), omit the `data/` folder and note this in `_zenodo.md`.
If only a dataset is being uploaded (no report), omit the `report/` folder and note this.

Copy provided files into the correct subfolder. If a file's correct location is ambiguous, use your judgement and note the placement in `_zenodo.md` under Notes.

---

## The `_zenodo.md` File — Format

```markdown
# Zenodo Upload — {Full Title}

## Title
{Full title as it will appear on Zenodo}

## Authors
{Firstname Lastname (Affiliation: iSRL)} — list all, one per line
{If co-authored with an external institution, use their stated affiliation}

## Description
{See description writing guidelines below}

## Upload Type
{Publication / Dataset / Software / Other — pick one}

## Publication Type (if Upload Type = Publication)
{Report / Preprint / Article / Working Paper}

## Keywords
{Comma-separated, 5–10 keywords}

## License
CC BY 4.0

## Related/alternate identifiers
{List any DOIs this work cites or supersedes, one per line}
{Format: doi:10.xxxx/xxxxx — IsSupplementTo / IsCitedBy / IsNewVersionOf / etc.}

## Project
IFID 2026 — Indian Food Informatics Data
iSRL Project Code: {iSRL-XX-XX-X-XXXXX}

## Notes
{Any caveats about version, preliminary status, living document status, or file placement decisions}
{If preliminary: state this explicitly — e.g. "This is a v0.1 working dataset. It will be updated as the taxonomy is refined."}
{If no note is needed, write: None}

## Files to Attach
### report/
- {filename.pdf}
- {filename.html} ← if applicable

### data/
- {filename.csv}
- {filename.xlsx}
← If no data folder: state "No dataset attached. Report only."
```

---

## Description Writing Guidelines — iSRL Brand Tone

The Zenodo description is the first thing a researcher from outside the lab reads. It must do three things: say what this output is, say why it exists, and say what someone would use it for. It should not sell, inflate, or hedge.

### Voice principles

**Precise without being academic.** Write as someone who has done the work and is describing it plainly. No jargon without definition. No passive constructions to sound neutral — actual neutrality comes from accurate description.

**The work speaks for itself.** Do not write "groundbreaking", "novel", "important", or "innovative." Describe what the output does and let the reader judge its significance.

**Honest about scope and limits.** If this is a preliminary dataset, a working document, or a first version, say so in the description — not just in the notes. Overstating completeness is a form of inaccuracy.

**No marketing language.** iSRL is public infrastructure. It does not need to pitch itself. The description is not a grant abstract or a press release.

### Structure of a good description (adapt as needed)

```
[One sentence: what this output is and what problem it addresses.]

[Two to four sentences: what was done — the method, the scope, the data source, the framework applied. Be specific. Numbers, document names, and exact definitions are welcome here.]

[One to two sentences: what the output can be used for, and by whom — regulators, researchers, industry, all three. Be honest about who it is and is not useful to.]

[If preliminary or living: one sentence stating this explicitly and what the update path is.]
```

### Examples by output type

**Report (analytical):**
> This report examines the regulatory treatment of allergen declaration in Indian packaged foods under FSSAI Labelling Regulations 2020, and compares India's requirements against the EU, US, and FSANZ frameworks. The analysis is organised across five sub-parts: current Indian law, declaration practice and enforcement, comparative international frameworks, constraint analysis, and epidemiological burden. It is intended as a reference for regulators, food systems researchers, and classification systems that need to represent allergen metadata accurately. Primary sources only; all claims are cited to specific regulatory provisions or peer-reviewed literature.

**Dataset (preliminary):**
> This is a v0.1 working dataset of canonical ingredient identifiers for the Indian Food Informatics Data (IFID) taxonomy. It contains [N] entries mapped from [X] raw ingredient name variants drawn from the top [N] packaged food products by market presence in India. Each entry carries a canonical ID, primary name, variant list, EMF score, and HS chapter assignment. This dataset is preliminary — classifications are subject to revision as the taxonomy is reviewed by subject matter experts. It will be versioned on Zenodo as updates are made.

**Working document / encyclopedia:**
> This is a working reference document for the Indian Food Informatics Data project, listing [N] food ingredient entries with canonical names, regional variants, and classification notes. It is not a finalised reference — entries are being added and revised as part of the IFID 2026 research cycle. It is published openly so that researchers and practitioners can engage with the work in progress and identify gaps or errors.

---

## Keywords — How to Generate Them

Pull keywords from: the subject domain, the regulatory framework cited, the methodology, the geography, and the output type.

**Good:** `food labelling, FSSAI, ingredient taxonomy, canonical identifiers, Indian food systems, allergen declaration, open data, data infrastructure, EMF model, food classification`

**Avoid:** generic terms (`research`, `India`, `data`), brand names, internal project codes as keywords.

---

## Related Identifiers — How to Use Them

Use Zenodo's relationship vocabulary. Common patterns for iSRL:

- A report that cites a prior iSRL output → `IsCitedBy: doi:10.xxxx`
- A dataset that is the source for a report → `IsSupplementTo: doi:10.xxxx`
- A new version of an earlier upload → `IsNewVersionOf: doi:10.xxxx`
- A companion/justification document → `IsSupplementTo: doi:10.xxxx`

If no related identifiers exist, write `None` — do not leave blank.

---

## Preliminary / Living Document Notes — Exact Language to Use

When flagging version or living status, use one of these formulations (adapt as needed):

- **Preliminary dataset:** "This is a v0.1 working dataset published for transparency and external engagement. It will be updated as the taxonomy is reviewed and refined. Check the iSRL Zenodo community for the latest version."
- **Living document:** "This document is updated as the research develops. The version published here reflects the state of the work as of [month year]. Later versions will be deposited separately with version numbers."
- **Pre-peer-review:** "This report has not undergone formal peer review. It is published as a working document under iSRL's open research model. Feedback and critique are welcome via the iSRL GitHub repository."
- **First of a series:** "This is the first output in the [series name] workstream. Subsequent outputs will be linked via Zenodo related identifiers."

---

## What to Check Before Finalising

- [ ] Title matches the report/dataset exactly as it will be published
- [ ] All authors listed with correct affiliation
- [ ] Description follows the structure: what it is → what was done → who can use it → any caveats
- [ ] No marketing language, no inflation of significance
- [ ] Preliminary/living status stated in both description and notes if applicable
- [ ] Keywords are specific and domain-relevant (5–10)
- [ ] Related identifiers filled in or explicitly marked None
- [ ] Files listed under correct subfolder (report/ or data/)
- [ ] Notes field addresses any ambiguities in file placement or version status
- [ ] License is CC BY 4.0 (always, unless Lalitha specifies otherwise)

---

## What to Flag and Refuse to Package

Do not build the upload package if any of the following are true. State the problem clearly and wait for resolution:

- **Inconsistent data:** column headers don't match across sheets, IDs are duplicated, values are clearly erroneous
- **Missing files:** files are listed in the description but not provided
- **Unclear authorship:** it is not clear who authored or co-authored the work
- **Version mismatch:** the report references a methodology or dataset version that doesn't match what's been provided
- **Description cannot be written accurately:** not enough information has been provided to write a truthful description — ask for what's missing rather than guessing

When flagging, name the specific problem. Do not say "this seems incomplete." Say "The dataset references 487 canonical entries but the file provided contains 312 rows with no explanation of the gap."

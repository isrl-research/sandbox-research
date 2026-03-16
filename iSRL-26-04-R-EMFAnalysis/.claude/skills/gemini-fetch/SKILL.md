---
name: gemini-fetch
description: >
  Orchestrates AI API fetch tasks end-to-end using Gemini (or any LLM API). Triggers whenever
  the user wants to fetch, process, or analyze data using an AI API — especially Gemini.
  Use this skill when the user says things like "use the Gemini API to...", "call the AI API to...",
  "batch process with Gemini...", "run this through the LLM...", "fetch using AI...", or any
  phrasing that implies an AI API should be called to process a batch of inputs or documents.
  This skill orchestrates two sub-skills: system-instructions writer and api-script writer.
  Always trigger this skill even if the user's request seems simple — the sub-skills handle
  the actual complexity.
---

# Gemini Fetch Orchestrator

This skill orchestrates end-to-end AI API fetch tasks. It coordinates two sub-skills:
- `subskills/system-instructions/SKILL.md` — writes system instructions in XML
- `subskills/api-script/SKILL.md` — writes the Python fetch script

---

## Step 0: Read Sub-Skills First

Before doing anything else, read both sub-skills so you know what they require:
- `subskills/system-instructions/SKILL.md`
- `subskills/api-script/SKILL.md`

---

## Step 1: Clarify the Task

Before writing anything, gather the following. If any item is already explicit in the user's prompt, skip asking for it — but **always confirm** items that are ambiguous.

### Required clarifications (ask all at once, not one by one):

1. **What is the task?**
   - What input does each API call receive?
   - What output is expected?
   - Is this a batch job (multiple inputs) or a single call?

2. **Batch size**
   - How many items per batch? (e.g., 10, 50, 100)
   - What is the total expected volume?

3. **Model**
   - Which exact Gemini model? (e.g., `gemini-1.5-pro-002`, `gemini-2.0-flash`, `gemini-1.5-flash-8b`)
   - If not specified, ask explicitly — never assume.

4. **Temperature**
   - Should temperature be 0? (Almost always yes — confirm unless user says otherwise.)
   - If not 0, what value?

5. **System instructions**
   - Does the user have existing system instructions, or should they be written from scratch?
   - What tone/persona should the model adopt?

6. **Output format**
   - What columns/fields should the output `.txt` file have?
   - Should output be one-line-per-input or multi-line blocks?

7. **Edge cases** (ask these explicitly):
   - What should happen if the model returns an empty response?
   - What if the input is malformed or missing a field?
   - What if the model hallucinates a format that doesn't match expectation?
   - Are there inputs that should be skipped entirely?

> After collecting answers, **summarize back to the user** what you understood before proceeding. Get a green light before writing any files.

---

## Step 2: Write System Instructions

Delegate to `subskills/system-instructions/SKILL.md`.

Pass it:
- The task description
- Input format
- Output format
- Edge cases confirmed with user
- Any persona/tone constraints

The sub-skill will produce a `system_instructions.xml` file.

---

## Step 3: Create Fetch Folder

Create a new folder under `fetch/` named descriptively for this task, e.g.:
```
fetch/classify-emf-descriptions/
fetch/summarize-papers/
fetch/extract-entities-batch1/
```

Inside this folder:
- Copy `system_instructions.xml` here
- The Python script will also live here
- All outputs will be saved here

The `api-key-loader.py` lives in the root `fetch/` folder and must not be moved.

---

## Step 4: Write the Python Fetch Script

Delegate to `subskills/api-script/SKILL.md`.

Pass it:
- Path to `system_instructions.xml` (relative: `./system_instructions.xml`)
- Path to `api-key-loader.py` (relative: `../api-key-loader.py`)
- Model name
- Temperature (almost always 0)
- Batch size
- Input file/format
- Output format and fields
- Edge case handling rules

The sub-skill will produce the Python script saved inside the task folder.

---

## Step 5: Review Before Execution

Before running anything, show the user:
1. The `system_instructions.xml` content
2. The Python script (key sections — clarify_task prompt, output logic, backoff config)
3. The folder structure that will be created

Ask: "Does everything look right? Should I proceed?"

---

## Step 6: Execute

Once approved:
```bash
cd fetch/<task-folder>
python <script-name>.py
```

Monitor output. If 429 errors are persistent (more than 3 in a row), the script will auto-pause — inform the user.

---

## Step 7: Verify Outputs

After completion, confirm:
- `_raw.txt` file exists and has content
- Formatted output file exists (if applicable)
- No batches were silently skipped (check logs)
- Row/record count matches input
- Statistics block printed at end of script run (flag marker counts, unique values, top-N)

Report summary to user. Include the key statistics figures in your report.

---

## Folder Structure Reference

```
fetch/
├── api-key-loader.py              ← shared, never move this
├── classify-emf-descriptions/     ← example task folder
│   ├── system_instructions.xml
│   ├── run_fetch.py
│   ├── output_raw.txt
│   └── output_formatted.txt
└── another-task/
    ├── system_instructions.xml
    ├── run_fetch.py
    └── output_raw.txt
```

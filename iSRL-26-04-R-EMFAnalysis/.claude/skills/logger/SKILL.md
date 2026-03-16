---
name: experiment-log
description: >
  Appends a timestamped entry to experiment.log.md after completing any meaningful task in a
  Claude Code session. Triggers automatically at the end of every task completion — not for
  minor fixes, edits, or refinements, but whenever a distinct task is done and the session
  moves on. Also triggers when the user says "log this", "add to experiment log", "update the
  log", or "mark task complete". Must always run at natural task boundaries. If in doubt about
  whether something counts as a loggable task, log it. Never skip logging after a completed
  task, even if the user didn't ask explicitly.
---

# Experiment Log Skill

Appends a concise entry to `experiment.log.md` every time a task is completed in a session.

---

## What counts as a loggable task

Log when:
- A script was written and ran successfully (or failed with a conclusion reached)
- A pipeline stage was completed
- A data fetch / API run finished
- A file or module was built and works
- A deadblock was hit and resolved (or abandoned with a decision made)
- The session moves on to a new distinct task

Do NOT log:
- Typo fixes or minor variable renames
- Re-runs of the same script with no meaningful change
- Clarification exchanges with no output produced

---

## Log format

Each entry looks like:

```
## [DD-Mon-YYYY HH:MM IST] — <Task name / one-line summary>

<2–3 sentences. What was done. Any deadblocks hit. Any edge cases or surprises encountered.>

---
```

Rules:
- Timestamp is always in IST (UTC+5:30). Compute it correctly.
- Task summary on the `##` line is a short title, not a sentence.
- Body is 2–3 sentences maximum. No bullet points. Plain prose.
- If there were NO deadblocks and NO edge cases, just describe what was done and that it completed cleanly.
- If a deadblock was hit, name it clearly: what failed, why, how it was resolved or worked around.
- Append only — never overwrite existing entries.

---

## File location

The log file lives at the project root as `experiment.log.md`.

If it doesn't exist yet, create it with this header first:

```markdown
# Experiment Log

---

```

Then append the entry.

---

## How to write the entry

Before writing, ask yourself:
1. What was the task? (one phrase)
2. Did anything block progress? If yes — what exactly, and what was the outcome?
3. Was there an unexpected edge case or surprising behavior?

Then write 2–3 sentences covering those points. Be specific. "Script failed due to 429 rate limit on batch 3; paused 60s and resumed cleanly" is useful. "There were some issues" is not.

---

## Example entries

```
## [07-Jun-2025 14:32 IST] — EMF Classification Fetch Run 1

Ran gemini-1.5-pro-002 batch classification on 312 EMF descriptions across 16 batches of 20.
Hit 3 consecutive 429s at batch 9; script auto-paused 60s and recovered without data loss.
All 312 records written to output_raw.txt and output_formatted.txt cleanly.

---

## [07-Jun-2025 16:10 IST] — System Instructions XML for Entity Extraction

Wrote system_instructions.xml for extracting ingredient names and CAS numbers from regulatory text.
Edge case confirmed with user: entries with no CAS number output CAS::NONE rather than being skipped.
No deadblocks; instructions reviewed and approved before script generation.

---

## [08-Jun-2025 09:45 IST] — E/M/F Score Table Parser

Built parser to extract E, M, F scores from LaTeX table source into structured txt.
No issues; all three tables parsed cleanly with correct delimiter formatting.

---
```

---

## Execution

```bash
# Append entry to log (never overwrite)
# If file doesn't exist, create with header first, then append
```

Write the entry using the `str_replace` or `create_file` tool — always append, never replace the whole file.

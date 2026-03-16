---
name: gemini-fetch/api-script
description: >
  Writes production-grade Python scripts for Gemini (or any LLM) API batch processing.
  Called by the gemini-fetch orchestrator, or directly when the user needs a Python script
  to call an AI API. Triggers on phrases like "write the fetch script", "create the Python
  script for the API call", "batch process with Gemini", or when the orchestrator delegates
  script writing. Always includes: exponential backoff for Tier 1 paid Gemini, raw output
  saving, per-batch saving, API key loading from api-key-loader.py, system instructions
  loaded from XML, and a new folder under fetch/ per task.
---

# AI API Script Writer

This sub-skill writes Python scripts that call the Gemini API (or other LLM APIs) for
batch processing tasks. Every script it produces follows a strict set of non-negotiable
patterns.

---

## Non-Negotiable Script Requirements

Every script produced by this skill MUST implement ALL of the following:

### 1. API Key Loading
```python
import subprocess
result = subprocess.run(["python", "../api-key-loader.py"], capture_output=True, text=True)
# OR use the pattern below if api-key-loader.py simply prints the key:
import os
api_key = os.getenv("API_KEY")
```
The `api-key-loader.py` lives at `../api-key-loader.py` relative to the task folder.
Never hardcode API keys. Never prompt the user for them at runtime.

### 2. System Instructions from XML
```python
import xml.etree.ElementTree as ET

def load_system_instructions(path="./system_instructions.xml"):
    tree = ET.parse(path)
    root = tree.getroot()
    # Concatenate all relevant text nodes into a single system prompt string
    parts = []
    for child in root:
        if child.text and child.text.strip():
            parts.append(child.text.strip())
    return "\n\n".join(parts)
```
Always load from `./system_instructions.xml` (relative to script location).

### 3. Exponential Backoff for Gemini Tier 1 Paid

Gemini Tier 1 paid limits: ~360 RPM, ~4M TPM. Backoff must handle 429s gracefully.

```python
import time
import random

def call_with_backoff(fn, max_retries=8, base_delay=2.0, max_delay=120.0):
    """
    Exponential backoff with jitter for Gemini Tier 1 paid.
    Pauses the entire script if >3 consecutive 429s are received.
    """
    consecutive_429s = 0
    for attempt in range(max_retries):
        try:
            result = fn()
            consecutive_429s = 0  # reset on success
            return result
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                consecutive_429s += 1
                if consecutive_429s >= 3:
                    pause_seconds = 60
                    print(f"\n⚠️  3+ consecutive 429s. Pausing {pause_seconds}s before retry...\n")
                    time.sleep(pause_seconds)
                    consecutive_429s = 0
                delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                print(f"  429 rate limit hit. Retrying in {delay:.1f}s (attempt {attempt+1}/{max_retries})")
                time.sleep(delay)
            else:
                raise  # non-429 errors bubble up immediately
    raise RuntimeError(f"Max retries ({max_retries}) exceeded")
```

### 4. Raw Output Saved Immediately

Every API response MUST be saved raw, exactly as returned, to `_raw.txt`:
```python
RAW_OUTPUT_PATH = "./output_raw.txt"

def append_raw(response_text: str, record_id: str):
    with open(RAW_OUTPUT_PATH, "a", encoding="utf-8") as f:
        f.write(f"--- RECORD {record_id} ---\n")
        f.write(response_text)
        f.write("\n\n")
```
- Raw saving happens **before** any parsing or formatting.
- If the script crashes mid-run, the raw file must still contain all completed outputs.
- Never wait until the end to write raw output.

### 5. Save After Every Batch (not at the end)

```python
FORMATTED_OUTPUT_PATH = "./output_formatted.txt"

def save_batch(batch_results: list):
    with open(FORMATTED_OUTPUT_PATH, "a", encoding="utf-8") as f:
        for line in batch_results:
            f.write(line + "\n")
    print(f"  ✓ Batch saved ({len(batch_results)} records)")
```
- Open in append mode (`"a"`) always — never overwrite.
- Log confirmation after each batch save.

### 6. Batch Processing Loop Structure

```python
BATCH_SIZE = 20  # confirm with user — never hardcode without asking

def process_in_batches(records: list, system_prompt: str):
    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i : i + BATCH_SIZE]
        batch_results = []

        for record in batch:
            def api_call():
                return call_gemini(record, system_prompt)

            raw_response = call_with_backoff(api_call)
            append_raw(raw_response, record["id"])
            formatted = parse_response(raw_response, record["id"])
            batch_results.append(formatted)

        save_batch(batch_results)
        print(f"  Batch {i // BATCH_SIZE + 1} complete ({i + len(batch)}/{len(records)} total)")
```

### 7. Model and Temperature

```python
MODEL_NAME = "gemini-1.5-pro-002"   # always confirm exact model with user
TEMPERATURE = 0                      # almost always 0 — confirm explicitly

import google.generativeai as genai

genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=system_prompt,
    generation_config=genai.GenerationConfig(temperature=TEMPERATURE)
)
```

---

## Full Script Template

Use this as the base. Fill in task-specific logic.

```python
#!/usr/bin/env python3
"""
Task: [TASK NAME]
Model: [MODEL NAME]
Temperature: [0 or other]
Batch size: [N]
Created: [DATE]
"""

import os
import sys
import time
import random
import xml.etree.ElementTree as ET
import google.generativeai as genai

# ── Configuration ──────────────────────────────────────────────────────────────
MODEL_NAME   = "[MODEL]"
TEMPERATURE  = 0
BATCH_SIZE   = [N]
INPUT_FILE   = "./input.txt"          # adjust as needed
RAW_OUT      = "./output_raw.txt"
FMT_OUT      = "./output_formatted.txt"
SYS_XML      = "./system_instructions.xml"
API_KEY_SCRIPT = "../api-key-loader.py"

# ── API Key ─────────────────────────────────────────────────────────────────────
api_key = os.getenv("API_KEY")
if not api_key:
    print("ERROR: API_KEY environment variable not set. Run api-key-loader.py first.")
    sys.exit(1)

genai.configure(api_key=api_key)

# ── Load System Instructions ────────────────────────────────────────────────────
def load_system_instructions(path=SYS_XML):
    tree = ET.parse(path)
    root = tree.getroot()
    parts = []
    for child in root:
        text = "".join(child.itertext()).strip()
        if text:
            parts.append(text)
    return "\n\n".join(parts)

# ── Gemini Client ───────────────────────────────────────────────────────────────
def make_model(system_prompt):
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=system_prompt,
        generation_config=genai.GenerationConfig(temperature=TEMPERATURE)
    )

# ── Exponential Backoff ─────────────────────────────────────────────────────────
def call_with_backoff(fn, max_retries=8, base_delay=2.0, max_delay=120.0):
    consecutive_429s = 0
    for attempt in range(max_retries):
        try:
            result = fn()
            consecutive_429s = 0
            return result
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                consecutive_429s += 1
                if consecutive_429s >= 3:
                    print(f"\n⚠️  3 consecutive 429s. Pausing 60s...\n")
                    time.sleep(60)
                    consecutive_429s = 0
                delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                print(f"  Rate limited. Retry in {delay:.1f}s (attempt {attempt+1}/{max_retries})")
                time.sleep(delay)
            else:
                print(f"  Non-429 error: {err}")
                raise
    raise RuntimeError(f"Max retries exceeded for record")

# ── Raw Output ──────────────────────────────────────────────────────────────────
def append_raw(response_text, record_id):
    with open(RAW_OUT, "a", encoding="utf-8") as f:
        f.write(f"--- RECORD {record_id} ---\n")
        f.write(response_text.strip())
        f.write("\n\n")

# ── Formatted Output ────────────────────────────────────────────────────────────
def save_batch(lines):
    with open(FMT_OUT, "a", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    print(f"  ✓ Saved {len(lines)} records")

# ── Parse Response ──────────────────────────────────────────────────────────────
def parse_response(raw, record_id):
    """
    [FILL IN: task-specific parsing logic]
    Default: return raw stripped line
    """
    return raw.strip()

# ── Load Input ──────────────────────────────────────────────────────────────────
def load_input(path=INPUT_FILE):
    """
    [FILL IN: task-specific input loading]
    Return list of dicts with at minimum {"id": ..., "text": ...}
    """
    records = []
    # example: read CSV, JSON, or plain text
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                records.append({"id": str(i+1), "text": line})
    return records

# ── Main ────────────────────────────────────────────────────────────────────────
def main():
    print(f"Loading system instructions from {SYS_XML}...")
    system_prompt = load_system_instructions()

    print(f"Loading input from {INPUT_FILE}...")
    records = load_input()
    print(f"  {len(records)} records loaded.")

    gemini = make_model(system_prompt)

    print(f"\nStarting batch processing: {len(records)} records, batch_size={BATCH_SIZE}\n")

    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i : i + BATCH_SIZE]
        batch_results = []

        for record in batch:
            user_msg = record["text"]  # adjust per task

            def api_call(msg=user_msg):
                response = gemini.generate_content(msg)
                return response.text

            raw = call_with_backoff(api_call)
            append_raw(raw, record["id"])
            formatted = parse_response(raw, record["id"])
            batch_results.append(formatted)

        save_batch(batch_results)
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (len(records) + BATCH_SIZE - 1) // BATCH_SIZE
        print(f"  Batch {batch_num}/{total_batches} done ({i + len(batch)}/{len(records)} records)\n")

    print(f"\n✅ Done. Raw output: {RAW_OUT} | Formatted: {FMT_OUT}")

if __name__ == "__main__":
    main()
```

---

### 8. Post-Run Statistics Block (Context-Adaptive)

Every script MUST end with a statistics section that reads `output_formatted.txt` AFTER
the fetch loop completes. This is pure Python post-processing — no API calls.

**The agent decides what statistics to include based on the task context.**
If the context is not clear enough to determine what statistics are meaningful, ask the user
before writing this block. Do not invent arbitrary stats for stats' sake.

#### How to decide what to include

Inspect the output format the script will produce. Ask:
- Does the output contain a flag/marker field (e.g., `UNSURE`, `MISSING`, `NONE`, `SKIP`)?
  → Always count how many lines contain each flag and report %
- Does the output contain a categorical value (e.g., a source, a label, a category)?
  → Count unique values, top-N most common
- Is a specific count meaningful as a quality signal?
  → e.g., line count vs. expected total, how many lines are fully filled vs. partially

If none of these apply clearly, ask the user: "What statistics would be meaningful
for this output?" before writing the block.

#### Required structure

```python
# ── Post-Run Statistics ─────────────────────────────────────────────────────────
def print_statistics(formatted_path: str, expected_total: int):
    """
    Reads output_formatted.txt and prints summary statistics.
    Adapt this function to the specific output format of this task.
    """
    from collections import Counter

    lines = []
    with open(formatted_path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    total = len(lines)
    print(f"\n{'='*50}")
    print(f"OUTPUT STATISTICS")
    print(f"{'='*50}")
    print(f"Total lines written : {total}")
    print(f"Expected            : {expected_total}")
    if total != expected_total:
        print(f"  *** WARNING: count mismatch ({total - expected_total:+d}) ***")

    # [FILL IN: task-specific stats — examples below, adapt as needed]

    # Example: count flag markers (e.g., UNSURE, MISSING, SKIP)
    # flag_counts = Counter()
    # for line in lines:
    #     if ":: UNSURE" in line:
    #         flag_counts["UNSURE"] += 1
    #     elif ":: MISSING" in line:
    #         flag_counts["MISSING"] += 1
    # for flag, count in flag_counts.most_common():
    #     print(f"  {flag:20s}: {count:5d}  ({100*count/total:.1f}%)")

    # Example: count unique source values (for source-identification tasks)
    # from collections import Counter
    # source_counter = Counter()
    # for line in lines:
    #     if " :: " in line:
    #         sources_part = line.split(" :: ", 1)[1]
    #         for src in sources_part.split(" | "):
    #             source_counter[src.strip()] += 1
    # print(f"\nUnique sources      : {len(source_counter)}")
    # print("Top 15 sources:")
    # for src, count in source_counter.most_common(15):
    #     print(f"  {src:30s}: {count:5d}")

    print(f"{'='*50}\n")
```

Call this function at the very end of `main()` (or at the bottom of the script):
```python
print_statistics(FMT_OUT, total_expected)
```

#### Rules for this block

- Always fill in the task-specific stats — the template comments are a guide, not the
  final code. The actual stat logic must match the real output format.
- If the output has flag markers (`UNSURE`, `MISSING`, `NONE`, `SKIP`, etc.) always count them.
- If the output has a categorical field (source, label, category), always count unique values
  and print top-N most common (N=15 is a good default, adjust for task).
- Print % alongside counts where useful.
- If the count doesn't match expected, print a clear WARNING.
- This block runs AFTER the fetch loop — it only reads files, makes no API calls.

---

## Before Writing the Script, Confirm

Always verify these are settled before generating the script:

| Item | Status |
|------|--------|
| Exact model name | Must be confirmed |
| Temperature = 0? | Must be confirmed (default: yes) |
| Batch size | Must be confirmed |
| Input file path and format | Must be confirmed |
| Output format (what `parse_response` should do) | Must be confirmed |
| Edge case handling rules | Must be confirmed |
| Task folder name under `fetch/` | Agree with user |

If any of these are missing, ask before writing.

---

## After Writing the Script

- Save the script as `run_fetch.py` (or a task-appropriate name) inside the task folder.
- Print the key config block to the user for final review.
- Wait for green light before executing.

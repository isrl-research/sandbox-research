---
name: gemini-fetch/system-instructions
description: >
  Writes high-quality system instructions in XML format for Gemini (or any LLM) API calls.
  Called by the gemini-fetch orchestrator, or directly when the user wants to write or refine
  system instructions for an AI model. Triggers when user says "write system instructions",
  "create a system prompt for...", "define what the model should do for...", or when the
  orchestrator delegates this step. Always produces an XML file — never plain text or JSON.
---

# System Instructions Writer

This sub-skill produces a `system_instructions.xml` file for use in AI API calls.
It follows best practices for LLM instruction writing: explicit, detailed, with defined
input/output formats, edge case handling, and worked examples.

---

## Principles

- **Never be succinct for the sake of it.** Take exactly as much space as the task requires.
- **Explicit is better than implicit.** If a rule seems obvious, state it anyway.
- **Define all formats precisely.** Use a mix of `::`, `|`, and `=` as delimiters in examples.
- **Output is always `.txt`** unless the user explicitly requests JSON.
- **Edge cases must be confirmed with the user** before being written into instructions.
- **NEVER instruct the model to guess when uncertain.** Always define an explicit flag marker
  (`UNSURE`, `NONE`, `UNKNOWN`, `UNCLASSIFIABLE`, or a task-appropriate equivalent) and tell
  the model to use it. The choice of marker must be confirmed with the user or clearly derived
  from context. The same marker must be used consistently throughout the XML — define it once
  in `<rules>` and reference it everywhere else.

---

## Step 1: Understand the Task

Collect from the orchestrator (or from the user directly):

- What is the model supposed to do? (e.g., classify, extract, summarize, compare)
- What does each input look like? (fields, format, length, language)
- What should the output look like? (columns, delimiters, line structure)
- What persona or tone should the model adopt?
- What are the confirmed edge cases?

---

## Step 2: Draft Edge Cases for User Confirmation

Before writing the XML, identify likely edge cases and present them to the user:

Examples to always check:
- **Empty/null input**: What should the model output?
- **Ambiguous input**: Should the model pick the most likely answer or flag uncertainty?
- **Multiple valid answers**: Output all, or just the top one?
- **Input in unexpected language**: Skip, flag, or translate?
- **Input that's too long**: Truncate silently, summarize, or raise error?
- **Model is unsure**: Use a flag marker — NEVER instruct the model to "best guess". Choose the most appropriate flag for the task (e.g., `UNSURE`, `NONE`, `UNKNOWN`, `UNCLASSIFIABLE`) and always use it consistently throughout the XML.

Present these as a numbered list. Wait for the user to answer each one.
Then confirm: "I'll include these rules in the system instructions. Ready to proceed?"

Only after green light — write the XML.

---

## Step 3: Write the XML

### Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<system_instructions>

  <role>
    <!-- Who the model is and what its job is -->
  </role>

  <task>
    <!-- What the model must do, step by step -->
  </task>

  <input_format>
    <!-- Exact format of each input, with field names and delimiters -->
    <!-- Include a worked example -->
  </input_format>

  <output_format>
    <!-- Exact format of each output, with field names and delimiters -->
    <!-- Include a worked example -->
    <!-- State explicitly: output is plain text, not JSON -->
  </output_format>

  <rules>
    <!-- Numbered list of explicit rules -->
    <!-- Include: tone, consistency, what to do when uncertain -->
  </rules>

  <edge_cases>
    <!-- One <case> block per confirmed edge case -->
    <!-- Each has: <trigger>, <instruction>, <example_output> -->
  </edge_cases>

  <examples>
    <!-- 2–4 full worked examples (input → output) -->
    <!-- Include at least one "tricky" or edge-case example -->
  </examples>

</system_instructions>
```

---

### Delimiter Guidelines

Use these consistently throughout the XML:

| Delimiter | Use for |
|-----------|---------|
| `::` | Separating a field name from its value in output lines |
| `\|` | Separating multiple values within a single field |
| `=` | Key=value pairs inside structured fields |
| newlines | Separating records/rows in batch output |

Example output line:
```
ID::001 | LABEL::positive | CONFIDENCE::high | NOTES::tone is clearly affirmative
```

---

### Example — Classification Task

```xml
<?xml version="1.0" encoding="UTF-8"?>
<system_instructions>

  <role>
    You are a precise scientific classifier. Your job is to read short descriptions of
    electromagnetic field (EMF) exposure scenarios and classify each one according to
    a defined taxonomy. You are methodical, consistent, and never guess when uncertain.
  </role>

  <task>
    For each input record, you will:
    1. Read the description carefully.
    2. Assign exactly one primary category from the allowed list.
    3. Assign up to two secondary tags if applicable.
    4. Output a confidence level: HIGH, MEDIUM, or LOW.
    5. Write a one-sentence rationale.
  </task>

  <input_format>
    Each input arrives as a plain text block with the following fields:
      ID = [numeric identifier]
      DESCRIPTION = [free text, 1–5 sentences]

    Example input:
      ID = 042
      DESCRIPTION = Worker standing next to a 50Hz power transformer for 8 hours per day.
  </input_format>

  <output_format>
    Output one line per record using this exact format:
      ID::[id] | CATEGORY::[category] | TAGS::[tag1|tag2] | CONFIDENCE::[level] | RATIONALE::[one sentence]

    Output is plain text. Do not use JSON. Do not add headers or footers.

    Example output:
      ID::042 | CATEGORY::occupational_ELF | TAGS::chronic|high_field | CONFIDENCE::HIGH | RATIONALE::Daily 8-hour exposure near a power transformer is a classic occupational ELF scenario.
  </output_format>

  <rules>
    1. Always output exactly one line per input record.
    2. Never skip a record, even if uncertain — use CONFIDENCE::LOW and explain in RATIONALE.
    3. Use only categories from the allowed list. Never invent new category names.
    4. Tags are optional — output TAGS::NONE if no tags apply.
    5. Rationale must be one sentence only. No period at the end.
    6. Do not output any preamble, explanation, or closing statement.
    7. Maintain consistent formatting across all records in the batch.
  </rules>

  <edge_cases>
    <case>
      <trigger>Input description is empty or contains only whitespace</trigger>
      <instruction>Output: ID::[id] | CATEGORY::UNCLASSIFIABLE | TAGS::NONE | CONFIDENCE::LOW | RATIONALE::Input description was empty or missing</instruction>
    </case>
    <case>
      <trigger>Description mentions multiple distinct EMF sources</trigger>
      <instruction>Classify by the dominant or most clearly described source. Note the ambiguity in RATIONALE.</instruction>
      <example_output>ID::099 | CATEGORY::occupational_ELF | TAGS::mixed_sources | CONFIDENCE::MEDIUM | RATIONALE::Multiple sources described; classified by dominant transformer reference</example_output>
    </case>
    <case>
      <trigger>Model is genuinely unsure between two categories</trigger>
      <instruction>Output CATEGORY::UNSURE, set CONFIDENCE::LOW, and name both candidates in RATIONALE. Do NOT guess or pick one arbitrarily.</instruction>
      <example_output>ID::055 | CATEGORY::UNSURE | TAGS::NONE | CONFIDENCE::LOW | RATIONALE::Could not distinguish between occupational_ELF and RF_consumer — insufficient detail in description</example_output>
    </case>
  </edge_cases>

  <examples>
    <example id="1">
      <input>ID = 007 | DESCRIPTION = Child using tablet with WiFi for 3 hours daily.</input>
      <output>ID::007 | CATEGORY::RF_consumer | TAGS::pediatric|chronic | CONFIDENCE::HIGH | RATIONALE::WiFi-enabled tablet use is a standard RF consumer exposure scenario for children</output>
    </example>
    <example id="2">
      <input>ID = 088 | DESCRIPTION = ???</input>
      <output>ID::088 | CATEGORY::UNCLASSIFIABLE | TAGS::NONE | CONFIDENCE::LOW | RATIONALE::Input description was empty or missing</output>
    </example>
  </examples>

</system_instructions>
```

---

## Step 4: Save the File

Save as `system_instructions.xml` in the task folder under `fetch/`.

Confirm to the orchestrator (or user): "System instructions written. Ready for script generation."

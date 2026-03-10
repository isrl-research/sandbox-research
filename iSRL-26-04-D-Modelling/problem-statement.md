ID: iSRL-26-04-D-Modelling

## Background

IFID is building a coordination layer for Indian food ingredient data. The core problem it addresses is this: the same ingredient appears under dozens of different names across product labels, regulatory documents, and trade records. "Groundnut oil," "refined groundnut oil," "arachis oil," and "hydrolysed groundnut protein" all originate from the same source — but no current system connects them in a way that is useful for classification, compliance, or research. IFID's goal is to make that coordination possible without flattening the differences that actually matter.

> All contributions to this discussion will be acknowledged in the final output. Substantial contributions — modelling proposals, schema design, or validated approaches adopted into the system — will be credited as co-authorship on the published output. All outputs are published open access under CC BY 4.0 with a DOI on Zenodo under the iSRL community: https://zenodo.org/communities/isrl/


We cleaned back-of-packet ingredient data from 896 sampled Indian packaged food products and thousands of Open Food Facts Indian product entries (sampling methodology releasing April 2026: https://github.com/isrl-research/ifid-roadmap/issues/1), and have 2,684 ingredient variants mapped to their canonical source. 

> For data, context on the data and scoring model, refer to the `iSRL-26-04-R-EMFAnalysis` folder in the repo — specifically: https://github.com/isrl-research/sandbox-research/blob/main/iSRL-26-04-R-EMFAnalysis/EMF_Info.md


A few examples of what that mapping looks like:

```
hydrolysed groundnut protein  →  groundnut
neem azadirachta indica leaf  →  neem azadirachta indica
preservative sodium benzoate  →  synthetic
acidity regulator ins 331 ii  →  synthetic | corn
grapefruit juice concentrate  →  grapefruit
```

Each variant has been tagged using the EMF framework (doi:10.5281/zenodo.18714527), which characterises an ingredient along three axes:

- **E (Energy / Process):** what processing has been applied and how intensive it is — from minimal handling (sorting, washing) to heavy industrial transformation (hydrogenation, solvent extraction, acetylation)
- **M (Matter state):** how far the ingredient has moved from its biological source — whole fruit at one end, crystalline chemical at the other
- **F (Function):** what role the ingredient plays in the final product — base ingredient, preservative, emulsifier, flavouring agent, and so on

Each tag is marked as **explicit** (directly inferrable from the variant name) or **could-be** (plausible but not stated — a refined oil does not specify whether solvent extraction or cold pressing preceded the refining step, but either is possible). The validated lists for each field are fixed. If a new process, matter state, or functional class needs adding, it gets flagged and validated — not added ad hoc.

---

## What the tags produce — and what comes next

Once variants are tagged, the EMF scores place each ingredient into one of three zones defined in the manuscript:

- **Zone 1 — Source-attached:** the ingredient is close enough to its source that it is best understood as an expression of it. Mango juice, whole wheat flour, fresh ginger — these are not independent entities, they are forms of their source.
- **Zone 2 — Canonical separation:** the ingredient has moved far enough from its source through processing that it becomes its own canon. Butter is not a variant of milk — it is a separate ingredient that happens to originate from milk. The source relationship is retained as metadata, but the ingredient stands alone.
- **Zone 3 — Functional identity:** the ingredient is defined primarily by what it does rather than what it is. A flavouring agent, a colour, a preservative — these are functional tools. Their source may be documented, but it is secondary to their role in the product.

The scoring itself is mechanical once the tags are in place — each tag maps to a score, bulk calculation assigns each variant to its zone. What is not yet resolved is how the relationships between ingredients across all three zones should be modelled.

---

## Why the relationship structure matters — a concrete example

Consider a food brand that makes mango products and wants to register their ingredients in IFID. Rather than submitting a free-text string like "mango juice concentrate," the system should let them navigate a structured selection:

```
mango
├── plant state:      fruit | kernel
├── matter state:     whole/fresh pieces | pulp/puree | concentrate | 
│                     powder | juice | flakes | extract/oleoresin | ...
├── process:          sorting | washing | chilling | clarification |
│                     cold pressing | refining | solvent extraction | ...
└── functional class: base ingredient | taste profile / spice | 
                      flavouring agent | lipid base | ...
```

They select: source → mango, plant state → fruit, matter state → concentrate, process → clarification, function → taste profile. The frontend renders "mango juice concentrate." The backend stores a set of coordinated tags.

The value is in what this enables on the other side: a researcher or regulator searching `source: mango` retrieves every product using mango in any form. Searching `matter state: concentrate` retrieves every concentrate across all sources. Searching `source: wheat` returns whole wheat flour, refined wheat flour, wheat starch, and wheat protein isolate — even if some of those are Zone 2 canons in their own right. The string "mango juice concentrate" and the string "mango pulp" are no longer isolated — they are connected through shared metadata.

This works cleanly for Zone 1. The modelling gets harder as you move into Zone 2 and Zone 3.

---

## The modelling problem

The system needs to satisfy three requirements simultaneously:

1. **Source and source-derived properties are always retained and searchable** — `source: palm` surfaces every palm derivative including heavily processed fractions, regardless of which zone they sit in
2. **Zone 2 and Zone 3 ingredients are represented by their canon, not collapsed into their source** — butter is butter, not "processed milk"; sodium benzoate is sodium benzoate, not "synthetic preservative from toluene"
3. **Any metadata field is a valid search axis** — `functional_class: preservative` returns everything serving that function across all sources and zones; `process: hydrogenation` returns every hydrogenated ingredient regardless of source

These three requirements are easy to satisfy individually. Satisfying all three in a single schema without either losing the source relationship or obscuring the canonical identity is the problem.

Zone 3 adds a further layer. A flavouring agent is not just an ingredient that flavours — it is a functional node that may reference another ingredient as its mimic source. "Mango flavouring (nature-identical)" is not mango → flavouring agent. It is: flavouring node → type: nature-identical → mimic-source: mango. The ingredient is not mango. It is a synthetic construct that references mango. The same logic applies to colours (beta-carotene as a colour referencing carrot), and potentially others. These are graph relationships, not tree branches.

---

## Open questions for this discussion

1. **Zone placement and schema:** should Zone 1, Zone 2, and Zone 3 ingredients share a single schema with a zone field, or should they have structurally different representations? What are the tradeoffs?

2. **The explicit~could-be distinction:** how should this be represented in the data model — a confidence field on each tag, a parallel could-be array, or something else? It needs to be queryable without polluting explicit data.

3. **Multi-source variants:** `acidity regulator ins 331 ii :: synthetic | corn` has two valid sources. Does the ingredient node carry multiple source values, or does it split into two nodes with different source assignments?

4. **Zone 3 cross-references:** for flavourings, colours, and similar functional ingredients that reference a mimic source — is this a graph edge, a foreign key to the source ingredient's node, or a separate functional taxonomy that ingredients point into?

5. **Source-based search across zones:** what does the schema look like such that `source: wheat` reliably returns Zone 1 variants (whole wheat flour), Zone 2 canons (wheat starch, wheat protein isolate), and Zone 3 functional uses (wheat-derived maltodextrin as a carrier) without requiring three separate queries?

Data modelling, graph database, and taxonomy people especially welcome. This moves to a formal issue once the approach is clearer.

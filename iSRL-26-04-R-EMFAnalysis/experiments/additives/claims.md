---

## Category: Additives & Preservatives

---

### EMFA.C.01 — INS additives with dual plant–animal origin are not required to declare their biological source on Indian product labels, creating an unresolvable gap for consumers with dietary or religious constraints.

- INS numbers (International Numbering System, codified under Codex Alimentarius) identify a food additive by chemical function, not by biological origin. The same INS number can legally refer to a substance produced from entirely different biological sources depending on the manufacturer's supply chain.
- Analysis of 358 INS additive variant labels found in the Indian FMCG corpus identified at least 25 additive entries where the source type is simultaneously plant-origin and animal-origin — meaning the same INS-numbered additive may derive from either source depending on the product and batch.
- The most prevalent example is INS 471 (mono and diglycerides of fatty acids), which is commercially sourced from palm oil, soybean oil, or sunflower oil (plant), but also from tallow (bovine fat) or lard (porcine fat) in other manufacturing contexts. Current FSSAI labeling standards require declaration of the INS number only; disclosure of the specific biological source is not mandated.
- This creates a structural information gap for consumers who make dietary decisions based on source — including vegetarian and vegan consumers, consumers observing religious dietary codes (e.g., halal, kosher, Hindu ahimsa practices), and consumers with medically prescribed diets.
- The gap is legally significant in light of the Ram Gau Raksha Dal ruling, in which the judiciary affirmed that undisclosed use of animal-derived substances in food products sold to consumers who observe religious prohibitions against such substances implicates the right to dignity and religious freedom protected under Articles 21 and 25 of the Constitution of India. The structural ambiguity of dual-origin INS additives means that this disclosure gap is reproducible at scale across the FMCG sector, not confined to any single product or incident.
- **Policy implication:** The biological source of any INS additive with documented plant–animal dual origin should be treated as mandatory label metadata, not optional. Where source varies by batch, a disclosure scheme analogous to the allergen declaration framework would address the gap.

---

### EMFA.C.02 — A recurring pattern of function descriptor–INS number mismatch in Indian FMCG ingredient declarations indicates that the textual function label printed before an INS number is unreliable as a primary signal of additive identity or function.

- Indian FMCG ingredient labels commonly follow the convention of printing a function descriptor alongside the INS number (e.g., "stabilizer ins 415", "acidity regulator ins 330"). This practice implies that the descriptor and the INS number are informationally redundant — that they describe the same substance doing the same thing.
- Systematic analysis of the corpus found multiple instances where the function descriptor on the label does not correspond to any Codex-recognised function of the INS number cited. In the clearest observed case, the descriptor "caramel color" was paired with INS 415 — INS 415 is Xanthan gum, a thickener and stabilizer; caramel colours are INS 150a through 150d, an entirely different class of additives. The two are not related by function, source, or chemistry.
- A further recurring pattern involves INS 451 (Triphosphates) and INS 452 (Polyphosphates) being labeled with the descriptor "humectant". Humectant refers to an additive that retains moisture by attracting water molecules. Phosphates at these INS numbers function as sequestrants and stabilizers; they are not classified as humectants under Codex GSFA, EU food additive regulations, or FSSAI standards. This mismatch was observed across multiple distinct product entries, not a single isolated case.
- The analytical consequence is that the textual descriptor alone cannot be used to determine what additive is present. The INS number is the only unambiguous identifier, but it requires cross-referencing against an external regulatory database to interpret — a step not available to the average consumer at point of purchase.
- **Policy implication:** Where an INS number is declared, the INS number should be treated as the authoritative identifier and the function descriptor as secondary and unverified. Any automated processing of ingredient lists for allergen tracking, dietary classification, or regulatory compliance should resolve function from INS number, not from the text descriptor.

---

### EMFA.C.03 — A subset of INS numbers found on Indian product labels cannot be verified against any recognised regulatory database, meaning the declared additive identity is unresolvable from the label alone.

- INS numbers have defined ranges and are maintained by the Codex Alimentarius Commission (CAC). A valid INS number maps uniquely to an officially named additive with known functions. An INS number that falls outside the defined ranges, or that is not present in the Codex GSFA, EU additive database, or FSSAI permitted additives list, cannot be resolved to an additive identity.
- The corpus contained label strings citing INS 4806 (appearing in two distinct product entries as "emulsifier" and "stabilizer"), INS 4726 (appearing as "emulsifier"), INS 196 (appearing as "acidity regulator"), and INS 1223 (appearing as "flour treatment agent"). None of these numbers are present in the Codex GSFA, EU food additive database, or FSSAI consolidated list. Cross-checking against adjacent valid INS numbers suggests these may be transcription errors (e.g., INS 4726 may correspond to the 472-series acetic/citric acid esters of monoglycerides; INS 4806 may correspond to the 48x-series phosphates), but no definitive correction is possible from the label text alone.
- Additionally, the label string "cucumber seed ins 396" was observed in the corpus. INS 396 is not a recognised Codex number, and "cucumber seed" is not a classified food additive. This entry is unresolvable as an additive declaration under any current regulatory framework.
- An unverifiable INS number on a label means that the additive identity, function, source, and safety assessment cannot be determined by a third party — including inspectors, researchers, and consumers — using publicly available regulatory references.
- **Policy implication:** Label declarations citing INS numbers outside the recognised Codex range should be subject to mandatory correction as part of FSSAI compliance review. A published, machine-readable mapping of all FSSAI-permitted INS numbers would enable automated detection of such entries at scale.

---

### EMFA.C.04 — INS numbers as printed on Indian product labels frequently contain formatting and transcription errors that alter the number to reference a different or non-existent additive, without any visible indication of error to the reader.

- The corpus analysis identified 27 INS number corrections across 358 additive label entries — approximately 1 in 13 INS declarations required correction to match a valid Codex number. Error types include: appended digits (e.g., 3410 instead of 341, 5030 instead of 503, 4401 instead of 440, 4700 instead of 470, 6351 instead of 635), truncated numbers (e.g., INS 10 instead of 100, INS 30 instead of 300), EU E-number prefix carried over into INS format (e.g., "ins e330" instead of "ins 330", "ins e440" instead of "ins 440"), and sub-variant suffixes used inconsistently (e.g., 420i, 500 i, 341 iii with varying spacing and suffix conventions).
- An appended digit error is particularly significant because it does not produce an obviously malformed number — "ins 3410" reads as a plausible four-digit INS number, but INS 3410 does not exist; the intended additive is INS 341 (Calcium phosphates). A reader without access to a Codex reference list has no basis to identify the error.
- The errors do not cluster around a single INS range or additive category, suggesting they arise from multiple independent sources rather than a single systemic transcription event.
- These are transcription-layer errors in the declared number, distinct from the descriptor-number mismatches described in EMFA.C.02. A label can have a correctly spelled descriptor and a numerically incorrect INS, or a correct INS and an incorrect descriptor, or both correct.
- **Policy implication:** INS number validity (existence in Codex GSFA) is a checkable constraint that could be enforced programmatically at the label approval stage. A validation step requiring each declared INS number to resolve to a recognised Codex entry would eliminate this class of error before products reach retail.

---

### EMFA.C.05 — The same INS-numbered additive is declared under a wide range of different function descriptors across products, indicating that function descriptor vocabulary on Indian FMCG labels is not standardised and is used inconsistently across the sector.

- Each INS number corresponds to one or more Codex-recognised functions. While it is legitimate for a single additive to perform different functions in different food matrices (e.g., a phosphate used as a sequestrant in one product and a stabilizer in another), the function descriptor on the label is expected to reflect the specific function in that specific product.
- Analysis of the corpus found that 153 unique additives are represented by 358 distinct label strings — an average of 2.34 label representations per additive. Of 153 unique INS numbers, 78 (51%) appear under two or more different descriptor labels. INS 341 (Calcium phosphates) was found under 13 different descriptors in the corpus, including "stabilizer", "acidity regulator", "preservative", "raising agent", "anticaking agent", "texturizer", and "aregulators" (a likely typographic fragment of "acidity regulators"). INS 330 (Citric acid) appeared as "antioxidant", "acidifying agent", "acidity regulator", and "preservative" across different products.
- The variation is not uniformly explained by legitimate function differences across food matrices. "Preservative" is not a Codex-recognised function of INS 341 or INS 330 under any food category, yet both appear under that descriptor in the corpus.
- From a data infrastructure perspective, this means that the function descriptor field in an ingredient declaration cannot be used as a reliable grouping or classification signal without first resolving each entry to its corrected INS number and then looking up the official function from a regulatory reference.
- **Policy implication:** Standardisation of the permitted function descriptor vocabulary for each INS number — consistent with the Codex GSFA permitted uses — would improve the interpretability of ingredient declarations for downstream regulatory processing, allergen management systems, and public-facing transparency tools.


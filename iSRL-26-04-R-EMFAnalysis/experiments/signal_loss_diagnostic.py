"""
signal_loss_diagnostic.py
─────────────────────────
Deep Signal-Loss Diagnostic — Collision Taxonomy Across Full Corpus

Classifies every collision group into:
  Type A  — NULL field, could_be has alternatives
  Type B  — Value too broad/generic
  Type C  — Multi-value compound (pipe-separated field)
  Type D  — Legitimate linguistic duplicate

Run from the experiments/ directory:
    python signal_loss_diagnostic.py
"""

import csv
import itertools
from collections import defaultdict

# ── Configuration ─────────────────────────────────────────────────────────────
CSV_PATH               = '../tagged_variants.csv'
MIN_SOURCE_SIZE        = 2      # only analyse sources with ≥ 2 variants
TARGET_SOURCES         = 100    # report on at least this many sources
LEVENSHTEIN_THRESHOLD  = 3      # edit-distance for Type D (linguistic duplicates)

# ── Helpers ───────────────────────────────────────────────────────────────────

def tag(val):
    """Return None for 'NULL' strings, else the raw string."""
    return None if (val is None or val.strip() == 'NULL' or val.strip() == '') else val.strip()


def levenshtein(a, b):
    """Pure-Python Levenshtein distance (no external deps)."""
    a, b = a.lower(), b.lower()
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            curr.append(min(prev[j] + 1,
                            curr[j - 1] + 1,
                            prev[j - 1] + (0 if ca == cb else 1)))
        prev = curr
    return prev[-1]


def pipe_vals(val):
    """Split a pipe-separated field into a set of stripped values."""
    if val is None:
        return set()
    return {v.strip() for v in val.split('|') if v.strip() and v.strip() != 'NULL'}


def has_pipe(val):
    return val is not None and '|' in val


# ── Step 1: Build collision registry ─────────────────────────────────────────
# records[source][variant] = full_row_dict
records = defaultdict(dict)

with open(CSV_PATH, newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        sources = [s.strip() for s in row['source'].split('|') if s.strip()]
        for src in sources:
            records[src][row['variant']] = row

print(f"Total sources loaded: {len(records)}")

# ── Step 2: Select analysis scope ─────────────────────────────────────────────
# Sort sources by variant count descending; keep those with ≥ MIN_SOURCE_SIZE
# and take enough to cover ≥ TARGET_SOURCES sources
sorted_sources = sorted(
    [(src, len(variants)) for src, variants in records.items() if len(variants) >= MIN_SOURCE_SIZE],
    key=lambda x: -x[1]
)
# Always take all sources that qualify; ensure ≥ TARGET_SOURCES
analysed_sources = [src for src, _ in sorted_sources]
print(f"Sources with ≥ {MIN_SOURCE_SIZE} variants: {len(analysed_sources)}")
if len(analysed_sources) < TARGET_SOURCES:
    print(f"  (All qualify — fewer than {TARGET_SOURCES} sources total)")

# ── Step 3: Build collision groups per source ─────────────────────────────────
def emf_key(row):
    return (tag(row['e_explicit']), tag(row['m_explicit']), tag(row['f_explicit']))

def build_collision_groups(src):
    """Return list of (emf_key, [variant, ...]) for groups with ≥ 2 variants."""
    groups = defaultdict(list)
    for variant, row in records[src].items():
        groups[emf_key(row)].append(variant)
    return [(k, vs) for k, vs in groups.items() if len(vs) >= 2]

# ── Step 4: Classify each collision group ─────────────────────────────────────

def classify_group(src, key, variants):
    """
    Return a dict with classification results for this collision group.
    Classification priority: D → C → A → B
    A group can receive multiple types (mixed).
    """
    e_key, m_key, f_key = key
    rows = [records[src][v] for v in variants]

    types    = []
    subtypes = []

    # ── Type D: linguistic duplicates ────────────────────────────────────────
    is_d = False
    if len(variants) >= 2:
        pairs = list(itertools.combinations(variants, 2))
        dists = [levenshtein(a, b) for a, b in pairs]
        # All pairwise within threshold → D
        if all(d <= LEVENSHTEIN_THRESHOLD for d in dists):
            is_d = True
        else:
            # Substring / word-order heuristic: share dominant token
            token_sets = [set(v.lower().split()) for v in variants]
            common = token_sets[0]
            for ts in token_sets[1:]:
                common &= ts
            if common:  # non-empty intersection of tokens → likely linguistic dup
                is_d = True
    if is_d:
        types.append('D')

    # ── Type C: multi-value compound ─────────────────────────────────────────
    is_c = False
    pipe_count = sum(1 for f in [e_key, m_key, f_key] if has_pipe(f))
    if pipe_count >= 1:
        is_c = True
        types.append('C')
        subtypes.append('C2' if pipe_count >= 2 else 'C1')

    # ── Type A: NULL-driven collision, could_be has alternatives ──────────────
    null_fields = []
    if e_key is None: null_fields.append('e')
    if m_key is None: null_fields.append('m')
    if f_key is None: null_fields.append('f')

    is_a = False
    a_subtypes = []
    if null_fields:
        e_hints = any(pipe_vals(r['e_could_be']) for r in rows) if e_key is None else False
        m_hints = any(pipe_vals(r['m_could_be']) for r in rows) if m_key is None else False
        if e_hints or m_hints:
            is_a = True
            if e_hints and m_hints:
                a_subtypes.append('A3')
            elif e_hints:
                a_subtypes.append('A1')
            else:
                a_subtypes.append('A2')
    if is_a:
        types.append('A')
        subtypes.extend(a_subtypes)

    # ── Type B: value too broad (default when no other type) ──────────────────
    is_b = False
    b_subtypes = []
    # Check how many sources share this exact emf key (cross-source overloading)
    # We'll populate this later in a post-processing pass; use placeholder here.
    BROAD_M_TOKENS = {'powder', 'oil', 'liquid', 'paste', 'flake', 'flakes',
                      'granule', 'granules', 'concentrate', 'extract', 'blend',
                      'crystalline chemical', 'additive', 'base', 'raw',
                      'solid', 'gel', 'emulsifier powder', 'flour'}
    BROAD_F_TOKENS = {'base ingredient', 'ingredient', 'additive', 'processing aid'}

    if m_key and m_key.lower() in BROAD_M_TOKENS:
        is_b = True
        b_subtypes.append('B1')
    if f_key and f_key.lower() in BROAD_F_TOKENS:
        is_b = True
        b_subtypes.append('B2')
    # B3 (cross-source overloading) added in post-processing
    if is_b:
        if 'B' not in types:
            types.append('B')
        subtypes.extend(b_subtypes)

    # Default: if no type assigned, call it B (too broad / unknown)
    if not types:
        types.append('B')
        subtypes.append('B?')

    return {
        'source'    : src,
        'emf_key'   : key,
        'n_variants': len(variants),
        'variants'  : variants,
        'types'     : types,
        'subtypes'  : subtypes,
        'null_fields': null_fields,
        'is_mixed'  : len(types) > 1,
    }

# ── Step 5: NULL analysis per collision group ─────────────────────────────────

def null_analysis(src, key, variants):
    """
    For each NULL field in the emf_key, determine:
      - What could_be values exist across variants in the group?
      - Would filling from could_be break the tie?
    Returns dict with per-field fillability.
    """
    e_key, m_key, f_key = key
    rows = [records[src][v] for v in variants]

    result = {}
    for field, key_val, could_be_col in [
            ('e', e_key, 'e_could_be'),
            ('m', m_key, 'm_could_be'),
            ('f', f_key, 'f_could_be'),
    ]:
        if key_val is not None:
            result[field] = {'null': False}
            continue
        # Field is NULL — inspect could_be
        could_be_sets = [pipe_vals(r[could_be_col]) for r in rows]
        all_hints = set().union(*could_be_sets)
        per_variant = {v: pipe_vals(rows[i][could_be_col])
                       for i, v in enumerate(variants)}
        if not all_hints:
            fillability = 'no_hint'
        else:
            # Would variants get different could_be values → disambiguating
            unique_sets = set(frozenset(s) for s in could_be_sets)
            if len(unique_sets) > 1:
                fillability = 'fillable'
            else:
                fillability = 'still_ambiguous'
        result[field] = {
            'null'       : True,
            'hints'      : sorted(all_hints),
            'per_variant': per_variant,
            'fillability': fillability,
        }
    return result

# ── Step 6: Multiselect simulation ───────────────────────────────────────────

def multiselect_simulation(src, key, variants):
    """
    Expand each field by unioning e_explicit + e_could_be.
    Return True if variants now have distinct expanded keys.
    """
    e_key, m_key, f_key = key
    rows = [records[src][v] for v in variants]

    def expanded_key(row):
        e = pipe_vals(row['e_explicit']) | pipe_vals(row['e_could_be'])
        m = pipe_vals(row['m_explicit']) | pipe_vals(row['m_could_be'])
        f = pipe_vals(row['f_explicit']) | pipe_vals(row['f_could_be'])
        return (frozenset(e), frozenset(m), frozenset(f))

    expanded_keys = [expanded_key(r) for r in rows]
    # Resolved if all expanded keys are distinct
    return len(set(expanded_keys)) == len(variants)

# ── Build full collision registry ─────────────────────────────────────────────
all_collision_groups = []   # list of enriched group dicts

for src in analysed_sources:
    cg = build_collision_groups(src)
    for key, variants in cg:
        group = classify_group(src, key, variants)
        group['null_detail']           = null_analysis(src, key, variants)
        group['multiselect_resolves']  = multiselect_simulation(src, key, variants)
        all_collision_groups.append(group)

print(f"Total collision groups found: {len(all_collision_groups)}")

# ── Post-processing: add B3 (cross-source overloading) ───────────────────────
# Count how many sources have each emf_key as a collision
emf_source_collision_count = defaultdict(int)
for g in all_collision_groups:
    emf_source_collision_count[g['emf_key']] += 1

for g in all_collision_groups:
    cross_count = emf_source_collision_count[g['emf_key']]
    if cross_count >= 3:  # same emf_key collides in 3+ independent sources
        if 'B' not in g['types']:
            g['types'].append('B')
        if 'B3' not in g['subtypes']:
            g['subtypes'].append('B3')
        g['is_mixed'] = len(g['types']) > 1

# ── Step 7: Type B deep dive (top 30 most-colliding) ─────────────────────────

def type_b_deep_dive(groups, top_n=30):
    """
    For the top-N Type B groups by n_variants, identify distinguishing tokens
    in variant names that are absent from EMF fields, and propose a fix.
    """
    b_groups = [g for g in groups if 'B' in g['types']]
    b_groups.sort(key=lambda g: -g['n_variants'])
    results = []

    for g in b_groups[:top_n]:
        e_key, m_key, f_key = g['emf_key']
        emf_tokens = set()
        for val in [e_key, m_key, f_key]:
            if val:
                emf_tokens.update(val.lower().split())

        # Tokens in variant names not in any emf field
        extra_tokens = {}
        for v in g['variants']:
            vtokens = set(v.lower().replace('-', ' ').split())
            diff = vtokens - emf_tokens
            if diff:
                extra_tokens[v] = sorted(diff)

        # Heuristic: detect INS numbers (digits in name)
        has_ins = any(any(c.isdigit() for c in v) for v in g['variants'])

        # Propose fix
        if has_ins:
            proposal = "Add chemical_id / INS_number tag to distinguish additives by code"
        elif extra_tokens:
            sample_extras = sorted({t for ts in extra_tokens.values() for t in ts})[:5]
            proposal = f"Finer tag needed — distinguishing tokens: {sample_extras}"
        else:
            proposal = "Taxonomy sub-category or qualifier needed"

        results.append({
            'source'      : g['source'],
            'emf_key'     : g['emf_key'],
            'n_variants'  : g['n_variants'],
            'variants'    : g['variants'],
            'subtypes'    : g['subtypes'],
            'extra_tokens': extra_tokens,
            'proposal'    : proposal,
        })
    return results

type_b_analysis = type_b_deep_dive(all_collision_groups)

# ── Step 8: Summary Reports ───────────────────────────────────────────────────

SEP  = '─' * 100
SEP2 = '═' * 100

# ── 8a: Per-collision-group table ────────────────────────────────────────────
print(f"\n{SEP2}")
print("REPORT 8a — Per-Collision-Group Table (all groups)")
print(SEP2)
hdr = (f"{'source':<25} {'emf_key':<55} {'n':>3} "
       f"{'type':<8} {'subtype':<12} {'null_fields':<12} "
       f"{'fillable':<14} {'ms_resolves'}")
print(hdr)
print(SEP)

def fillable_summary(null_detail):
    """Summarise fillability across all NULL fields."""
    statuses = []
    for field in ('e', 'm', 'f'):
        info = null_detail.get(field, {})
        if info.get('null'):
            statuses.append(info.get('fillability', 'no_hint'))
    if not statuses:
        return 'n/a'
    if 'fillable' in statuses:
        return 'fillable'
    if 'still_ambiguous' in statuses:
        return 'ambiguous'
    return 'no_hint'

for g in sorted(all_collision_groups, key=lambda x: (x['source'], str(x['emf_key']))):
    e_k, m_k, f_k = g['emf_key']
    key_str = f"e={e_k or 'NULL'}, m={m_k or 'NULL'}, f={f_k or 'NULL'}"
    type_str    = '+'.join(sorted(set(g['types'])))
    subtype_str = ','.join(g['subtypes']) if g['subtypes'] else '-'
    null_str    = ','.join(g['null_fields']) if g['null_fields'] else '-'
    fill_str    = fillable_summary(g['null_detail'])
    ms_str      = 'yes' if g['multiselect_resolves'] else 'no'

    print(f"{g['source']:<25} {key_str:<55} {g['n_variants']:>3} "
          f"{type_str:<8} {subtype_str:<12} {null_str:<12} "
          f"{fill_str:<14} {ms_str}")

# ── 8b: Aggregate type distribution ──────────────────────────────────────────
print(f"\n{SEP2}")
print("REPORT 8b — Aggregate Type Distribution")
print(SEP2)

type_counts    = defaultdict(int)
subtype_counts = defaultdict(int)
mixed_count    = 0

for g in all_collision_groups:
    for t in g['types']:
        type_counts[t] += 1
    for st in g['subtypes']:
        subtype_counts[st] += 1
    if g['is_mixed']:
        mixed_count += 1

total_groups = len(all_collision_groups)
print(f"Total collision groups: {total_groups}\n")

for t in sorted(type_counts):
    n = type_counts[t]
    pct = 100 * n / total_groups if total_groups else 0
    label = {
        'A': 'NULL-driven (could_be has alternatives)',
        'B': 'Too broad/generic',
        'C': 'Multi-value compound (pipe-separated)',
        'D': 'Linguistic duplicate (correct behaviour)',
    }.get(t, '')
    print(f"  Type {t}: {n:4d} groups ({pct:5.1f}%)  — {label}")

print(f"\n  Mixed types: {mixed_count:4d} groups ({100*mixed_count/total_groups:5.1f}%)\n")

print("  Sub-type breakdown:")
for st in sorted(subtype_counts):
    n = subtype_counts[st]
    desc = {
        'A1': 'e is NULL, e_could_be exists',
        'A2': 'm is NULL, m_could_be exists',
        'A3': 'both e and m NULL with could_be hints',
        'B1': 'm_explicit too broad',
        'B2': 'f_explicit too broad',
        'B3': 'cross-source EMF overloading (≥3 sources)',
        'B?': 'broad (unclassified sub-type)',
        'C1': 'one field is compound (partial)',
        'C2': 'two+ fields are compound (complex)',
    }.get(st, '')
    print(f"    {st}: {n:4d}  — {desc}")

ms_resolves_count = sum(1 for g in all_collision_groups
                        if g['multiselect_resolves'] and
                        ('A' in g['types'] or 'C' in g['types']))
print(f"\n  Multiselect-resolved (Type A or C): {ms_resolves_count} groups")

# ── 8c: Per-source summary ───────────────────────────────────────────────────
print(f"\n{SEP2}")
print(f"REPORT 8c — Per-Source Summary (top {TARGET_SOURCES}+ sources)")
print(SEP2)

# Build per-source stats
source_stats = defaultdict(lambda: {
    'total_variants': 0, 'collision_groups': 0,
    'type_A': 0, 'type_B': 0, 'type_C': 0, 'type_D': 0,
})

for src in analysed_sources:
    source_stats[src]['total_variants'] = len(records[src])

for g in all_collision_groups:
    src = g['source']
    source_stats[src]['collision_groups'] += 1
    for t in g['types']:
        source_stats[src][f'type_{t}'] += 1

hdr2 = (f"{'source':<30} {'variants':>9} {'coll_grps':>10} "
        f"{'A':>5} {'B':>5} {'C':>5} {'D':>5} {'compression':>12}")
print(hdr2)
print(SEP)

# Sort sources by total_variants desc; show top TARGET_SOURCES
shown = 0
for src, _ in sorted_sources[:max(TARGET_SOURCES, len(sorted_sources))]:
    ss = source_stats[src]
    total = ss['total_variants']
    if total == 0:
        continue
    # unique EMF combos for this source
    groups = defaultdict(list)
    for variant, row in records[src].items():
        groups[emf_key(row)].append(variant)
    unique_emf = len(groups)
    compression = unique_emf / total if total else 1.0
    cg = ss['collision_groups']
    flag = ' **' if cg > 0 else ''
    print(f"{src:<30} {total:>9} {cg:>10} "
          f"{ss['type_A']:>5} {ss['type_B']:>5} {ss['type_C']:>5} {ss['type_D']:>5} "
          f"{compression:>12.4f}{flag}")
    shown += 1

print(f"\n({shown} sources shown)")

# ── 8d: Actionable Tagging Recommendations ───────────────────────────────────
print(f"\n{SEP2}")
print("REPORT 8d — Actionable Tagging Recommendations")
print(SEP2)

# ── 8d-A: Top-10 (source, null_field) pairs where adding from could_be resolves most collisions
print("\n[Type A] Top sources where filling NULL from could_be would resolve collisions:")
print(f"  {'source':<30} {'null_field':<12} {'fillable_groups':>16} {'total_A_groups':>15}")
print(f"  {'-'*30} {'-'*12} {'-'*16} {'-'*15}")

source_null_fillable = defaultdict(lambda: defaultdict(lambda: {'fillable': 0, 'total': 0}))
for g in all_collision_groups:
    if 'A' not in g['types']:
        continue
    src = g['source']
    for field in ('e', 'm', 'f'):
        info = g['null_detail'].get(field, {})
        if info.get('null'):
            source_null_fillable[src][field]['total'] += 1
            if info.get('fillability') == 'fillable':
                source_null_fillable[src][field]['fillable'] += 1

ranked_A = []
for src, fields in source_null_fillable.items():
    for field, counts in fields.items():
        ranked_A.append((src, field, counts['fillable'], counts['total']))
ranked_A.sort(key=lambda x: -x[2])

for src, field, fillable, total in ranked_A[:10]:
    print(f"  {src:<30} {field:<12} {fillable:>16} {total:>15}")

# ── 8d-B: Top-10 over-generic EMF keys
print("\n[Type B] Top overly-generic EMF keys by collision count:")
print(f"  {'emf_key':<60} {'collision_groups':>17} {'total_variants':>15} {'proposed_fix'}")
print(f"  {'-'*60} {'-'*17} {'-'*15}")

emf_b_stats = defaultdict(lambda: {'groups': 0, 'variants': 0, 'proposals': set()})
for g in all_collision_groups:
    if 'B' not in g['types']:
        continue
    k = g['emf_key']
    emf_b_stats[k]['groups'] += 1
    emf_b_stats[k]['variants'] += g['n_variants']

# Get proposals from type_b_analysis
for item in type_b_analysis:
    k = item['emf_key']
    emf_b_stats[k]['proposals'].add(item['proposal'])

ranked_B = sorted(emf_b_stats.items(), key=lambda x: -x[1]['groups'])
for k, stats in ranked_B[:10]:
    e_k, m_k, f_k = k
    key_str = f"e={e_k or 'NULL'}, m={m_k or 'NULL'}, f={f_k or 'NULL'}"
    proposals = '; '.join(stats['proposals']) if stats['proposals'] else '—'
    print(f"  {key_str:<60} {stats['groups']:>17} {stats['variants']:>15}")
    print(f"    → {proposals}")

# ── 8d-C: All multi-value (Type C) groups
print("\n[Type C] Multi-value compound groups and whether splitting resolves them:")
c_groups = [g for g in all_collision_groups if 'C' in g['types']]
c_groups.sort(key=lambda g: (g['source'], str(g['emf_key'])))
print(f"  {'source':<25} {'emf_key':<55} {'n':>3} {'subtype':<5} {'ms_resolves'}")
print(f"  {'-'*25} {'-'*55} {'-'*3} {'-'*5} {'-'*11}")
for g in c_groups:
    e_k, m_k, f_k = g['emf_key']
    key_str = f"e={e_k or 'NULL'}, m={m_k or 'NULL'}, f={f_k or 'NULL'}"
    st = ','.join([s for s in g['subtypes'] if s.startswith('C')]) or '-'
    ms = 'yes' if g['multiselect_resolves'] else 'no'
    print(f"  {g['source']:<25} {key_str:<55} {g['n_variants']:>3} {st:<5} {ms}")

# ── 8d-D: Confirmed linguistic duplicates
print("\n[Type D] Confirmed linguistic-duplicate groups (no fix needed):")
d_groups = [g for g in all_collision_groups if 'D' in g['types']]
d_groups.sort(key=lambda g: g['source'])
print(f"  {'source':<25} {'emf_key':<45} {'variants'}")
print(f"  {'-'*25} {'-'*45} {'-'*40}")
for g in d_groups:
    e_k, m_k, f_k = g['emf_key']
    key_str = f"e={e_k or 'NULL'}, m={m_k or 'NULL'}, f={f_k or 'NULL'}"
    variant_str = ' | '.join(g['variants'])
    print(f"  {g['source']:<25} {key_str:<45} {variant_str}")

# ── Type B deep-dive report ───────────────────────────────────────────────────
print(f"\n{SEP2}")
print("REPORT 7 — Type B Deep Dive (top 30 most-colliding groups)")
print(SEP2)
for i, item in enumerate(type_b_analysis, 1):
    e_k, m_k, f_k = item['emf_key']
    key_str = f"e={e_k or 'NULL'}, m={m_k or 'NULL'}, f={f_k or 'NULL'}"
    print(f"\n  [{i:02d}] source={item['source']}  n_variants={item['n_variants']}")
    print(f"       emf_key : {key_str}")
    print(f"       subtypes: {item['subtypes']}")
    print(f"       variants: {', '.join(item['variants'][:10])}{'...' if len(item['variants']) > 10 else ''}")
    if item['extra_tokens']:
        for v, extras in list(item['extra_tokens'].items())[:5]:
            print(f"         extra tokens in '{v}': {extras}")
    print(f"       proposal: {item['proposal']}")

# ── Verification summary ──────────────────────────────────────────────────────
print(f"\n{SEP2}")
print("VERIFICATION")
print(SEP2)
print(f"  Total collision groups        : {total_groups}  (expected ~394)")
print(f"  Sources analysed              : {shown}  (expected ≥ 100)")
print(f"  Type D (linguistic dup)       : {type_counts['D']}  (should include amchur/amchoor etc.)")
print(f"  Type A (NULL-driven)          : {type_counts['A']}  (expected substantial given 64.9% e_explicit NULL)")
print(f"  Multiselect resolves          : {ms_resolves_count}  (expected ≤ Type A + C)")
print(f"  Type A + C count              : {type_counts['A'] + type_counts['C']}")
print(f"  Multiselect ≤ A+C constraint  : {'PASS' if ms_resolves_count <= type_counts['A'] + type_counts['C'] else 'FAIL'}")
print()

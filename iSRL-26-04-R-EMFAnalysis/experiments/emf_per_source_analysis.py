import csv
from collections import defaultdict

CSV_PATH = '../tagged_variants.csv'
FOCUS_SOURCES = {'milk', 'mango', 'palm'}

def tag(val):
    return None if val == 'NULL' else val

# ── Step 1: build per-source buckets ─────────────────────────────────────────
# source_buckets[source][variant] = (e, m, f)
source_buckets = defaultdict(dict)

with open(CSV_PATH) as f:
    for row in csv.DictReader(f):
        sources = [s.strip() for s in row['source'].split('|')]
        emf = (tag(row['e_explicit']), tag(row['m_explicit']), tag(row['f_explicit']))
        for src in sources:
            source_buckets[src][row['variant']] = emf

print(f"Total sources: {len(source_buckets)}")
print(f"Source sizes: { {s: len(v) for s, v in source_buckets.items()} }\n")


# ── Step 2: per-source duplicate / collision analysis ────────────────────────
def analyze_source(source, bucket):
    """Return (groups_by_emf, collisions)."""
    groups = defaultdict(list)
    for variant, emf in bucket.items():
        groups[emf].append(variant)
    collisions = {emf: variants for emf, variants in groups.items() if len(variants) > 1}
    return groups, collisions


def print_source_report(source, bucket, show_full_dict=True):
    groups, collisions = analyze_source(source, bucket)
    total = len(bucket)
    unique_emf = len(groups)
    rate = unique_emf / total if total else 0
    print(f"{'='*60}")
    print(f"SOURCE: {source}  (total variants: {total})")
    print(f"  Unique EMF combos : {unique_emf}")
    print(f"  Compression rate  : {rate:.4f}  ({'no duplicates' if rate == 1.0 else 'DUPLICATES EXIST'})")

    if show_full_dict:
        print(f"\n  Variant → (e, m, f):")
        for variant, emf in sorted(bucket.items()):
            print(f"    {variant!r:45s} → {emf}")

    print(f"\n  Groups by EMF (sorted by size desc):")
    for emf, variants in sorted(groups.items(), key=lambda x: -len(x[1])):
        print(f"    {str(emf):55s} → {len(variants)} variant(s): {variants}")

    if collisions:
        print(f"\n  COLLISIONS ({len(collisions)} EMF combo(s) shared by >1 variant):")
        for emf, variants in collisions.items():
            print(f"    EMF={emf}  →  {variants}")
    else:
        print(f"\n  No collisions — (source, EMF) is lossless for this source.")
    print()


# Focus sources
for src in sorted(FOCUS_SOURCES):
    if src in source_buckets:
        print_source_report(src, source_buckets[src], show_full_dict=True)
    else:
        print(f"Source '{src}' not found in corpus.")


# ── Step 3 & 4: corpus-wide compression + signal loss ────────────────────────
print(f"\n{'#'*60}")
print("CORPUS-WIDE ANALYSIS")
print(f"{'#'*60}\n")

total_variant_source_pairs = 0
total_unique_emf_combos = 0
all_source_emf_pairs = {}       # (source, emf) → [variants]
collision_cases = []

summary_rows = []

for source, bucket in source_buckets.items():
    groups, collisions = analyze_source(source, bucket)
    n_variants = len(bucket)
    n_emf = len(groups)
    rate = n_emf / n_variants if n_variants else 0

    total_variant_source_pairs += n_variants
    total_unique_emf_combos += n_emf

    for emf, variants in collisions.items():
        collision_cases.append({'source': source, 'emf': emf, 'variants': variants})

    summary_rows.append({
        'source': source,
        'total_variants': n_variants,
        'unique_emf_combos': n_emf,
        'compression_rate': rate,
        'collisions': len(collisions),
    })

    for emf, variants in groups.items():
        key = (source, emf)
        all_source_emf_pairs[key] = variants

global_compression = len(all_source_emf_pairs) / total_variant_source_pairs if total_variant_source_pairs else 0

print(f"Total variant-source pairs         : {total_variant_source_pairs}")
print(f"Unique (source, EMF) pairs         : {len(all_source_emf_pairs)}")
print(f"Global compression rate            : {global_compression:.4f}")
print(f"Total collision EMF combos         : {len(collision_cases)}")
print(f"Lossless globally?                 : {len(collision_cases) == 0}\n")


# ── Step 5: summary table ────────────────────────────────────────────────────
print(f"{'source':<30} {'total_variants':>15} {'unique_emf_combos':>18} {'compression_rate':>17} {'collisions':>11}")
print('-' * 95)
for r in sorted(summary_rows, key=lambda x: x['source']):
    flag = ' **' if r['collisions'] > 0 else ''
    print(f"{r['source']:<30} {r['total_variants']:>15} {r['unique_emf_combos']:>18} {r['compression_rate']:>17.4f} {r['collisions']:>11}{flag}")

print(f"\n{'TOTAL':<30} {total_variant_source_pairs:>15} {len(all_source_emf_pairs):>18} {global_compression:>17.4f} {len(collision_cases):>11}")


# ── Collision detail ──────────────────────────────────────────────────────────
if collision_cases:
    print(f"\n{'='*60}")
    print("COLLISION DETAILS (signal loss cases)")
    print(f"{'='*60}")
    for c in collision_cases:
        print(f"  Source: {c['source']}")
        print(f"  EMF   : {c['emf']}")
        print(f"  Variants sharing this key: {c['variants']}")
        print()

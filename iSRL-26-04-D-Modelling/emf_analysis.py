"""
EMF Analysis Script — iSRL-26-04-R-EMFAnalysis
Answers all zone/source/score questions for the tagged_variants dataset.
"""

import pandas as pd
import numpy as np
from scipy import stats
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

DATA = '/home/lalithakanha/sandbox-research/iSRL-26-04-R-EMFAnalysis/tagged_variants.csv'

df = pd.read_csv(DATA, na_values=['NULL', ''])

# Normalise booleans
for col in ['uncertain', 'question_tags']:
    df[col] = df[col].map({'True': True, 'False': False, True: True, False: False}).fillna(False).astype(bool)

# Derived column: source count
df['source_count'] = df['source'].fillna('').apply(
    lambda x: len([s for s in x.split('|') if s.strip()]) if x else 0
)
df['d_gap'] = df['d_max'] - df['d_min']

SEP = '=' * 70

def header(title):
    print(f'\n{SEP}')
    print(f'  {title}')
    print(SEP)

# ─────────────────────────────────────────────────────────────────
# SECTION 1 — SOURCE COMPLEXITY VS ZONE
# ─────────────────────────────────────────────────────────────────
header('SECTION 1: SOURCE COMPLEXITY VS ZONE')

print('\n── 1a. Mean, median, distribution of source count per zone ──')
for zone in [1, 2, 3]:
    zdf = df[df['zone'] == zone]['source_count']
    dist = zdf.value_counts().sort_index().to_dict()
    print(f'\n  Zone {zone} (n={len(zdf)}):')
    print(f'    mean={zdf.mean():.3f}  median={zdf.median():.1f}  std={zdf.std():.3f}')
    print(f'    distribution: {dist}')

print('\n── 1b. Fraction of multi-source variants per zone ──')
multi = df[df['source_count'] > 1]
for zone in [1, 2, 3]:
    total = (df['zone'] == zone).sum()
    m = ((df['zone'] == zone) & (df['source_count'] > 1)).sum()
    print(f'  Zone {zone}: {m}/{total} = {m/total*100:.1f}%')

# Chi-squared test: zone 1 vs zone 3 multi-source proportions
z1 = df[df['zone'] == 1]
z3 = df[df['zone'] == 3]
ct = pd.crosstab(df[df['zone'].isin([1,3])]['zone'],
                 (df[df['zone'].isin([1,3])]['source_count'] > 1))
chi2, p, dof, _ = stats.chi2_contingency(ct)
print(f'  Chi-squared (zone1 vs zone3 multi-source): χ²={chi2:.3f}, p={p:.4f}')

print('\n── 1c. Zone distribution for exactly-2 vs 3+ sources ──')
for sc, label in [(2, 'exactly 2 sources'), (None, '3+ sources')]:
    if sc:
        sub = df[df['source_count'] == sc]
    else:
        sub = df[df['source_count'] >= 3]
    if len(sub) == 0:
        print(f'  {label}: no variants')
        continue
    zdist = sub['zone'].value_counts().sort_index()
    print(f'\n  {label} (n={len(sub)}):')
    for z, cnt in zdist.items():
        print(f'    Zone {z}: {cnt} ({cnt/len(sub)*100:.1f}%)')

print('\n── 1d. Top source combinations and their zone concentration ──')
combo_records = []
for _, row in df.iterrows():
    if pd.isna(row['source']) or row['source'] == '':
        continue
    parts = sorted([s.strip() for s in str(row['source']).split('|') if s.strip()])
    if len(parts) > 1:
        combo_records.append((' | '.join(parts), row['zone']))

combo_df = pd.DataFrame(combo_records, columns=['combo', 'zone'])
top_combos = combo_df['combo'].value_counts().head(15)
print(f'\n  Top 15 multi-source combos:')
for combo, cnt in top_combos.items():
    zdist = combo_df[combo_df['combo'] == combo]['zone'].value_counts().sort_index().to_dict()
    print(f'    [{cnt:3d}]  {combo}  →  zones: {zdist}')

# ─────────────────────────────────────────────────────────────────
# SECTION 2 — PER-SOURCE ZONE SPREAD
# ─────────────────────────────────────────────────────────────────
header('SECTION 2: PER-SOURCE ZONE SPREAD')

# Explode sources
src_rows = []
for _, row in df.iterrows():
    if pd.isna(row['source']) or row['source'] == '':
        continue
    for s in str(row['source']).split('|'):
        s = s.strip()
        if s:
            src_rows.append({'source': s, 'zone': row['zone'],
                             'd_min': row['d_min'], 'd_max': row['d_max']})
src_df = pd.DataFrame(src_rows)

print('\n── 2a. Zone distribution per source (top 30 by volume) ──')
src_counts = src_df['source'].value_counts()
top_sources = src_counts.head(30).index.tolist()

src_zone_tbl = src_df[src_df['source'].isin(top_sources)].groupby(['source','zone']).size().unstack(fill_value=0)
for z in [1,2,3]:
    if z not in src_zone_tbl.columns:
        src_zone_tbl[z] = 0
src_zone_tbl = src_zone_tbl[[1,2,3]]
src_zone_tbl['total'] = src_zone_tbl.sum(axis=1)
src_zone_tbl['pct_z1'] = (src_zone_tbl[1]/src_zone_tbl['total']*100).round(1)
src_zone_tbl['pct_z2'] = (src_zone_tbl[2]/src_zone_tbl['total']*100).round(1)
src_zone_tbl['pct_z3'] = (src_zone_tbl[3]/src_zone_tbl['total']*100).round(1)
src_zone_tbl = src_zone_tbl.sort_values('total', ascending=False)
print(f'\n  {"Source":<30} {"Total":>5} {"Z1%":>6} {"Z2%":>6} {"Z3%":>6}')
print(f'  {"-"*55}')
for src, row in src_zone_tbl.iterrows():
    print(f'  {src:<30} {int(row["total"]):>5} {row["pct_z1"]:>6} {row["pct_z2"]:>6} {row["pct_z3"]:>6}')

print('\n── 2b. Widest zone spread (present in all 3 zones) ──')
src_zones_set = src_df.groupby('source')['zone'].apply(set)
wide_sources = src_zones_set[src_zones_set.apply(lambda x: {1,2,3}.issubset(x))]
print(f'  Sources in all 3 zones ({len(wide_sources)}):')
for s in wide_sources.index:
    counts = src_df[src_df['source']==s]['zone'].value_counts().sort_index().to_dict()
    print(f'    {s}: {counts}')

zone_locked = src_zones_set[src_zones_set.apply(len) == 1]
print(f'\n  Zone-locked sources (n={len(zone_locked)}):')
for s, zs in zone_locked.items():
    cnt = src_counts.get(s, 0)
    if cnt >= 3:  # only show meaningful ones
        print(f'    {s} → only zone {list(zs)[0]}  (n={cnt})')

print('\n── 2c. Zone 3 sources: do they also appear in zones 1 and 2? ──')
z3_sources = src_zones_set[src_zones_set.apply(lambda x: 3 in x)]
print(f'  Sources appearing in zone 3: {len(z3_sources)}')
z3_also_z1 = z3_sources[z3_sources.apply(lambda x: 1 in x)]
z3_also_z2 = z3_sources[z3_sources.apply(lambda x: 2 in x)]
z3_all3 = z3_sources[z3_sources.apply(lambda x: {1,2,3}.issubset(x))]
z3_jump = z3_sources[z3_sources.apply(lambda x: 3 in x and 1 not in x and 2 not in x)]
print(f'  Also in zone 1: {len(z3_also_z1)}  |  Also in zone 2: {len(z3_also_z2)}  |  All 3: {len(z3_all3)}  |  Jump directly (only zone 3): {len(z3_jump)}')
if len(z3_jump) > 0:
    print(f'  Zone-3-only sources: {list(z3_jump.index)}')

print('\n── 2d. d_min and d_max variance per source per zone (top sources) ──')
for src in top_sources[:10]:
    print(f'\n  Source: {src}')
    for zone in [1,2,3]:
        sub = src_df[(src_df['source']==src) & (src_df['zone']==zone)]
        if len(sub) == 0:
            continue
        print(f'    Zone {zone} (n={len(sub)}): d_min var={sub["d_min"].var():.4f}  d_max var={sub["d_max"].var():.4f}')

# ─────────────────────────────────────────────────────────────────
# SECTION 3 — ZONE 1 VS ZONE 2 BOUNDARY
# ─────────────────────────────────────────────────────────────────
header('SECTION 3: ZONE 1 vs ZONE 2 BOUNDARY')

print('\n── 3a. d_min and d_max distributions: zone 1 vs zone 2 ──')
for metric in ['d_min', 'd_max']:
    print(f'\n  {metric}:')
    for zone in [1,2]:
        vals = df[df['zone']==zone][metric].dropna()
        print(f'    Zone {zone}: mean={vals.mean():.3f}  std={vals.std():.3f}  min={vals.min():.3f}  max={vals.max():.3f}  p25={vals.quantile(0.25):.3f}  p75={vals.quantile(0.75):.3f}')
    t, p = stats.ttest_ind(df[df['zone']==1][metric].dropna(), df[df['zone']==2][metric].dropna())
    print(f'    t-test zone1 vs zone2: t={t:.3f}, p={p:.4e}')

print('\n── 3b. Fraction uncertain per zone ──')
for zone in [1,2,3]:
    total = (df['zone'] == zone).sum()
    unc = ((df['zone'] == zone) & df['uncertain']).sum()
    print(f'  Zone {zone}: {unc}/{total} uncertain = {unc/total*100:.1f}%')

print('\n── 3c. Top E/M/F tags for uncertain variants straddling zone 1/2 boundary ──')
boundary_12 = df[df['uncertain'] & df['zone'].isin([1,2])]
print(f'  Uncertain variants in zone 1 or 2: n={len(boundary_12)}')
for col, label in [('e_explicit','E'), ('m_explicit','M'), ('f_explicit','F')]:
    top_tags = boundary_12[col].dropna().value_counts().head(8)
    print(f'\n  Top {label} tags:')
    for tag, cnt in top_tags.items():
        print(f'    {cnt:3d}  {tag}')

print('\n── 3d. m_explicit distribution: zone 1 vs zone 2 ──')
for zone in [1,2]:
    top = df[df['zone']==zone]['m_explicit'].dropna().value_counts().head(10)
    print(f'\n  Zone {zone} m_explicit:')
    for tag, cnt in top.items():
        pct = cnt/(df['zone']==zone).sum()*100
        print(f'    {cnt:4d} ({pct:4.1f}%)  {tag}')

print('\n── 3e. Most common f_explicit for zone 2 ──')
top_f2 = df[df['zone']==2]['f_explicit'].dropna().value_counts().head(10)
print(f'\n  Zone 2 f_explicit:')
for tag, cnt in top_f2.items():
    pct = cnt/(df['zone']==2).sum()*100
    print(f'  {cnt:4d} ({pct:4.1f}%)  {tag}')
top_f1 = df[df['zone']==1]['f_explicit'].dropna().value_counts().head(5)
print(f'\n  Zone 1 f_explicit (top 5 for contrast):')
for tag, cnt in top_f1.items():
    pct = cnt/(df['zone']==1).sum()*100
    print(f'  {cnt:4d} ({pct:4.1f}%)  {tag}')

# ─────────────────────────────────────────────────────────────────
# SECTION 4 — ZONE 2 VS ZONE 3 BOUNDARY
# ─────────────────────────────────────────────────────────────────
header('SECTION 4: ZONE 2 vs ZONE 3 BOUNDARY')

print('\n── 4a. f_explicit tags exclusive to zone 3 ──')
f_by_zone = df.groupby('zone')['f_explicit'].apply(lambda x: set(x.dropna()))
z1_f = f_by_zone.get(1, set())
z2_f = f_by_zone.get(2, set())
z3_f = f_by_zone.get(3, set())
exclusive_z3 = z3_f - z1_f - z2_f
print(f'  Tags only in zone 3: {sorted(exclusive_z3)}')
shared_z23_not_z1 = (z2_f | z3_f) - z1_f
print(f'  Tags in zones 2+3 but NOT zone 1: {sorted(shared_z23_not_z1)}')

print('\n── 4b. e_explicit distribution in zone 3 vs zones 1 and 2 ──')
e_total = df['e_explicit'].dropna()
e_total_n = len(df)
for zone in [1,2,3]:
    print(f'\n  Zone {zone} e_explicit (n={len(df[df["zone"]==zone])}):')
    top = df[df['zone']==zone]['e_explicit'].dropna().value_counts()
    zone_n = (df['zone']==zone).sum()
    for tag, cnt in top.items():
        pct_zone = cnt/zone_n*100
        total_for_tag = (df['e_explicit']==tag).sum()
        pct_tag_in_zone = cnt/total_for_tag*100 if total_for_tag else 0
        print(f'    {cnt:4d} ({pct_zone:4.1f}% of zone)  {tag}  [{pct_tag_in_zone:.0f}% of all "{tag}" entries]')

print('\n── 4c. Mean f_score zone 2 vs zone 3; E/M/F as separator ──')
for zone in [2,3]:
    sub = df[df['zone']==zone]
    print(f'\n  Zone {zone}: e_score mean={sub["e_score"].mean():.3f}  m_score mean={sub["m_score"].mean():.3f}  f_score mean={sub["f_score"].mean():.3f}')
    print(f'           e_score std={sub["e_score"].std():.3f}   m_score std={sub["m_score"].std():.3f}   f_score std={sub["f_score"].std():.3f}')

# ANOVA / effect size for each axis between zone 2 and 3
for axis in ['e_score','m_score','f_score']:
    v2 = df[df['zone']==2][axis].dropna()
    v3 = df[df['zone']==3][axis].dropna()
    t, p = stats.ttest_ind(v2, v3)
    d = (v3.mean()-v2.mean()) / np.sqrt((v2.std()**2 + v3.std()**2)/2)
    print(f'  {axis}: t={t:.3f}, p={p:.4e}, Cohen d={d:.3f}')

# ─────────────────────────────────────────────────────────────────
# SECTION 5 — TAG EXPLICITNESS AND UNCERTAINTY
# ─────────────────────────────────────────────────────────────────
header('SECTION 5: TAG EXPLICITNESS AND UNCERTAINTY')

print('\n── 5a. Fraction NULL explicit per axis per zone ──')
for zone in [1,2,3]:
    sub = df[df['zone']==zone]
    n = len(sub)
    for col, label in [('e_explicit','E'), ('m_explicit','M'), ('f_explicit','F')]:
        null_pct = sub[col].isna().sum() / n * 100
        print(f'  Zone {zone}  {label}_explicit NULL: {null_pct:.1f}%')
    print()

print('\n── 5b. question_tags distribution and top ?-prefixed tags ──')
for zone in [1,2,3]:
    sub = df[df['zone']==zone]
    n = len(sub)
    qt = sub['question_tags'].sum()
    print(f'  Zone {zone}: {qt}/{n} question_tags = {qt/n*100:.1f}%')

# Collect ?-prefixed tags from e_could_be
print('\n  Top ?-prefixed tags (from e_could_be + m_could_be + f_could_be):')
q_tags = Counter()
for col in ['e_could_be','m_could_be','f_could_be','e_explicit','m_explicit','f_explicit']:
    for val in df[col].dropna():
        for t in str(val).split('|'):
            t = t.strip()
            if t.startswith('?'):
                q_tags[t] += 1
for tag, cnt in q_tags.most_common(20):
    print(f'    {cnt:4d}  {tag}')

print('\n── 5c. d_gap (d_max - d_min) by zone ──')
for zone in [1,2,3]:
    vals = df[df['zone']==zone]['d_gap']
    print(f'  Zone {zone}: mean={vals.mean():.4f}  std={vals.std():.4f}  p25={vals.quantile(0.25):.4f}  p75={vals.quantile(0.75):.4f}  max={vals.max():.4f}')

print('\n── 5d. Variants with NULL e_explicit but multiple e_could_be options ──')
null_e_multi_could = df[
    df['e_explicit'].isna() &
    df['e_could_be'].notna() &
    df['e_could_be'].apply(lambda x: '|' in str(x) if pd.notna(x) else False)
]
print(f'  Count: {len(null_e_multi_could)}')
zdist = null_e_multi_could['zone'].value_counts().sort_index()
print(f'  Zone distribution: {zdist.to_dict()}')
print(f'  Top e_could_be combos:')
for combo, cnt in null_e_multi_could['e_could_be'].value_counts().head(10).items():
    print(f'    {cnt:4d}  {combo}')

# ─────────────────────────────────────────────────────────────────
# SECTION 6 — COMPOSITE SCORE STRUCTURE
# ─────────────────────────────────────────────────────────────────
header('SECTION 6: COMPOSITE SCORE STRUCTURE')

print('\n── 6a. Correlation matrix: e_score, m_score, f_score ──')
score_cols = ['e_score','m_score','f_score']
corr = df[score_cols].corr()
print(f'\n  Full dataset:')
print(corr.round(3).to_string())

for zone in [1,2,3]:
    sub = df[df['zone']==zone][score_cols]
    print(f'\n  Zone {zone}:')
    print(sub.corr().round(3).to_string())

print('\n── 6b. Variance of each axis per zone (which axis discriminates most) ──')
for zone in [1,2,3]:
    sub = df[df['zone']==zone][score_cols]
    print(f'\n  Zone {zone} variance:  e={sub["e_score"].var():.4f}  m={sub["m_score"].var():.4f}  f={sub["f_score"].var():.4f}')
    dominant = sub.var().idxmax()
    print(f'  → Dominant axis: {dominant}')

print('\n── 6c. Variants where two scores are low but one is high ──')
# Define low < 0.35, high > 0.5
low, high = 0.35, 0.5

# e low, m low, f high
case1 = df[(df['e_score'] < low) & (df['m_score'] < low) & (df['f_score'] > high)]
print(f'\n  e_low + m_low + f_high: n={len(case1)}')
print(f'  Zone dist: {case1["zone"].value_counts().sort_index().to_dict()}')
print(f'  Top sources: {case1["source"].value_counts().head(5).to_dict()}')

# e high, m low, f low
case2 = df[(df['e_score'] > high) & (df['m_score'] < low) & (df['f_score'] < low)]
print(f'\n  e_high + m_low + f_low: n={len(case2)}')
print(f'  Zone dist: {case2["zone"].value_counts().sort_index().to_dict()}')
print(f'  Top sources: {case2["source"].value_counts().head(5).to_dict()}')

# m high, e low, f low
case3 = df[(df['m_score'] > high) & (df['e_score'] < low) & (df['f_score'] < low)]
print(f'\n  m_high + e_low + f_low: n={len(case3)}')
print(f'  Zone dist: {case3["zone"].value_counts().sort_index().to_dict()}')
print(f'  Top sources: {case3["source"].value_counts().head(5).to_dict()}')

# e low, m high, f high
case4 = df[(df['e_score'] < low) & (df['m_score'] > high) & (df['f_score'] > high)]
print(f'\n  e_low + m_high + f_high: n={len(case4)}')
print(f'  Zone dist: {case4["zone"].value_counts().sort_index().to_dict()}')
print(f'  Top sources: {case4["source"].value_counts().head(5).to_dict()}')

print(f'\n{SEP}')
print('  ANALYSIS COMPLETE')
print(SEP)

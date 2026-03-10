#!/usr/bin/env python3
"""
Soy Taxonomy — EMF Tag Navigator

Tags are the selection axes. A combination of (E, M, F) tags resolves to a
canonical variant name. The name is the output of the combination, not the
starting point. Linguistic noise lives in a resolver layer outside this model.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from collections import defaultdict

from rich.console import Console
from rich.tree import Tree
from rich.table import Table
from rich.text import Text


# ---------------------------------------------------------------------------
# Core structure
# ---------------------------------------------------------------------------

@dataclass
class Variant:
    """
    One unique soy form, defined entirely by its EMF tag combination.
    resolves_to is what the system shows the user when they complete selection.
    For Zone 1 it is a "soybean expression" name.
    For Zone 2/3 it is its own canonical name (vanaspati, lecithin, etc.).
    """
    resolves_to: str              # the name this combination maps to
    zone: int
    e_explicit: List[str] = field(default_factory=list)
    e_could_be: List[str] = field(default_factory=list)
    m_explicit: List[str] = field(default_factory=list)
    m_could_be: List[str] = field(default_factory=list)
    f_explicit: List[str] = field(default_factory=list)
    f_could_be: List[str] = field(default_factory=list)
    e_score: float = 0.0
    m_score: float = 0.0
    f_score: float = 0.0
    uncertain: bool = False
    question_tags: bool = False
    note: Optional[str] = None


# ---------------------------------------------------------------------------
# Soy variants — one entry per unique (E, M, F) signal
# Derived from EMF zone assignments in the data as ground truth
# ---------------------------------------------------------------------------

SOY_VARIANTS: List[Variant] = [

    # ── Zone 1: soybean expressions ─────────────────────────────────────────

    Variant(
        resolves_to="soybean",
        zone=1,
        m_explicit=["whole/fresh pieces"],
        f_explicit=["base ingredient"],
        m_score=0.05, f_score=0.12,
    ),
    Variant(
        resolves_to="roasted soybean",
        zone=1,
        e_explicit=["roasting"],
        m_explicit=["whole/fresh pieces"],
        f_explicit=["base ingredient"],
        e_score=0.58, m_score=0.05, f_score=0.12,
    ),
    Variant(
        resolves_to="soy grits",
        zone=1,
        e_explicit=["milling"],
        m_explicit=["coarse grits"],
        f_explicit=["base ingredient"],
        e_score=0.28, m_score=0.30, f_score=0.12,
    ),
    Variant(
        resolves_to="soy flour",
        zone=1,
        e_explicit=["milling"],
        m_explicit=["flour/fine powder"],
        f_explicit=["base ingredient"],
        e_score=0.28, m_score=0.33, f_score=0.12,
    ),
    Variant(
        resolves_to="defatted soy flour",
        zone=1,
        e_explicit=["skim/defatted", "milling"],
        m_explicit=["flour/fine powder"],
        f_explicit=["base ingredient"],
        e_score=0.28, m_score=0.33, f_score=0.12,
    ),
    Variant(
        resolves_to="soy flakes",
        zone=1,
        m_explicit=["flakes"],
        f_explicit=["base ingredient"],
        m_score=0.36, f_score=0.12,
    ),
    Variant(
        resolves_to="defatted soy",
        zone=1,
        m_explicit=["skim/defatted meal"],
        f_explicit=["base ingredient"],
        m_score=0.55, f_score=0.12,
    ),
    Variant(
        resolves_to="soy granules",
        zone=1,
        e_could_be=["?extrusion"],
        m_explicit=["granules"],
        f_explicit=["base ingredient"],
        m_score=0.80, f_score=0.12,
        uncertain=True, question_tags=True,
        note="?extrusion unvalidated",
    ),
    Variant(
        resolves_to="soy protein concentrate",
        zone=1,
        e_could_be=["?extrusion"],
        m_explicit=["protein concentrate"],
        f_explicit=["base ingredient"],
        m_score=0.74, f_score=0.12,
        uncertain=True, question_tags=True,
        note="?extrusion unvalidated",
    ),
    Variant(
        resolves_to="soy protein isolate",
        zone=1,
        m_explicit=["protein isolate"],
        f_explicit=["base ingredient"],
        m_score=0.78, f_score=0.12,
    ),
    Variant(
        resolves_to="soybean oil",
        zone=1,
        e_could_be=["cold pressing", "solvent extraction"],
        m_explicit=["oil"],
        f_explicit=["lipid base"],
        m_score=0.70, f_score=0.22,
        uncertain=True,
        note="process unspecified — cold pressing or solvent extraction both plausible",
    ),

    # ── Zone 2: canonical separation (source: soybean is metadata) ──────────

    Variant(
        resolves_to="refined soybean oil",
        zone=2,
        e_explicit=["refining"],
        e_could_be=["cold pressing", "solvent extraction"],
        m_explicit=["oil"],
        f_explicit=["lipid base"],
        e_score=0.75, m_score=0.70, f_score=0.22,
    ),
    Variant(
        resolves_to="vanaspati",
        zone=2,
        e_explicit=["hydrogenation", "interesterification"],
        e_could_be=["refining"],
        m_explicit=["fat fraction"],
        f_explicit=["lipid base"],
        e_score=0.92, m_score=0.72, f_score=0.22,
        note="Indian hydrogenated fat",
    ),
    Variant(
        resolves_to="margarine",
        zone=2,
        e_explicit=["interesterification", "hydrogenation"],
        m_explicit=["fat fraction"],
        f_explicit=["lipid base"],
        f_could_be=["emulsifier"],
        e_score=0.92, m_score=0.72, f_score=0.22,
        uncertain=True,
    ),
    Variant(
        resolves_to="soya sauce",
        zone=2,
        e_explicit=["fermentation"],
        m_could_be=["extract/oleoresin"],
        f_explicit=["flavouring agent"],
        f_could_be=["base ingredient"],
        e_score=0.56, f_score=0.675,
    ),
    Variant(
        resolves_to="soya bean extract",
        zone=2,
        e_explicit=["solvent extraction"],
        m_explicit=["extract/oleoresin"],
        f_explicit=["base ingredient"],
        e_score=0.82, m_score=0.86, f_score=0.12,
    ),
    Variant(
        resolves_to="hvp",
        zone=2,
        e_explicit=["?hydrolysis"],
        m_explicit=["protein concentrate"],
        f_explicit=["base ingredient"],
        f_could_be=["flavouring agent"],
        e_score=0.60, m_score=0.74, f_score=0.12,
        question_tags=True,
        note="?hydrolysis unvalidated",
    ),
    Variant(
        resolves_to="tvp",
        zone=2,
        e_explicit=["?extrusion"],
        m_explicit=["protein concentrate"],
        f_explicit=["base ingredient"],
        e_score=0.60, m_score=0.74, f_score=0.12,
        question_tags=True,
        note="?extrusion unvalidated",
    ),

    # ── Zone 3: functional identity (source: soybean is provenance only) ────

    Variant(
        resolves_to="lecithin",
        zone=3,
        e_explicit=["solvent extraction"],
        m_explicit=["emulsifier powder"],
        f_explicit=["emulsifier"],
        e_score=0.82, m_score=0.89, f_score=0.825,
        note="also produced from: sunflower",
    ),
]


# ---------------------------------------------------------------------------
# Resolver: (e, m, f) tags → Variant
# ---------------------------------------------------------------------------

def resolve(
    e: Optional[List[str]] = None,
    m: Optional[List[str]] = None,
    f: Optional[List[str]] = None,
) -> List[Variant]:
    """
    Given a partial or complete tag combination, return matching variants.
    Matches against explicit tags only (not could-be).
    """
    e_set = set(e or [])
    m_set = set(m or [])
    f_set = set(f or [])

    results = []
    for v in SOY_VARIANTS:
        if e_set and not e_set.issubset(set(v.e_explicit)):
            continue
        if m_set and not m_set.issubset(set(v.m_explicit)):
            continue
        if f_set and not f_set.issubset(set(v.f_explicit)):
            continue
        results.append(v)
    return results


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

ZONE_COLOR = {1: "green", 2: "yellow", 3: "red"}
ZONE_LABEL = {
    1: "Zone 1 — soybean expressions",
    2: "Zone 2 — canonical separation  [dim](source: soybean)[/dim]",
    3: "Zone 3 — functional identity   [dim](source: soybean)[/dim]",
}


def _flags(v: Variant) -> str:
    parts = []
    if v.uncertain:
        parts.append("[yellow]~[/yellow]")
    if v.question_tags:
        parts.append("[red]?[/red]")
    return " " + "".join(parts) if parts else ""


def _tag_str(explicit: List[str], could_be: List[str]) -> str:
    out = ", ".join(explicit) if explicit else "—"
    if could_be:
        out += f"  [dim](could-be: {', '.join(could_be)})[/dim]"
    return out


def _leaf(v: Variant, c: str) -> Text:
    t = Text()
    t.append("⇒  ", style="dim")
    t.append(v.resolves_to, style=f"bold {c}")
    if v.uncertain:
        t.append("  ~", style="yellow")
    if v.question_tags:
        t.append("?", style="red")
    t.append(
        f"   E={v.e_score:.2f} M={v.m_score:.2f} F={v.f_score:.2f}",
        style="dim",
    )
    if v.note:
        t.append(f"   [{v.note}]", style="dim italic")
    return t


# ---------------------------------------------------------------------------
# Navigation tree: E-axis → M-axis → F-axis → resolved name
# ---------------------------------------------------------------------------

def display_navigation_tree(console: Console):
    root = Tree(
        "[bold]soybean[/bold]  [dim]— pick axes to resolve a variant[/dim]",
        guide_style="dim",
    )

    by_zone: Dict[int, List[Variant]] = defaultdict(list)
    for v in SOY_VARIANTS:
        by_zone[v.zone].append(v)

    for zone in [1, 2, 3]:
        c = ZONE_COLOR[zone]
        zone_node = root.add(f"[bold {c}]{ZONE_LABEL[zone]}[/bold {c}]")

        # Group by E-explicit (primary axis)
        by_e: Dict[str, List[Variant]] = defaultdict(list)
        for v in by_zone[zone]:
            key = " + ".join(v.e_explicit) if v.e_explicit else "none"
            by_e[key].append(v)

        for e_key in sorted(by_e):
            e_node = zone_node.add(f"[dim]E:[/dim]  {e_key}")

            for v in by_e[e_key]:
                # M-axis
                m_str = ", ".join(v.m_explicit) if v.m_explicit else "—"
                m_node = e_node.add(f"[dim]M:[/dim]  {m_str}")

                # F-axis + resolution
                f_str = ", ".join(v.f_explicit) if v.f_explicit else "—"
                f_node = m_node.add(f"[dim]F:[/dim]  {f_str}")
                f_node.add(_leaf(v, c))

                # could-be hints
                if v.e_could_be or v.m_could_be or v.f_could_be:
                    cb = f_node.add("[dim]could-be hints[/dim]")
                    if v.e_could_be:
                        cb.add(f"[dim]E: {', '.join(v.e_could_be)}[/dim]")
                    if v.m_could_be:
                        cb.add(f"[dim]M: {', '.join(v.m_could_be)}[/dim]")
                    if v.f_could_be:
                        cb.add(f"[dim]F: {', '.join(v.f_could_be)}[/dim]")

    console.print(root)


# ---------------------------------------------------------------------------
# Resolver demo: show that selecting tags produces a name
# ---------------------------------------------------------------------------

def display_resolver_demo(console: Console):
    console.print("\n[bold]Resolver demo — select tag combination, get canonical name[/bold]\n")

    queries = [
        (["milling"],              ["flour/fine powder"],  ["base ingredient"]),
        (["roasting"],             ["whole/fresh pieces"], ["base ingredient"]),
        ([],                       ["protein isolate"],    ["base ingredient"]),
        (["refining"],             ["oil"],                ["lipid base"]),
        (["fermentation"],         [],                     ["flavouring agent"]),
        (["hydrogenation",
          "interesterification"],  ["fat fraction"],       ["lipid base"]),
        (["solvent extraction"],   ["emulsifier powder"],  ["emulsifier"]),
        (["?extrusion"],           ["protein concentrate"],["base ingredient"]),
    ]

    table = Table(show_header=True, header_style="bold")
    table.add_column("E selected",    style="cyan",    no_wrap=True)
    table.add_column("M selected",    style="cyan",    no_wrap=True)
    table.add_column("F selected",    style="cyan",    no_wrap=True)
    table.add_column("resolves to",   style="bold",    no_wrap=True)
    table.add_column("zone",          justify="center")
    table.add_column("flags",         justify="center")

    for e, m, f in queries:
        matches = resolve(e=e or None, m=m or None, f=f or None)
        for v in matches:
            zc = ZONE_COLOR[v.zone]
            flags = ("~" if v.uncertain else "") + ("?" if v.question_tags else "")
            table.add_row(
                ", ".join(e) or "—",
                ", ".join(m) or "—",
                ", ".join(f) or "—",
                f"[{zc}]{v.resolves_to}[/{zc}]",
                f"[{zc}]{v.zone}[/{zc}]",
                f"[yellow]{flags}[/yellow]" if flags else "",
            )

    console.print(table)
    console.print(
        "[dim]~ uncertain zone boundary   ? unvalidated tag pending review[/dim]\n"
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    console = Console()
    console.print()
    console.print("[bold]SOY TAXONOMY — EMF tag navigation[/bold]")
    console.print("[dim]Each path through E → M → F resolves to a canonical name.[/dim]\n")
    display_navigation_tree(console)
    display_resolver_demo(console)
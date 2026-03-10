"""
enrich_tagged_variants.py
=========================
Implements Tier 1/2/3 enrichment from the EMF Signal-Loss Taxonomy analysis.

Adds the following new columns to tagged_variants.csv:
  ins_number           – Codex Alimentarius INS/E code extracted by regex or lookup
  compound_name        – IUPAC/Codex common name (where known)
  nutrient_class       – enum for vitamins/amino acids/mineral salts (Cluster 2)
  dairy_product_subtype– enum for fermented dairy products (Cluster 3)
  milling_grade        – enum for grain flour grades (Cluster 5)
  oil_fraction         – enum for oil processing/fractionation (Cluster 6)
  protein_fraction     – enum for protein forms (Cluster 7)
  sugar_form           – enum for sugar variants (Cluster 8)
  language_tag         – ISO 639-1 code for non-English variant names
  f_revised            – Corrected f_explicit; splits 'base ingredient' into four
                         sub-types: raw_agricultural_material | processed_ingredient |
                         fortification_agent | fermentation_agent

Outputs:
  tagged_variants_enriched.csv   – drop-in replacement with all original columns
                                   plus the new enrichment columns
  enrichment_summary.txt         – counts of how many rows each rule fired on

Usage:
  python3 experiments/enrich_tagged_variants.py
"""

import csv
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
INPUT_CSV  = REPO / "tagged_variants.csv"
OUTPUT_CSV = REPO / "tagged_variants_enriched.csv"
SUMMARY    = REPO / "experiments" / "enrichment_summary.txt"

# ---------------------------------------------------------------------------
# Lookup tables
# ---------------------------------------------------------------------------

# INS → compound name (Codex Alimentarius common names)
INS_TO_NAME: dict[str, str] = {
    # Acidity regulators
    "260": "acetic acid", "261": "potassium acetate", "262": "sodium acetate",
    "263": "calcium acetate", "270": "lactic acid", "296": "malic acid",
    "325": "sodium lactate", "326": "potassium lactate", "327": "calcium lactate",
    "330": "citric acid", "331": "sodium citrate", "331i": "monosodium citrate",
    "331ii": "disodium citrate", "331iii": "trisodium citrate",
    "332": "potassium citrate", "333": "calcium citrate",
    "334": "tartaric acid", "335": "sodium tartrate", "336": "potassium tartrate",
    "337": "potassium sodium tartrate", "338": "phosphoric acid",
    "339": "sodium phosphate", "340": "potassium phosphate",
    "341": "calcium phosphate", "342": "ammonium phosphate",
    "343": "magnesium phosphate",
    # Anticaking agents
    "341i": "monocalcium phosphate", "341ii": "dicalcium phosphate",
    "341iii": "tricalcium phosphate",
    "500": "sodium carbonates", "500i": "sodium carbonate",
    "500ii": "sodium bicarbonate", "501": "potassium carbonate",
    "503": "ammonium carbonate", "504": "magnesium carbonate",
    "508": "potassium chloride", "509": "calcium chloride",
    "511": "magnesium chloride", "516": "calcium sulphate",
    "524": "sodium hydroxide", "525": "potassium hydroxide",
    "526": "calcium hydroxide", "527": "ammonium hydroxide",
    "528": "magnesium hydroxide",
    "551": "silicon dioxide", "552": "calcium silicate",
    "553": "magnesium silicate", "554": "sodium aluminosilicate",
    "556": "calcium aluminium silicate", "559": "aluminium silicate",
    # Preservatives
    "200": "sorbic acid", "201": "sodium sorbate", "202": "potassium sorbate",
    "203": "calcium sorbate", "210": "benzoic acid", "211": "sodium benzoate",
    "212": "potassium benzoate", "213": "calcium benzoate",
    "220": "sulphur dioxide", "221": "sodium sulphite",
    "222": "sodium bisulphite", "223": "sodium metabisulphite",
    "224": "potassium metabisulphite", "225": "potassium sulphite",
    "249": "potassium nitrite", "250": "sodium nitrite",
    "251": "sodium nitrate", "252": "potassium nitrate",
    "280": "propionic acid", "281": "sodium propionate",
    "282": "calcium propionate", "283": "potassium propionate",
    # Antioxidants
    "300": "ascorbic acid", "301": "sodium ascorbate",
    "302": "calcium ascorbate", "304": "ascorbyl palmitate",
    "306": "tocopherols", "307": "alpha-tocopherol",
    "310": "propyl gallate", "319": "tert-butylhydroquinone (TBHQ)",
    "320": "butylated hydroxyanisole (BHA)",
    "321": "butylated hydroxytoluene (BHT)",
    # Colours
    "100": "curcumin", "101": "riboflavin (colour)",
    "102": "tartrazine", "104": "quinoline yellow",
    "110": "sunset yellow FCF", "120": "carmines",
    "122": "azorubine", "123": "amaranth",
    "124": "ponceau 4R", "127": "erythrosine",
    "129": "allura red AC", "131": "patent blue V",
    "132": "indigotine", "133": "brilliant blue FCF",
    "140": "chlorophylls", "141": "copper complexes of chlorophyll",
    "150a": "plain caramel", "150b": "caustic sulphite caramel",
    "150c": "ammonia caramel", "150d": "sulphite ammonia caramel",
    "160": "carotenes", "160a": "beta-carotene",
    "160b": "annatto extracts", "160c": "paprika extract",
    "162": "beetroot red", "163": "anthocyanins",
    "170": "calcium carbonate", "171": "titanium dioxide",
    "172": "iron oxides", "174": "silver",
    # Emulsifiers
    "322": "lecithins", "331iii": "trisodium citrate",
    "400": "alginic acid", "401": "sodium alginate",
    "402": "potassium alginate", "404": "calcium alginate",
    "405": "propylene glycol alginate",
    "406": "agar", "407": "carrageenan",
    "410": "locust bean gum", "412": "guar gum",
    "413": "tragacanth", "414": "acacia gum (gum arabic)",
    "415": "xanthan gum", "416": "karaya gum",
    "418": "gellan gum", "420": "sorbitols",
    "420i": "sorbitol", "420ii": "sorbitol syrup",
    "421": "mannitol", "422": "glycerol",
    "425": "konjac", "427": "cassia gum",
    "429": "oxystearin", "431": "polyoxyethylene (40) stearate",
    "432": "polysorbate 20", "433": "polysorbate 80",
    "434": "polysorbate 40", "435": "polysorbate 60",
    "436": "polysorbate 65",
    "440": "pectins", "442": "ammonium phosphatides",
    "444": "sucrose acetate isobutyrate",
    "445": "glycerol esters of wood rosin",
    "450": "diphosphates", "451": "triphosphates",
    "452": "polyphosphates",
    "460": "cellulose", "461": "methyl cellulose",
    "462": "ethyl cellulose", "463": "hydroxypropyl cellulose",
    "464": "hydroxypropyl methyl cellulose",
    "465": "methyl ethyl cellulose", "466": "sodium carboxymethyl cellulose",
    "471": "mono- and diglycerides of fatty acids",
    "472a": "acetic acid esters of mono- and diglycerides",
    "472b": "lactic acid esters of mono- and diglycerides",
    "472c": "citric acid esters of mono- and diglycerides",
    "472e": "diacetyl tartaric acid esters of mono- and diglycerides",
    "473": "sucrose esters of fatty acids",
    "474": "sucroglycerides",
    "475": "polyglycerol esters of fatty acids",
    "476": "polyglycerol polyricinoleate (PGPR)",
    "477": "propylene glycol esters of fatty acids",
    "478": "mixed tartaric acetic citric acid esters of glycerol",
    "479b": "thermally oxidised soya bean oil",
    "481": "sodium stearoyl lactylate", "482": "calcium stearoyl lactylate",
    "491": "sorbitan monostearate", "492": "sorbitan tristearate",
    "494": "sorbitan monooleate", "495": "sorbitan monopalmitate",
    # Flavour enhancers
    "620": "glutamic acid", "621": "monosodium glutamate (MSG)",
    "622": "monopotassium glutamate", "623": "calcium glutamate",
    "624": "monoammonium glutamate", "625": "magnesium glutamate",
    "626": "guanylic acid", "627": "disodium guanylate",
    "628": "dipotassium guanylate", "629": "calcium guanylate",
    "630": "inosinic acid", "631": "disodium inosinate",
    "632": "dipotassium inosinate", "633": "calcium inosinate",
    "634": "calcium 5-ribonucleotides",
    "635": "disodium 5-ribonucleotides",
    # Sweeteners
    "420": "sorbitols", "421": "mannitol", "950": "acesulfame potassium",
    "951": "aspartame", "952": "cyclamic acid",
    "953": "isomalt", "954": "saccharin", "955": "sucralose",
    "957": "thaumatin", "960": "steviol glycosides",
    "961": "neotame", "962": "aspartame-acesulfame salt",
    "968": "erythritol", "999": "quillaia extracts",
    # Raising agents / leavening
    "170": "calcium carbonate (raising)",
    # Modified starches
    "1400": "dextrin", "1401": "acid-treated starch",
    "1402": "alkaline-treated starch", "1403": "bleached starch",
    "1404": "oxidised starch", "1405": "starch treated with enzymes",
    "1410": "monostarch phosphate", "1412": "distarch phosphate",
    "1413": "phosphated distarch phosphate",
    "1414": "acetylated distarch phosphate",
    "1420": "starch acetate", "1422": "acetylated distarch adipate",
    "1440": "hydroxypropyl starch",
    "1442": "hydroxypropyl distarch phosphate",
    "1450": "starch sodium octenyl succinate",
    "1451": "acetylated oxidised starch",
    # Enzyme preparations (flour treatment)
    "1100": "alpha-amylase", "1101": "proteases",
    "1102": "glucose oxidase", "1104": "lipases",
    # Gases / propellants
    "290": "carbon dioxide", "938": "argon",
    "939": "helium", "941": "nitrogen",
    "942": "nitrous oxide", "944": "propane",
    "948": "oxygen",
    # Humectants
    "1200": "polydextrose", "1201": "polyvinylpyrrolidone",
    "1202": "polyvinyl polypyrrolidone",
    "1400": "dextrin",
    "1518": "glyceryl triacetate (triacetin)",
    "1520": "propylene glycol",
    "1521": "polyethylene glycol",
}

# Vitamin / amino acid / mineral → nutrient_class
# Keys are lowercased fragment patterns to match against variant text
NUTRIENT_CLASS_RULES: list[tuple[str, str]] = [
    # Fat-soluble vitamins
    ("vitamin a",           "vitamin_fat_soluble"),
    ("retinol",             "vitamin_fat_soluble"),
    ("vitamin d",           "vitamin_fat_soluble"),
    ("vitamin d2",          "vitamin_fat_soluble"),
    ("vitamin d3",          "vitamin_fat_soluble"),
    ("ergocalciferol",      "vitamin_fat_soluble"),
    ("cholecalciferol",     "vitamin_fat_soluble"),
    ("vitamin e",           "vitamin_fat_soluble"),
    ("tocopherol",          "vitamin_fat_soluble"),
    ("vitamin k",           "vitamin_fat_soluble"),
    ("phylloquinone",       "vitamin_fat_soluble"),
    # Water-soluble vitamins
    ("vitamin b1",          "vitamin_water_soluble"),
    ("thiamin",             "vitamin_water_soluble"),
    ("thiamine",            "vitamin_water_soluble"),
    ("vitamin b2",          "vitamin_water_soluble"),
    ("riboflavin",          "vitamin_water_soluble"),
    ("vitamin b3",          "vitamin_water_soluble"),
    ("niacin",              "vitamin_water_soluble"),
    ("nicotinamide",        "vitamin_water_soluble"),
    ("nicotinic acid",      "vitamin_water_soluble"),
    ("vitamin b5",          "vitamin_water_soluble"),
    ("pantothenic acid",    "vitamin_water_soluble"),
    ("vitamin b6",          "vitamin_water_soluble"),
    ("pyridoxine",          "vitamin_water_soluble"),
    ("pyridoxal",           "vitamin_water_soluble"),
    ("vitamin b7",          "vitamin_water_soluble"),
    ("biotin",              "vitamin_water_soluble"),
    ("vitamin b9",          "vitamin_water_soluble"),
    ("folic acid",          "vitamin_water_soluble"),
    ("folate",              "vitamin_water_soluble"),
    ("vitamin b12",         "vitamin_water_soluble"),
    ("cyanocobalamin",      "vitamin_water_soluble"),
    ("cobalamin",           "vitamin_water_soluble"),
    ("vitamin c",           "vitamin_water_soluble"),
    ("ascorbic acid",       "vitamin_water_soluble"),
    ("vitamin b complex",   "vitamin_water_soluble"),
    ("vitamins vitamin",    "vitamin_water_soluble"),
    ("vitamins a",          "vitamin_fat_soluble"),
    ("vitamins d",          "vitamin_fat_soluble"),
    # Amino acids
    ("amino acid",          "amino_acid"),
    ("l-leucine",           "amino_acid"),
    ("leucine",             "amino_acid"),
    ("valine",              "amino_acid"),
    ("isoleucine",          "amino_acid"),
    ("lysine",              "amino_acid"),
    ("l-lysine",            "amino_acid"),
    ("threonine",           "amino_acid"),
    ("methionine",          "amino_acid"),
    ("dl methionine",       "amino_acid"),
    ("dl-methionine",       "amino_acid"),
    ("tryptophan",          "amino_acid"),
    ("phenylalanine",       "amino_acid"),
    ("phenylalaline",       "amino_acid"),
    ("histidine",           "amino_acid"),
    ("arginine",            "amino_acid"),
    ("l-arginine",          "amino_acid"),
    ("glutamine",           "amino_acid"),
    ("l-glutamine",         "amino_acid"),
    ("taurine",             "amino_acid"),
    ("carnitine",           "amino_acid"),
    ("l-carnitine",         "amino_acid"),
    ("l-camitine",          "amino_acid"),   # typo in corpus
    ("cysteine",            "amino_acid"),
    ("creatine",            "amino_acid"),
    ("glutamine peptides",  "amino_acid"),
    ("l-hpc",               "amino_acid"),   # hydroxyprolyl collagen peptide
    ("peptide",             "amino_acid"),
    # Minerals / inorganic nutrients
    ("zinc gluconate",      "mineral_nutrient"),
    ("ferrous gluconate",   "mineral_nutrient"),
    ("ferrous sulphate",    "mineral_nutrient"),
    ("electrolytic iron",   "mineral_nutrient"),
    ("manganese citrate",   "mineral_nutrient"),
    ("magnesium aspartate", "mineral_nutrient"),
    ("magnesium gluconate", "mineral_nutrient"),
    ("magnesium threonate", "mineral_nutrient"),
    ("zinc",                "mineral_nutrient"),
    ("magnesium",           "mineral_nutrient"),
    ("calcium b-hydroxy",   "mineral_nutrient"),  # HMB
    ("cahmb",               "mineral_nutrient"),
    ("electrolyte",         "mineral_nutrient"),
    ("sodium img",          "mineral_nutrient"),   # sodium iodide
    ("iodate",              "mineral_nutrient"),
]

# Dairy product subtype classification
DAIRY_SUBTYPE_RULES: list[tuple[str, str]] = [
    ("yogurt",          "yogurt"),
    ("yoghurt",         "yogurt"),
    ("dahi",            "fresh_curd"),
    ("curd",            "fresh_curd"),
    ("paneer",          "paneer"),
    ("chhena",          "paneer"),
    ("chenna",          "paneer"),
    ("cottage cheese",  "soft_cheese"),
    ("cream cheese",    "soft_cheese"),
    ("cheese",          "hard_cheese"),       # generic — needs further refinement
    ("khoa",            "heat_concentrated"),
    ("khoya",           "heat_concentrated"),
    ("rabdi",           "heat_concentrated"),
    ("ice cream",       "frozen_dessert"),
    ("sour cream",      "fermented_cream"),
    ("cultured cream",  "fermented_cream"),
    ("buttermilk",      "fermented_milk"),
    ("lassi",           "fermented_milk"),
    ("kefir",           "fermented_milk"),
    ("quark",           "soft_cheese"),
    ("fromage",         "soft_cheese"),
]

# Milling grade rules keyed on variant name tokens
MILLING_GRADE_RULES: list[tuple[str, str]] = [
    ("maida",               "refined"),
    ("refined flour",       "refined"),
    ("white flour",         "refined"),
    ("all purpose flour",   "refined"),
    ("atta",                "whole"),
    ("whole wheat",         "whole"),
    ("whole grain",         "whole"),
    ("wholewheat",          "whole"),
    ("wholegrain",          "whole"),
    ("resultant atta",      "resultant"),
    ("semolina",            "semolina"),
    ("sooji",               "semolina"),
    ("suji",                "semolina"),
    ("rava",                "semolina"),
    ("rawa",                "semolina"),
    ("bran",                "bran"),
    ("wheat bran",          "bran"),
    ("rice bran",           "bran"),
    ("fortified",           "fortified"),
    ("bleached",            "bleached"),
    ("enriched flour",      "fortified"),
    ("starch",              "starch"),
    ("gluten",              "gluten_extract"),
    ("vital gluten",        "gluten_extract"),
]

# Oil fraction rules
OIL_FRACTION_RULES: list[tuple[str, str]] = [
    ("crude",               "crude"),
    ("raw oil",             "crude"),
    ("unrefined",           "crude"),
    ("cold pressed",        "cold_pressed"),
    ("cold-pressed",        "cold_pressed"),
    ("virgin",              "cold_pressed"),
    ("extra virgin",        "cold_pressed"),
    ("refined",             "refined"),
    ("rbd",                 "bleached_deodorised"),     # refined, bleached, deodorised
    ("bleached",            "bleached_deodorised"),
    ("deodorised",          "bleached_deodorised"),
    ("deodorized",          "bleached_deodorised"),
    ("hydrogenated",        "hydrogenated"),
    ("partially hydrogenated", "partially_hydrogenated"),
    ("vanaspati",           "hydrogenated"),
    ("palmolein",           "palmolein"),
    ("palm olein",          "palmolein"),
    ("palm kernel",         "kernel"),
    ("kernel oil",          "kernel"),
    ("stearin",             "stearin"),
    ("palm stearin",        "stearin"),
    ("fractionated",        "fractionated"),
    ("high oleic",          "high_oleic"),
    ("mid oleic",           "mid_oleic"),
    ("interesterified",     "interesterified"),
]

# Protein fraction rules
PROTEIN_FRACTION_RULES: list[tuple[str, str]] = [
    ("whey protein isolate",    "whey_isolate"),
    ("wpi",                     "whey_isolate"),
    ("whey protein concentrate","whey_concentrate"),
    ("wpc",                     "whey_concentrate"),
    ("whey protein hydrolsate", "whey_hydrolysate"),
    ("whey protein",            "whey_concentrate"),   # generic whey → concentrate
    ("casein",                  "casein"),
    ("sodium caseinate",        "casein"),
    ("calcium caseinate",       "casein"),
    ("milk protein concentrate","total_milk_protein"),
    ("mpc",                     "total_milk_protein"),
    ("milk protein",            "total_milk_protein"),
    ("paneer protein",          "casein"),
    ("hydrolysed",              "hydrolysate"),
    ("hydrolyzed",              "hydrolysate"),
    ("hydralyzed",              "hydrolysate"),
    ("hydrolized",              "hydrolysate"),
    ("hvp",                     "hydrolysate"),
    ("tvp",                     "textured_plant_protein"),
    ("soya protein",            "plant_protein"),
    ("pea protein",             "plant_protein"),
    ("lentil protein",          "plant_protein"),
    ("moong dal protein",       "plant_protein"),
    ("vegetable protein",       "plant_protein"),
    ("wheat gluten",            "plant_protein"),
    ("vital gluten",            "plant_protein"),
    ("vital wheat protein",     "plant_protein"),
    ("sunflower gluten",        "plant_protein"),
    ("egg white",               "egg_white_protein"),
    ("glutamine peptides",      "hydrolysate"),
    ("nutritional yeast protein","microbial_protein"),
]

# Sugar form rules
SUGAR_FORM_RULES: list[tuple[str, str]] = [
    ("isomalt",         "sugar_alcohol"),
    ("maltitol",        "sugar_alcohol"),
    ("sorbitol",        "sugar_alcohol"),
    ("xylitol",         "sugar_alcohol"),
    ("erythritol",      "sugar_alcohol"),
    ("mishri",          "raw_unrefined"),
    ("misri",           "raw_unrefined"),
    ("sharkara",        "raw_unrefined"),
    ("shakkar",         "raw_unrefined"),
    ("khandsari",       "molasses_partial"),
    ("jaggery",         "raw_unrefined"),
    ("gur ",            "raw_unrefined"),
    ("raw sugar",       "raw_unrefined"),
    ("brown sugar",     "molasses_partial"),
    ("molasses",        "molasses_partial"),
    ("invert sugar",    "invert_sugar"),
    ("sucrose",         "refined_sucrose"),
    ("sugar",           "refined_sucrose"),    # generic — overridden by specific rules above
    # Multilingual names for sucrose
    ("zucker",          "refined_sucrose"),
    ("sucre",           "refined_sucrose"),
    ("đường",           "refined_sucrose"),
    ("suco",            "refined_sucrose"),
]

# Language tags for non-English variants (ISO 639-1)
LANGUAGE_RULES: list[tuple[str, str]] = [
    ("salz",    "de"),
    ("zucker",  "de"),
    ("wasser",  "de"),
    ("sucre",   "fr"),
    ("sel",     "fr"),
    ("eau",     "fr"),
    ("đường",   "vi"),
    ("muối",    "vi"),
    ("nước",    "vi"),
    ("suco",    "pt"),
    ("açúcar",  "pt"),
    ("sal",     "es"),   # also pt — ambiguous, mark es
    ("azúcar",  "es"),
    ("sait",    "fr"),   # French misspelling of "sel" in corpus
    ("kalanamak", "hi"),
    ("khandsari", "hi"),
    ("shakkar",   "hi"),
    ("sharkara",  "hi"),
    ("mishri",    "hi"),
    ("misri",     "hi"),
    ("khar alkaline salt", "hi"),  # Assamese/Hindi term
    ("himalayan", None),           # not a language tag, skip
]

# ---------------------------------------------------------------------------
# f=base ingredient → f_revised taxonomy rules
# Applied in order; first match wins.
# ---------------------------------------------------------------------------

# Variant tokens or source that signal fortification agents
FORTIFICATION_TOKENS: set[str] = {
    "vitamin", "vitamins", "thiamin", "thiamine", "riboflavin", "niacin",
    "nicotinamide", "folic acid", "folate", "biotin", "cobalamin", "cyanocobalamin",
    "ergocalciferol", "cholecalciferol", "tocopherol", "retinol",
    "pyridoxine", "pyridoxal",
    "amino acid", "leucine", "isoleucine", "valine", "lysine", "threonine",
    "methionine", "tryptophan", "phenylalanine", "phenylalaline",
    "histidine", "arginine", "l-arginine", "glutamine", "l-glutamine",
    "taurine", "carnitine", "l-carnitine", "l-camitine", "cysteine",
    "creatine", "peptide", "l-hpc",
    "zinc gluconate", "ferrous gluconate", "ferrous sulphate",
    "electrolytic iron", "manganese citrate", "sodium img", "iodate",
    "electrolyte",
    # Standalone mineral nutrients (single-element supplement forms)
    "zinc oxide", "zinc sulphate",
    "magnesium oxide", "magnesium sulphate", "magnesium aspartate",
    "magnesium carbonate", "magnesium gluconate", "magnesium hydroxide",
    "magnesium threonate", "salts of magnesium",
    "ferrous salt", "ferrous fumarate",
    "calcium salt",
    "potassium chloride",          # mineral fortification / salt substitute
    "calcium b-hydroxy", "cahmb", # HMB — functional nutrient
    "l-camitine",                  # typo for l-carnitine in corpus
}

# m_explicit values that signal a processed (not raw) ingredient
PROCESSED_M: set[str] = {
    "protein concentrate", "protein isolate", "fat fraction",
    "powder", "dense block", "skim/defatted meal", "starch flour",
    "whey powder", "modified starch powder", "oil", "concentrate",
    "refined oil",
}

# Variant tokens that signal fermentation agents (cultures, enzymes)
FERMENTATION_TOKENS: set[str] = {
    "culture", "lactic", "lactobacillus", "lactococcus", "streptococcus",
    "bifidobacterium", "acidophilus", "bulgaricus", "thermophilus",
    "rennet", "enzyme", "amylase", "protease", "lipase", "lactase",
    "glucoamylase", "beta-galactosidase", "galactosidase",
    "aspergillus", "kluyveromyces", "yeast", "ferment",
    "microbial rennet", "cheese enzymes", "starter",
    "ultrasorb tech lactase",
}

# Sources that are primarily agricultural whole/raw materials
AGRICULTURAL_SOURCES: set[str] = {
    "wheat", "rice", "corn", "soybean", "palm", "sunflower", "groundnut",
    "coconut", "cotton", "rapeseed", "tapioca", "wood pulp", "sugarcane",
    "milk", "egg", "mango", "chickpea", "lentil", "mung bean", "urad dal",
    "black gram", "green gram", "pea", "carrot", "tomato", "onion",
    "potato", "spinach", "ginger", "garlic", "chilli", "coriander",
    "cardamom", "pepper", "turmeric", "cumin", "mustard", "fenugreek",
    "fennel", "clove", "cinnamon", "nutmeg", "mace", "bay leaf",
    "tamarind", "amla", "tulsi", "ashwagandha", "moringa", "neem",
    "quinoa", "oat", "barley", "millet", "sorghum", "teff", "amaranth",
    "sesame", "flax", "chia", "hemp", "sunflower", "pumpkin", "yeast",
    "hazelnut", "almond", "walnut", "cashew", "pistachio", "peanut",
    "cocoa", "coffee", "tea", "apple", "banana", "orange", "lemon",
    "berry", "grape", "watermelon", "papaya", "pineapple",
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _lower(v: str) -> str:
    return v.lower().strip()


def extract_ins_number(variant: str) -> str:
    """
    Extract the INS/E-number from a variant string.
    Patterns handled:
      - 'ins 471'         → '471'
      - 'ins 160b(i)'     → '160b(i)'
      - 'ins e330'        → '330'
      - 'color ins 102'   → '102'
      - standalone 'ins 941' → '941'
    Returns the code string or '' if not found.
    """
    v = variant.lower()
    # Pattern: 'ins' followed by optional 'e', then digits, optional suffix
    pat = re.compile(
        r'\bins\s+e?'               # 'ins ' or 'ins e'
        r'(\d{2,4}'                 # 2-4 digits
        r'(?:[a-z]{1,2})?'          # optional letter suffix (a, b, ii …)
        r'(?:\([ivx]+\))?)',        # optional roman numeral in parens
        re.IGNORECASE
    )
    m = pat.search(v)
    if m:
        return m.group(1).lower()
    return ""


def lookup_compound_name(ins: str) -> str:
    """Return the Codex common name for a given INS code, or ''."""
    return INS_TO_NAME.get(ins, "")


def classify_nutrient(variant: str, source: str) -> str:
    """Return nutrient_class enum value or ''."""
    v = _lower(variant)
    for token, cls in NUTRIENT_CLASS_RULES:
        if token in v:
            return cls
    return ""


def classify_dairy_subtype(variant: str, m_explicit: str) -> str:
    """Return dairy_product_subtype enum value or ''."""
    if m_explicit not in ("dense block", "NULL"):
        return ""
    v = _lower(variant)
    for token, subtype in DAIRY_SUBTYPE_RULES:
        if token in v:
            return subtype
    return ""


def classify_milling_grade(variant: str, m_explicit: str, source: str) -> str:
    """Return milling_grade enum value or ''."""
    grain_sources = {"wheat", "corn", "rice", "black gram", "chickpea",
                     "millet", "oat", "barley", "sorghum", "rye"}
    # Only apply to grain-like sources
    if not any(gs in source.lower() for gs in grain_sources):
        return ""
    if m_explicit not in ("flour/fine powder", "coarse grits", "skim/defatted meal",
                          "starch flour", "NULL", "flakes", "protein isolate",
                          "protein concentrate"):
        return ""
    v = _lower(variant)
    for token, grade in MILLING_GRADE_RULES:
        if token in v:
            return grade
    return ""


def classify_oil_fraction(variant: str, m_explicit: str, source: str) -> str:
    """Return oil_fraction enum value or ''."""
    if m_explicit not in ("oil", "fat fraction", "NULL"):
        return ""
    v = _lower(variant)
    for token, frac in OIL_FRACTION_RULES:
        if token in v:
            return frac
    # Default: if m=oil and source names an oil crop, mark as source_specified/unclassified
    return ""


def classify_protein_fraction(variant: str, m_explicit: str) -> str:
    """Return protein_fraction enum value or ''."""
    if m_explicit not in ("protein concentrate", "protein isolate", "NULL"):
        return ""
    v = _lower(variant)
    for token, frac in PROTEIN_FRACTION_RULES:
        if token in v:
            return frac
    return ""


def classify_sugar_form(variant: str, source: str) -> str:
    """Return sugar_form enum value or ''."""
    sweet_sources = {"sugarcane", "corn", "synthetic", "palm"}
    if not any(ss in source.lower() for ss in sweet_sources):
        return ""
    v = _lower(variant)
    # Apply rules in order (more specific first)
    for token, form in SUGAR_FORM_RULES:
        if token in v:
            return form
    return ""


def detect_language(variant: str) -> str:
    """Return ISO 639-1 language tag if non-English variant detected, else ''."""
    v = _lower(variant)
    for token, tag in LANGUAGE_RULES:
        if not tag:
            continue
        # Use word-boundary matching to avoid substring false positives
        # e.g. 'sal' must not match 'salt'
        if re.search(r'\b' + re.escape(token) + r'\b', v):
            return tag
    return ""


def revise_f(row: dict) -> str:
    """
    Compute f_revised.

    - For f_explicit == 'base ingredient': splits into four sub-types
      (raw_agricultural_material | processed_ingredient |
       fortification_agent | fermentation_agent).
    - For f_explicit == 'NULL': fills in fortification_agent or
      fermentation_agent where the variant clearly signals it (e.g. vitamins,
      amino acids, cultures) — per Cluster 2 analysis.
    - All other f_explicit values are returned unchanged.
    """
    f = row["f_explicit"]
    v = _lower(row["variant"])
    m = row["m_explicit"]

    if f == "NULL":
        # Only fill NULLs we can be confident about
        if any(tok in v for tok in FERMENTATION_TOKENS):
            return "fermentation_agent"
        if any(tok in v for tok in FORTIFICATION_TOKENS):
            return "fortification_agent"
        return f  # leave other NULLs alone

    if f != "base ingredient":
        return f

    v = _lower(row["variant"])
    m = row["m_explicit"]
    src = _lower(row["source"])

    # 1. Fermentation agents (cultures, enzymes)
    if any(tok in v for tok in FERMENTATION_TOKENS):
        return "fermentation_agent"

    # 2. Fortification agents (vitamins, amino acids, functional nutrients)
    if any(tok in v for tok in FORTIFICATION_TOKENS):
        return "fortification_agent"

    # 3. Processed ingredients (extracted/refined forms)
    if m in PROCESSED_M:
        return "processed_ingredient"

    # 4. Default for agricultural whole/raw forms
    return "raw_agricultural_material"


# ---------------------------------------------------------------------------
# Main enrichment loop
# ---------------------------------------------------------------------------

def enrich(rows: list[dict]) -> list[dict]:
    enriched = []
    for row in rows:
        v = row["variant"]
        m = row["m_explicit"]
        f = row["f_explicit"]
        src = row["source"]

        # 1. INS number
        ins = extract_ins_number(v)
        row["ins_number"] = ins

        # 2. Compound name (from INS lookup, or known chemical name in variant)
        row["compound_name"] = lookup_compound_name(ins) if ins else ""

        # 3. Nutrient class (only for synthetic/mineral sources where relevant)
        row["nutrient_class"] = classify_nutrient(v, src)

        # 4. Dairy product subtype (only for milk source)
        if "milk" in src.lower():
            row["dairy_product_subtype"] = classify_dairy_subtype(v, m)
        else:
            row["dairy_product_subtype"] = ""

        # 5. Milling grade
        row["milling_grade"] = classify_milling_grade(v, m, src)

        # 6. Oil fraction
        row["oil_fraction"] = classify_oil_fraction(v, m, src)

        # 7. Protein fraction
        row["protein_fraction"] = classify_protein_fraction(v, m)

        # 8. Sugar form
        row["sugar_form"] = classify_sugar_form(v, src)

        # 9. Language tag
        row["language_tag"] = detect_language(v)

        # 10. Revised f taxonomy
        row["f_revised"] = revise_f(row)

        enriched.append(row)
    return enriched


# ---------------------------------------------------------------------------
# Statistics / summary
# ---------------------------------------------------------------------------

def summarise(original: list[dict], enriched: list[dict]) -> str:
    lines: list[str] = ["EMF Enrichment Summary", "=" * 60, ""]

    def _count(rows, field, exclude=("", "NULL")):
        return sum(1 for r in rows if r.get(field, "") not in exclude)

    lines.append(f"Total rows processed: {len(enriched)}")
    lines.append("")

    # INS numbers
    ins_count = _count(enriched, "ins_number")
    lines.append(f"ins_number populated:         {ins_count:5d} ({ins_count/len(enriched)*100:.1f}%)")

    # Compound names derived
    cname_count = _count(enriched, "compound_name")
    lines.append(f"compound_name populated:      {cname_count:5d} ({cname_count/len(enriched)*100:.1f}%)")

    # Nutrient class
    nc_count = _count(enriched, "nutrient_class")
    lines.append(f"nutrient_class populated:     {nc_count:5d} ({nc_count/len(enriched)*100:.1f}%)")

    # Dairy subtype
    ds_count = _count(enriched, "dairy_product_subtype")
    lines.append(f"dairy_product_subtype:        {ds_count:5d} ({ds_count/len(enriched)*100:.1f}%)")

    # Milling grade
    mg_count = _count(enriched, "milling_grade")
    lines.append(f"milling_grade populated:      {mg_count:5d} ({mg_count/len(enriched)*100:.1f}%)")

    # Oil fraction
    of_count = _count(enriched, "oil_fraction")
    lines.append(f"oil_fraction populated:       {of_count:5d} ({of_count/len(enriched)*100:.1f}%)")

    # Protein fraction
    pf_count = _count(enriched, "protein_fraction")
    lines.append(f"protein_fraction populated:   {pf_count:5d} ({pf_count/len(enriched)*100:.1f}%)")

    # Sugar form
    sf_count = _count(enriched, "sugar_form")
    lines.append(f"sugar_form populated:         {sf_count:5d} ({sf_count/len(enriched)*100:.1f}%)")

    # Language tag
    lt_count = _count(enriched, "language_tag")
    lines.append(f"language_tag populated:       {lt_count:5d} ({lt_count/len(enriched)*100:.1f}%)")

    lines.append("")
    lines.append("f_revised: changes from f=base ingredient")
    lines.append("-" * 45)
    from collections import Counter
    orig_base = [r for r in original if r["f_explicit"] == "base ingredient"]
    orig_count = len(orig_base)
    lines.append(f"  f=base ingredient rows:     {orig_count}")

    revised = [r for r in enriched if r["f_explicit"] == "base ingredient"]
    new_vals = Counter(r["f_revised"] for r in revised)
    for val, cnt in sorted(new_vals.items(), key=lambda x: -x[1]):
        lines.append(f"  → {val:<35} {cnt:4d} ({cnt/orig_count*100:.1f}%)")

    lines.append("")
    lines.append("Nutrient class distribution (nutrient_class != ''):")
    lines.append("-" * 45)
    nc_vals = Counter(r["nutrient_class"] for r in enriched if r["nutrient_class"])
    for val, cnt in sorted(nc_vals.items(), key=lambda x: -x[1]):
        lines.append(f"  {val:<35} {cnt:4d}")

    lines.append("")
    lines.append("Dairy product subtypes:")
    lines.append("-" * 45)
    ds_vals = Counter(r["dairy_product_subtype"] for r in enriched if r["dairy_product_subtype"])
    for val, cnt in sorted(ds_vals.items(), key=lambda x: -x[1]):
        lines.append(f"  {val:<35} {cnt:4d}")

    lines.append("")
    lines.append("Oil fraction distribution:")
    lines.append("-" * 45)
    of_vals = Counter(r["oil_fraction"] for r in enriched if r["oil_fraction"])
    for val, cnt in sorted(of_vals.items(), key=lambda x: -x[1]):
        lines.append(f"  {val:<35} {cnt:4d}")

    lines.append("")
    lines.append("Protein fraction distribution:")
    lines.append("-" * 45)
    pf_vals = Counter(r["protein_fraction"] for r in enriched if r["protein_fraction"])
    for val, cnt in sorted(pf_vals.items(), key=lambda x: -x[1]):
        lines.append(f"  {val:<35} {cnt:4d}")

    lines.append("")
    lines.append("Milling grade distribution:")
    lines.append("-" * 45)
    mg_vals = Counter(r["milling_grade"] for r in enriched if r["milling_grade"])
    for val, cnt in sorted(mg_vals.items(), key=lambda x: -x[1]):
        lines.append(f"  {val:<35} {cnt:4d}")

    lines.append("")
    lines.append("Sugar form distribution:")
    lines.append("-" * 45)
    sg_vals = Counter(r["sugar_form"] for r in enriched if r["sugar_form"])
    for val, cnt in sorted(sg_vals.items(), key=lambda x: -x[1]):
        lines.append(f"  {val:<35} {cnt:4d}")

    lines.append("")
    lines.append("Language tags detected:")
    lines.append("-" * 45)
    lt_vals = Counter(r["language_tag"] for r in enriched if r["language_tag"])
    for val, cnt in sorted(lt_vals.items(), key=lambda x: -x[1]):
        lines.append(f"  {val:<35} {cnt:4d}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    print(f"Reading {INPUT_CSV} …", flush=True)
    with open(INPUT_CSV, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        original_fieldnames = list(reader.fieldnames)
        rows = list(reader)

    print(f"  {len(rows)} rows loaded.")

    # Keep a copy of originals for summary comparison
    import copy
    original_rows = copy.deepcopy(rows)

    print("Enriching …", flush=True)
    enriched = enrich(rows)

    # Define output column order: original columns first, then new enrichment columns
    NEW_COLS = [
        "ins_number", "compound_name", "nutrient_class",
        "dairy_product_subtype", "milling_grade", "oil_fraction",
        "protein_fraction", "sugar_form", "language_tag", "f_revised",
    ]
    out_fieldnames = original_fieldnames + NEW_COLS

    print(f"Writing {OUTPUT_CSV} …", flush=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=out_fieldnames)
        writer.writeheader()
        writer.writerows(enriched)

    summary_text = summarise(original_rows, enriched)
    SUMMARY.write_text(summary_text, encoding="utf-8")

    print(f"Writing summary to {SUMMARY} …")
    print()
    print(summary_text)


if __name__ == "__main__":
    main()

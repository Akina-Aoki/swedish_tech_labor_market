from __future__ import annotations
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple, Set
from tqdm import tqdm

"""
Syfte: Detta skript agerar 'silver Layer' i vår pipeline. 
Det tar rådata (JSONL) från Arbetsförmedlingen, filtrerar ut irrelevanta annonser och taggar upp kompetenser (skills) baserat på vår taxonomi. 
Input: data/raw/2025_enriched.jsonl 
Output: data/clean/af/af_ads_focus.jsonl (Endast relevanta Data/IT-jobb)
"""

# =========================
# 1. Config & Constants
# =========================
DATA_IT_CONCEPT_ID = "apaj_2ja_luf"
DATA_IT_LABEL = "data/it"

# Regex för ord-tokenisering (tillåter c++, .net, node.js)
_WORD_RE = re.compile(r"[a-zåäö0-9\+#\.]+")


@dataclass
class TaxonomyConfig:
    tags: Dict[str, List[str]]
    exclude_phrases: List[str]
    weak_hits: Set[str]


@dataclass
class RunStats:
    read: int = 0
    skipped_not_data_it: int = 0
    written_silver_raw: int = 0  # Data/IT (allt)
    written_silver_focus: int = 0  # Focus (filtrerat)
    top_tags: Counter = field(default_factory=Counter)


# =========================
# 2. Helpers (Pure Functions)
# =========================


def normalize_text(s: str) -> str:
    """Tar bort extra whitespace och gör lowercase."""
    if not s:
        return ""
    return " ".join(s.lower().split())


def load_taxonomy_and_config(path: Path) -> TaxonomyConfig:
    """Laddar både keywords och config (exclude/weak) från samma JSON."""
    raw = json.loads(path.read_text(encoding="utf-8"))

    # Hämta config blocket om det finns, annars tomma listor
    config = raw.pop("__config__", {})
    exclude = config.get("exclude_phrases", [])
    weak = set(config.get("weak_hits", []))

    # Resten är taggar
    tags = {k: [normalize_text(x) for x in v] for k, v in raw.items()}

    return TaxonomyConfig(tags=tags, exclude_phrases=exclude, weak_hits=weak)


def get_text_tokens(text: str) -> Set[str]:
    """Returnerar ett set av unika ord för snabb sökning."""
    return set(_WORD_RE.findall(text.lower()))


# =========================
# 3. Core Logic (The Brain)
# =========================
def is_data_it_ad(ad: Dict[str, Any]) -> bool:
    """Dörrvakten: Är detta en Data/IT-annons?"""
    occ = ad.get("occupation_field")
    if not occ:
        return False

    # Helper för att kolla enskilt objekt
    def check_field(o: Dict[str, Any]) -> bool:
        cid = str(o.get("concept_id", "")).strip().lower()
        lbl = str(o.get("label", "")).strip().lower()
        return (cid == DATA_IT_CONCEPT_ID) or (DATA_IT_LABEL in lbl)

    # Hantera att occupation_field kan vara list eller dict
    if isinstance(occ, list):
        return any(check_field(x) for x in occ if isinstance(x, dict))
    if isinstance(occ, dict):
        return check_field(occ)
    return False


def tag_ad(text: str, config: TaxonomyConfig) -> Tuple[List[str], List[str]]:
    """Matchar text mot taxonomin."""
    found_tags = []
    found_hits = []

    # Förbered text för snabb matchning
    tokens = get_text_tokens(text)

    for tag, keywords in config.tags.items():
        tag_match = False
        for kw in keywords:
            # 1. Exakt matchning (token)
            if " " not in kw:
                if kw in tokens:
                    found_hits.append(kw)
                    tag_match = True
            # 2. Fras-matchning (substring)
            else:
                if kw in text:
                    found_hits.append(kw)
                    tag_match = True

        if tag_match:
            found_tags.append(tag)

    return sorted(list(set(found_tags))), sorted(list(set(found_hits)))


def is_focus_ad(
    text: str, tags: List[str], hits: List[str], config: TaxonomyConfig
) -> bool:
    """
    Avgör om annonsen är "Focus" (Värd att analysera).
    Krav:
    1. Inga exkluderade fraser (t.ex "support")
    2. Har minst en tagg
    3. Har minst en "stark" hit (inte bara "api" eller "server")
    """
    # 1. Check Excludes
    for phrase in config.exclude_phrases:
        if phrase in text:
            return False

    # 2. Check Tags
    if not tags:
        return False

    # 3. Check Strong Hits
    has_strong = any(h not in config.weak_hits for h in hits)
    return has_strong


# =========================
# 4. Pipeline (The Runner)
# =========================


def process_ads(input_path: Path, output_raw: Path, output_focus: Path, tax_path: Path):
    print(f"Starting pipeline...")
    print(f"Input: {input_path}")

    # Init
    config = load_taxonomy_and_config(tax_path)
    stats = RunStats()

    # Öppna filerna
    output_raw.parent.mkdir(parents=True, exist_ok=True)

    # Öppnar output-filerna direkt för streaming-skrivning (sparar minne)
    with open(input_path, "r", encoding="utf-8") as fin, open(
        output_raw, "w", encoding="utf-8"
    ) as f_raw, open(output_focus, "w", encoding="utf-8") as f_focus:

        for line in tqdm(fin, desc="Processing Ads", unit="ads"):
            line = line.strip()
            if not line:
                continue

            try:
                ad = json.loads(line)
                stats.read += 1
            except json.JSONDecodeError:
                continue

            # --- STEP 1: Broad Filter (Data/IT) ---
            if not is_data_it_ad(ad):
                stats.skipped_not_data_it += 1
                continue

            # --- STEP 2: Transform & Tag ---
            # Extrahera text
            title = str(ad.get("headline") or ad.get("title") or "").lower()
            desc = str(ad.get("description") or ad.get("text") or "").lower()
            full_text = f"{title} {desc}"  # Normalized i lower() ovan

            # Tagga
            tags, hits = tag_ad(full_text, config)

            # Bygg Clean Record
            clean_record = {
                "id": ad.get("id") or ad.get("external_id"),
                "title": ad.get("headline") or ad.get("title"),
                "description_limit": full_text[:200],  # Preview för debug
                "tags": tags,
                "hits": hits,
                "url": ad.get("webpage_url", ""),
            }

            # --- STEP 3: Write Silver Raw (Alla Data/IT) ---
            f_raw.write(json.dumps(clean_record, ensure_ascii=False) + "\n")
            stats.written_silver_raw += 1

            # --- STEP 4: Focus Filter (Silver Refined) ---
            if is_focus_ad(full_text, tags, hits, config):
                f_focus.write(json.dumps(clean_record, ensure_ascii=False) + "\n")
                stats.written_silver_focus += 1
                stats.top_tags.update(tags)

    # Summary
    print(f"\nDONE!")
    print(f"Read Rows:       {stats.read}")
    print(f"Data/IT Ads:     {stats.written_silver_raw}")
    print(f"Focus Ads:       {stats.written_silver_focus} (The focus area)")
    print(f"Noise Filtered:  {stats.skipped_not_data_it}")

    if stats.written_silver_raw:
        rate = (stats.written_silver_focus / stats.written_silver_raw) * 100
        print(f"Focus Rate:      {rate:.1f}%")

    print("\n Top Skills (Focus Group):")
    for tag, count in stats.top_tags.most_common(10):
        print(f" - {tag}: {count}")


# =========================
# 5. Main
# =========================
if __name__ == "__main__":
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent  # Anpassa om det behövs
    # Justera sökvägarna om vi flyttar/kör från 'src/transform' eller root
    IN_FILE = Path("data/raw/2020_full_year.jsonl")
    TAX_FILE = Path("sql/mappings/keyword_taxonomy.json")

    OUT_RAW = Path("data/clean/af/af_ads_datait_full_year_2020.jsonl")
    OUT_FOCUS = Path("data/clean/af/af_ads_focus_full_year_2020.jsonl")

    process_ads(IN_FILE, OUT_RAW, OUT_FOCUS, TAX_FILE)

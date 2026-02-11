# =========================
# Block 1: Imports & Config
# =========================
# Skript för att läsa in vår master.jsonl fil i data/clean/af
import json
import psycopg
from pathlib import Path
from tqdm import tqdm


"""
Syfte: Laddar data från Silver Layer (JSONL) till Gold Layer (PostgreSQL).
Kräver att Docker containern är igång.
"""

# Konfig - connection string till Docker
DB_DSN = "postgresql://admin:password123@localhost:5433/skillgap"
# Master filen från silver layer
INPUT_FILE = Path ("data/clean/af/all_years_focus_master.jsonl")


# =========================
# Block 2: Helpers
# =========================
def get_year_from_filename(path: Path) -> int:
    """Placeholder. I framtiden kan denna parsa filnamn eller datumfält
    för att ge korrekt årtal till statistiken."""
    return 2025

# =========================
# Block 3: The Loader (Core Logic)
# =========================
def load_data():
    if not INPUT_FILE.exists():
        print(f"Cannot find input file: {INPUT_FILE}")
        return
    
    print(f"Connecting to DB")

    # Context manager (with...) hanterar kopplingen säkert
    # Den stänger automatiskt kopplingen även om koden kraschar
    with psycopg.connect(DB_DSN) as conn:
        with conn.cursor() as cur:

            # 1. Städa först (Idempotens)
            # RENSAR alla tabeller först för att undvika dubbletter vid omkörning
            print("clearing old data (TRUNCATE)")
            cur.execute("TRUNCATE TABLE ad_skills, ads CASCADE;")

            
            # 2. Förbered läsning
            # Räknar rader, progress bar för att ej drabbas av panik LOL
            total_lines = sum(1 for _ in open(INPUT_FILE, 'r', encoding='utf-8'))
            print("Reading input: {INPUT_FILE}")

            # 3. Loopa och ladda (Streaming)
            with open(INPUT_FILE, "r", encoding="utf-8") as f:
                for line in tqdm(f, total=total_lines, desc="Inserting:"):
                    row = json.loads(line)

                    # A) Insert ad (annons)
                    # Kör med ON CONFLICT DO NOTHING, uppkommer issues så görs ingenting för säkerhets skull
                    cur.execute("""
                                INSERT INTO ads (id, title, url, description, source_year)
                                VALUES (%s, %s, %s, %s, %s)
                                ON CONFLICT (id) DO NOTHING;
                    """, (
                        row.get('id'),
                        row.get('title'),
                        row.get('url'),
                        row.get('description_limit'), # Kan byta till description_raw
                        get_year_from_filename(INPUT_FILE) # Anropar helpern
                    ))

                    # B) Insert TAGS (våra kategorier)
                    for tag in row.get('tags', []):
                        cur.execute("""
                            INSERT INTO ad_skills(ad_id, skill, skill_type)
                            VALUES (%s, %s, 'tag');
                        """, (row.get('id'), tag))


                    # C) Insert HITS(Specifika KEYWORDS i keyword_taxonomy.json)
                    for hit in row.get('hits', []):
                        cur.execute("""
                            INSERT INTO ad_skills (ad_id, skill, skill_type)
                            VALUES (%s, %s, 'keyword');
                        """, (row.get('id'), hit))
    # Notera: 'with psycopg.connect' committar (sparar) automatiskt när blocket tar slut!
    print("Done, vår data ligger ni i PostgreSQL DB")

# =========================
# Block 4: Execution
# =========================
if __name__ == "__main__":
    load_data()
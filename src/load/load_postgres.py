# Skript för att läsa in vår master.jsonl fil i data/clean/af

import json
import psycopg
from pathlib import Path
from tqdm import tqdm

# Konfig
DB_DSN = "postgresql://admin:password123@localhost:5433/skillgap"
# Master filen från silver layer
INPUT_FILE = Path ("data/clean/af/all_years_focus_master.jsonl")



def get_year_from_filename(path: Path) -> int:
    """Default till år 2025. Eftersom vi kör en master fil kan vi behöva vara smartare här sen,
    men vi får köra på 2025 som placeholder om det ej finns datum i jsonl filen"""
    return 2025

# Läs in datan
def load_data():
    if not INPUT_FILE.exists():
        print(f"Cannot find input file: {INPUT_FILE}")
        return
    

    print(f"Connecting to DB")

    # Context manager(Psycopg) hanterar connection och transaction automatiskt samtidigt
    with psycopg.connect(DB_DSN) as conn:
        with conn.cursor() as cur:

            # RENSAR alla tabeller först för att undvika dubbletter vid omkörning
            print("clearing old data (TRUNCATE)")
            cur.execute("TRUNCATE TABLE ad_skills, ads CASCADE;")

            print("Reading input: {INPUT_FILE}")
            # Räknar rader, progress bar för att ej drabbas av panik LOL
            total_lines = sum(1 for _ in open(INPUT_FILE, 'r', encoding='utf-8'))

            with open(INPUT_FILE, "r", encoding="utf-8") as f:
                for line in tqdm(f, total=total_lines, desc="Inserting:"):
                    row = json.loads(line)

                    # 1) Insert AD
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
                        2025 # TODO: Kolla upp om det måste parsas från 'publication_data' om det finns i json om vi vill ha rätt år
                    ))

                    # 2) Insert TAGS (våra kategorier)
                    for tag in row.get('tags', []):
                        cur.execute("""
                            INSERT INTO ad_skills(ad_id, skill, skill_type)
                            VALUES (%s, %s, 'tag');
                        """, (row.get('id'), tag))


                    # 3) Insert HITS(Specifika KEYWORDS i keyword_taxonomy.json)
                    for hit in row.get('hits', []):
                        cur.execute("""
                            INSERT INTO ad_skills (ad_id, skill, skill_type)
                            VALUES (%s, %s, 'keyword');
                        """, (row.get('id'), hit))

    print("Done, vår data ligger ni i PostgreSQL DB")

if __name__ == "__main__":
    load_data()
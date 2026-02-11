# Module Overview -  Gold layer loader

`src/load/load_postgres.py` ansvarar för **EL**steget (Extract + load) in i vårt gold layer. Den tar den tvättade datan och strukturerar den i vår postgres db.

## Block 1: Config & Setup
- Vad block 1 gör? 
    - Definierar kopplingen till infrastrukturen.
    - `DB_DSN`: Connection string som pekar på vår Docker container. Vi använder port 5433 för att inte krocka med lokala installationer.
    - `INPUT_FILE`: Pekar på 'Master dataset' från Silver Layer.

## Block 2: Helpers
- Vad block 2 gör? 
    - Stödfunktioner för datatvätt i sista minuten.
    - `get_year_from_filename`: En funktion för att bestämma vilket årtal annonsen tillhör. (Just nu placeholder, ska utvecklas vid nästa session för att hantera historisk data)

## Block 3: The Loader (Core Logic)
- Vad block 3 gör?
    - Läser JSONL och normaliserar datan till SQL tabeller.
    - `Context Management`: Använder `with psycopg.connect` för att automatiskt hantera transaktioner. 
    - `Truncate`: Tömmer tabellerna (`ads` och `ad_skills`) innan laddning. Det garanterar att vi aldrig får dubbletter, även om vi kör skriptet 100 gånger.
    - `Streaming`: Läser filen rad för rad med `json.loads` för att vara minneseffektivt och ej krascha.

- **Normalization (JSON to Star Schema för Power BI):**
    - Delar upp hierarkisk JSON struktur.
    - Annonsens metadata sparas i tabellen `ads`.
    - Kompetenser (De tags och keywords vi har) exploderas ut till tabellen `ad_skills`. Det gör att vi kan filtrera enklare i Power BI.

## Block 4: Execution
- Vad block 4 gör?
    - Startpunkten för allting.
    - Säkerställer att vårt skript bara körs om man anropar det direkt, inte om man importerar det.
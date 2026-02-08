# Readme för clean_ads_keywords.py

## Hur ändrar du logiken?

- **Lägga till nytt ord?** 
  -  Redigera sql/mappings/keyword_taxonomy.json. Lägg till ordet i listan. Rör inte Python koden.

- **Får vi med för mycket support-jobb?**
  - Lägg till ordet (tex "helpdesk") i listan exclude_phrases i JSON-filen.

- **Vill du ändra filnamn?** (Både input OCH output)
  - Kolla längst ner i Python-filen under if `__name__ == "__main__":`
  - Var även noga med att markera filnamnen med t.ex 
  - `2025_full_year.jsonl`
  - `af_ads_datait_full_year.jsonl`
  - `af_ads_focus_full_year.jsonl`
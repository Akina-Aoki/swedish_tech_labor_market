# Module overview

## Block 2: Helpers (Pure Functions)
- Vad block 2 gör?
    - Små verktyg som inte ändrar på något utanför sig själva.  

- `load_taxonomy_and_config`: Hämtar både keywords och regler (tex. ord att exkludera) från vår externa JSON-fil. Detta gör att vi kan ändra logik utan att ändra kod.  

- `normalize_text`: Städar text (tar bort konstiga mellanslag, gör allt till gemener) så att vi kan jämföra äpplen med äpplen.

## Block 3: Core logic
- Vad block 3 gör?
    - Själva "hjärnan" i det hela. Where the magic happens.  

- `is_data_it_ad`: "Dörrvakten". Kollar om annonsen har rätt concept_id eller etikett för att ens få komma in i systemet.  

- `tag_ad`: Scannar annonstexten mot vår keyword_lista. Returnerar hittade taggar (tex. "Data Engineering") och specifika ord (tex. "Python")

- `is_focus_ad`: Vårt kvalitetsfilter. Avgör om annonsen är värd att analysera. Den måste ha relevanta taggar och får inte innehålla exkluderade ord (som "supporttekniker")

## Block 4: Pipeline (the runner)
- Vad block 4 gör?
    - Här flödet styrs.

- Öppnar filer "streamat" (rad för rad) för att spara minne.
- Kör Step 1: Grovsortering (Data/IT eller ej?)
- Kör Step 2: Tvättar och taggar texten.
- Kör Step 3: Sparar ner alla Data/IT-annonser (bra för totalstatistik)
- Kör Step 4: Sparar ner fokus-annonserna (vår "Guldgruva" för analys)
- Skriver ut statistik i terminalen när det är klart.
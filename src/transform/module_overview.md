# Module overview

## Block 1: Config och constants
- Vad block 1 gör?
    - Sätter våra regler i stora drag.

- Definierar `DATA_IT_CONCEPT_ID` och label för att veta vad som är en Data/IT annons.

- Sätter upp `_WORD_RE` (Regular Expression) som bestämmer vad som räknas som ett ord (viktigt för att kunna matcha udda ord så som 'c++' eller '.net' mer korrekt utan att koden tror att punkten är ett slut på meningen)

## Block 2: Helpers (Pure Functions)
- Vad block 2 gör?
    - Små verktyg som inte ändrar på något utanför sig själva.  

- `load_taxonomy_and_config`: Hämtar både keywords och regler (tex. ord att exkludera) från vår externa JSON-fil. Detta gör att vi kan ändra logik utan att ändra kod.  

- `normalize_text`: Städar text (tar bort konstiga mellanslag, gör allt till gemener) så att vi kan jämföra äpplen med äpplen.

- `get_text_tokens`: Hackar upp texten i unika ord för snabb sökning.

## Block 3: Core logic
- Vad block 3 gör?
    - Själva "hjärnan" i det hela.  

- `is_data_it_ad`: "Dörrvakten". Kollar om annonsen har rätt concept_id eller etikett för att ens få komma in i systemet.  

- `tag_ad`: Scannar annonstexten mot vår keyword_lista. Returnerar hittade taggar t.ex Data Engineering(Tags) och exakta ord t.ex Python (Hits)

- `is_focus_ad`: Vårt kvalitetsfilter. Avgör om annonsen är värd att analysera. Den måste ha relevanta taggar och får inte innehålla exkluderade ord (som "supporttekniker")

## Block 4: Pipeline (the runner)
- Vad block 4 gör?
    - Här flödet styrs.
- Streaming: Öppnar filer rad för rad (`with open...`) för att spara minne.

- Date Extraction: **Ny** logik som letar upp `publication_date` i rådatan och extraherar årtalet t.ex 2023 så vi kan göra analyser över tid.

- Transformation:
    1.  Sortering (Data/IT eller inte??)
    2.  Tvättar text och extraherar datum.
    3.  Taggar kompetenser.
    4.  Sparar ner till `_datait_` (brutto) och `_focus_` (netto).

- Statistik: Räknar live hur många procent av annonserna som är relevanta "Focus Rate"


## Block 5: Batching
- Vad block 5 gör?
    - Här så står for loopen för batch körningen. Istället för att manuellt mata in filens namn och köra. Dvs **Automatisering**

- Istället för att köra allting och ändra manuellt för varje år så la jag till en lista
    - `YEARS_TO_PROCESS = [2020, 2021, ..., 2025]`

- En for loop itererar igenom listan och konstruerar filnamnen dynamiskt med hjälp av f-strings och kör pipelinen för alla år i en följd.
    - `for year in YEARS_TO_PROCESS:` 

- Detta pga ren lathet samt att garanterar att all data behandlas på exakt samma sätt utan misstag.

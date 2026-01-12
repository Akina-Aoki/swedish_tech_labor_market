# Repo Structure Bible — v1.0

Syfte: En tydlig karta över var allt ska ligga och vad som FÅR ligga i Git.
Se det här dokumentet som "grundlag nr 2" och kompletterar `team_workflow_and_rules.md` dokumentet.

---

## 0) Kärnprinciper (Non-negotiables)

### Git är för: kod + docs + små samples
Git är INTE vår datalake.
Vi committar:
- kod
- dokumentation
- SQL schema/migrations
- små anonymiserade sample-filer (för test och demo) <-- Kom ihåg det som nämns i steg 0 i `team_workflow_and_rules.md` (GDPR & PII)

Vi committar INTE:
- rådata (API dumps, Forms exports)
- filer med PII (GDPR)
- stora binärer (Power BI .pbix, stora Excel, DB-volymer)

**Varför:** säkerhet, ordning, och för att repot ska vara snabbt och delbart.

---

## 1) Folder tree (standard)

Repo-root kan/ska se ut så här:

```
├─ docs/
│  ├─ team_workflow_and_rules.md... ... ... 
│  ├─ glossary_and_how_to.md... ... ... 
│  ├─ pull_requests_checklist.md... ... ... 
│  ├─ repo_structure_bible.md... ... ... 
│  └─ diagrams/
│     ├─ LDM/
│     └─ PDM/
│
├─ src/
│  ├─ ingest/        # hämta data (API/exports) -> raw (lokalt/utanför git)
│  ├─ transform/     # tvätta + normalisera -> clean
│  ├─ load/          # skriva till DB (Postgres)
│  └─ utils/
│
├─ sql/
│  ├─ schema/        # CREATE TABLE, constraints
│  ├─ views/         # BI-vänliga views
│  └─ mappings/      # title aliases, taxonomy mapping
│
├─ data/
│  ├─ samples/       # små anonymiserade exempel som FÅR committas
│  ├─ raw/           # finns lokalt, men IGNORERAS av git (rådata)
│  ├─ private/       # finns lokalt, men IGNORERAS av git (PII/exports)
│  └─ README.md      # var riktig data ligger (SharePoint/Onedrive/google docs etc) + policy
│
├─ notebooks/        # valfritt: endast om vi kör notebooks i teamet
├─ reports/          # export CSV/figurer (om små och icke känsliga)
├─ .gitignore
├─ README.md
└─ pyproject.toml / requirements.txt (beroende på våra val)
```

OBS: Om en mapp behöver finnas men är tom, lägg en `.gitkeep` i den(så sparas det och committas till github)

---

## 2) Vad ska ligga VAR?

### docs/
- Allt som beskriver hur vi jobbar och hur systemet hänger ihop.
- Diagram (PNG/SVG + källfiler, t.ex Mermaid) under `docs/diagrams/`

### src/
- Endast Python-kod.
- Inga datafiler här.

### sql/
- Schema och constraints (Postgres tex).
- Views som Power BI kan konsumera.
- Mapping filer (taxonomi, title aliases) som SQL eller CSV (små filer såklart).

### data/
`data/` finns för att göra repot självförklarande. Men **riktig data** ligger utanför Git (Återigen, GDPR PII som vi måste tänka på!)

- `data/samples/`: små, anonymiserade exempel (max några KB/MB).
- `data/raw/`: rådata från API/Forms. **IGNORERAS**
- `data/private/`: exports som kan innehålla PII. **IGNORERAS**
- `data/README.md`: pekar på var data ligger (delad yta) + hur man hämtar.

### reports/
- Endast outputs som är små och ofarliga (tex en aggregerad CSV utan PII).
- Stora exports: utanför Git.

### notebooks/ (om vi vill använda oss av det)
- Notebooks kan committas, men:
  - inga outputs (plots/dataframes) som gör filerna gigantiska
  - inga hemligheter/PII i notebooks

---

## 3) Data policy

### ALLOWED i Git
- anonymiserade samples (`data/samples/`)
- schema/migrations (`sql/schema/`)
- views (`sql/views/`)
- dokumentation/diagram (`docs/`)

### FORBIDDEN i Git
- Forms exports (rå)
- API dumps / rå JSON (om inte explicit anonymiserad sample)
- Excel med namn/mejl/telefon
- `.env` / tokens
- `.pbix` (Power BI) om de blir stora/binära
- DB-volymer / lokala DB-filer

---

## 4) Namnstandard (så allt blir sökbart)

### Filnamn
- `snake_case`
- inga mellanslag
- gärna datum i ISO: `YYYY-MM-DD`

Exempel:
- `af_ads_2026-01-12.jsonl`
- `survey_responses_2026-01-12_clean.csv`
- `title_aliases_v1.csv`
- `cleaning_pipeline_json.py`

### SQL
- tabeller: `snake_case`
- primärnycklar(PKs) tydligt (tex `job_role_id`)
- constraints namnges (om vi orkar): `chk_share_range`, `uq_title_alias`

---

## 5) Hur vi lägger till en ny datakälla (recept)

1) Bestäm "source name" (t.ex. `af_api`, `forms`, `interviews`)
2) Raw hamnar i `data/raw/<source>/...` (lokalt, ignoreras)
3) Skapa en transform som producerar en clean fil (eller skriver direkt till staging-tabell)
4) Validera (minst: tomma fält, datatyper, uppenbara outliers)
5) Load till DB med idempotens (UPSERT på stabil nyckel)
6) Dokumentera i `docs/`:
   - vilken källa
   - vilka fält
   - hur man kör

---

## 6) README (minimikrav)

`README.md` ska ha:
- vad projektet gör (2–5 rader)
- "Start here" (länkar till docs/biblarna)
- hur man kör (kort, utan hemligheter)
- var data ligger (länk/namn på delad plats, ej inloggning)

---

### 7) Extra
- Se teamlist.md
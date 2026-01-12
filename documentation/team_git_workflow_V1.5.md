### Dokumentförslag: Team Git Workflow & Standards (v1.1)

---

# Git Workflow & Standards för oss

Målet: jobba smidigt ihop, undvika konfliktkaos och ha en historik som är lätt att förstå (och ser proffsig ut).

**Språkpolicy**
- **Commit messages: ENGLISH**
- **Code & comments: ENGLISH**
- Diskussion i chatten kan vara svenska — men repo-historiken ska vara konsekvent.

---

## 0) Main branch policy (viktigast av allt)

**`main` är skyddad**
- Inga direkta pushes till `main`
- Allt går via PR (Pull Request)
- Minst **1 reviewer**  innan merge (om möjligt)
- "Checks" (tester/lint) ska vara gröna innan merge (när vi har det)

**Merge-strategi**
- Rekommenderat: **Squash merge**
  - 1 PR = 1 commit på `main`
  - Ren historik, lätt att backa, lätt att läsa

---

## 1) Commit Messages (Conventional Commits)

Vi skriver tydliga meddelanden så att vi vet **vad** som hände, inte bara att något hände.

**Format:**
`type(scope): short description`

- `type` = vad för typ av ändring
- `scope` = (valfritt men rekommenderat) var ändringen hör hemma, t.ex. `db`, `api`, `docs`, `ui`
- beskrivningen ska vara kort och börja med verb (imperativ), t.ex. "add", "fix", "update"

**Vanliga typer**
- **`feat:`** ny funktionalitet  
  Ex: `feat(db): add order_line table`
- **`fix:`** buggfix  
  Ex: `fix(api): handle empty payload`
- **`docs:`** bara dokumentation/diagram/README  
  Ex: `docs(readme): add setup instructions`
- **`chore:`** städning/config (ingen ändring i runtime-beteende)  
  Ex: `chore: reorganize folders`
- **`refactor:`** omstrukturering (samma beteende, bättre kod)  
  Ex: `refactor(core): simplify parsing logic`
- **`test:`** bara tester  
  Ex: `test(db): add constraints tests`
- **`perf:`** prestandaoptimering  
  Ex: `perf(query): add index for search`
- **`ci:`** CI/automation  
  Ex: `ci: add github actions workflow`
- **`build:`** dependencies/buildsystem  
  Ex: `build: bump dependencies`
- **`style:`** formatering (inga logikändringar)  
  Ex: `style: run formatter`

**Regel:** en commit = en logisk idé (atomisk ändring).

---

## 2) Branch naming

Skapa alltid branch från uppdaterad `main`.

**Format:**
- `feat/<short-desc>`
- `fix/<short-desc>`
- `docs/<short-desc>`
- `chore/<short-desc>`
- `refactor/<short-desc>`

Exempel:
- `feat/create-db-schema`
- `fix/null-handling`
- `docs/add-erd`
- `chore/setup-hooks`

---

## 3) Arbetsprocess (The Workflow)

### Steg 1: Starta passet (hämta senaste)
```bash
git checkout main
git pull origin main
````

### Steg 2: Skapa en egen branch

```bash
git checkout -b feat/<short-desc>
# Ex: git checkout -b feat/create-db-schema
```

### Steg 3: Jobba & spara (commit)

**Undvik `git add .` som standard.** Det är lätt att råka committa fel filer.

Rekommenderat:

```bash
git add -p
git commit -m "feat(db): create initial schema"
```

Om du måste stage:a allt (t.ex. ny liten feature i början), gör det medvetet:

```bash
git add .
git commit -m "docs(readme): update instructions"
```

### Steg 4: Push till remote

```bash
git push -u origin feat/<short-desc>
```

### Steg 5: Håll din branch i fas med `main` (innan PR)

För att undvika "merge-commit spaghetti":

```bash
git checkout main
git pull origin main

git checkout feat/<short-desc>
git rebase main
```

Om det blir konflikter: lös dem, sen:

```bash
git add -p
git rebase --continue
```

### Steg 6: Pull Request (PR)

1. Skapa PR från din branch -> `main`
2. Skriv en kort sammanfattning
3. Be minst 1 person i teamet review:a
4. Merge via **Squash merge**
5. Ta bort branchen efter merge (städ)

---

## 4) PR-mall (för snabb review)

Kopiera in i PR-beskrivningen:

**What changed**

* [ ] Bullet 1
* [ ] Bullet 2

**How to test**

* [ ] Steps / commands

**Notes / Risks**

* [ ] Anything reviewers should know

**Screenshots / Diagrams (if relevant)**

* [ ] Attach / link

---

## 5) Stora "NEJ" (filer vi inte committar)

**Secrets**

* `.env` (ALDRIG)
* API-nycklar, tokens, lösenord

**Gör istället**

* committa `.env.example` (utan hemligheter) som visar vilka variabler som behövs

**Stora/automatiskt genererade filer (om relevant för projektet)**

* DB-filer (`*.db`, `*.sqlite`, `*.duckdb`)
* Docker-volymer (`pgdata/`, `postgres-data/`)
* Loggar (`*.log`)
* Build-artefakter/cache (`__pycache__/`, `.pytest_cache/`, osv)

---

## 6) Gyllene regler (team-versionen)

1. **Jobba aldrig direkt på `main`.**
2. **Commit ofta, men commit smart:** små, atomiska commits.
3. **Pull/rebase innan PR** så du inte drar in konfliktkaos.
4. **PR är en konversation:** kort sammanfattning + hur man testar.
5. **Panik är förbjudet:** konflikter händer. Läs felmeddelandet, lös steg för steg, fråga i chatten.

---

## 7) Snabb konflikt-guide (när det brinner)

* Se vad som är konflikt:

  ```bash
  git status
  ```
* Öppna filerna med konfliktmarkeringar (`<<<<<<`, `======`, `>>>>>>`)
* Välj rätt kod / kombinera
* Stage:a och fortsätt:

  ```bash
  git add -p
  git rebase --continue
  ```

Om du råkar fastna:

* Avbryt rebase och börja om:

  ```bash
  git rebase --abort
  ```

---

**Slut. Hellre att vi följer 80% konsekvent än att vi skriver en bibel som ingen orkar läsa.**
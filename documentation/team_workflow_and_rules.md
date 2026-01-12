# Team Workflow & Rules (Git Bible) — v1.0

Syfte: Jobba effektivt i team utan konfliktkaos, utan mystery commits och utan att råka pusha känslig data.
Målet är att vår `main` alltid är stabil och att historiken går att läsa som en loggbok.

**Princip:** Hellre att vi följer 80% konsekvent än att vi skriver 50 sidor och ingen orkar.

---

## 0) Vårt löfte till varandra (Non negotiables)

### Main är helig!
- **Inga direkta pushes till `main`.**
- Allt in via **Pull Request (PR)**.
- **Minst 1 reviewer** innan merge (när möjligt).
- Merge sker via **Squash merge** (1 PR = 1 commit på `main`).

**Varför:** Main ska alltid vara 'demo ready'. Squash gör historiken ren och felsökning enklare.

### Inga hemligheter i Git. Aldrig!
- `.env`, tokens, API-nycklar, lösenord --> **ALDRIG** i repo.
- Vi committar `.env.example` (utan hemligheter) om vi behöver visa vilka variabler som krävs.

**Varför:** Ett repo är en kopieringsmaskin. Det som hamnar där sprids.

### Ingen PII i Git (GDPR/etik) (PII under GDPR = Personally Identifiable Information)
- Inga respondentnamn, personmail, telefonnummer eller raw form exporter med persondata i Git.
- PII ska ligga i avsedda delade ytor (t.ex SharePoint/OneDrive) och behandlas enligt projektets etik/GDPR principer.

**Varför:** Integritet + riskminimering. Vi ska kunna dela repot öppet utan hjärtattack.

---

## 1) Språkpolicy (för konsekvens)
- **Commit messages: ENGLISH**
- **Kod + kommentarer: ENGLISH**
- Snack i disc etc är skitsamma.

**Varför:** Repo-historik ska vara konsekvent och **professionellt läsbar**

---

## 2) Commit standard (Conventional Commits)

### Format
`type(scope): short description`

Exempel:
- `feat(db): add job_role table`
- `fix(api): handle empty payload`
- `docs(erd): update LDM`
- `chore: update gitignore`

### Vanliga types
- `feat` ny funktion
- `fix` buggfix
- `docs` dokument/diagram/README
- `chore` städ, config, tooling
- `refactor` omstrukturering utan beteendeförändring
- `test` tester
- `perf` prestanda
- `ci` github actions/automation

### Atomiska commits
**En commit = en logisk idé.**
- Blanda inte 'refactor' + 'feat' + 'docs' i samma commit om du kan undvika det.
- Hellre 2 små commits än 1 gigantisk dump.

**Varför:** Review går snabbare och rollback blir möjlig.

---

## 3) Branch-namn

Skapa alltid branch från uppdaterad `main`.

Format:
- `feat/<short-desc>`
- `fix/<short-desc>`
- `docs/<short-desc>`
- `chore/<short-desc>`
- `refactor/<short-desc>`

Exempel:
- `feat/ingest-af-api`
- `docs/add-architecture-notes`
- `fix/null-trend-prediction`

**Varför:** Alla ser direkt vad branchen handlar om.


# 4) Arbetsflödet (The Loop) — varje gång du kodar  

## Steg 1: Starta passet (synka)
```
git checkout main
git pull origin main
```

## Steg 2: Skapa branch
```
git checkout -b feat/<short-desc>
```

## Steg 3: Jobba -> kontrollera -> stage -> commit
**Kolla ALLTID detta:**
```
git status  
git diff  
```
**Den viktiga regeln är: `git add .` Är **INTE** default!** 

### Istället rekommenderar jag det här:  
```
git add -p
git commit -m "feat(db): created initial schema"
```
### Varför `git add .` är en BIG NONO som rutin:
* du råkar stagea skräp (data, secrets, loggar, något som ej bör committas och pushas )

* du tappar kontroll över vad som faktiskt ingår

* det leder till future chaos när repot växer

### NÄR git add . är OKEJ (Medvetet val):
* Du gör en ren docs ändring, ren liten ändring där du till 100% vet vad som har ändrats

* Du har precis gjort en `git status` och allting ser 'rimligt' ut. T.ex endast en röd fil (Den du jobbat på och ingenting annat som är rött!)


## Steg 4: Push
```
git push -u origin feat/<short desc>
```

## Steg 5: Håll din branch i fas med main (innan PR - Pull request)  
```
git checkout main
git pull origin main

git checkout feat/<short desc>
git rebase main
git push --force-with-lease
```
**Förklaring: Efter git rebase main ändras historiken. Vanlig git push KAN faila. Därför är det säkrare med --force-with-lease vs --force och räddar oss ifrån 'Varför går det inte att pusha för?!'** 


### **OM KONFLIKTER:**  
```
git status
``` 
### lös konflikter i filerna
```
git add -p
git rebase --continue
```

### Om du fastnar:
```
git rebase --abort
```
**Varför rebase?**
* Du undviker 'merge commit kaos' och håller PR ren.

# 5) Pull requests (PR) Så vi arbetar tillsammans

## När du öppnar PR
* PR från din branch till -> `main`
* Beskriv **kort** vad som har ändrats
* Lägg gärna till ett 'how to test' (via kommandon eller steg)

## Review regler.
* Minst en i gruppen reviewar när och om det är möjligt.

* Den som review'ar ska vara snäll och inte elak eller nedlåtande men var ärliga mot varandra och ställ dig frågan: 
  - 'Förstår jag ändringen?'
  - 'Är ändringen testbar? Går det att testa?'(enklare att vi hittar buggar som kanske inte hade hittats utan review)
  - Finns det någon risk? Vad säger GDPR(PII). (Ingen av oss vill ha problem med big daddy EU...)

## Merge regler:
* Merge via **Squash merge**
* Radera branch efter merge(städning)

**Varför?** 
- En pull request(PR) == 1 commit på `main`.  
det blir superlätt att läsa och backa om så behövs.

# 6) PR mall (Pull request mall)

**What changed?**  
- [ ] ...
 

**How to test**
- [ ] Commands / steps

**Notes / risks**
- [ ] Anything reviewers should know

**Screenshots / diagrams (if relevant)**
- [ ] attach file / link

# 7) Alla stora **NEJ**. Filer som vi **INTE** committar.
  
**Secrets** 
* `.env`

* tokens, keys, passwords  

**Stora eller auto genererade filer** 
* DB filer: `*.db`, `*.sqlite`, `*.duckdb`, etc.
* Docker volumer: `pgdata/`, `postgres-data/`
* Loggar: `*.log`
* Cache/build: `__pycache__/`, `.pytest_cache/`, etc

**Data med RISK!(PII / raw exports)** 

* Forms/formulär exports med persondata.
* 'raw' API dumps om de kan innehålla NÅGOT känsligt.
* Intervjudokument med namn/något annat som kan identifiera

**Varför?:** Git är inte en datalake/warehouse. Vi använder git för kod, docs + små testdata / sample filer.

# 8) Snabb konflikt guide (När du har panik och tror att allting går åt helvete)

### Steg 1: Kolla läget.
```
git status
```
### Steg 2: Öppna konfliktfilerna(dom som bråkar med dig) och leta
* <<<<<<<<<<
* ==========
* >>>>>>>>>>

### Steg 3: Lös, stage'a, fortsätt!
```
git add -p
git rebase --continue
```
### Steg 4: Om du behöver backa ur 
```
git rebase --abort
```

# 9) Regler för att vi ska må bra och inte ta allt för mycket stryk psykiskt med git/github (LOL :D)  
* Detta är ett **GRUPParbete** och vi jobbar som ett **TEAM**. Ingen kan allting men alla kan något och bidra till det stora hela.

* Fråga tidigt OM och NÄR du är osäker. Git konflikter blir inte bättre av att ignorera dom, tvärtom.

* Små pull request'ar(PR) slår stora PR's. En PR ska helst gå att reviewa på en 25-30 minuter (ish).

* PR är en konversation, inte en domstol.

# 10) Mini checklist innan du öppnar PR
- [ ] Jag är rebased mot senaste `main`
- [ ] Jag vet exakt vad jag har staged (inte 'bara allt')
- [ ] Inga secrets/PII/raw exports i diffen (<---VIKTIGT)
- [ ] PR beskrivningen säger HUR man testar (om relevant ofc)
- [ ] Jag kan förklara ändringen på 30-60 sekunder
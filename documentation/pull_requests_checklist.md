# Så här funkar checklistan kring steg 10 i team_workflow_and_rules.md.

**Så här funkar det**  
I markdown skriver man 
- [ ] = obockad ruta
- [x] = ibockad ruta

# Exempel:

**What changed**
- [ ] Added initial schema for job roles
- [ ] Updated validation rules
-------------------------------------------------

## När du fyller i en PR på Github / Gitlab kan du antingen:
* Bocka i dom i webläsaren (klicka i rutan) eller
* ändra texten själv till `- [x]` när punkten är klar.

## Varför ska vi ha dom i PR mallen?  
Jo, det tvingar oss att vara tydliga.
* What changed: Vad gjorde jag egentligen?
* How to test: Hur ska någon annan verifiera det snabbt?
* Notes/risks: Finns det något som kan överraska?
* Screenshots/diagrams: Om det är relevant, typ LDM, PDM eller andra diagram.

## Hur du använder det i praktiken?  
När du öppnar en PR, klistra då in:
```
**What changed**
- [ ] Added `job_role` and `title_alias` tables
- [ ] Created initial mapping script

**How to test**
- [ ] Run `python -m src.ingest_af --dry-run`
- [ ] Verify `sql/schema.sql` applies cleanly

**Notes / Risks**
- [ ] No PII included. Raw exports stored outside repo.

```
Sen bockar du i när du faktiskt har gjort sakerna, eller lämnar dom som 'to do' för PR'n.

Det är som en liten checklista inbyggt i PR(pull requesten) så att en review blir 100x enklare och ingen av oss missar och tänker "vänta nu, hur testar jag det här?"
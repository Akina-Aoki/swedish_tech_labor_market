# Glossary & How-To (Team Git) — v0.1

Syfte: Snabba svar på vanliga frågor. Denna fil kompletterar `team_workflow_and_rules.md`.

---

## Glossary (ordlista)

**Branch**  
En separat 'linje' av arbete. Du jobbar i branch, inte direkt i `main`.

**PR (Pull Request)**  
En begäran att få in din branch i `main`. Här sker review.

**Review**  
När en annan person läser din PR och ger feedback.

**Squash merge**  
När PRen blir 1 commit på `main` (ren historik).

**Rebase**  
Flyttar din branch 'ovanpå' senaste `main` för att undvika merge-spaghetti.

**Staging**  
Det du valt att inkludera i nästa commit (`git add ...`).

---

## How-To

### Hur skapar jag en ny feature-branch?
```
git checkout main
git pull origin main
git checkout -b feat/<short-desc>
```

### Hur ser jag vad jag ändrat?

```
git status
git diff
```

### Hur stagear jag 'bara det jag menar'?

```
git add -p
```

**Tips:** tryck `y` för att stagea en del, `n` för att hoppa över.

### Hur gör jag en commit?

```
git commit -m "feat(scope): short description"
```

### Hur pushar jag första gången?

```
git push -u origin feat/<short-desc>
```

### Hur uppdaterar jag min branch med senaste main (rebase)?

```
git checkout main
git pull origin main

git checkout feat/<short-desc>
git rebase main
git push --force-with-lease
```

### Jag fick konflikter, vad gör jag?

1. Se vilka filer som är konfliktade:

```
git status
```

2. Lös konflikter i filerna (leta efter `<<<<<<`, `======`, `>>>>>>`)
3. Stagea och fortsätt:

```
git add -p
git rebase --continue
```

Om du måste avbryta:

```
git rebase --abort
```

### Jag råkade stagea för mycket

Avstagea allt:

```
git reset
```

Avstagea en fil:

```
git restore --staged path/to/file
```

### Jag committade något dumt (lokalt, inte pushat)

```
git reset --soft HEAD~1
```

Då behåller du ändringarna men tar bort committen.

---

## “Red flags” (vanliga misstag)

* `git add .` utan att ha kollat `git status` och `git diff`
* pusha till `main`
* committa `.env` eller exports/raw data
* jättestora PRar (svåra att reviewa)

# Setup Guide: Docker & PgAdmin4

Här är stegen för att få igång databasen och se datan. Vi håller det enkelt

## 1. Spinna upp containern (Databasen)

Vi använder `docker-compose.yml` som redan innehåller all konfiguration (användare, lösenord, portar)

**Gör så här:**
1.  Öppna terminalen i projektmappen.
2.  Kör: `docker-compose up -d`
    - (Flaggan `-d` betyder detached, så den körs i bakgrunden)
3.  Vänta 10 sek så databasen hinner starta och köra vårt `init.sql` skript automatiskt.

**Ladda datan:**
1.  Se till att du har paketen installerade: `uv pip install "psycopg[binary]" tqdm`
2.  Kör laddnings-scriptet: `python src/load/load_postgres.py`
3.  Ser du en progress bar som tuggar på? Jippie!

**Felsökning:**
- Om det krånglar: Kör `docker-compose down` (tar bort allt)
- Kör sen `docker-compose up -d` igen.
- Kör python-scriptet igen.


## 2. Connecta med PgAdmin4 (Se data i GUI)

1.  Öppna **pgAdmin4**.
2.  Högerklicka på **Servers** (i vänstermenyn) --> **Register** --> **Server...**
3.  Fliken **General**:
    - **Name:** `Skillgap Docker` (eller vad du vill)
4.  Fliken **Connection VIKTIGT!:** 
    * **Host name/address:** `localhost`
    * **Port:** `5433` *(**Inte 5432!** Vi kör på 5433 för att inte krocka med din lokala installation av postgres)*
    * **Maintenance database:** `skillgap`
    * **Username:** `admin`
    * **Password:** `password123`
    * *Spara gärna lösenordet så slipper du skriva det igen*
5.  Klicka på **Save**. 

**Verifiera att det funkar:**
1.  Navigera i trädet: `Databases` --> `skillgap` --> `Schemas` --> `public` --> `Tables`.
2.  Du ska se två tabeller, `ads` och `ad_skills`.
3.  Högerklicka på `ads` --> **View/Edit Data** --> **First 100 Rows**

Ser du jobbannonser? **Grymt allting står rätt till och har fungerar. Query away!**
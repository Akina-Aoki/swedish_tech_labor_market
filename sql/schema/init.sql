-- Sql schema skript.


-- 1. Tabel för våra annonser(Fakta/Objekt)
CREATE TABLE IF NOT EXISTS ads (
    id TEXT PRIMARY KEY,        -- Arbetsförmedlingens annons ID
    title TEXT,
    url TEXT,
    description TEXT,           -- Hela texten (Användbart för sökning sen)
    source_year INT,            -- T.ex 2021, 2023, eller 2025
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

-- 2. Tabellen för skills(de skills som finns i keyword_taxonomy.json) (Dimension/egenskap)
-- en 'junction table' som gör att vi kan filtrera via Power BI

CREATE TABLE IF NOT EXISTS ad_skills (
    id SERIAL PRIMARY KEY,
    ad_id TEXT REFERENCES ads(id) ON DELETE CASCADE,    -- Tar även bort skills om annonsen tas bort
    skill TEXT,                                         -- T.ex 'Python', 'SQL', 'Docker' (även kallad hit i clean_ads_keywords)
    skill_type TEXT,                                    -- 'tag' (från kategori) eller 'keyword' (specifika ord. Även kallad hits i pipeline)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index för att våra sökningar ska gå fort
CREATE INDEX IF NOT EXISTS indx_ads_year ON ads(source_year);
CREATE INDEX IF NOT EXISTS indx_skills_skill ON ad_skills(skill);
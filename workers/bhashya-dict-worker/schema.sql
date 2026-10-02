-- Cloudflare D1 Schema for Sankara Bhasya Dictionary & Mula Analysis

-- 1. Bhasya Dictionary (95,585 terms across commentary body)
DROP TABLE IF EXISTS bhasya_dictionary;
CREATE TABLE bhasya_dictionary (
  id INTEGER PRIMARY KEY,
  surface TEXT NOT NULL,
  padaccheda TEXT,
  grammar TEXT,
  meaning_en TEXT,
  confidence TEXT,
  meaning_bn TEXT
);

CREATE INDEX idx_bhasya_surface ON bhasya_dictionary(surface);
CREATE INDEX idx_bhasya_padaccheda ON bhasya_dictionary(padaccheda);
CREATE INDEX idx_bhasya_meaning_en ON bhasya_dictionary(meaning_en);

-- 2. Mula Analysis (36,881 terms across all 3,452 original verses/sutras)
DROP TABLE IF EXISTS mula_analysis;
CREATE TABLE mula_analysis (
  id INTEGER PRIMARY KEY,
  work_slug TEXT NOT NULL,
  unit_key TEXT NOT NULL,
  surface TEXT NOT NULL,
  padaccheda TEXT,
  grammar TEXT,
  meaning_en TEXT,
  confidence TEXT,
  meaning_bn TEXT
);

CREATE INDEX idx_mula_surface ON mula_analysis(surface);
CREATE INDEX idx_mula_work_ref ON mula_analysis(work_slug, unit_key);
CREATE INDEX idx_mula_padaccheda ON mula_analysis(padaccheda);
CREATE INDEX idx_mula_meaning_en ON mula_analysis(meaning_en);

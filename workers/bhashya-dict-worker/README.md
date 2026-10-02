# Prasthānatrayī Complete Lexicon Cloudflare Worker (Mūla & Śāṅkara Bhāṣya)

High-performance Edge API serving **132,466 Sanskrit terms** backed by Cloudflare D1:
- **36,881 terms from Mūla Verses & Sūtras** (`mula_analysis` across Upaniṣads, Brahma Sūtras, and Bhagavad Gītā).
- **95,585 terms from Śāṅkara Bhāṣya** (`bhasya_dictionary`).

---

## 🚀 Quick Setup & Deployment

### Step 1: Create the Cloudflare D1 Database
```bash
npx wrangler d1 create sankara-bhasya-db
```
Copy the returned `database_id` into `wrangler.toml`:
```toml
[[d1_databases]]
binding = "DB"
database_name = "sankara-bhasya-db"
database_id = "<PASTE_DATABASE_ID_HERE>"
```

### Step 2: Initialize Schema & Seed Data
```bash
# 1. Create tables and indexes for both Mula and Bhasya
npx wrangler d1 execute sankara-bhasya-db --file=schema.sql --remote

# 2. Seed all 132,466 entries (Bhasya + Mula)
npx wrangler d1 execute sankara-bhasya-db --file=seed_d1.sql --remote
```

### Step 3: Deploy Worker
```bash
npx wrangler deploy
```

Your worker will be live at:
`https://bhashya-dict-worker.<your-subdomain>.workers.dev`

---

## 📡 API Endpoints

### 1. Mūla Verse Word-by-Word
`GET /api/dict/mula?work=Gita&ref=2.47`
`GET /api/dict/mula?work=BS&ref=1.1.1`
Returns sequential word-by-word grammatical tokens for that specific verse/sūtra directly from D1.

### 2. Universal Word Lookup (Mūla & Bhāṣya)
`GET /api/dict/word?term=कर्मण्येवाधिकारस्ते&scope=all`
- `scope`: `all` | `mula` | `bhasya`
Returns grammatical analysis, root/compound breakdown, English meaning, and Bengali translation.

### 3. Full-Text Search
`GET /api/dict/search?q=ब्रह्म&scope=all&category=noun&limit=50`
- `q`: search query in Devanāgarī, Roman transliteration, or English definition
- `scope`: `all` | `mula` | `bhasya`
- `category`: `all` | `noun` | `verb` | `avyaya`

### 4. Autocomplete Suggestions
`GET /api/dict/suggest?prefix=अध्य`
```json
["अध्यास", "अध्यासः", "अध्यासात्", "अध्यासेन"]
```

---

## 🔗 Connecting to VedāntVāṇī
In VedāntVāṇī, navigate to `/bhashya-dictionary` and enter your deployed Worker URL in the Settings modal, or configure `PUBLIC_CF_WORKER_URL` in `.env`.
VedāntVāṇī also includes local static shards in `/data/dict/` as an automatic zero-config offline fallback.

import sqlite3
import os

DB_PATH = '/tmp/sankara_bhasya.sqlite'
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_SQL = os.path.join(OUT_DIR, '../seed_d1.sql')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

def escape_sql(val):
    if val is None:
        return 'NULL'
    return "'" + str(val).replace("'", "''") + "'"

with open(OUT_SQL, 'w', encoding='utf-8') as f:
    f.write("-- Complete Seed Data for Cloudflare D1 (Bhasya Dictionary + Mula Analysis)\n\n")

    # 1. Bhasya Dictionary
    print("Exporting bhasya_dictionary (95,585 rows)...")
    rows = c.execute('SELECT id, surface, padaccheda, grammar, meaning_en, confidence, meaning_bn FROM bhasya_dictionary ORDER BY id').fetchall()
    BATCH_SIZE = 100
    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        val_strs = []
        for r in batch:
            row_vals = [
                str(r[0]),
                escape_sql(r[1]),
                escape_sql(r[2]),
                escape_sql(r[3]),
                escape_sql(r[4]),
                escape_sql(r[5]),
                escape_sql(r[6])
            ]
            val_strs.append(f"({', '.join(row_vals)})")
        f.write(f"INSERT OR REPLACE INTO bhasya_dictionary (id, surface, padaccheda, grammar, meaning_en, confidence, meaning_bn) VALUES\n  {',\n  '.join(val_strs)};\n")

    # 2. Mula Analysis
    print("Exporting mula_analysis (36,881 rows)...")
    m_rows = c.execute('SELECT id, work_slug, unit_key, surface, padaccheda, grammar, meaning_en, confidence, meaning_bn FROM mula_analysis ORDER BY id').fetchall()
    for i in range(0, len(m_rows), BATCH_SIZE):
        batch = m_rows[i:i + BATCH_SIZE]
        val_strs = []
        for r in batch:
            row_vals = [
                str(r[0]),
                escape_sql(r[1]),
                escape_sql(r[2]),
                escape_sql(r[3]),
                escape_sql(r[4]),
                escape_sql(r[5]),
                escape_sql(r[6]),
                escape_sql(r[7]),
                escape_sql(r[8])
            ]
            val_strs.append(f"({', '.join(row_vals)})")
        f.write(f"INSERT OR REPLACE INTO mula_analysis (id, work_slug, unit_key, surface, padaccheda, grammar, meaning_en, confidence, meaning_bn) VALUES\n  {',\n  '.join(val_strs)};\n")

print(f"Generated {OUT_SQL} successfully! Size: {os.path.getsize(OUT_SQL) / (1024*1024):.2f} MB")

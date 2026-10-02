#!/usr/bin/env python3
"""
Enhanced Migration Script to ingest enriched metadata into all 16 Prakarana Granthas,
Vivekachudamani, and Yoga Sutras.
"""

import os
import json
import re

SOURCE_DIR = "/home/anurag/Projects/Mega Datahub/shlokam/advaita-prakarana"
PROJECT_DIR = "/home/anurag/Projects/vedantvani"

PRACTICE_MAPPING = {
    "Atmabodha.json": {
        "id": "prakarana-atmabodha",
        "name": "Atmabodha",
        "commentator": "Swami Paramarthananda",
        "commentary_lang": "English",
        "commentary_school": "Advaita Vedanta"
    },
    "aparokshanubhuti.json": {
        "id": "prakarana-aparokshanubhuti",
        "name": "Aparokshanubhuti",
        "commentator": "Traditional Commentary",
        "commentary_lang": "English",
        "commentary_school": "Advaita Vedanta"
    },
    "brahma-jnanavali-mala.json": {
        "id": "prakarana-brahma-jnanavali-mala",
        "name": "Brahma Jnanavali Mala",
        "commentator": "Traditional Commentary",
        "commentary_lang": "English",
        "commentary_school": "Advaita Vedanta"
    },
    "dasa-shloki.json": {
        "id": "prakarana-dasa-shloki",
        "name": "Dasa Shloki",
        "commentator": "Pavan K. Varma",
        "commentary_lang": "English",
        "commentary_school": "Advaita Vedanta"
    },
    "hastamalaka-stotram.json": {
        "id": "prakarana-hastamalaka-stotram",
        "name": "Hastamalaka Stotram",
        "commentator": "Adi Shankaracharya Bhashya Notes",
        "commentary_lang": "English",
        "commentary_school": "Advaita Vedanta"
    },
    "hastamalakiya-bhashya.json": {
        "id": "prakarana-hastamalakiya-bhashya",
        "name": "Hastamalakiya Bhashya",
        "commentator": "आदि शङ्कराचार्य (शङ्करभाष्यम्)",
        "commentary_lang": "Sanskrit",
        "commentary_school": "अद्वैत वेदान्त"
    },
    "kaupina-panchakam.json": {
        "id": "prakarana-kaupina-panchakam",
        "name": "Kaupina Panchakam",
        "commentator": "Traditional Commentary",
        "commentary_lang": "English",
        "commentary_school": "Advaita Vedanta"
    },
    "manisha-panchakam.json": {
        "id": "prakarana-manisha-panchakam",
        "name": "Manisha Panchakam",
        "commentator": "Traditional Commentary",
        "commentary_lang": "English",
        "commentary_school": "Advaita Vedanta"
    },
    "nyayarakshamani.json": {
        "id": "prakarana-nyayarakshamani",
        "name": "Nyayarakshamani",
        "commentator": "श्री अप्पय्य दीक्षित (न्यायरक्षामणिः)",
        "commentary_lang": "Sanskrit",
        "commentary_school": "अद्वैत वेदान्त"
    },
    "saddarshanam.json": {
        "id": "prakarana-saddarshanam",
        "name": "Saddarshanam",
        "commentator": "Traditional Commentary",
        "commentary_lang": "English",
        "commentary_school": "Advaita Vedanta"
    },
    "sadhana-panchakam.json": {
        "id": "prakarana-sadhana-panchakam",
        "name": "Sadhana Panchakam",
        "commentator": "Sri Bharati Tirtha Mahaswami",
        "commentary_lang": "English",
        "commentary_school": "Advaita Vedanta"
    },
    "shatashloki.json": {
        "id": "prakarana-shatashloki",
        "name": "Shatashloki",
        "commentator": "आदि शङ्कराचार्य भाष्यम्",
        "commentary_lang": "Sanskrit",
        "commentary_school": "अद्वैत वेदान्त"
    },
    "tattvabodha.json": {
        "id": "prakarana-tattvabodha",
        "name": "Tattvabodha",
        "commentator": "Traditional Commentary",
        "commentary_lang": "English",
        "commentary_school": "Advaita Vedanta"
    },
    "upadesa-saaram.json": {
        "id": "prakarana-upadesa-saaram",
        "name": "Upadesa Saaram",
        "commentator": "Traditional Commentary",
        "commentary_lang": "English",
        "commentary_school": "Advaita Vedanta"
    },
    "vakya-vritti.json": {
        "id": "prakarana-vakya-vritti",
        "name": "Vakya Vritti",
        "commentator": "Traditional Commentary",
        "commentary_lang": "English",
        "commentary_school": "Advaita Vedanta"
    },
}

def parse_word_meanings(wm_text):
    if not wm_text or not isinstance(wm_text, str):
        return []
    entries = re.split(r";\s*|\n(?=[\u0900-\u097F])", wm_text.strip())
    results = []
    for e in entries:
        e = e.strip()
        if not e:
            continue
        m = re.match(r"^([\u0900-\u097F\s\w\.\-]+?)(?:\s*\(([^)]+)\))?\s*[\u2013\-\:\–]\s*(.+)$", e, re.DOTALL)
        if m:
            skt = m.group(1).strip()
            tr = m.group(2) or ""
            mean = m.group(3).strip()
            results.append({
                "word_sanskrit": skt,
                "word_english": mean,
                "transliteration": tr,
                "grammar_role": tr
            })
    return results

def format_padacheda(padacheda_list):
    if not padacheda_list or not isinstance(padacheda_list, list):
        return []
    results = []
    for p in padacheda_list:
        if not isinstance(p, dict):
            continue
        skt = p.get("sanskrit", "").strip()
        tr = p.get("transliteration", "").strip()
        en = p.get("meaning_english", "").strip()
        hi = p.get("meaning_hindi", "").strip()
        
        meaning_str = en
        if hi:
            meaning_str = f"{en}<div style='color: var(--accent-gold); font-size: 0.85em; margin-top: 3px;'>{hi}</div>" if en else hi
        
        results.append({
            "word_sanskrit": skt,
            "word_english": meaning_str,
            "transliteration": tr,
            "grammar_role": tr
        })
    return results

def extract_metadata(v_data, sid, sname, v_num, ch_num=None, sec_title=None):
    meta = {
        "scripture_name": sname,
        "scripture_slug": sid,
        "verse_number": v_num,
        "chapter_number": ch_num
    }
    if sec_title:
        meta["section_title"] = sec_title

    summary_line = v_data.get("summary_line", "").strip()
    if summary_line:
        meta["summary_line"] = summary_line

    exhaustive_schema = v_data.get("exhaustive_schema")
    meta_tags = v_data.get("meta_tags")
    if not exhaustive_schema and isinstance(meta_tags, dict):
        exhaustive_schema = meta_tags.get("exhaustive_schema")

    if exhaustive_schema and isinstance(exhaustive_schema, dict):
        c1 = exhaustive_schema.get("1. Core Philosophical & Doctrinal Mapping", {})
        if isinstance(c1, dict):
            pd = c1.get("primary_doctrine")
            if isinstance(pd, dict):
                meta["primary_doctrine"] = pd.get("value") or pd.get("primary_doctrine")
            elif isinstance(pd, str):
                meta["primary_doctrine"] = pd

            mc = c1.get("metaphysical_category")
            if isinstance(mc, dict):
                meta["metaphysical_category"] = mc.get("value") or mc.get("metaphysical_category")
            elif isinstance(mc, str):
                meta["metaphysical_category"] = mc

            prk = c1.get("prakriya_mapped")
            if isinstance(prk, dict):
                meta["prakriya_mapped"] = prk.get("value") or prk.get("prakriya_mapped")
            elif isinstance(prk, str):
                meta["prakriya_mapped"] = prk

        c2 = exhaustive_schema.get("2. Textual Mechanics & Cross-Referencing", {})
        if isinstance(c2, dict):
            echo = c2.get("sruti_smriti_echo")
            if echo and str(echo).lower() not in ["none", ""]:
                meta["sruti_smriti_echo"] = str(echo)

            mhk = c2.get("mahavakya_correlative")
            if mhk and str(mhk).lower() not in ["none", ""]:
                meta["mahavakya_correlative"] = str(mhk)

            kws = c2.get("keywords_sanskrit")
            if kws and isinstance(kws, list) and len(kws) > 0:
                meta["keywords_sanskrit"] = kws

        c3 = exhaustive_schema.get("3. Pedagogical & Spiritual Journey Framework", {})
        if isinstance(c3, dict):
            stage = c3.get("sadhana_stage")
            if stage and str(stage).lower() not in ["none", ""]:
                meta["sadhana_stage"] = str(stage)

            obs = c3.get("target_obstacle")
            if isinstance(obs, dict):
                meta["target_obstacle"] = obs.get("value") or obs.get("target_obstacle")
            elif isinstance(obs, str) and str(obs).lower() not in ["none", ""]:
                meta["target_obstacle"] = str(obs)

            ctx = c3.get("dialogue_context")
            if ctx and str(ctx).lower() not in ["none", ""]:
                meta["dialogue_context"] = str(ctx).replace("_", " ")

    return meta

def build_faqs(meta, section_title=None):
    faqs = []
    sec = section_title or meta.get("section_title")
    if sec:
        faqs.append({
            "question": "Thematic Context",
            "answer": f"This verse forms part of the section: \"{sec}\"."
        })

    doctrine = meta.get("primary_doctrine")
    prakriya = meta.get("prakriya_mapped")
    category = meta.get("metaphysical_category")
    if doctrine or prakriya:
        ans_parts = []
        if doctrine: ans_parts.append(f"Primary Doctrine: {doctrine}")
        if category: ans_parts.append(f"Metaphysical Sphere: {category}")
        if prakriya and prakriya != "None": ans_parts.append(f"Teaching Methodology (Prakriyā): {prakriya}")
        faqs.append({
            "question": "Philosophical Framework & Methodology",
            "answer": " • ".join(ans_parts)
        })

    stage = meta.get("sadhana_stage")
    obstacle = meta.get("target_obstacle")
    if stage or obstacle:
        ans_parts = []
        if stage: ans_parts.append(f"Sādhana Stage: {stage}")
        if obstacle: ans_parts.append(f"Target Obstacle Dismantled: {obstacle}")
        faqs.append({
            "question": "Spiritual Journey & Sadhana Progression",
            "answer": " • ".join(ans_parts)
        })

    echo = meta.get("sruti_smriti_echo")
    if echo:
        faqs.append({
            "question": "Scriptural Echoes & Cross-References",
            "answer": echo
        })

    mhk = meta.get("mahavakya_correlative")
    if mhk:
        faqs.append({
            "question": "Mahāvākya Correlation",
            "answer": f"Directly illuminates the Vedāntic Mahāvākya: \"{mhk}\"."
        })

    kws = meta.get("keywords_sanskrit")
    if kws and isinstance(kws, list) and len(kws) > 0:
        faqs.append({
            "question": "Key Sanskrit Concepts",
            "answer": ", ".join(kws)
        })

    ctx = meta.get("dialogue_context")
    if ctx:
        faqs.append({
            "question": "Instructional Context",
            "answer": f"Context: {ctx}"
        })

    return faqs

def migrate_vivekachudamani():
    print("\n==========================================")
    print("Migrating Vivekachudamani with full metadata...")
    print("==========================================")
    
    vc_json_path = os.path.join(SOURCE_DIR, "vivekachudamani.json")
    with open(vc_json_path, "r", encoding="utf-8") as f:
        vc_meta = json.load(f)
    
    sections = vc_meta.get("Sections", [])
    verses_dir = os.path.join(SOURCE_DIR, "vivekachudamani")
    dest_dir = os.path.join(PROJECT_DIR, "data/prakarana-vivekachudamani")
    dest_summary_path = os.path.join(dest_dir, "summary.json")
    
    with open(dest_summary_path, "r", encoding="utf-8") as f:
        summary_data = json.load(f)
        
    all_verses = []
    
    for i in range(1, 581):
        v_path = os.path.join(verses_dir, f"verse_{i}.json")
        with open(v_path, "r", encoding="utf-8") as f:
            v_data = json.load(f)
            
        shloka = v_data.get("shloka", "").strip()
        translit = v_data.get("transliteration", "").strip()
        en_trans = v_data.get("translation_english", "").strip()
        hi_trans = v_data.get("translation_hindi", "").strip()
        padacheda = v_data.get("padacheda", [])
        
        # Section mapping
        sec_title = ""
        for s in sections:
            if s.get("start", 0) <= i <= s.get("end", 0):
                sec_title = s.get("title", "")
                break
                
        meta = extract_metadata(v_data, "prakarana-vivekachudamani", "Vivekachudamani", i, sec_title=sec_title)
        
        translations = []
        if en_trans:
            translations.append({
                "author": "English Translation",
                "author_name": "English Translation",
                "language": "English",
                "text": en_trans
            })
        if hi_trans:
            translations.append({
                "author": "Hindi Translation",
                "author_name": "हिन्दी अनुवाद",
                "language": "Hindi",
                "text": hi_trans
            })
            
        word_by_word = format_padacheda(padacheda)
        
        verse_obj = {
            "id": f"prakarana-vivekachudamani_verse_{i}",
            "verse_number": i,
            "chapter_number": None,
            "sanskrit_shloka": shloka,
            "text": shloka,
            "transliteration": translit,
            "section_title": sec_title,
            "summary_line": meta.get("summary_line", ""),
            "sadhana_stage": meta.get("sadhana_stage", ""),
            "primary_doctrine": meta.get("primary_doctrine", ""),
            "prakriya_mapped": meta.get("prakriya_mapped", ""),
            "target_obstacle": meta.get("target_obstacle", ""),
            "keywords_sanskrit": meta.get("keywords_sanskrit", []),
            "translations": translations,
            "commentaries": [],
            "word_by_word": word_by_word,
            "commentary_faqs": [],
            "metadata": meta
        }
        all_verses.append(verse_obj)
        
    print(f"Loaded and enriched {len(all_verses)} verses for Vivekachudamani.")
    
    verse_idx = 0
    updated_summary = []
    
    for ch_info in summary_data:
        ch_num = ch_info["chapter_number"]
        v_count = ch_info["verses_count"]
        ch_verses = all_verses[verse_idx:verse_idx + v_count]
        
        ch_sec_titles = []
        for cv_idx, cv in enumerate(ch_verses):
            cv["id"] = f"prakarana-vivekachudamani_{ch_num}_{cv_idx + 1}"
            cv["chapter_number"] = ch_num
            cv["metadata"]["chapter_number"] = ch_num
            cv["metadata"]["chapter_name"] = ch_info["name"]
            cv["metadata"]["chapter_slug"] = f"part-{ch_num}"
            if cv["section_title"] and cv["section_title"] not in ch_sec_titles:
                ch_sec_titles.append(cv["section_title"])
                
        ch_file_path = os.path.join(dest_dir, "chapters", f"chapter_{ch_num}.json")
        with open(ch_file_path, "w", encoding="utf-8") as f:
            json.dump(ch_verses, f, ensure_ascii=False, indent=2)
            
        start_v = verse_idx + 1
        end_v = verse_idx + v_count
        sec_summary = ", ".join(ch_sec_titles[:4]) + ("..." if len(ch_sec_titles) > 4 else "")
        
        updated_ch = dict(ch_info)
        updated_ch["summary"] = f"Part {ch_num} (Verses {start_v}-{end_v}) covering sections: {sec_summary}"
        updated_summary.append(updated_ch)
        
        verse_idx += v_count
        
    with open(dest_summary_path, "w", encoding="utf-8") as f:
        json.dump(updated_summary, f, ensure_ascii=False, indent=2)
    print("Vivekachudamani migration with metadata complete!")

def migrate_other_prakaranas():
    print("\n==========================================")
    print("Migrating other 15 Prakarana Granthas with metadata...")
    print("==========================================")
    
    for fname, cfg in PRACTICE_MAPPING.items():
        src_path = os.path.join(SOURCE_DIR, fname)
        sid = cfg["id"]
        sname = cfg["name"]
        commentator = cfg["commentator"]
        comm_lang = cfg["commentary_lang"]
        comm_school = cfg["commentary_school"]
        
        dest_dir = os.path.join(PROJECT_DIR, f"data/{sid}")
        dest_summary_path = os.path.join(dest_dir, "summary.json")
        
        if not os.path.exists(src_path):
            continue
            
        with open(src_path, "r", encoding="utf-8") as f:
            src_data = json.load(f)
            
        with open(dest_summary_path, "r", encoding="utf-8") as f:
            summary_data = json.load(f)
            
        src_verses_dict = src_data.get("Verses", {})
        sections = src_data.get("Sections", [])
        verse_keys = list(src_verses_dict.keys())
        all_verses = []
        
        for idx, k in enumerate(verse_keys):
            v_raw = src_verses_dict[k]
            v_num = idx + 1
            
            shloka = v_raw.get("shloka", "").strip()
            translit = v_raw.get("transliteration", "").strip()
            
            # Section matching
            sec_title = ""
            if sections:
                try:
                    k_int = int(float(k))
                except Exception:
                    k_int = idx
                for s in sections:
                    if s.get("start", 0) <= k_int <= s.get("end", 0):
                        sec_title = s.get("title", "")
                        break
                        
            meta = extract_metadata(v_raw, sid, sname, v_num, sec_title=sec_title)
            
            translations = []
            en_trans = v_raw.get("translation_english", "").strip()
            hi_trans = v_raw.get("translation_hindi", "").strip()
            gen_trans = v_raw.get("translation", "").strip()
            
            if en_trans:
                translations.append({
                    "author": "English Translation",
                    "author_name": "English Translation",
                    "language": "English",
                    "text": en_trans
                })
            elif gen_trans:
                translations.append({
                    "author": "Traditional Translation",
                    "author_name": "Traditional Translation",
                    "language": "English",
                    "text": gen_trans
                })
                
            if hi_trans:
                translations.append({
                    "author": "Hindi Translation",
                    "author_name": "हिन्दी अनुवाद",
                    "language": "Hindi",
                    "text": hi_trans
                })
                
            wm_text = v_raw.get("word_meanings", "")
            if sid == "prakarana-saddarshanam" and wm_text:
                translations.append({
                    "author": "Prose Translation",
                    "author_name": "Prose Translation",
                    "language": "English",
                    "text": wm_text.strip()
                })
                
            commentaries = []
            comm_text = v_raw.get("commentary", "")
            if comm_text and isinstance(comm_text, str) and comm_text.strip():
                is_sanskrit = bool(re.search(r"[\u0900-\u097F]", comm_text[:200]))
                actual_lang = "Sanskrit" if is_sanskrit else comm_lang
                commentaries.append({
                    "author": commentator,
                    "author_name": commentator,
                    "language": actual_lang,
                    "school": comm_school,
                    "text": comm_text.strip()
                })
                
            word_by_word = []
            padacheda = v_raw.get("padacheda")
            if padacheda and isinstance(padacheda, list) and len(padacheda) > 0:
                word_by_word = format_padacheda(padacheda)
            elif wm_text and sid != "prakarana-saddarshanam":
                word_by_word = parse_word_meanings(wm_text)
                if not word_by_word and isinstance(wm_text, str) and wm_text.strip():
                    word_by_word = wm_text.strip()
                    
            verse_obj = {
                "id": f"{sid}_verse_{v_num}",
                "verse_number": v_num,
                "chapter_number": None,
                "sanskrit_shloka": shloka,
                "text": shloka,
                "transliteration": translit,
                "section_title": sec_title,
                "summary_line": meta.get("summary_line", ""),
                "sadhana_stage": meta.get("sadhana_stage", ""),
                "primary_doctrine": meta.get("primary_doctrine", ""),
                "prakriya_mapped": meta.get("prakriya_mapped", ""),
                "target_obstacle": meta.get("target_obstacle", ""),
                "keywords_sanskrit": meta.get("keywords_sanskrit", []),
                "translations": translations,
                "commentaries": commentaries,
                "word_by_word": word_by_word,
                "commentary_faqs": [],
                "metadata": meta
            }
            all_verses.append(verse_obj)
            
        verse_idx = 0
        for ch_info in summary_data:
            ch_num = ch_info["chapter_number"]
            v_count = ch_info["verses_count"]
            ch_verses = all_verses[verse_idx:verse_idx + v_count]
            
            for cv_idx, cv in enumerate(ch_verses):
                cv["id"] = f"{sid}_{ch_num}_{cv_idx + 1}"
                cv["chapter_number"] = ch_num
                cv["metadata"]["chapter_number"] = ch_num
                cv["metadata"]["chapter_name"] = ch_info["name"]
                cv["metadata"]["chapter_slug"] = f"part-{ch_num}"
                
            ch_file_path = os.path.join(dest_dir, "chapters", f"chapter_{ch_num}.json")
            with open(ch_file_path, "w", encoding="utf-8") as f:
                json.dump(ch_verses, f, ensure_ascii=False, indent=2)
                
            verse_idx += v_count
            
        print(f"  Migrated {sid} with metadata ({len(all_verses)} verses).")

def enrich_yogasutras_metadata():
    print("\n==========================================")
    print("Enriching Yoga Sutras metadata...")
    print("==========================================")
    padas = {
        1: "Samādhi Pāda",
        2: "Sādhana Pāda",
        3: "Vibhūti Pāda",
        4: "Kaivalya Pāda"
    }
    ys_dir = os.path.join(PROJECT_DIR, "data/yogasutras/chapters")
    for ch_num, pada_name in padas.items():
        ch_file = os.path.join(ys_dir, f"chapter_{ch_num}.json")
        if not os.path.exists(ch_file):
            continue
        with open(ch_file, "r", encoding="utf-8") as f:
            verses = json.load(f)
        for v in verses:
            v_num = v.get("sutra_number") or v.get("verse_number")
            v["section_title"] = pada_name
            v["metadata"] = {
                "scripture_name": "Patanjali Yoga Sutras",
                "scripture_slug": "yogasutras",
                "chapter_number": ch_num,
                "sutra_number": v_num,
                "verse_number": v_num,
                "section_title": pada_name,
                "pada_name": pada_name,
                "darshana": "Yoga Darśana",
                "author": "Patañjali Maharṣi"
            }
        with open(ch_file, "w", encoding="utf-8") as f:
            json.dump(verses, f, ensure_ascii=False, indent=2)
        print(f"  Enriched Yoga Sutras Chapter {ch_num} ({len(verses)} sutras)")

if __name__ == "__main__":
    migrate_vivekachudamani()
    migrate_other_prakaranas()
    enrich_yogasutras_metadata()
    print("\nAll scripture metadata enriched and serialized!")

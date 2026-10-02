#!/usr/bin/env python3
"""
Migrate Sāṅkhyakārikā with Gauḍapāda Bhāṣya from:
- '/home/anurag/Projects/Mega Datahub/shlokam/sankhya/gaudapada sankhyakarika intro.json'
- '/home/anurag/Projects/Mega Datahub/shlokam/sankhya/gaudapada sankhyakarika without intro.json'

Target destination:
- data/sankhya-karika-gaudapada/summary.json
- data/sankhya-karika-gaudapada/chapters/chapter_1.json
- data/scriptures.json
- src/data/scripturesData.json

Incorporates:
1. Verse 1: Maṅgalācaraṇam (Gauḍapāda's opening invocatory verses: 'कपिलाय नमस्तस्मै...')
   with English & Hindi translations, word-by-word breakdown, Upodghāta bhāṣya, and concept analysis.
2. Verses 2-70: Kārikās 1 to 69 with Gauḍapāda's Sanskrit Bhāṣya, Avataraṇikā (introductory prose)
   and its English/Hindi translations, word-by-word synonyms, and concept analysis.
3. Registered under tradition: 'advaita' in the Vedānta section as requested by the user.
"""

import json
import os
import re

INTRO_SOURCE = '/home/anurag/Projects/Mega Datahub/shlokam/sankhya/gaudapada sankhyakarika intro.json'
KARIKA_SOURCE = '/home/anurag/Projects/Mega Datahub/shlokam/sankhya/gaudapada sankhyakarika without intro.json'
REPO_DIR = '/home/anurag/Projects/vedantvani'
TARGET_DATA_DIR = os.path.join(REPO_DIR, 'data/sankhya-karika-gaudapada')
CHAPTERS_DIR = os.path.join(TARGET_DATA_DIR, 'chapters')

CHAPTER_METAS = [
    {
        "chapter_number": 1,
        "name": "Sāṅkhyakārikā with Gauḍapāda Bhāṣya",
        "name_sanskrit": "साङ्ख्यकारिका गौडपादभाष्यसहिता",
        "name_transliterated": "Sāṅkhyakārikā Gauḍapādabhāṣyasahitā",
        "verses_count": 70,
        "summary": "Complete 69 Kārikās of Īśvarakṛṣṇa preceded by the opening Maṅgalācaraṇa verses of Śrī Gauḍapādācārya, along with his illuminating classical Bhāṣya, Avataraṇikā introductions, word-by-word grammatical breakdowns, and philosophical analysis.",
        "summary_hindi": "ईश्वरकृष्ण विरचित साङ्ख्यकारिका (६९ कारिकाएँ) तथा श्रीमद्गौडपादाचार्य कृत मङ्गलाचरण सहित सम्पूर्ण भाष्य, अवतरणिका, पदच्छेद एवं दार्शनिक विश्लेषण।"
    }
]

def clean_str(s):
    if not s:
        return ""
    return str(s).strip()

def map_synonyms(synonyms_list):
    res = []
    for syn in (synonyms_list or []):
        sanskrit_w = clean_str(syn.get("word"))
        english_m = clean_str(syn.get("meaning"))
        grammar_r = clean_str(syn.get("grammar"))
        padas_r = clean_str(syn.get("padas"))
        if not sanskrit_w and not english_m:
            continue
        res.append({
            "word_sanskrit": sanskrit_w,
            "word_english": english_m,
            "grammar_role": grammar_r,
            "root": padas_r
        })
    return res

def main():
    print(f"Loading intro source: {INTRO_SOURCE}")
    with open(INTRO_SOURCE, 'r', encoding='utf-8') as f:
        intro_raw = json.load(f)

    print(f"Loading karika source: {KARIKA_SOURCE}")
    with open(KARIKA_SOURCE, 'r', encoding='utf-8') as f:
        karika_raw = json.load(f)

    intro_by_id = {}
    for item in intro_raw:
        vid = item.get("verse_id")
        if vid and vid not in intro_by_id:
            intro_by_id[vid] = item

    os.makedirs(CHAPTERS_DIR, exist_ok=True)

    # 1. Build summary.json
    summary_path = os.path.join(TARGET_DATA_DIR, 'summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(CHAPTER_METAS, f, indent=2, ensure_ascii=False)
    print(f"Written {summary_path}")

    converted_verses = []

    # -------------------------------------------------------------
    # Verse 1: Maṅgalācaraṇam (Gauḍapāda's Opening Invocatory Verses)
    # -------------------------------------------------------------
    intro_item0 = intro_raw[0]
    mangal_sanskrit = clean_str(intro_item0.get("verse"))
    mangal_translit = clean_str(intro_item0.get("transliteration"))
    mangal_en = clean_str(intro_item0.get("translation"))
    mangal_hi = clean_str(intro_item0.get("translation_hindi"))
    mangal_meter = clean_str(intro_item0.get("meter") or "Upajāti")
    mangal_synonyms = map_synonyms(intro_item0.get("synonyms"))
    mangal_concept = intro_item0.get("concept_analysis") or {}

    mangal_commentaries = [
        {
            "author": "Śrī Gauḍapādācārya (गौडपादाचार्यः)",
            "author_name": "Gauḍapāda Bhāṣya (गौडपादभाष्यम्) - मङ्गलाचरणम्",
            "language": "Sanskrit",
            "school": "Advaita Vedānta / Gauḍapāda Bhāṣya",
            "description": (
                "॥ मङ्गलाचरणम् ॥\n"
                "कपिलाय नमस्तस्मै येनाविद्योदधौ जगति मग्ने ।\n"
                "कारुण्यात्सांख्यमयी नौरिव विहिता प्रतरणाय ॥\n"
                "अल्पग्रन्थं स्पष्टं प्रमाणसिद्धान्तहेतुभिर्युक्तम् ।\n"
                "शास्त्रं शिष्यहिताय समासतोऽहं प्रवक्ष्यामि ॥\n\n"
                "॥ उपोद्घातभाष्यम् ॥\n"
                "अस्या आर्याया उपोद्घातः क्रियते । इह भगवान् ब्रह्मसुतः कपिलो नाम । तद्यथा –\n"
                "सनकश्च सनन्दनश्च तृतीयश्च सनातनः ।\n"
                "आसुरिः कपिलश्चैव वोढुः पञ्चशिखस्तथा ॥\n"
                "इत्येते सप्त ब्रह्मसुताः प्रकृतेरुत्पन्नाः । महर्षेः कपिलात् प्राकृता धर्माः सप्तोत्पन्नाः, तद्यथा – ज्ञानं, वैराग्यम्, ऐश्वर्यम्, अधर्मः, अज्ञानम्, अवैराग्यम्, अनैश्वर्यम् इति । तस्य जन्मना सहोत्पन्नः । एवं स समुत्पन्नो जगदन्धकारमवलोक्य, संसारे संसरमाणान् जन्तून् विलोक्य परमकारुणिकस्तस्य आसुरिसगोत्रस्य ब्राह्मणस्याष्टवर्षसहस्रायुषः पाशुपतव्रतधारिणः प्रतिबोधनाय प्रादुर्बभूव ।"
            )
        },
        {
            "author": "Philosophical Analysis & Exegesis",
            "author_name": "Philosophical Exegesis (मङ्गलाचरण-विवेचनम्)",
            "language": "English",
            "school": "Sāṅkhya-Vedānta Synthesis",
            "description": (
                f"**Theme**: {mangal_concept.get('theme', 'Guru-paramparā and the Compassionate Transmission of Knowledge')}\n\n"
                f"**Philosophical Summary**: {mangal_concept.get('summary', '')}\n\n"
                f"**Spiritual Significance**: {mangal_concept.get('cultural_relevance', '')}"
            )
        }
    ]

    v1_obj = {
        "id": "sankhya-karika-gaudapada_1_1",
        "verse_number": 1,
        "chapter_number": 1,
        "sutra_number": "Intro",
        "sanskrit_shloka": mangal_sanskrit,
        "text": mangal_sanskrit,
        "transliteration": mangal_translit,
        "section_title": "मङ्गलाचरणम् (Maṅgalācaraṇam - Opening Invocatory Verses)",
        "summary_line": "Salutations to Sage Kapila who built the boat of Sāṅkhya to cross the ocean of ignorance, and Gauḍapāda's vow to expound the scripture.",
        "sadhana_stage": "Guru-Smaraṇam / Adhikāri-Lakṣaṇam",
        "primary_doctrine": "Guru-Kāruṇya & Sāṅkhya-Tattva-Jñāna",
        "keywords_sanskrit": ["कपिलाय", "अविद्योदधि", "कारुण्यात्", "सांख्यमयी", "प्रमाण", "सिद्धान्त", "हेतु", "शिष्यहित"],
        "translation": mangal_en,
        "translations": [
            {
                "author": "Traditional English Translation",
                "author_name": "Swami Virupakshananda / Classical Translation",
                "language": "English",
                "description": mangal_en
            },
            {
                "author": "हिन्दी अनुवाद",
                "author_name": "हिन्दी व्याख्या",
                "language": "Hindi",
                "description": mangal_hi
            }
        ],
        "commentaries": mangal_commentaries,
        "word_by_word": mangal_synonyms,
        "commentary_faqs": [
            {
                "question": "What is the purpose of the opening Maṅgalācaraṇa verse composed by Gauḍapādācārya?",
                "answer": "Gauḍapādācārya pays reverent homage to Sage Kapila, the primeval seer (Ādi-Vidvān) who out of sheer compassion fashioned the boat of Sāṅkhya wisdom to rescue souls drowning in the ocean of cosmic ignorance (Avidyā). He also clarifies that this commentary will be concise ('alpagrantham'), lucid ('spaṣṭam'), and rigorously grounded in epistemology ('pramāṇa'), doctrinal tenets ('siddhānta'), and rational logic ('hetu') for the spiritual welfare of seekers."
            }
        ],
        "metadata": {
            "meter": mangal_meter,
            "type": "Maṅgalācaraṇam",
            "author": "Śrī Gauḍapādācārya",
            "original_verse_id": "SKG_C01_V00_INTRO"
        }
    }
    converted_verses.append(v1_obj)

    # -------------------------------------------------------------
    # Verses 2 to 70: Sāṅkhyakārikā 1 to 69
    # -------------------------------------------------------------
    for idx, item in enumerate(karika_raw):
        karika_num = idx + 1
        v_num = idx + 2
        vid = item.get("verse_id", f"SKG_C01_V{karika_num:02d}")

        sanskrit_k = clean_str(item.get("verse_text") or item.get("verse"))
        translit_k = clean_str(item.get("transliteration"))
        en_trans = clean_str(item.get("translation"))
        hi_trans = clean_str(item.get("translation_hindi"))
        meter_k = clean_str(item.get("meter") or "Arya")
        synonyms_k = map_synonyms(item.get("synonyms"))
        concept_k = item.get("concept_analysis") or {}

        theme = clean_str(concept_k.get("theme"))
        summary = clean_str(concept_k.get("summary"))
        relevance = clean_str(concept_k.get("cultural_relevance"))

        sec_title = f"Kārikā {karika_num}"
        if theme:
            sec_title += f": {theme}"

        # Gauḍapāda's Sanskrit Bhāṣya and Avataraṇikā
        bhashya_raw = clean_str(item.get("bhashya_text"))
        verse_intro = clean_str(item.get("verse_intro"))

        commentaries_list = []

        bhashya_parts = []
        if verse_intro and vid != "SKG_C01_V01":
            # For V01, the verse_intro was the Maṅgalācaraṇa, which is already Verse 1.
            bhashya_parts.append(f"॥ अवतरणिका ॥\n{verse_intro}")
        if bhashya_raw:
            bhashya_parts.append(f"॥ भाष्यम् ॥\n{bhashya_raw}")

        if bhashya_parts:
            commentaries_list.append({
                "author": "Śrī Gauḍapādācārya (गौडपादाचार्यः)",
                "author_name": "Gauḍapāda Bhāṣya (गौडपादभाष्यम्)",
                "language": "Sanskrit",
                "school": "Advaita Vedānta / Gauḍapāda Bhāṣya",
                "description": "\n\n".join(bhashya_parts)
            })

        # Avataraṇikā Context & Translation (from intro source if available)
        intro_item = intro_by_id.get(vid)
        if intro_item and vid != "SKG_C01_V01":
            intro_en = clean_str(intro_item.get("translation"))
            intro_hi = clean_str(intro_item.get("translation_hindi"))
            intro_v_text = clean_str(intro_item.get("verse"))
            if intro_en or intro_hi:
                ctx_parts = []
                if intro_v_text:
                    ctx_parts.append(f"**Avataraṇikā (Connecting Context)**:\n{intro_v_text}")
                if intro_en:
                    ctx_parts.append(f"**English Translation of Avataraṇikā**:\n{intro_en}")
                if intro_hi:
                    ctx_parts.append(f"**हिन्दी अवतरणिका अनुवाद**:\n{intro_hi}")
                commentaries_list.append({
                    "author": "Gauḍapāda Avataraṇikā (Context)",
                    "author_name": "Gauḍapāda Avataraṇikā (Introductory Context)",
                    "language": "English & Hindi",
                    "school": "Gauḍapāda Bhāṣya Exegesis",
                    "description": "\n\n".join(ctx_parts)
                })

        # Philosophical Exegesis
        if theme or summary:
            exegesis_parts = []
            if theme:
                exegesis_parts.append(f"**Theme**: {theme}")
            if summary:
                exegesis_parts.append(f"**Philosophical Summary**: {summary}")
            if relevance:
                exegesis_parts.append(f"**Doctrinal Significance**: {relevance}")
            commentaries_list.append({
                "author": "Philosophical Analysis & Exegesis",
                "author_name": "Philosophical Exegesis (तत्वविवेचनम्)",
                "language": "English",
                "school": "Sāṅkhya-Vedānta Synthesis",
                "description": "\n\n".join(exegesis_parts)
            })

        translations_list = []
        if en_trans:
            translations_list.append({
                "author": "Swami Virupakshananda / Traditional English",
                "author_name": "Traditional English Translation",
                "language": "English",
                "description": en_trans
            })
        if hi_trans:
            translations_list.append({
                "author": "हिन्दी अनुवाद",
                "author_name": "हिन्दी व्याख्या",
                "language": "Hindi",
                "description": hi_trans
            })

        keywords = [clean_str(s.get("word")) for s in (item.get("synonyms") or []) if s.get("word")][:8]

        v_obj = {
            "id": f"sankhya-karika-gaudapada_1_{v_num}",
            "verse_number": v_num,
            "chapter_number": 1,
            "sutra_number": karika_num,
            "sanskrit_shloka": sanskrit_k,
            "text": sanskrit_k,
            "transliteration": translit_k,
            "section_title": sec_title,
            "summary_line": summary[:140] if summary else en_trans[:140],
            "sadhana_stage": "Tattva-Jijñāsā & Viveka",
            "primary_doctrine": theme or "Sāṅkhya Tattva-Vicāra",
            "keywords_sanskrit": keywords,
            "translation": en_trans,
            "translations": translations_list,
            "commentaries": commentaries_list,
            "word_by_word": synonyms_k,
            "commentary_faqs": [],
            "metadata": {
                "meter": meter_k,
                "karika_number": karika_num,
                "original_verse_id": vid,
                "theme": theme
            }
        }
        converted_verses.append(v_obj)

    # Save chapter_1.json
    ch1_path = os.path.join(CHAPTERS_DIR, 'chapter_1.json')
    with open(ch1_path, 'w', encoding='utf-8') as f:
        json.dump(converted_verses, f, indent=2, ensure_ascii=False)
    print(f"Written {ch1_path} with {len(converted_verses)} verses.")

    # -------------------------------------------------------------
    # Update data/scriptures.json
    # -------------------------------------------------------------
    scriptures_path = os.path.join(REPO_DIR, 'data/scriptures.json')
    with open(scriptures_path, 'r', encoding='utf-8') as f:
        scriptures = json.load(f)

    scripture_entry_minimal = {
        "id": "sankhya-karika-gaudapada",
        "name": "Sāṅkhyakārikā (Gauḍapāda Bhāṣya)",
        "name_sanskrit": "साङ्ख्यकारिका (गौडपादभाष्यम्)",
        "category": "Advaita Prakarana Texts",
        "chapters_count": 1,
        "total_verses": len(converted_verses),
        "description": "The Sāṅkhyakārikā of Īśvarakṛṣṇa with the classical commentary (Bhāṣya) by Śrī Gauḍapādācārya (the revered Paramaguru of Ādi Śaṅkarācārya). Preserved in the Advaita Vedānta tradition as the definitive classical exposition of Sāṅkhya metaphysics and epistemology, essential for understanding Vedāntic dialectics, Tattva Viveka, and the refutation of Pradhānadvaita in the Brahma Sūtras."
    }

    existing_idx = next((i for i, s in enumerate(scriptures) if s.get('id') == 'sankhya-karika-gaudapada'), -1)
    if existing_idx >= 0:
        scriptures[existing_idx] = scripture_entry_minimal
        print("Updated entry in data/scriptures.json")
    else:
        # Insert under Advaita Prakarana Texts
        prakarana_indices = [i for i, s in enumerate(scriptures) if s.get('category') == 'Advaita Prakarana Texts']
        if prakarana_indices:
            insert_at = max(prakarana_indices) + 1
            scriptures.insert(insert_at, scripture_entry_minimal)
        else:
            scriptures.append(scripture_entry_minimal)
        print("Inserted new entry in data/scriptures.json")

    with open(scriptures_path, 'w', encoding='utf-8') as f:
        json.dump(scriptures, f, indent=2, ensure_ascii=False)

    # -------------------------------------------------------------
    # Update src/data/scripturesData.json
    # -------------------------------------------------------------
    scriptures_data_path = os.path.join(REPO_DIR, 'src/data/scripturesData.json')
    with open(scriptures_data_path, 'r', encoding='utf-8') as f:
        scriptures_data = json.load(f)

    scripture_entry_full = {
        "id": "sankhya-karika-gaudapada",
        "name": "Sāṅkhyakārikā (Gauḍapāda Bhāṣya)",
        "name_sanskrit": "साङ्ख्यकारिका (गौडपादभाष्यम्)",
        "category": "Advaita Prakarana Texts",
        "tradition": "advaita",
        "traditionLabel": "Advaita Vedānta",
        "subcategory": "Advaita Prakarana Texts",
        "author": "Īśvarakṛṣṇa & Gauḍapādācārya (ईश्वरकृष्णः व गौडपादाचार्यः)",
        "chapters_count": 1,
        "total_verses": len(converted_verses),
        "description": "The Sāṅkhyakārikā of Īśvarakṛṣṇa with the classical commentary (Bhāṣya) by Śrī Gauḍapādācārya (the revered Paramaguru of Ādi Śaṅkarācārya). Preserved in the Advaita Vedānta tradition as the definitive classical exposition of Sāṅkhya metaphysics and epistemology, essential for understanding Vedāntic dialectics, Tattva Viveka, and the refutation of Pradhānadvaita in the Brahma Sūtras.",
        "chapters": CHAPTER_METAS
    }

    existing_sd_idx = next((i for i, s in enumerate(scriptures_data) if s.get('id') == 'sankhya-karika-gaudapada'), -1)
    if existing_sd_idx >= 0:
        scriptures_data[existing_sd_idx] = scripture_entry_full
        print("Updated entry in src/data/scripturesData.json")
    else:
        advaita_indices = [i for i, s in enumerate(scriptures_data) if s.get('tradition') == 'advaita']
        if advaita_indices:
            insert_at = max(advaita_indices) + 1
            scriptures_data.insert(insert_at, scripture_entry_full)
        else:
            scriptures_data.append(scripture_entry_full)
        print("Inserted new entry in src/data/scripturesData.json")

    with open(scriptures_data_path, 'w', encoding='utf-8') as f:
        json.dump(scriptures_data, f, indent=2, ensure_ascii=False)

    print("Migration finished successfully!")

if __name__ == '__main__':
    main()

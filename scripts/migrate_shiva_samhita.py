#!/usr/bin/env python3
"""
Migrate Shiva Samhita from '/home/anurag/Projects/Mega Datahub/shlokam/shiva samhita.json'
into VedāntVāṇī standard schema and file structure:
- data/shiva-samhita/summary.json
- data/shiva-samhita/chapters/chapter_{1..5}.json
- data/scriptures.json
- src/data/scripturesData.json
"""

import json
import os
import re

SOURCE_PATH = '/home/anurag/Projects/Mega Datahub/shlokam/shiva samhita.json'
REPO_DIR = '/home/anurag/Projects/vedantvani'
TARGET_DATA_DIR = os.path.join(REPO_DIR, 'data/shiva-samhita')
CHAPTERS_DIR = os.path.join(TARGET_DATA_DIR, 'chapters')

CHAPTER_METAS = [
    {
        "chapter_number": 1,
        "name": "Prathama Patala (Non-Dual Gnosis & Epistemology)",
        "name_sanskrit": "प्रथमः पटलः - ज्ञानकाण्डम्",
        "name_transliterated": "Paṭala 1",
        "verses_count": 96,
        "summary": "Lord Shiva expounds the supreme non-dual truth (Advaita) to Goddess Parvati, declaring pure consciousness (Jnana) alone as eternal, unconditioned, and all-pervading. He dismantles dualistic dogmas and ritualistic delusions, explaining how the phenomenal universe appears through sensory conditionings (Upadhis) and karma.",
        "summary_hindi": "भगवान् शिव देवी पार्वती को परम अद्वैत सत्य का उपदेश देते हैं, जिसमें शुद्ध ज्ञान को ही नित्य और सर्वव्यापी बताया गया है तथा कर्मकाण्ड व द्वैतवादी मतों का खण्डन कर उपाधियों के निरसन का मार्ग दर्शाया गया है।"
    },
    {
        "chapter_number": 2,
        "name": "Dvitiya Patala (Microcosm, Mount Meru & Nadis)",
        "name_sanskrit": "द्वितीयः पटलः - पिण्डब्रह्माण्डविवेकः नाडीनिरूपणम्",
        "name_transliterated": "Paṭala 2",
        "verses_count": 54,
        "summary": "Reveals the profound correspondence between the human body (microcosm) and the cosmos (macrocosm). Describes Mount Meru in the spinal column, the sun and moon, the 350,000 Nadis with special emphasis on Ida, Pingala, and Sushumna (Chitrini), the Jivatman, and the digestive fire (Vaishvanara).",
        "summary_hindi": "मानव देह (पिण्ड) और ब्रह्माण्ड की एकात्मता का निरूपण। मेरुदण्ड में मेरु पर्वत, सूर्य-चन्द्र, ३,५०,००० नाड़ियों (विशेषतः इड़ा, पिङ्गला, सुषुम्णा व चित्रिणी) तथा जीवात्मा एवं वैश्वानर अग्नि का रहस्य।"
    },
    {
        "chapter_number": 3,
        "name": "Tritiya Patala (Vayus, Guru & Pranayama)",
        "name_sanskrit": "तृतीयः पटलः - प्राणायामपद्धतिः",
        "name_transliterated": "Paṭala 3",
        "verses_count": 98,
        "summary": "Explains the ten vital airs (Prana, Apana, Samana, Udana, Vyana, and five secondary vayus), the indispensable guidance of the Guru, prerequisites of sadhana, systematic Nadi purification through Pranayama (Kumbhaka), signs of yogic progress (perspiration, tremor, levitation), and four foundational asanas (Siddhasana, Padmasana, Ugrasana, Svastikasana).",
        "summary_hindi": "दश प्राण वायुओं, गुरु-महिमा, प्राणायाम साधना द्वारा नाड़ी-शुद्धि के सोपान (स्वेद, कम्प, दर्दुरी गति) तथा सिद्धासन, पद्मासन, उग्रासन और स्वस्तिकासन का विस्तृत विधान।"
    },
    {
        "chapter_number": 4,
        "name": "Chaturtha Patala (The Ten Mudras & Kundalini)",
        "name_sanskrit": "चतुर्थः पटलः - मुद्राविवरणम्",
        "name_transliterated": "Paṭala 4",
        "verses_count": 58,
        "summary": "Expounds the ten great seals (Mudras) that awaken the coiled serpentine power (Kundalini Shakti) and bestow longevity and victory over death: Mahamudra, Mahabandha, Mahavedha, Khechari, Jalandhara Bandha, Mula Bandha, Uddiyana Bandha, Viparita Karani, Vajroli, and Shaktichalana.",
        "summary_hindi": "कुण्डलिनी जागरण एवं मृत्यु-जय के लिए दस महामुद्राओं (महामुद्रा, महाबन्ध, महावेध, खेचरी, जालन्धर, मूलबन्ध, उड्डीयान, विपरीतकरणी, वज्रोली व शक्तिचालन) का रहस्यमय निरूपण।"
    },
    {
        "chapter_number": 5,
        "name": "Panchama Patala (Chakras, Obstacles & Rajayoga)",
        "name_sanskrit": "पञ्चमः पटलः - चक्रनिरूपणं राजयोगश्च",
        "name_transliterated": "Paṭala 5",
        "verses_count": 212,
        "summary": "Comprehensive exposition on the four types of practitioners (Mridu, Madhya, Adhimatra, Adhimatratama), the obstacles to yoga (bhoga, dharma, jnana), contemplation on the six subtle Chakras (Muladhara, Svadhisthana, Manipura, Anahata, Vishuddha, Ajna, Sahasrara), Mantrayoga, Nadanusandhana, and supreme non-dual immersion in Rajayoga.",
        "summary_hindi": "साधकों के चार भेद, योग के विघ्न, षट्चक्रों (मूलाधार, स्वाधिष्ठान, मणिपूर, अनाहत, विशुद्ध, आज्ञा) व सहस्रार का विशद ध्यान, मन्त्रयोग, नादानुसन्धान तथा समाधिस्थ राजयोग की सिद्धि।"
    }
]

def main():
    print(f"Reading source from {SOURCE_PATH}...")
    with open(SOURCE_PATH, 'r', encoding='utf-8') as f:
        raw_verses = json.load(f)

    os.makedirs(CHAPTERS_DIR, exist_ok=True)

    # Write summary.json
    summary_path = os.path.join(TARGET_DATA_DIR, 'summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(CHAPTER_METAS, f, indent=2, ensure_ascii=False)
    print(f"Saved {summary_path}")

    # Process per chapter
    chapters_data = {1: [], 2: [], 3: [], 4: [], 5: []}
    for item in raw_verses:
        ch = item.get('chapter', 1)
        if ch in chapters_data:
            chapters_data[ch].append(item)

    total_converted = 0
    for ch_num, items in chapters_data.items():
        converted_chapter_verses = []
        for idx, item in enumerate(items, start=1):
            v_num = idx
            sanskrit_text = (item.get("sanskrit") or item.get("verse") or "").strip()
            transliteration = (item.get("transliteration") or "").strip()
            primary_trans = (item.get("translation") or item.get("english") or "").strip()
            trad_trans = (item.get("english") or "").strip()
            hindi_trans = (item.get("translation_hindi") or "").strip()

            # Translations list
            translations_list = []
            if primary_trans:
                translations_list.append({
                    "author": "Modern English Translation",
                    "author_name": "Modern English Translation",
                    "language": "English",
                    "description": primary_trans,
                    "text": primary_trans
                })
            if trad_trans and trad_trans != primary_trans:
                translations_list.append({
                    "author": "Srisa Chandra Vasu (Traditional)",
                    "author_name": "Srisa Chandra Vasu (Traditional)",
                    "language": "English",
                    "description": trad_trans,
                    "text": trad_trans
                })
            if hindi_trans:
                translations_list.append({
                    "author": "Hindi Translation (भावार्थ)",
                    "author_name": "Hindi Translation (भावार्थ)",
                    "language": "Hindi",
                    "description": hindi_trans,
                    "text": hindi_trans
                })

            # Word by word breakdown
            word_by_word_list = []
            for syn in item.get("synonyms", []):
                w_sanskrit = (syn.get("word") or "").strip()
                w_meaning = (syn.get("meaning") or "").strip()
                w_grammar = (syn.get("grammar") or "").strip()
                w_root = (syn.get("padas") or "").strip()
                if w_sanskrit or w_meaning:
                    word_by_word_list.append({
                        "word_sanskrit": w_sanskrit,
                        "word_english": w_meaning,
                        "grammar_role": w_grammar,
                        "root": w_root
                    })

            # Concept analysis & commentary
            commentaries_list = []
            faqs_list = []
            ca = item.get("concept_analysis", {})
            if ca:
                theme = ca.get("theme", "").strip()
                summary = ca.get("summary", "").strip()
                relevance = ca.get("cultural_relevance", "").strip()

                desc_parts = []
                if theme:
                    desc_parts.append(f"**Theme**: {theme}")
                if summary:
                    desc_parts.append(f"**Exposition**: {summary}")
                if relevance:
                    desc_parts.append(f"**Yogic & Philosophical Significance**: {relevance}")

                if desc_parts:
                    full_desc = "\n\n".join(desc_parts)
                    commentaries_list.append({
                        "author": "Yogic & Philosophical Exegesis",
                        "author_name": "Yogic & Philosophical Exegesis",
                        "language": "English",
                        "school": "Classical Yoga (Śiva Saṁhitā)",
                        "description": full_desc,
                        "text": full_desc
                    })

                if theme and summary:
                    faqs_list.append({
                        "question": f"Essence: {theme}",
                        "answer": summary
                    })
                if relevance:
                    faqs_list.append({
                        "question": "Somatic & Spiritual Significance in Practice",
                        "answer": relevance
                    })

            # Metadata
            metadata_obj = {
                "meter": item.get("meter", ""),
                "theme": ca.get("theme", "") if ca else "",
                "primary_doctrine": "Advaita / Hatha Yoga",
                "prakriya_mapped": "Nadi & Chakra Prana Vidya"
            }

            v_obj = {
                "id": f"shiva-samhita_{ch_num}_{v_num}",
                "verse_number": v_num,
                "chapter_number": ch_num,
                "sanskrit_shloka": sanskrit_text,
                "text": sanskrit_text,
                "transliteration": transliteration,
                "translation": primary_trans,
                "translations": translations_list,
                "commentaries": commentaries_list,
                "word_by_word": word_by_word_list,
                "commentary_faqs": faqs_list,
                "metadata": metadata_obj
            }
            converted_chapter_verses.append(v_obj)

        ch_out_path = os.path.join(CHAPTERS_DIR, f"chapter_{ch_num}.json")
        with open(ch_out_path, 'w', encoding='utf-8') as f:
            json.dump(converted_chapter_verses, f, indent=2, ensure_ascii=False)
        print(f"Saved Chapter {ch_num} with {len(converted_chapter_verses)} verses -> {ch_out_path}")
        total_converted += len(converted_chapter_verses)

    print(f"Total verses converted: {total_converted} (expected 518)")

    # 1. Update data/scriptures.json
    scriptures_path = os.path.join(REPO_DIR, 'data/scriptures.json')
    with open(scriptures_path, 'r', encoding='utf-8') as f:
        all_scrs = json.load(f)

    # Check if already present
    exists = any(s['id'] == 'shiva-samhita' for s in all_scrs)
    shiva_samhita_entry = {
        "id": "shiva-samhita",
        "name": "Shiva Samhita",
        "name_sanskrit": "शिवसंहिता",
        "category": "Yoga Scriptures",
        "chapters_count": 5,
        "total_verses": total_converted,
        "description": "The Shiva Samhita is one of the three monumental classical treatises of Hatha Yoga (alongside Hatha Yoga Pradipika and Gheranda Samhita). Presented as an esoteric dialogue between Lord Shiva and Goddess Parvati, it expounds non-dual metaphysics (Advaita), micro-macrocosmic correspondence, the 350,000 Nadis, 10 vital Vayus, Kundalini awakening, the seven Chakras, Bandhas, Mudras, and Rajayoga realization."
    }

    if not exists:
        all_scrs.append(shiva_samhita_entry)
        with open(scriptures_path, 'w', encoding='utf-8') as f:
            json.dump(all_scrs, f, indent=2, ensure_ascii=False)
        print(f"Added 'shiva-samhita' to {scriptures_path}")
    else:
        # Update existing
        for i, s in enumerate(all_scrs):
            if s['id'] == 'shiva-samhita':
                all_scrs[i] = shiva_samhita_entry
        with open(scriptures_path, 'w', encoding='utf-8') as f:
            json.dump(all_scrs, f, indent=2, ensure_ascii=False)
        print(f"Updated 'shiva-samhita' in {scriptures_path}")

    # 2. Update src/data/scripturesData.json
    scriptures_data_path = os.path.join(REPO_DIR, 'src/data/scripturesData.json')
    with open(scriptures_data_path, 'r', encoding='utf-8') as f:
        all_data_scrs = json.load(f)

    full_shiva_entry = {
        "id": "shiva-samhita",
        "name": "Shiva Samhita",
        "name_sanskrit": "शिवसंहिता",
        "category": "Yoga Scriptures",
        "tradition": "yoga",
        "traditionLabel": "Yoga Scriptures",
        "subcategory": "Classical Yoga",
        "author": "Lord Shiva (भगवान् शिवः)",
        "chapters_count": 5,
        "total_verses": total_converted,
        "description": "The Shiva Samhita is one of the three monumental classical treatises of Hatha Yoga (alongside Hatha Yoga Pradipika and Gheranda Samhita). Presented as an esoteric dialogue between Lord Shiva and Goddess Parvati, it expounds non-dual metaphysics (Advaita), micro-macrocosmic correspondence, the 350,000 Nadis, 10 vital Vayus, Kundalini awakening, the seven Chakras, Bandhas, Mudras, and Rajayoga realization.",
        "chapters": CHAPTER_METAS
    }

    data_exists = any(s['id'] == 'shiva-samhita' for s in all_data_scrs)
    if not data_exists:
        all_data_scrs.append(full_shiva_entry)
        with open(scriptures_data_path, 'w', encoding='utf-8') as f:
            json.dump(all_data_scrs, f, indent=2, ensure_ascii=False)
        print(f"Added 'shiva-samhita' to {scriptures_data_path}")
    else:
        for i, s in enumerate(all_data_scrs):
            if s['id'] == 'shiva-samhita':
                all_data_scrs[i] = full_shiva_entry
        with open(scriptures_data_path, 'w', encoding='utf-8') as f:
            json.dump(all_data_scrs, f, indent=2, ensure_ascii=False)
        print(f"Updated 'shiva-samhita' in {scriptures_data_path}")

    print("Shiva Samhita migration completed successfully!")

if __name__ == '__main__':
    main()

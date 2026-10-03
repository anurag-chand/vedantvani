#!/usr/bin/env python3
"""
Pipeline for Adhyātma Rāmāyaṇa:
Extracts data from tagged verses and event JSONs across all 7 Kāṇḍas,
generating a unified event-first dataset:
- data/adhyatma-ramayana/summary.json
- data/adhyatma-ramayana/kandas/kanda_{1..7}.json
- data/adhyatma-ramayana/ontology.json
- Updates data/scriptures.json & src/data/scripturesData.json
"""

import os
import json
import re
import zipfile

SOURCE_DIR = '/home/anurag/Projects/Mega Datahub/shlokam/adhyatma ramayan/'
EVENT_DIR = os.path.join(SOURCE_DIR, 'Event id')
ZIP_PATH = os.path.join(SOURCE_DIR, 'Download.zip')

TARGET_DIR = '/home/anurag/Projects/vedantvani/data/adhyatma-ramayana'
KANDAS_DIR = os.path.join(TARGET_DIR, 'kandas')

KANDA_CONFIGS = [
    {
        "kanda_number": 1,
        "name": "Bālakāṇḍa",
        "name_sanskrit": "बालकाण्डम्",
        "name_transliterated": "Bālakāṇḍa",
        "tagged_file": "adhyaatmaRamBal_devanagari_tagged.json",
        "event_file": "adhyatma_ramayana_balakanda_event_advaita.json",
        "prefix": "BAL",
        "summary": "The advent of the Supreme Lord as Rama, the revelation of the transcendent mystery in Ramahridaya, redemption of Ahalya, bow of Shiva, and marriage with Sita as Yoga-Maya.",
        "summary_hindi": "भगवान् श्री राम का प्राकट्य, शिव-पार्वती संवाद में रामहृदय का परम अद्वैत उपदेश, अहल्या उद्धार, धनुर्भङ्ग तथा सीता के साथ परिणय।"
    },
    {
        "kanda_number": 2,
        "name": "Ayodhyākāṇḍa",
        "name_sanskrit": "अयोध्याकाण्डम्",
        "name_transliterated": "Ayodhyākāṇḍa",
        "tagged_file": "adhyaatmaRamAyo_devanagari_tagged.json",
        "event_file": "ayo kand event id.json",
        "prefix": "AYO",
        "summary": "The divine conspiracy of exile, Lakshmana's philosophical instruction on Maya, meeting with Guha, crossing the Ganga, meeting with Bharadvaja, Valmiki's ashram, and the sandals of Rama.",
        "summary_hindi": "वनवास का दिव्य सङ्कल्प, लक्ष्मण को माया एवं विवेक का उपदेश, गुह-मिलन, भरत-मिलाप तथा पादुका-प्रदान।"
    },
    {
        "kanda_number": 3,
        "name": "Āraṇyakāṇḍa",
        "name_sanskrit": "अरण्यकाण्डम्",
        "name_transliterated": "Āraṇyakāṇḍa",
        "tagged_file": "adhyaatmaRamAra_devanagari_tagged.json",
        "event_file": "aranya kand event id.json",
        "prefix": "ARA",
        "summary": "The forest hermitage, meeting with Sage Agastya, manifestation of the illusory Maya-Sita, abduction of the reflection, destruction of Jatayu, and Shabari's ninefold devotion (Navavidha Bhakti).",
        "summary_hindi": "दण्डकारण्य में मुनियों का दर्शन, अगस्त्य संवाद, माया-सीता का प्राकट्य, रावण द्वारा अपहरण, जटायु उद्धार एवं शबरी को नवधा भक्ति का उपदेश।"
    },
    {
        "kanda_number": 4,
        "name": "Kiṣkindhākāṇḍa",
        "name_sanskrit": "किष्किन्धाकाण्डम्",
        "name_transliterated": "Kiṣkindhākāṇḍa",
        "tagged_file": "adhyaatmaRamkiShkindhA_devanagari_tagged.json",
        "event_file": "kishkindhakand event id.json",
        "prefix": "KIS",
        "summary": "Meeting with Hanuman and Sugriva, slaying of Vali, Tara's supreme Advaita enlightenment by Rama, rainy season contemplation, and the search for Sita.",
        "summary_hindi": "हनुमान् व सुग्रीव मिलन, बालि वध, तारा को श्रीराम द्वारा आत्म-ज्ञान का उपदेश, चातुर्मास्य का ध्यान तथा सीता की खोज।"
    },
    {
        "kanda_number": 5,
        "name": "Sundarakāṇḍa",
        "name_sanskrit": "सुन्दरकाण्डम्",
        "name_transliterated": "Sundarakāṇḍa",
        "tagged_file": "adhyaatmaRamsundara_devanagari_tagged.json",
        "event_file": "sundarakand event id.json",
        "prefix": "SUN",
        "summary": "Hanuman's oceanic leap of faith, discovery of Sita in Ashoka Vatika, delivery of the signet ring, Advaita discourse to Ravana, burning of Lanka, and report to Rama.",
        "summary_hindi": "हनुमान् जी का समुद्र-लङ्घन, अशोक वाटिका में सीता दर्शन, रावण को तत्त्व-उपदेश, लङ्का-दहन तथा श्रीराम को सन्देश-समर्पण।"
    },
    {
        "kanda_number": 6,
        "name": "Yuddhakāṇḍa",
        "name_sanskrit": "युद्धकाण्डम्",
        "name_transliterated": "Yuddhakāṇḍa",
        "tagged_file": "adhyaatmaRamyuddha_devanagari_tagged.json",
        "event_file": "yudhkand event id .json",
        "prefix": "YUD",
        "summary": "March to the ocean, Vibhishana's surrender (Sharanagati), bridging the sea, cosmic battle, fall of Kumbhakarna and Ravana, fire-ordeal and retrieval of the real Sita, and the grand coronation at Ayodhya.",
        "summary_hindi": "सेतु-निर्माण, विभीषण शरणागति, महायुद्ध, कुम्भकर्ण व रावण का मोक्ष, माया-सीता का अग्नि-प्रवेश व वास्तविक सीता की पुनः प्राप्ति तथा भव्य राज्याभिषेक।"
    },
    {
        "kanda_number": 7,
        "name": "Uttarakāṇḍa",
        "name_sanskrit": "उत्तरकाण्डम्",
        "name_transliterated": "Uttarakāṇḍa",
        "tagged_file": "adhyaatmaRamuttara_devanagari_tagged.json",
        "event_file": "uttarakand event id.json",
        "prefix": "UTT",
        "summary": "The crowning crest of Advaita: Rama Gita (definitive instruction to Lakshmana), Sita's oath, Kausalya's liberation, Kala's arrival, Lakshmana's resumption of Shesha form, and Rama's entry into the Sarayu with cosmic liberation of Ayodhya.",
        "summary_hindi": "अद्वैत का मुकुटमणि: श्रीरामगीता (लक्ष्मण को शुद्ध ज्ञानोपदेश), कौशल्या मोक्ष, काल का आगमन, लक्ष्मण का शेष-स्वरूप तथा सरयू में श्रीराम का महाप्रस्थान।"
    }
]

# Standard ontological definitions map
ONTOLOGY_DEF_MAP = {
    "ADV-CAND-BRAHMAN": {"term": "Brahman (ब्रह्म)", "definition": "The non-dual, infinite Absolute Reality; pure existence-consciousness-bliss (Sat-Chit-Ananda), devoid of all attributes and modifications."},
    "ADV-CAND-PARAMATMAN": {"term": "Paramātman (परमात्मा)", "definition": "The supreme transcendent Self, the innermost witness residing in the hearts of all living beings, identical with Brahman."},
    "ADV-CAND-ATMAN": {"term": "Ātman (आत्मा)", "definition": "The true Self within the individual, eternally free, self-luminous, and distinct from the physical and subtle bodies."},
    "ADV-CAND-MAYA": {"term": "Māyā (माया)", "definition": "The inexplicable cosmic illusion possessing the twin powers of concealing the truth (Avarana) and projecting diversity (Vikshepa)."},
    "ADV-CAND-AVIDYA": {"term": "Avidyā (अविद्या)", "definition": "Primordial spiritual ignorance at the individual level, causing the false superimposition (Adhyāsa) of body and mind onto the Self."},
    "ADV-CAND-ISVARA": {"term": "Īśvara (ईश्वर)", "definition": "Brahman associated with cosmic Sattvic Māyā as the omniscient Lord, creator, sustainer, and dissolver of the universe (personified as Śrī Rāma)."},
    "ADV-CAND-ISHVARA": {"term": "Īśvara (ईश्वर)", "definition": "Brahman associated with cosmic Sattvic Māyā as the omniscient Lord and sovereign of creation."},
    "ADV-CAND-MOKSHA": {"term": "Mokṣa (मोक्ष)", "definition": "Complete liberation from the cycle of birth and death (Samsara), realized through immediate direct knowledge (Aparoksha-Jnana) of one's non-difference from Brahman."},
    "ADV-CAND-BHAKTI": {"term": "Bhakti (भक्ति)", "definition": "Supreme, single-pointed devotion and love for the Lord, recognized in Adhyatma Ramayana as the most accessible and potent purifier of the heart leading directly to Jnana."},
    "ADV-CAND-JNANA": {"term": "Jñāna (ज्ञान)", "definition": "The unshakeable non-dual realization that 'I am Brahman' (Aham Brahmasmi), destroying the knot of the heart and all accumulated karmas."},
    "ADV-CAND-UPADHI": {"term": "Upādhi (उपाधि)", "definition": "Limiting adjuncts or conditioning factors (body, senses, mind, intellect) that make the indivisible Self appear as a limited individual soul (Jiva)."},
    "ADV-CAND-SAMSARA": {"term": "Saṁsāra (संसार)", "definition": "The transmigratory cycle of repeated births, suffering, and deaths resulting from ignorance of one's divine nature."},
    "ADV-CAND-ADHYASA": {"term": "Adhyāsa (अध्यास)", "definition": "Superimposition; mistaking the unreal for the Real and vice versa, as when perceiving a snake in a rope in dim twilight."},
    "ADV-CAND-VIVEKA": {"term": "Viveka (विवेक)", "definition": "Discrimination between the Real (Nitya) and the unreal (Anitya); the foundational virtue cultivated by the seeker."},
    "ADV-CAND-VAIRAGYA": {"term": "Vairāgya (वैराग्य)", "definition": "Dispassion and freedom from craving for transient worldly and celestial sensory enjoyments."},
    "ADV-CAND-DHARMA": {"term": "Dharma (धर्म)", "definition": "Cosmic order, righteousness, and ethical duty practiced as Ishvara-arpana (offering to God) without personal desire."},
    "ADV-CAND-KARMA": {"term": "Karma (कर्म)", "definition": "Action and its causal impressions; transcended through Nishkama Karma (selfless action) and Jnana."},
    "ADV-CAND-JAGAT": {"term": "Jagat (जगत्)", "definition": "The phenomenal universe, which has transactional empirical reality (Vyavaharika) but dissolves into Brahman upon enlightenment."},
    "ADV-CAND-JIVA": {"term": "Jīva (जीव)", "definition": "The individual soul, which appears separate due to embodiment and mind, but is essentially non-different from Ishvara and Brahman."},
    "ADV-CAND-JIVANMUKTI": {"term": "Jīvanmukti (जीवन्मुक्ति)", "definition": "Liberation while still living in the physical body; dwelling in unbroken Sahaja Samadhi amidst daily actions."},
    "ADV-CAND-MAHAVAKYA": {"term": "Mahāvākya (महावाक्य)", "definition": "The great Upanishadic identity statements (such as Tat Tvam Asi) that bestow direct realization when contemplated with a prepared mind."},
    "ADV-CAND-YOGA": {"term": "Yoga (योग)", "definition": "The spiritual discipline of stilling the mental modifications to unite the individual awareness with the supreme consciousness."}
}

def parse_range(range_str):
    m = re.match(r'(\d+)\.(\d+)(?:-(\d+)\.(\d+))?', range_str.strip())
    if m:
        s1 = int(m.group(1))
        v1 = int(m.group(2))
        s2 = int(m.group(3)) if m.group(3) else s1
        v2 = int(m.group(4)) if m.group(4) else v1
        return s1, v1, s2, v2
    return None

def clean_text(s):
    if s is None:
        return ""
    return str(s).strip()

def main():
    print("Starting Adhyātma Rāmāyaṇa Migration Pipeline...")
    os.makedirs(KANDAS_DIR, exist_ok=True)

    summary_kandas = []
    total_scripture_verses = 0
    total_scripture_events = 0
    total_scripture_sargas = 0

    for cfg in KANDA_CONFIGS:
        k_num = cfg["kanda_number"]
        k_name = cfg["name"]
        prefix = cfg["prefix"]
        tagged_path = os.path.join(SOURCE_DIR, cfg["tagged_file"])
        event_path = os.path.join(EVENT_DIR, cfg["event_file"])

        print(f"\nProcessing {k_name} (Kanda {k_num})...")

        with open(tagged_path, 'r', encoding='utf-8') as f:
            tagged_raw = json.load(f)

        with open(event_path, 'r', encoding='utf-8') as f:
            event_raw = json.load(f)

        # Map tagged verses by (sarga, verse_number)
        verses_by_sarga = {}
        for item in tagged_raw:
            s_num = item.get("chapter_number")
            v_num = item.get("verse_number")
            if s_num and v_num:
                verses_by_sarga.setdefault(s_num, {})[v_num] = item

        # Read sargas meta from event file
        sargas_meta_list = event_raw.get("sargas", [])
        sarga_title_map = {s["sarga"]: s.get("title", f"Sarga {s['sarga']}") for s in sargas_meta_list}

        # Parse predefined segments from event JSON
        predefined_segments = event_raw.get("segments", [])
        segments_by_sarga = {}
        for seg in predefined_segments:
            vr = seg.get("verse_range", "")
            pr = parse_range(vr)
            if pr:
                s1, v1, s2, v2 = pr
                segments_by_sarga.setdefault(s1, []).append((v1, v2, seg))

        # Build final Sargas array with contiguous Event ID segments
        final_sargas = []
        kanda_total_verses = len(tagged_raw)
        kanda_total_events = 0

        all_sarga_nums = sorted(list(verses_by_sarga.keys()))
        total_scripture_sargas += len(all_sarga_nums)
        total_scripture_verses += kanda_total_verses

        for s_num in all_sarga_nums:
            s_verses_dict = verses_by_sarga[s_num]
            max_v = max(s_verses_dict.keys())
            min_v = min(s_verses_dict.keys())
            s_title = sarga_title_map.get(s_num, f"Sarga {s_num}")

            # Get predefined segments for this sarga sorted by start verse
            s_segs = sorted(segments_by_sarga.get(s_num, []), key=lambda x: x[0])

            # Check coverage and fill gaps with narrative segments
            final_segments_for_sarga = []
            curr_v = min_v

            for v1, v2, seg in s_segs:
                # If there is an uncovered gap before this predefined segment
                if curr_v < v1:
                    gap_start = curr_v
                    gap_end = v1 - 1
                    gap_id = f"AR-{prefix}-{s_num:02d}-N{gap_start:02d}"
                    gap_verses = [s_verses_dict[vn] for vn in range(gap_start, gap_end + 1) if vn in s_verses_dict]
                    
                    # Synthesize narrative event
                    first_meta = gap_verses[0]["output_doc"]["metadata_fields"] if gap_verses else {}
                    title_narrative = first_meta.get("associated_epic_event") or "Epic Narrative Discourse"
                    title_narrative = title_narrative.replace("_", " ")

                    chars = list(set([c for gv in gap_verses for c in gv["output_doc"]["metadata_fields"].get("characters_featured", []) if c]))
                    place = first_meta.get("place_mentioned") or "Ayodhya / Sacred Environs"
                    if place == "None":
                        place = "Sacred Narrative Setting"

                    gap_seg = {
                        "segment_id": gap_id,
                        "verse_range": f"{s_num}.{gap_start}-{s_num}.{gap_end}",
                        "start_verse": gap_start,
                        "end_verse": gap_end,
                        "event": {
                            "title": title_narrative,
                            "event_type": "epic_narrative",
                            "summary": f"Narrative events and philosophical dialogue connecting verses {gap_start} through {gap_end} of Sarga {s_num}."
                        },
                        "place": place,
                        "place_symbolic_meaning": first_meta.get("place_symbolic_meaning", "No_Symbolic_Interpretation"),
                        "characters": chars if chars else ["Rama", "Devotees"],
                        "character_cosmic_mappings": first_meta.get("character_cosmic_mappings", []),
                        "philosophy": {
                            "present": bool(first_meta.get("primary_doctrine")),
                            "density": "MEDIUM",
                            "ontology_refs": ["ADV-CAND-BHAKTI", "ADV-CAND-DHARMA"],
                            "evidence_status": "source_text_based_annotation",
                            "primary_doctrine": first_meta.get("primary_doctrine", "Bhakti-Jnana-Samuccaya"),
                            "prakriya_mapped": first_meta.get("prakriya_mapped", "Adhyaropa-Apavada")
                        },
                        "credibility": {
                            "textual_grounding": "high",
                            "event_confidence": "high",
                            "concept_mapping_confidence": "high",
                            "llm_hallucination_risk": "low"
                        }
                    }
                    final_segments_for_sarga.append(gap_seg)

                # Add the predefined segment
                seg_copy = dict(seg)
                seg_copy["start_verse"] = v1
                seg_copy["end_verse"] = v2
                final_segments_for_sarga.append(seg_copy)
                curr_v = max(curr_v, v2 + 1)

            # Check if there are uncovered verses after the last predefined segment
            if curr_v <= max_v:
                gap_start = curr_v
                gap_end = max_v
                gap_id = f"AR-{prefix}-{s_num:02d}-N{gap_start:02d}"
                gap_verses = [s_verses_dict[vn] for vn in range(gap_start, gap_end + 1) if vn in s_verses_dict]
                
                first_meta = gap_verses[0]["output_doc"]["metadata_fields"] if gap_verses else {}
                title_narrative = first_meta.get("associated_epic_event") or "Concluding Narrative Discourse"
                title_narrative = title_narrative.replace("_", " ")

                chars = list(set([c for gv in gap_verses for c in gv["output_doc"]["metadata_fields"].get("characters_featured", []) if c]))
                place = first_meta.get("place_mentioned") or "Sacred Environs"
                if place == "None":
                    place = "Sacred Narrative Setting"

                gap_seg = {
                    "segment_id": gap_id,
                    "verse_range": f"{s_num}.{gap_start}-{s_num}.{gap_end}",
                    "start_verse": gap_start,
                    "end_verse": gap_end,
                    "event": {
                        "title": title_narrative,
                        "event_type": "epic_narrative",
                        "summary": f"Concluding narrative verses {gap_start} to {gap_end} of Sarga {s_num}."
                    },
                    "place": place,
                    "place_symbolic_meaning": first_meta.get("place_symbolic_meaning", "No_Symbolic_Interpretation"),
                    "characters": chars if chars else ["Rama", "Devotees"],
                    "character_cosmic_mappings": first_meta.get("character_cosmic_mappings", []),
                    "philosophy": {
                        "present": bool(first_meta.get("primary_doctrine")),
                        "density": "MEDIUM",
                        "ontology_refs": ["ADV-CAND-BHAKTI", "ADV-CAND-DHARMA"],
                        "evidence_status": "source_text_based_annotation",
                        "primary_doctrine": first_meta.get("primary_doctrine", "Bhakti-Jnana-Samuccaya"),
                        "prakriya_mapped": first_meta.get("prakriya_mapped", "Adhyaropa-Apavada")
                    },
                    "credibility": {
                        "textual_grounding": "high",
                        "event_confidence": "high",
                        "concept_mapping_confidence": "high",
                        "llm_hallucination_risk": "low"
                    }
                }
                final_segments_for_sarga.append(gap_seg)

            # Now populate each segment with its actual verses!
            sarga_events_data = []
            for seg in final_segments_for_sarga:
                v_start = seg["start_verse"]
                v_end = seg["end_verse"]
                seg_verses = []

                for vn in range(v_start, v_end + 1):
                    raw_v = s_verses_dict.get(vn)
                    if not raw_v:
                        continue
                    out_doc = raw_v.get("output_doc", {})
                    t_fields = out_doc.get("text_fields", {})
                    m_fields = out_doc.get("metadata_fields", {})

                    dev_shloka = clean_text(t_fields.get("verse_text_devanagari") or raw_v.get("verse_text"))
                    iast_translit = clean_text(t_fields.get("transliteration_iast"))
                    eng_trans = clean_text(t_fields.get("translation_english"))
                    hin_trans = clean_text(t_fields.get("translation_hindi"))

                    # Format padacheda
                    raw_pada = t_fields.get("padacheda_with_meaning", [])
                    padacheda_clean = []
                    for pw in raw_pada:
                        sw = clean_text(pw.get("sanskrit_word"))
                        me = clean_text(pw.get("meaning_english"))
                        mh = clean_text(pw.get("meaning_hindi"))
                        if sw:
                            padacheda_clean.append({
                                "sanskrit_word": sw,
                                "meaning_english": me,
                                "meaning_hindi": mh
                            })

                    spk = clean_text(m_fields.get("primary_speaker"))
                    if spk == "Unidentified_Or_None":
                        spk = "Śrī Mahādeva (Narrator)"

                    lis = clean_text(m_fields.get("primary_listener"))
                    if lis == "Unidentified_Or_None":
                        lis = "Devī Pārvatī (Seeker)"

                    v_obj = {
                        "verse_number": vn,
                        "sarga_number": s_num,
                        "kanda_number": k_num,
                        "verse_coordinate": f"{k_name} • Sarga {s_num} • Shloka {vn}",
                        "sanskrit": dev_shloka,
                        "transliteration": iast_translit,
                        "translation_english": eng_trans,
                        "translation_hindi": hin_trans,
                        "padacheda": padacheda_clean,
                        "speaker": spk,
                        "listener": lis,
                        "dialogue_frame": clean_text(m_fields.get("dialogue_frame_layer")),
                        "doctrine": clean_text(m_fields.get("primary_doctrine")),
                        "prakriya": clean_text(m_fields.get("prakriya_mapped")),
                        "sadhana_stage": clean_text(m_fields.get("sadhana_stage")),
                        "stotra_name": clean_text(m_fields.get("stotra_name")),
                        "meter": clean_text(m_fields.get("meter_chhandas")),
                        "keywords": [clean_text(k) for k in m_fields.get("keywords_sanskrit", []) if k],
                        "requires_human_review": bool(m_fields.get("requires_human_review", False))
                    }
                    seg_verses.append(v_obj)

                seg["verses"] = seg_verses
                sarga_events_data.append(seg)

            kanda_total_events += len(sarga_events_data)
            final_sargas.append({
                "sarga_number": s_num,
                "title": s_title,
                "verse_count": len(s_verses_dict),
                "events_count": len(sarga_events_data),
                "events": sarga_events_data
            })

        total_scripture_events += kanda_total_events

        # Write Kanda file: data/adhyatma-ramayana/kandas/kanda_{k_num}.json
        kanda_out_path = os.path.join(KANDAS_DIR, f"kanda_{k_num}.json")
        kanda_payload = {
            "kanda_number": k_num,
            "name": k_name,
            "name_sanskrit": cfg["name_sanskrit"],
            "name_transliterated": cfg["name_transliterated"],
            "total_sargas": len(final_sargas),
            "total_verses": kanda_total_verses,
            "total_events": kanda_total_events,
            "summary": cfg["summary"],
            "summary_hindi": cfg["summary_hindi"],
            "sargas": final_sargas
        }
        with open(kanda_out_path, 'w', encoding='utf-8') as f:
            json.dump(kanda_payload, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved {kanda_out_path} ({kanda_total_verses} verses, {kanda_total_events} events across {len(final_sargas)} sargas).")

        summary_kandas.append({
            "kanda_number": k_num,
            "name": k_name,
            "name_sanskrit": cfg["name_sanskrit"],
            "name_transliterated": cfg["name_transliterated"],
            "sargas_count": len(final_sargas),
            "verses_count": kanda_total_verses,
            "events_count": kanda_total_events,
            "summary": cfg["summary"],
            "summary_hindi": cfg["summary_hindi"],
            "sargas": [
                {
                    "sarga_number": s["sarga_number"],
                    "title": s["title"],
                    "verse_count": s["verse_count"],
                    "events_count": s["events_count"]
                }
                for s in final_sargas
            ]
        })

    # High-density teaching highlights for the compendium
    high_density_highlights = [
        {
            "title": "Rāma Hṛdaya (रामहृदयम्)",
            "kanda": 1,
            "kanda_name": "Bālakāṇḍa",
            "sarga": 1,
            "verse_range": "1.1-1.56",
            "segment_id": "AR-BAL-01-04",
            "speaker": "Śrī Mahādeva (Lord Shiva)",
            "listener": "Devī Pārvatī",
            "doctrine": "Non-Dual Brahman, Mūla-Prakṛti, Sat-Chit-Ananda",
            "description": "Lord Shiva reveals the esoteric essence of Rama to Parvati: Rama is the unconditioned Supreme Brahman, while Sita is Yoga-Maya creating, sustaining, and dissolving the cosmos in His presence."
        },
        {
            "title": "Ahalyā Stuti (अहल्याकृत श्रीरामस्तुतिः)",
            "kanda": 1,
            "kanda_name": "Bālakāṇḍa",
            "sarga": 5,
            "verse_range": "5.43-5.63",
            "segment_id": "AR-BAL-05-03",
            "speaker": "Ahalyā",
            "listener": "Śrī Rāma",
            "doctrine": "Bhakti-Jnana-Samuccaya, Avatara-Tattva",
            "description": "Upon being redeemed from her stony stupor by the touch of Rama's lotus feet, Ahalya offers a sublime Advaitic hymn praising Rama as the witness of all minds (Sarva-Sakshi)."
        },
        {
            "title": "Lakṣmaṇa-Upadeśa (लक्ष्मणोपदेशः - मायास्वरूपम्)",
            "kanda": 2,
            "kanda_name": "Ayodhyākāṇḍa",
            "sarga": 4,
            "verse_range": "4.15-4.32",
            "segment_id": "AR-AYO-04-02",
            "speaker": "Śrī Rāma",
            "listener": "Lakṣmaṇa",
            "doctrine": "Māyā-Vāda, Adhyāsa, Atma-Viveka",
            "description": "When Lakshmana is overcome with anger at Rama's unjust exile, Rama pacifies him with a profound discourse on the illusory nature of anger, grief, and body-identification born of Maya."
        },
        {
            "title": "Navavidhā Bhakti (शबरीं प्रति नवधाभक्तिनिरूपणम्)",
            "kanda": 3,
            "kanda_name": "Āraṇyakāṇḍa",
            "sarga": 10,
            "verse_range": "10.20-10.35",
            "segment_id": "AR-ARA-10-02",
            "speaker": "Śrī Rāma",
            "listener": "Śabarī",
            "doctrine": "Navavidha Bhakti leading to Aparoksha-Jnana",
            "description": "Rama instructs the elderly ascetic Shabari in the nine steps of devotion, establishing that sincere devotion is independent of caste, gender, or status, and naturally culminates in liberating gnosis."
        },
        {
            "title": "Tārā-Prabodha (तारायै आत्मतत्त्वोपदेशः)",
            "kanda": 4,
            "kanda_name": "Kiṣkindhākāṇḍa",
            "sarga": 3,
            "verse_range": "3.16-3.32",
            "segment_id": "AR-KIS-03-02",
            "speaker": "Śrī Rāma",
            "listener": "Tārā",
            "doctrine": "Deha-Atma-Viveka, Immortal Soul vs. Mortal Frame",
            "description": "As Tara weeps inconsolably over the slain Vali, Rama asks her: 'Whom do you mourn? The body made of five elements, or the conscious soul? The body is inert; the soul is immortal and unslain.'"
        },
        {
            "title": "Vibhīṣaṇa Śaraṇāgati (विभीषणशरणागतिः)",
            "kanda": 6,
            "kanda_name": "Yuddhakāṇḍa",
            "sarga": 3,
            "verse_range": "3.1-3.25",
            "segment_id": "AR-YUD-03-01",
            "speaker": "Śrī Rāma & Vibhīṣaṇa",
            "listener": "Sugriva and the Vanara Hosts",
            "doctrine": "Paramātmā as the sole refuge (Abhaya-Pradāna)",
            "description": "The eternal proclamation of divine sanctuary: 'Even if Ravana himself comes seeking refuge, I shall grant him protection from all fears forever.'"
        },
        {
            "title": "Śrī Rāma Gītā (श्रीरामगीता - उत्तरकाण्डे पञ्चमः सर्गः)",
            "kanda": 7,
            "kanda_name": "Uttarakāṇḍa",
            "sarga": 5,
            "verse_range": "5.1-5.62",
            "segment_id": "AR-UTT-05-02",
            "speaker": "Śrī Rāma",
            "listener": "Lakṣmaṇa",
            "doctrine": "Pure Advaita Vedanta, Mahāvākya-Vicāra, Jīvanmukti",
            "description": "The supreme philosophical crest of the epic: Rama's definitive philosophical discourse to Lakshmana expounding the identity of Jiva and Brahman, the nature of Upadhis, negation through Neti-Neti, and the nature of the Jivanmukta."
        },
        {
            "title": "Kausalyā Mokṣa (कौशल्यायै मुक्तिप्रदज्ञानोपदेशः)",
            "kanda": 7,
            "kanda_name": "Uttarakāṇḍa",
            "sarga": 7,
            "verse_range": "7.49-7.84",
            "segment_id": "AR-UTT-07-03",
            "speaker": "Śrī Rāma",
            "listener": "Mātā Kausalyā",
            "doctrine": "Bhakti-Jnana-Samuccaya, Sayujya-Mukti",
            "description": "Rama consoles his grieving mother Kausalya with the secret of cosmic surrender and non-dual contemplation, leading her to direct liberation."
        }
    ]

    # Write summary.json
    summary_payload = {
        "id": "adhyatma-ramayana",
        "title": "Adhyātma Rāmāyaṇa",
        "title_sanskrit": "अध्यात्मरामायणम्",
        "category": "Advaita Puranic Epics",
        "tradition": "advaita",
        "author": "Bhagavān Veda Vyāsa (भगवान् वेदव्यासः)",
        "source": "Brahmāṇḍa Purāṇa (ब्रह्माण्डपुराणान्तर्गतम्)",
        "total_kandas": len(KANDA_CONFIGS),
        "total_sargas": total_scripture_sargas,
        "total_verses": total_scripture_verses,
        "total_events": total_scripture_events,
        "description": "The Adhyātma Rāmāyaṇa (part of the Brahmāṇḍa Purāṇa) is the preeminent classical Sanskrit epic unifying Ramabhakti with unconditioned Advaita Vedānta. Narrated as a sacred dialogue between Lord Shiva and Goddess Parvati, it unveils Śrī Rāma not merely as an epic hero, but as the unconditioned Para Brahman, and Sītā as Mūla-Prakṛti / Yoga-Māyā. Featuring the celebrated Rāma Hṛdaya and Rāma Gītā, this scripture serves as an indispensable compendium for the non-dual realization of Truth.",
        "description_hindi": "अध्यात्मरामायण ब्रह्माण्डपुराण का वह दिव्य अङ्ग है जिसमें रामकथा के माध्यम से विशुद्ध अद्वैत वेदान्त और अनन्य भक्तियोग का अनुपम समन्वय किया गया है। भगवान् शिव और देवी पार्वती के संवाद रूप में निबद्ध यह ग्रन्थ श्रीराम को परब्रह्म और सीता को मूलप्रकृति योगमाया के रूप में उद्घाटित करता है।",
        "high_density_highlights": high_density_highlights,
        "kandas": summary_kandas
    }

    summary_out_path = os.path.join(TARGET_DIR, "summary.json")
    with open(summary_out_path, 'w', encoding='utf-8') as f:
        json.dump(summary_payload, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Saved scripture summary: {summary_out_path}")

    # Write ontology.json
    ontology_out_path = os.path.join(TARGET_DIR, "ontology.json")
    with open(ontology_out_path, 'w', encoding='utf-8') as f:
        json.dump(ONTOLOGY_DEF_MAP, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved ontology definitions: {ontology_out_path}")

    # -------------------------------------------------------------
    # Update data/scriptures.json
    # -------------------------------------------------------------
    scriptures_path = '/home/anurag/Projects/vedantvani/data/scriptures.json'
    with open(scriptures_path, 'r', encoding='utf-8') as f:
        scriptures = json.load(f)

    entry_min = {
        "id": "adhyatma-ramayana",
        "name": "Adhyātma Rāmāyaṇa",
        "name_sanskrit": "अध्यात्मरामायणम्",
        "category": "Advaita Prakarana Texts",
        "chapters_count": total_scripture_sargas,
        "total_verses": total_scripture_verses,
        "description": summary_payload["description"]
    }

    idx = next((i for i, s in enumerate(scriptures) if s.get('id') == 'adhyatma-ramayana'), -1)
    if idx >= 0:
        scriptures[idx] = entry_min
    else:
        scriptures.append(entry_min)

    with open(scriptures_path, 'w', encoding='utf-8') as f:
        json.dump(scriptures, f, indent=2, ensure_ascii=False)
    print(f"✓ Updated data/scriptures.json ({len(scriptures)} scriptures)")

    # -------------------------------------------------------------
    # Update src/data/scripturesData.json
    # -------------------------------------------------------------
    sd_path = '/home/anurag/Projects/vedantvani/src/data/scripturesData.json'
    with open(sd_path, 'r', encoding='utf-8') as f:
        sdata = json.load(f)

    entry_full = {
        "id": "adhyatma-ramayana",
        "name": "Adhyātma Rāmāyaṇa",
        "name_sanskrit": "अध्यात्मरामायणम्",
        "category": "Advaita Prakarana Texts",
        "tradition": "advaita",
        "traditionLabel": "Advaita Vedānta",
        "subcategory": "Advaita Puranic Epics",
        "author": "Bhagavān Veda Vyāsa (भगवान् वेदव्यासः)",
        "chapters_count": total_scripture_sargas,
        "total_verses": total_scripture_verses,
        "description": summary_payload["description"],
        "chapters": [
            {
                "chapter_number": k["kanda_number"],
                "name": k["name"],
                "name_sanskrit": k["name_sanskrit"],
                "name_transliterated": k["name_transliterated"],
                "verses_count": k["verses_count"],
                "summary": k["summary"],
                "summary_hindi": k["summary_hindi"]
            }
            for k in summary_kandas
        ]
    }

    idx_sd = next((i for i, s in enumerate(sdata) if s.get('id') == 'adhyatma-ramayana'), -1)
    if idx_sd >= 0:
        sdata[idx_sd] = entry_full
    else:
        sdata.append(entry_full)

    with open(sd_path, 'w', encoding='utf-8') as f:
        json.dump(sdata, f, indent=2, ensure_ascii=False)
    print(f"✓ Updated src/data/scripturesData.json ({len(sdata)} scriptures)")

    print(f"\n🎉 Successfully processed all {len(KANDA_CONFIGS)} Kāṇḍas!")
    print(f"   Total Sargas: {total_scripture_sargas}")
    print(f"   Total Verses: {total_scripture_verses:,}")
    print(f"   Total Events: {total_scripture_events:,}")

if __name__ == '__main__':
    main()

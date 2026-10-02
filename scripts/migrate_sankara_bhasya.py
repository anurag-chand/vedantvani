import zipfile
import json
import os
import re
from indic_transliteration import sanscript

ZIP_PATH = '/home/anurag/Projects/Mega Datahub/shlokam/Research/sankara_bhasya_verified_manageable_app.zip'
BASE_DIR = '/home/anurag/Projects/vedantvani'
PUBLIC_DATA = os.path.join(BASE_DIR, 'public/data')

def normalize_sk(text):
    if not text:
        return ""
    return re.sub(r'[\s\u0964\u0965\.\,\-\:\;\|\!\?\'\"0-9०-९]', '', text)

def to_iast(text):
    if not text:
        return ""
    try:
        return sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
    except Exception:
        return text

print("1. Opening zip archive...")
with zipfile.ZipFile(ZIP_PATH) as z:
    with z.open('corpus.json') as f:
        corpus = json.load(f)
    with z.open('mula_wordmap.json') as f:
        wordmap = json.load(f)

# 2. Index existing translations from current upanishads
print("2. Indexing existing translations...")
existing_translations = {} # (scrip_slug, norm_sk) -> (tr_text, tr_list)
existing_by_num = {} # (scrip_slug, c_num, v_num) -> (tr_text, tr_list)

for scrip_dir in os.listdir(PUBLIC_DATA):
    if not scrip_dir.startswith('upanishad-'):
        continue
    ch_dir = os.path.join(PUBLIC_DATA, scrip_dir, 'chapters')
    if not os.path.exists(ch_dir):
        continue
    for fname in os.listdir(ch_dir):
        if not fname.endswith('.json'):
            continue
        try:
            with open(os.path.join(ch_dir, fname), 'r', encoding='utf-8') as cf:
                data = json.load(cf)
                for item in data:
                    tr = item.get('translation', '')
                    trs = item.get('translations', [])
                    shloka = item.get('sanskrit_shloka', '')
                    norm = normalize_sk(shloka)
                    meta = item.get('metadata', {})
                    c_num = meta.get('chapter_number')
                    v_num = meta.get('verse_number')
                    if tr or trs:
                        if norm:
                            existing_translations[(scrip_dir, norm)] = (tr, trs)
                        if c_num and v_num:
                            existing_by_num[(scrip_dir, c_num, v_num)] = (tr, trs)
        except Exception:
            pass

print(f"Indexed {len(existing_translations)} existing translations by shloka.")

# Chapter name definitions
BS_PADA_NAMES = [
    ("Adhyāya 1, Pāda 1: Samanvaya", "समन्वयाध्यायः • प्रथमः पादः", "Inquiry into Brahman & Vedic Concordance (includes Adhyāsa Bhāṣya)"),
    ("Adhyāya 1, Pāda 2: Samanvaya", "समन्वयाध्यायः • द्वितीयः पादः", "Clear Marks of Brahman as the Object of Upāsanā"),
    ("Adhyāya 1, Pāda 3: Samanvaya", "समन्वयाध्यायः • तृतीयः पादः", "Clear Marks of Brahman as Supreme Object of Knowledge"),
    ("Adhyāya 1, Pāda 4: Samanvaya", "समन्वयाध्यायः • चतुर्थः पादः", "Resolution of Ambiguous Passages & Avyakta"),
    ("Adhyāya 2, Pāda 1: Avirodha", "अविरोधाध्यायः • प्रथमः पादः", "Refutation of Sāṅkhya & Yoga Objections (Smṛti-Avirodha)"),
    ("Adhyāya 2, Pāda 2: Avirodha", "अविरोधाध्यायः • द्वितीयः पादः", "Tarka Pāda: Refutation of Atomism, Buddhism & Jainism"),
    ("Adhyāya 2, Pāda 3: Avirodha", "अविरोधाध्यायः • तृतीयः पादः", "Origin of Elements (Ākāśa, etc.) and Nature of the Jīva"),
    ("Adhyāya 2, Pāda 4: Avirodha", "अविरोधाध्यायः • चतुर्थः पादः", "Origin and Nature of Prāṇas and Sense Organs"),
    ("Adhyāya 3, Pāda 1: Sādhana", "साधनाध्यायः • प्रथमः पादः", "Transmigration of the Soul & Cultivation of Dispassion (Vairāgya)"),
    ("Adhyāya 3, Pāda 2: Sādhana", "साधनाध्यायः • द्वितीयः पादः", "Analysis of Dream, Deep Sleep & Nature of Nirguṇa Brahman"),
    ("Adhyāya 3, Pāda 3: Sādhana", "साधनाध्यायः • तृतीयः पादः", "Guṇopasaṃhāra: Synthesis of Upaniṣadic Meditations"),
    ("Adhyāya 3, Pāda 4: Sādhana", "साधनाध्यायः • चतुर्थः पादः", "Jñāna as Independent Means to Liberation (Puruṣārtha)"),
    ("Adhyāya 4, Pāda 1: Phala", "फलाध्यायः • प्रथमः पादः", "Repetition of Contemplation & Destruction of Karma"),
    ("Adhyāya 4, Pāda 2: Phala", "फलाध्यायः • द्वितीयः पादः", "Departure of the Prāṇas at Death (Utkrānti)"),
    ("Adhyāya 4, Pāda 3: Phala", "फलाध्यायः • तृतीयः पादः", "The Solar Path of the Gods (Devayāna)"),
    ("Adhyāya 4, Pāda 4: Phala", "फलाध्यायः • चतुर्थः पादः", "State of Final Liberation (Mukti) & Cosmic Freedom")
]

AITAREYA_CH_NAMES = [
    ("Adhyāya 1: Creation of Cosmos", "प्रथमोऽध्यायः", "Creation of the universe, cosmic guardians, and entry of the Supreme Self"),
    ("Adhyāya 2: Three Births of the Soul", "द्वितीयोऽध्यायः", "The three stages/births of the transmigrating jīva and Sage Vāmadeva's realization"),
    ("Adhyāya 3: Prajñānaṃ Brahma", "तृतीयोऽध्यायः", "The great declaration: Consciousness is Brahman (Prajñānaṃ Brahma)")
]

MANDUKYA_CH_NAMES = [
    ("Prakaraṇa 1: Āgama Prakaraṇa", "आगमप्रकरणम्", "Māṇḍūkya Upaniṣad mantras with Gauḍapāda Kārikās on the Four Pādas of Aum"),
    ("Prakaraṇa 2: Vaitathya Prakaraṇa", "वैतथ्यप्रकरणम्", "Demonstration of the unreality/illusory nature of the phenomenal world"),
    ("Prakaraṇa 3: Advaita Prakaraṇa", "अद्वैतप्रकरणम्", "Exposition of Non-Duality through the analogy of space (Ghaṭākāśa)"),
    ("Prakaraṇa 4: Alātaśānti Prakaraṇa", "अलातशान्तिप्रकरणम्", "Quenching of the firebrand: Dialectical refutation of causation (Ajātivāda)")
]

TAITIRIYA_CH_NAMES = [
    ("Chapter 1: Śīkṣāvallī", "शीक्षावल्ली", "On phonetics, sacred discipline, and ethical exhortation (Satyaṃ vada, Dharmaṃ cara)"),
    ("Chapter 2: Brahmānandavallī", "ब्रह्मानन्दवल्ली", "The Five Kośas (Annamaya to Ānandamaya) and the infinite bliss of Brahman"),
    ("Chapter 3: Bhṛguvallī", "भृगुवल्ली", "The step-by-step inquiry of Sage Bhṛgu guided by Varuṇa to realize Brahman as Bliss")
]

MUNDAKA_CH_NAMES = [
    ("Muṇḍaka 1: Aparā & Parā Vidyā", "प्रथमं मुण्डकम्", "The distinction between lower empirical ritualism and higher Brahmavidyā"),
    ("Muṇḍaka 2: Origin from Brahman", "द्वितीयं मुण्डकम्", "All beings emerge from Akṣara Brahman like sparks from blazing fire"),
    ("Muṇḍaka 3: The Two Birds & Truth", "तृतीयं मुण्डकम्", "Dvā suparṇā (two birds on one tree), Satyameva Jayate, and Supreme Liberation")
]

KATHA_CH_NAMES = [
    ("Adhyāya 1 (Vallīs 1-3)", "प्रथमोऽध्यायः", "Nachiketa's three boons from Yama, dialogue on immortality, and the Chariot allegory"),
    ("Adhyāya 2 (Vallīs 4-6)", "द्वितीयोऽध्यायः", "The inward-turned senses, the Eternal Aśvattha tree, and final yoga of dissolution")
]

PRASHNA_CH_NAMES = [
    ("Question 1: Origin of Beings", "प्रथमः प्रश्नः", "Kabandhī's query to Pippalāda on the origin of creation through Prāṇa and Rayi"),
    ("Question 2: Glory of Prāṇa", "द्वितीयः प्रश्नः", "Bhārgava Vaidarbhi's query on the senses and the supreme sustainer Prāṇa"),
    ("Question 3: Nature of Prāṇa", "तृतीयः प्रश्नः", "Kausalya's query on the fivefold division and functioning of vital Prāṇa"),
    ("Question 4: Dream and Deep Sleep", "चतुर्थः प्रश्नः", "Sauryāyaṇī Gārgya's query on sleep, dreams, and the witnessing Self"),
    ("Question 5: Meditation on Om", "पञ्चमः प्रश्नः", "Satyakāma's query on meditation upon the sacred syllable Om with three mātrās"),
    ("Question 6: Sixteen Kalās", "षष्ठः प्रश्नः", "Sukeśā Bhāradvāja's query on the Puruṣa with sixteen limbs/kalās")
]

# Helper to process a work
def process_work(work_slug, target_slug, scrip_name, ch_count, split_mode='default'):
    print(f"\n---> Processing {work_slug} -> {target_slug}...")
    work = [w for w in corpus['works'] if w['slug'] == work_slug][0]
    wm = wordmap.get(work_slug, {})
    items = work['items']

    target_dir = os.path.join(PUBLIC_DATA, target_slug)
    chapters_dir = os.path.join(target_dir, 'chapters')
    os.makedirs(chapters_dir, exist_ok=True)

    # If BS, split_mode is 'pada16'
    if split_mode == 'pada16':
        # Group into 16 padas
        padas_data = {i: {'pres': [], 'verses': []} for i in range(1, 17)}
        current_adh = 1
        current_pad = 1
        pending_pres = []
        for it in items:
            t = it.get('t')
            if t == 'ch':
                current_adh = it.get('n', current_adh)
            elif t == 'sec':
                current_pad = it.get('n', current_pad)
            elif t == 'pre':
                pending_pres.append(it.get('text', ''))
            elif t == 'v':
                ref = it.get('ref')
                parts = ref.split('.')
                adh = int(parts[0])
                pad = int(parts[1])
                pada_idx = (adh - 1) * 4 + pad
                if pending_pres:
                    padas_data[pada_idx]['pres'].extend(pending_pres)
                    pending_pres = []
                padas_data[pada_idx]['verses'].append(it)

        summary = []
        total_verses = 0
        for p in range(1, 17):
            pada_info = padas_data[p]
            v_list = pada_info['verses']
            total_verses += len(v_list)
            p_name, p_sk, p_sum = BS_PADA_NAMES[p - 1]

            summary.append({
                "chapter_number": p,
                "name": p_name,
                "name_sanskrit": p_sk,
                "name_transliterated": p_name,
                "verses_count": len(v_list),
                "summary": p_sum,
                "summary_hindi": ""
            })

            chapter_verses = []
            for v_idx, v in enumerate(v_list, start=1):
                ref = v['ref'] # e.g. 1.1.1
                shloka = ' '.join(v.get('moola', []))
                translit = to_iast(shloka)

                # Word by word
                wbw_raw = wm.get(ref, [])
                wbw = []
                gloss_words = []
                for w in wbw_raw:
                    wbw.append({
                        "word_sanskrit": w.get('w', ''),
                        "word_english": w.get('m', ''),
                        "grammar_role": w.get('g', ''),
                        "root": w.get('p', '')
                    })
                    if w.get('m'):
                        gloss_words.append(w.get('m'))

                # English translation
                transl_text = " — ".join(gloss_words) if gloss_words else "Sutra aphorism."
                translations = [{
                    "author": "Canonical English Gloss",
                    "language": "english",
                    "text": transl_text
                }]

                # Bhāṣya text
                bhasya_paras = []
                # If first verse of pada and there are preambles:
                if v_idx == 1 and pada_info['pres']:
                    pre_title = "【अध्यासभाष्यम् - उपोद्घातः】\n" if p == 1 else "【पादपीठा / उपोद्घातः】\n"
                    bhasya_paras.append(pre_title + "\n\n".join(pada_info['pres']))

                if v.get('pre'):
                    bhasya_paras.append("【अवतरणिका】\n" + "\n\n".join(v['pre']))

                if v.get('body'):
                    bhasya_paras.append("\n\n".join(b['t'] for b in v['body']))

                full_bhasya = "\n\n".join(bhasya_paras)

                commentaries = [{
                    "author": "Adi Shankaracharya Bhashya",
                    "school": "Advaita Vedanta",
                    "language": "sanskrit",
                    "text": full_bhasya
                }]

                v_obj = {
                    "id": f"brahmasutra_{p}_{v_idx}",
                    "metadata": {
                        "scripture_name": "Brahma Sutras",
                        "scripture_slug": "brahmasutra",
                        "chapter_slug": f"chapter-{p}",
                        "chapter_name": p_name,
                        "verse_number": v_idx,
                        "chapter_number": p,
                        "sutra_ref": ref,
                        "source_url": ""
                    },
                    "section_title": p_name,
                    "sanskrit_shloka": shloka,
                    "transliteration": translit,
                    "translation": transl_text,
                    "word_by_word": wbw,
                    "translations": translations,
                    "commentaries": commentaries,
                    "commentary_faqs": []
                }
                chapter_verses.append(v_obj)

            with open(os.path.join(chapters_dir, f'chapter_{p}.json'), 'w', encoding='utf-8') as cf:
                json.dump(chapter_verses, cf, ensure_ascii=False, indent=2)

        with open(os.path.join(target_dir, 'summary.json'), 'w', encoding='utf-8') as sf:
            json.dump(summary, sf, ensure_ascii=False, indent=2)

        print(f"Generated {len(summary)} chapters for {target_slug} ({total_verses} sutras total)")
        return summary, total_verses

    # Normal Upanishads
    # Group items by chapter
    chapters_data = {ch: {'pres': [], 'verses': []} for ch in range(1, ch_count + 1)}
    current_ch = 1
    current_sec_name = ""
    pending_pres = []

    for it in items:
        t = it.get('t')
        if t == 'ch':
            current_ch = it.get('n', current_ch)
        elif t == 'sec':
            current_sec_name = it.get('name', '')
        elif t == 'pre':
            pending_pres.append(it.get('text', ''))
        elif t == 'v':
            ref = it.get('ref')
            ch_num = int(ref.split('.')[0])
            if ch_num not in chapters_data:
                chapters_data[ch_num] = {'pres': [], 'verses': []}
            if pending_pres:
                chapters_data[ch_num]['pres'].extend(pending_pres)
                pending_pres = []
            it['sec_title'] = current_sec_name
            chapters_data[ch_num]['verses'].append(it)

    summary = []
    total_verses = 0

    for ch in range(1, ch_count + 1):
        ch_info = chapters_data.get(ch, {'pres': [], 'verses': []})
        v_list = ch_info['verses']
        total_verses += len(v_list)

        # Get chapter names
        ch_name = f"Chapter {ch}"
        ch_sk = ""
        ch_sum = f"Chapter {ch} of {scrip_name} containing {len(v_list)} verses."

        if target_slug == 'upanishad-isha':
            ch_name = "Īśāvāsya Upaniṣad"
            ch_sk = "ईशावास्योपनिषद्"
            ch_sum = "The complete 18 mantras of the Isha Upanishad with Adi Shankara's Bhashya."
        elif target_slug == 'upanishad-aitareya' and ch <= len(AITAREYA_CH_NAMES):
            ch_name, ch_sk, ch_sum = AITAREYA_CH_NAMES[ch - 1]
        elif target_slug == 'upanishad-mandukya' and ch <= len(MANDUKYA_CH_NAMES):
            ch_name, ch_sk, ch_sum = MANDUKYA_CH_NAMES[ch - 1]
        elif target_slug == 'upanishad-taitiriya' and ch <= len(TAITIRIYA_CH_NAMES):
            ch_name, ch_sk, ch_sum = TAITIRIYA_CH_NAMES[ch - 1]
        elif target_slug == 'upanishad-mundaka' and ch <= len(MANDUKYA_CH_NAMES):
            if ch <= len(MUNDAKA_CH_NAMES):
                ch_name, ch_sk, ch_sum = MUNDAKA_CH_NAMES[ch - 1]
        elif target_slug == 'upanishad-kathaka' and ch <= len(KATHA_CH_NAMES):
            ch_name, ch_sk, ch_sum = KATHA_CH_NAMES[ch - 1]
        elif target_slug == 'upanishad-prashna' and ch <= len(PRASHNA_CH_NAMES):
            ch_name, ch_sk, ch_sum = PRASHNA_CH_NAMES[ch - 1]
        elif target_slug in ('upanishad-kena-pada', 'upanishad-kena-vakya'):
            ch_name = f"Khaṇḍa {ch}"
            ch_sk = f"खण्डः {ch}"
            ch_sum = f"Khaṇḍa {ch} of Kena Upanishad ({'Pada' if 'pada' in target_slug else 'Vakya'} Bhashya)."
        elif target_slug == 'upanishad-chandogya':
            ch_name = f"Prapāṭhaka {ch}"
            ch_sk = f"प्रपाठकः {ch}"
            ch_sum = f"Prapāṭhaka {ch} of the Chandogya Upanishad containing {len(v_list)} mantras."
        elif target_slug == 'upanishad-brha':
            ch_name = f"Adhyāya {ch}"
            ch_sk = f"अध्यायः {ch}"
            ch_sum = f"Adhyāya {ch} of the Brihadaranyaka Upanishad containing {len(v_list)} mantras."

        summary.append({
            "chapter_number": ch,
            "name": ch_name,
            "name_sanskrit": ch_sk,
            "name_transliterated": ch_name,
            "verses_count": len(v_list),
            "summary": ch_sum,
            "summary_hindi": ""
        })

        chapter_verses = []
        for v_idx, v in enumerate(v_list, start=1):
            ref = v['ref'] # e.g. 1.1 or 1.1.1
            shloka = ' '.join(v.get('moola', []))
            translit = to_iast(shloka)
            norm_sk = normalize_sk(shloka)

            # Check existing translation
            tr_text = ""
            tr_list = []
            if (target_slug, norm_sk) in existing_translations:
                tr_text, tr_list = existing_translations[(target_slug, norm_sk)]
            elif (target_slug, ch, v_idx) in existing_by_num:
                tr_text, tr_list = existing_by_num[(target_slug, ch, v_idx)]

            # Word by word
            # For Mandukya, check label first
            wm_key = v.get('label') or ref
            if work_slug == 'Mandukya' and wm_key not in wm:
                wm_key = ref
            wbw_raw = wm.get(wm_key, [])
            wbw = []
            gloss_words = []
            for w in wbw_raw:
                wbw.append({
                    "word_sanskrit": w.get('w', ''),
                    "word_english": w.get('m', ''),
                    "grammar_role": w.get('g', ''),
                    "root": w.get('p', '')
                })
                if w.get('m'):
                    gloss_words.append(w.get('m'))

            if not tr_text:
                if gloss_words:
                    tr_text = " — ".join(gloss_words)
                    tr_list = [{
                        "author": "Canonical English Gloss",
                        "language": "english",
                        "text": tr_text
                    }]
                else:
                    tr_text = "Mantra of the Upanishad."
                    tr_list = [{
                        "author": "Traditional",
                        "language": "english",
                        "text": tr_text
                    }]

            # Bhashya text
            bhasya_paras = []
            if v_idx == 1 and ch_info['pres']:
                bhasya_paras.append("【उपोद्घातभाष्यम्】\n" + "\n\n".join(ch_info['pres']))

            if v.get('pre'):
                bhasya_paras.append("【अवतरणिका】\n" + "\n\n".join(v['pre']))

            if v.get('body'):
                bhasya_paras.append("\n\n".join(b['t'] for b in v['body']))

            full_bhasya = "\n\n".join(bhasya_paras)

            commentaries = []
            if full_bhasya.strip():
                comm_name = "Adi Shankaracharya Bhashya"
                if "pada" in target_slug:
                    comm_name = "Adi Shankaracharya (Pada Bhashya)"
                elif "vakya" in target_slug:
                    comm_name = "Adi Shankaracharya (Vakya Bhashya)"
                commentaries.append({
                    "author": comm_name,
                    "school": "Advaita Vedanta",
                    "language": "sanskrit",
                    "text": full_bhasya
                })

            sec_title = v.get('sec_title', '')
            if not sec_title:
                sec_title = ch_name

            v_obj = {
                "id": f"{target_slug}_{ch}_{v_idx}",
                "metadata": {
                    "scripture_name": scrip_name,
                    "scripture_slug": target_slug,
                    "chapter_slug": f"chapter-{ch}",
                    "chapter_name": ch_name,
                    "verse_number": v_idx,
                    "chapter_number": ch,
                    "mantra_ref": ref,
                    "source_url": ""
                },
                "section_title": sec_title,
                "sanskrit_shloka": shloka,
                "transliteration": translit,
                "translation": tr_text,
                "word_by_word": wbw,
                "translations": tr_list,
                "commentaries": commentaries,
                "commentary_faqs": []
            }
            chapter_verses.append(v_obj)

        with open(os.path.join(chapters_dir, f'chapter_{ch}.json'), 'w', encoding='utf-8') as cf:
            json.dump(chapter_verses, cf, ensure_ascii=False, indent=2)

    with open(os.path.join(target_dir, 'summary.json'), 'w', encoding='utf-8') as sf:
        json.dump(summary, sf, ensure_ascii=False, indent=2)

    print(f"Generated {len(summary)} chapters for {target_slug} ({total_verses} verses total)")
    return summary, total_verses

# Process all 12 works (excluding Gita which is enriched in place)
scrip_registry_updates = {}

summary_bs, count_bs = process_work('BS', 'brahmasutra', 'Brahma Sutras', 16, split_mode='pada16')
scrip_registry_updates['brahmasutra'] = (summary_bs, count_bs)

summary_isha, count_isha = process_work('Isha', 'upanishad-isha', 'Isha Upanishad', 1)
scrip_registry_updates['upanishad-isha'] = (summary_isha, count_isha)

summary_aitareya, count_aitareya = process_work('Aitareya', 'upanishad-aitareya', 'Aitareya Upanishad', 3)
scrip_registry_updates['upanishad-aitareya'] = (summary_aitareya, count_aitareya)

summary_kathaka, count_kathaka = process_work('Kathaka', 'upanishad-kathaka', 'Katha Upanishad', 2)
scrip_registry_updates['upanishad-kathaka'] = (summary_kathaka, count_kathaka)

summary_prashna, count_prashna = process_work('Prashna', 'upanishad-prashna', 'Prashna Upanishad', 6)
scrip_registry_updates['upanishad-prashna'] = (summary_prashna, count_prashna)

summary_mundaka, count_mundaka = process_work('Mundaka', 'upanishad-mundaka', 'Mundaka Upanishad', 3)
scrip_registry_updates['upanishad-mundaka'] = (summary_mundaka, count_mundaka)

summary_mandukya, count_mandukya = process_work('Mandukya', 'upanishad-mandukya', 'Mandukya Upanishad', 4)
scrip_registry_updates['upanishad-mandukya'] = (summary_mandukya, count_mandukya)

summary_taitiriya, count_taitiriya = process_work('Taitiriya', 'upanishad-taitiriya', 'Taittiriya Upanishad', 3)
scrip_registry_updates['upanishad-taitiriya'] = (summary_taitiriya, count_taitiriya)

summary_chandogya, count_chandogya = process_work('Chandogya', 'upanishad-chandogya', 'Chandogya Upanishad', 8)
scrip_registry_updates['upanishad-chandogya'] = (summary_chandogya, count_chandogya)

summary_brha, count_brha = process_work('Brha', 'upanishad-brha', 'Brihadaranyaka Upanishad', 6)
scrip_registry_updates['upanishad-brha'] = (summary_brha, count_brha)

summary_kp, count_kp = process_work('Kena_pada', 'upanishad-kena-pada', 'Kena Upanishad (Pada Bhashya)', 4)
scrip_registry_updates['upanishad-kena-pada'] = (summary_kp, count_kp)

summary_kv, count_kv = process_work('Kena_vakya', 'upanishad-kena-vakya', 'Kena Upanishad (Vakya Bhashya)', 4)
scrip_registry_updates['upanishad-kena-vakya'] = (summary_kv, count_kv)

# 3. Enrich Bhagavad Gita
print("\n---> Enriching Bhagavad Gita with wordmap...")
gita_wm = wordmap.get('Gita', {})
gita_dir = os.path.join(PUBLIC_DATA, 'bhagavad-gita', 'chapters')
for ch in range(1, 19):
    cfpath = os.path.join(gita_dir, f'chapter_{ch}.json')
    if not os.path.exists(cfpath):
        continue
    with open(cfpath, 'r', encoding='utf-8') as cf:
        verses = json.load(cf)

    for v in verses:
        v_num = v.get('metadata', {}).get('verse_number')
        # If verse 1 of Ch 13 is Arjuna's extra verse, skip or keep
        ref = f"{ch}.{v_num}"
        if ch == 13 and v_num > 1:
            ref = f"{ch}.{v_num - 1}"
        elif ch == 13 and v_num == 1:
            continue

        if ref in gita_wm:
            wbw = []
            for w in gita_wm[ref]:
                wbw.append({
                    "word_sanskrit": w.get('w', ''),
                    "word_english": w.get('m', ''),
                    "grammar_role": w.get('g', ''),
                    "root": w.get('p', '')
                })
            v['word_by_word'] = wbw

    with open(cfpath, 'w', encoding='utf-8') as cf:
        json.dump(verses, cf, ensure_ascii=False, indent=2)

print("Bhagavad Gita enriched successfully!")


# 🕉️ VedāntVāṇī (वेदान्त वाणी)
### *Next-Generation Astro Scriptural Explorer & Vedāntic Study Sanctuary*

**VedāntVāṇī** is a modern, high-performance static web application built with the **Astro framework** and tailored with a **mobile-first design**. It houses **36 canonical scriptures** across the foundational traditions of Sanātana Dharma: **Advaita Vedānta**, **Itihāsas**, **Purāṇas**, and **Yoga**.

Live URLs:
👉 **[https://vedantvani.pages.dev/](https://vedantvani.pages.dev/)**
👉 **[https://vedantvani.qzz.io/](https://vedantvani.qzz.io/)**

---

## 🌟 Architecture & Traditions

VedāntVāṇī features dedicated hub pages for each sacred tradition alongside individual reader pages for all 29 texts:

### 1. 🕉️ [Advaita Vedānta](/advaita-vedanta) (`/advaita-vedanta`)
Dedicated page exploring the supreme non-dual truth codified by Adi Shankaracharya:
* **9 Major Mukhya Upaniṣads** with Adi Shankaracharya's Bhashya (*Māṇḍūkya, Chāndogya, Bṛhadāraṇyaka, Kaṭha, Muṇḍaka, Praśna, Taittirīya, Kena Pada, Kena Vākya*).
* **17 Prakaraṇa Granthas** (*Vivekacūḍāmaṇi, Aṣṭāvakra Gītā, Ātmabodha, Aparokṣānubhūti, Upadeśa Sāram, Tattvabodha, Śataślokī, Daśaślokī, Hastāmalaka Stotram, Kaupīna Pañcakam, Manīṣā Pañcakam, Nyāyarakṣāmaṇi, Saddarśanam, Sādhanā Pañcakam, Brahma Jñānavālī Mālā, Vākya Vṛtti*).
* Filter between Mukhya Upanishads and Prakaranas with one tap.

### 2. ⚔️ [Itihāsas](/itihasas) (`/itihasas`)
Dedicated page exploring the epic dialogue of the Mahabharata:
* **The Complete 18 Chapters of Srimad Bhagavad Gītā** (701 Verses).
* Interactive chapter explorer with Sanskrit titles, verse counts, and chapter summaries.
* The 4 Yogas: *Karma Yoga, Dhyāna Yoga, Bhakti Yoga, and Jñāna Yoga*.
* Exegesis across 4 classical schools: *Advaita (Shankaracharya), Viśiṣṭādvaita (Ramanujacharya), Dvaita (Madhavacharya), and Śuddhādvaita (Vallabhacharya)*.

### 3. 🔱 [Purāṇas & Sacred Hymns](/puranas) (`/puranas`)
Dedicated page for Puranic literature, Vedic liturgical hymns, and cosmology:
* **Śrī Rudram (Rudra Praśna)**: 169 mantras spanning Namakam and Chamakam from the Krishna Yajurveda Taittirīya Saṁhitā.
* **The 18 Mahāpurāṇas**: Comprehensive classification into Sāttvika (Vishnu), Rājasa (Brahma/Shakti), and Tāmasa (Shiva) traditions.
* Exposition of the 5 Characteristics of a Purana (*Pañcalakṣaṇa*).

### 4. 🧘 [Yoga Scriptures](/yoga) (`/yoga`)
Dedicated page for the science of meditation, mind-stilling, and liberation:
* **Patañjali Yoga Sūtras**: 205 aphorisms across the 4 Pādas (*Samādhi, Sādhana, Vibhūti, Kaivalya*).
* **8 Classical Commentaries** (Vyāsa Bhāṣya, Rājāmārtāṇḍa, Tattva Vaiśāradī, Yoga Sudhākara) in Sanskrit and Hindi.
* **Authentic Audio Chanting Recitation** integrated directly into the reader.
* Interactive guide to the 8 Limbs of Classical Yoga (*Aṣṭāṅga Yoga*) and the 5 Mental Modifications (*Pañca-Vṛttayaḥ*).
* Architectural pipeline ready for upcoming Yoga treatises (Haṭha Yoga Pradīpikā, Gheraṇḍa Saṁhitā, Śiva Saṁhitā, Yoga Vāsiṣṭha).

### 5. 📚 [All Scriptures Library](/scriptures) (`/scriptures`)
Searchable and filterable master catalog of all 29 canonical scriptures with live search and category chips.

### 6. 📖 Dedicated Scripture Reader (`/read/[scripture]`)
Every single one of the 29 scriptures has its own dedicated static route:
* Dynamic chapter selection and verse navigator drawer / bottom sheet.
* High-legibility Sanskrit shlokas rendered in **Noto Serif Devanagari**.
* Precise IAST English transliteration with diacritics.
* Comparative translations and theological commentaries.
* Word-by-word grammatical and root breakdown.
* Dynamic font sizing (`A-` / `A+`) saved to `localStorage`.
* One-click formatted verse copy engine with saffron toast notifications.
* Keyboard shortcuts (← / → for verse navigation, `/` for search).

---

## 📱 Mobile-First Features

* **Ergonomic Bottom Navigation**: Instant thumb access to Home, Advaita, Itihāsas, Purāṇas, and Library.
* **Touch Bottom Sheet**: Fluid slide-up sheet on phones for swift chapter selection and jumping to any verse (1 to N).
* **Bilingual Theming**: Seamless toggle between **Cosmic Void Slate** (Dark) and **Sattvic Ivory** (Light) with zero flash.
* **Vapor-Weight Performance**: On-demand asynchronous chapter payload fetching ensuring sub-50ms paint times.

---

## 🛠️ Local Development & Build

This project is built with **Astro v5** and can be run using Bun, Node, or npm:

```bash
# 1. Install dependencies
bun install
# or: npm install

# 2. Start development server (runs on port 4321)
bun run dev
# or: npm run dev

# 3. Build optimized static output (dist/)
bun run build
# or: npm run build

# 4. Preview static production build
bun run preview
# or: npm run preview
```

---

## 🚀 Deployment (Cloudflare Pages)

The static build is output to `dist/`:

```bash
# Build the Astro site
bun run build

# Deploy to Cloudflare Pages
wrangler pages deploy dist --project-name vedantvani --branch main
```

export interface PrasthanaDailyVerse {
  id: string;
  pillar: 'Śruti Prasthāna' | 'Smṛti Prasthāna' | 'Nyāya Prasthāna';
  pillarSanskrit: string;
  canon: string;
  source: string;
  sanskrit: string;
  transliteration: string;
  translation: string;
  readerUrl: string;
  theme: string;
  icon: string;
}

export const PRASTHANATRAYI_VERSES: PrasthanaDailyVerse[] = [
  // 1. Śruti (Upaniṣads)
  {
    id: 'sruti-isha-1',
    pillar: 'Śruti Prasthāna',
    pillarSanskrit: 'श्रुति प्रस्थान • उपनिषदः',
    canon: 'Upaniṣad',
    source: 'Īśāvāsya Upaniṣad, Mantra 1',
    sanskrit: 'ईशा वास्यमिदं सर्वं यत्किंच जगत्यां जगत् ।\nतेन त्यक्तेन भुञ्जीथा मा गृधः कस्य स्विद्धनम् ॥ १ ॥',
    transliteration: 'īśā vāsyam idaṃ sarvaṃ yatkiñca jagatyāṃ jagat |\ntena tyaktena bhuñjīthā mā gṛdhaḥ kasya sviddhanam || 1 ||',
    translation: 'All this—whatsoever moves in this transient world—is enveloped by the Supreme Lord. By renouncing the unreal, sustain yourself in the Self. Covet not any person’s wealth.',
    readerUrl: '/read/upanishad-isha?c=1&v=1',
    theme: 'Cosmic Pervasion & Renunciation',
    icon: '📜'
  },

  // 2. Smṛti (Bhagavad Gītā)
  {
    id: 'smrti-gita-2-47',
    pillar: 'Smṛti Prasthāna',
    pillarSanskrit: 'स्मृति प्रस्थान • श्रीमद्भगवद्गीता',
    canon: 'Bhagavad Gītā',
    source: 'Śrīmad Bhagavad Gītā 2.47',
    sanskrit: 'कर्मण्येवाधिकारस्ते मा फलेषु कदाचन ।\nमा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि ॥ २.४७ ॥',
    transliteration: 'karmaṇy evādhikāras te mā phaleṣu kadācana |\nmā karmaphalahetur bhūr mā te saṅgo ’stv akarmaṇi || 2.47 ||',
    translation: 'You have an absolute right to perform action alone, never to its fruits. Let not the fruit of action be your motive, nor let there be any attachment to inaction.',
    readerUrl: '/read/bhagavad-gita?c=2&v=47',
    theme: 'Selfless Action (Karmayoga)',
    icon: '🏹'
  },

  // 3. Nyāya (Brahma Sūtras)
  {
    id: 'nyaya-bs-1-1-1',
    pillar: 'Nyāya Prasthāna',
    pillarSanskrit: 'न्याय प्रस्थान • ब्रह्मसूत्राणि',
    canon: 'Brahma Sūtras',
    source: 'Brahma Sūtras 1.1.1',
    sanskrit: 'अथातो ब्रह्मजिज्ञासा ॥ १.१.१ ॥',
    transliteration: 'athāto brahma-jijñāsā || 1.1.1 ||',
    translation: 'Now, therefore, after acquiring the fourfold spiritual prerequisites, begins the profound inquiry into Brahman—the Ultimate Non-Dual Reality.',
    readerUrl: '/read/brahmasutra?c=1&v=1',
    theme: 'The Inception of Self-Inquiry',
    icon: '⚖️'
  },

  // 4. Śruti (Chāndogya)
  {
    id: 'sruti-chandogya-6-8-7',
    pillar: 'Śruti Prasthāna',
    pillarSanskrit: 'श्रुति प्रस्थान • उपनिषदः',
    canon: 'Upaniṣad',
    source: 'Chāndogya Upaniṣad 6.8.7',
    sanskrit: 'स य एषोऽणिमैतदात्म्यमिदं सर्वं तत्सत्यं स आत्मा तत्त्वमसि श्वेतकेतो ॥',
    transliteration: 'sa ya eṣo ’ṇimaitad-ātmyam idaṃ sarvaṃ tat satyaṃ sa ātmā tat tvam asi śvetaketo ||',
    translation: 'That subtle essence which is the source of all existence—that is the sole Reality. That is the Inmost Self. You are That, O Śvetaketu!',
    readerUrl: '/read/upanishad-chandogya?c=6&v=44',
    theme: 'The Supreme Identity (Tat Tvam Asi)',
    icon: '📜'
  },

  // 5. Smṛti (Bhagavad Gītā)
  {
    id: 'smrti-gita-2-20',
    pillar: 'Smṛti Prasthāna',
    pillarSanskrit: 'स्मृति प्रस्थान • श्रीमद्भगवद्गीता',
    canon: 'Bhagavad Gītā',
    source: 'Śrīmad Bhagavad Gītā 2.20',
    sanskrit: 'न जायते म्रियते वा कदाचिन्नायं भूत्वा भविता वा न भूयः ।\nअजो नित्यः शाश्वतोऽयं पुराणो न हन्यते हन्यमाने शरीरे ॥ २.२० ॥',
    transliteration: 'na jāyate mriyate vā kadācin nāyaṃ bhūtvā bhavitā vā na bhūyaḥ |\najo nityaḥ śāśvato ’yaṃ purāṇo na hanyate hanyamāne śarīre || 2.20 ||',
    translation: 'The Self is never born, nor does It ever die; having once been, It does not cease to be. Unborn, eternal, changeless, and primeval, It is not slain when the body is slain.',
    readerUrl: '/read/bhagavad-gita?c=2&v=20',
    theme: 'Immortality of the Ātman',
    icon: '🏹'
  },

  // 6. Nyāya (Brahma Sūtras)
  {
    id: 'nyaya-bs-1-1-2',
    pillar: 'Nyāya Prasthāna',
    pillarSanskrit: 'न्याय प्रस्थान • ब्रह्मसूत्राणि',
    canon: 'Brahma Sūtras',
    source: 'Brahma Sūtras 1.1.2',
    sanskrit: 'जन्माद्यस्य यतः ॥ १.१.२ ॥',
    transliteration: 'janmādyasya yataḥ || 1.1.2 ||',
    translation: 'Brahman is That Supreme Omniscient Source from which the origin, sustenance, and dissolution of this ordered universe proceed.',
    readerUrl: '/read/brahmasutra?c=1&v=2',
    theme: 'Cosmic Cause of Existence',
    icon: '⚖️'
  },

  // 7. Śruti (Māṇḍūkya)
  {
    id: 'sruti-mandukya-7',
    pillar: 'Śruti Prasthāna',
    pillarSanskrit: 'श्रुति प्रस्थान • उपनिषदः',
    canon: 'Upaniṣad',
    source: 'Māṇḍūkya Upaniṣad, Mantra 7',
    sanskrit: 'नान्तःप्रज्ञं न बहिःप्रज्ञं नोभयतःप्रज्ञं न प्रज्ञानघनं न प्रज्ञं नाप्रज्ञम् ।\nअदृश्यमव्यवहार्यमग्राह्यमलक्षणमचिन्त्यमव्यपदेश्यमेकात्मप्रत्ययसारं प्रपञ्चोपशमं शान्तं शिवमद्वैतं चतुर्थं मन्यन्ते स आत्मा स विज्ञेयः ॥ ७ ॥',
    transliteration: 'nāntaḥ-prajñaṃ na bahiḥ-prajñaṃ nobhayataḥ-prajñaṃ na prajñāna-ghanaṃ na prajñaṃ nāprajñam |\nadṛśyam avyavahāryam agrāhyam alakṣaṇam acintyam avyapadeśyam ekātma-pratyaya-sāraṃ prapañcopaśamaṃ śāntaṃ śivam advaitaṃ caturthaṃ manyante sa ātmā sa vijñeyaḥ || 7 ||',
    translation: 'It is neither inner consciousness nor outer, neither dense consciousness nor unconsciousness. Transcending speech, ungraspable, tranquil, auspicious, non-dual—That is the Fourth (Turīya). That is the Self to be realized.',
    readerUrl: '/read/upanishad-mandukya?c=1&v=16',
    theme: 'The Transcendent Fourth (Turīya)',
    icon: '📜'
  },

  // 8. Smṛti (Bhagavad Gītā)
  {
    id: 'smrti-gita-2-70',
    pillar: 'Smṛti Prasthāna',
    pillarSanskrit: 'स्मृति प्रस्थान • श्रीमद्भगवद्गीता',
    canon: 'Bhagavad Gītā',
    source: 'Śrīmad Bhagavad Gītā 2.70',
    sanskrit: 'आपूर्यमाणमचलप्रतिष्ठं समुद्रमापः प्रविशन्ति यद्वत् ।\nतद्वत्कामा यं प्रविशन्ति सर्वे स शान्तिमाप्नोति न कामकामी ॥ २.७० ॥',
    transliteration: 'āpūryamāṇam acala-pratiṣṭhaṃ samudram āpaḥ praviśanti yadvat |\ntadvat kāmā yaṃ praviśanti sarve sa śāntim āpnoti na kāma-kāmī || 2.70 ||',
    translation: 'As all waters enter the ocean, which is filled from all sides yet remains tranquil and unmoved, so all desires enter the realized sage without disturbing him. He alone attains peace.',
    readerUrl: '/read/bhagavad-gita?c=2&v=70',
    theme: 'The Oceanic Equilibrium of Wisdom',
    icon: '🏹'
  },

  // 9. Nyāya (Brahma Sūtras)
  {
    id: 'nyaya-bs-1-1-3',
    pillar: 'Nyāya Prasthāna',
    pillarSanskrit: 'न्याय प्रस्थान • ब्रह्मसूत्राणि',
    canon: 'Brahma Sūtras',
    source: 'Brahma Sūtras 1.1.3',
    sanskrit: 'शास्त्रयोनित्वात् ॥ १.१.३ ॥',
    transliteration: 'śāstra-yonitvāt || 1.1.3 ||',
    translation: 'Because Brahman is the omniscient author of the sacred scriptures, and because sacred revelation alone is the primary means of valid cognition for knowing Brahman.',
    readerUrl: '/read/brahmasutra?c=1&v=3',
    theme: 'Scripture as Pramāṇa',
    icon: '⚖️'
  },

  // 10. Śruti (Taittirīya)
  {
    id: 'sruti-taittiriya-2-1',
    pillar: 'Śruti Prasthāna',
    pillarSanskrit: 'श्रुति प्रस्थान • उपनिषदः',
    canon: 'Upaniṣad',
    source: 'Taittirīya Upaniṣad 2.1',
    sanskrit: 'सत्यं ज्ञानमनन्तं ब्रह्म ।\nयो वेद निहितं गुहायां परमे व्योमन् । सोऽश्नुते सर्वान् कामान् सह । ब्रह्मणा विपश्चितेति ॥',
    transliteration: 'satyaṃ jñānam anantaṃ brahma |\nyo veda nihitaṃ guhāyāṃ parame vyoman | so ’śnute sarvān kāmān saha | brahmaṇā vipaściteti ||',
    translation: 'Brahman is Absolute Reality, Pure Consciousness, and Infinitude. Whoever realizes It enshrined within the supreme cavern of the heart attains all fulfilled desires in unity with Brahman.',
    readerUrl: '/read/upanishad-taitiriya?c=2&v=2',
    theme: 'The Nature of Brahman (Svarūpa Lakṣaṇa)',
    icon: '📜'
  },

  // 11. Smṛti (Bhagavad Gītā)
  {
    id: 'smrti-gita-4-7',
    pillar: 'Smṛti Prasthāna',
    pillarSanskrit: 'स्मृति प्रस्थान • श्रीमद्भगवद्गीता',
    canon: 'Bhagavad Gītā',
    source: 'Śrīmad Bhagavad Gītā 4.7',
    sanskrit: 'यदा यदा हि धर्मस्य ग्लानिर्भवति भारत ।\nअभ्युत्थानमधर्मस्य तदात्मानं सृजाम्यहम् ॥ ४.७ ॥',
    transliteration: 'yadā yadā hi dharmasya glānir bhavati bhārata |\nabhyutthānam adharmasya tadātmānaṃ sṛjāmy aham || 4.7 ||',
    translation: 'Whenever there is a decline of righteousness (Dharma), O Bhārata, and an ascendancy of unrighteousness, at that time I manifest Myself into the manifest world.',
    readerUrl: '/read/bhagavad-gita?c=4&v=7',
    theme: 'Cosmic Descent of the Avatāra',
    icon: '🏹'
  },

  // 12. Nyāya (Brahma Sūtras)
  {
    id: 'nyaya-bs-1-1-4',
    pillar: 'Nyāya Prasthāna',
    pillarSanskrit: 'न्याय प्रस्थान • ब्रह्मसूत्राणि',
    canon: 'Brahma Sūtras',
    source: 'Brahma Sūtras 1.1.4',
    sanskrit: 'तत्तु समन्वयात् ॥ १.१.४ ॥',
    transliteration: 'tat tu samanvayāt || 1.1.4 ||',
    translation: 'That Brahman is indeed the supreme purport of all Vedāntic scriptures, because of the harmonious concordance and unified synthesis running through all sacred texts.',
    readerUrl: '/read/brahmasutra?c=1&v=4',
    theme: 'Harmonious Concordance of Vedānta',
    icon: '⚖️'
  },

  // 13. Śruti (Bṛhadāraṇyaka)
  {
    id: 'sruti-brha-1-4-10',
    pillar: 'Śruti Prasthāna',
    pillarSanskrit: 'श्रुति प्रस्थान • उपनिषदः',
    canon: 'Upaniṣad',
    source: 'Bṛhadāraṇyaka Upaniṣad 1.4.10',
    sanskrit: 'ब्रह्म वा इदमग्र आसीत्तदात्मानमेवावेत् ।\nअहं ब्रह्मास्मीति । तस्मात्तत्सर्वमभवत् ॥',
    transliteration: 'brahma vā idam agra āsīt tad ātmānam evāvet |\nahaṃ brahmāsmīti | tasmāt tat sarvam abhavat ||',
    translation: 'In the beginning this universe was Brahman alone. It recognized Itself as: ‘I am Brahman (Ahaṃ Brahmāsmi)’. Through that supreme realization, It became the All.',
    readerUrl: '/read/upanishad-brha?c=1&v=47',
    theme: 'The Supreme Realization (Ahaṃ Brahmāsmi)',
    icon: '📜'
  },

  // 14. Smṛti (Bhagavad Gītā)
  {
    id: 'smrti-gita-7-7',
    pillar: 'Smṛti Prasthāna',
    pillarSanskrit: 'स्मृति प्रस्थान • श्रीमद्भगवद्गीता',
    canon: 'Bhagavad Gītā',
    source: 'Śrīmad Bhagavad Gītā 7.7',
    sanskrit: 'मत्तः परतरं नान्यत्किञ्चिदस्ति धनञ्जय ।\nमयि सर्वमिदं प्रोतं सूत्रे मणिगणा इव ॥ ७.७ ॥',
    transliteration: 'mattaḥ parataraṃ nānyat kiñcid asti dhanañjaya |\nmayi sarvam idaṃ protaṃ sūtre maṇi-gaṇā iva || 7.7 ||',
    translation: 'There is nothing higher than Me, O Arjuna. The entirety of this cosmos is woven upon Me, just as pearls are strung upon a celestial thread.',
    readerUrl: '/read/bhagavad-gita?c=7&v=7',
    theme: 'The All-Sustaining Ground of Being',
    icon: '🏹'
  },

  // 15. Nyāya (Brahma Sūtras)
  {
    id: 'nyaya-bs-1-1-12',
    pillar: 'Nyāya Prasthāna',
    pillarSanskrit: 'न्याय प्रस्थान • ब्रह्मसूत्राणि',
    canon: 'Brahma Sūtras',
    source: 'Brahma Sūtras 1.1.12',
    sanskrit: 'आनन्दमयोऽभ्यासात् ॥ १.१.१२ ॥',
    transliteration: 'ānandamayo ’bhyāsāt || 1.1.12 ||',
    translation: 'The Ānandamaya (Sheath of Bliss) refers to the Supreme Self, on account of the repeated scriptural proclamation of unconditional Bliss as Brahman’s essence.',
    readerUrl: '/read/brahmasutra?c=1&v=12',
    theme: 'Brahman as Infinite Bliss (Ānanda)',
    icon: '⚖️'
  },

  // 16. Śruti (Kaṭha)
  {
    id: 'sruti-katha-1-2-20',
    pillar: 'Śruti Prasthāna',
    pillarSanskrit: 'श्रुति प्रस्थान • उपनिषदः',
    canon: 'Upaniṣad',
    source: 'Kaṭha Upaniṣad 1.2.20',
    sanskrit: 'अणोरणीयान्महतो महीयानात्मास्य जन्तोर्निहितो गुहायाम् ।\nतमक्रतुः पश्यति वीतशोको धातुप्रसादान्महिमानमात्मनः ॥ २० ॥',
    transliteration: 'aṇor aṇīyān mahato mahīyān ātmāsya jantor nihito guhāyām |\ntam akratuḥ paśyati vītaśoko dhātuprasādān mahimānam ātmanaḥ || 20 ||',
    translation: 'Subtler than the subtle, greater than the greatest, the Ātman dwells in the cave of the heart of each living being. The desireless person, through tranquility of the mind, beholds that glory and becomes free from sorrow.',
    readerUrl: '/read/upanishad-kathaka?c=1&v=49',
    theme: 'The Inmost Heart of Reality',
    icon: '📜'
  },

  // 17. Smṛti (Bhagavad Gītā)
  {
    id: 'smrti-gita-9-22',
    pillar: 'Smṛti Prasthāna',
    pillarSanskrit: 'स्मृति प्रस्थान • श्रीमद्भगवद्गीता',
    canon: 'Bhagavad Gītā',
    source: 'Śrīmad Bhagavad Gītā 9.22',
    sanskrit: 'अनन्याश्चिन्तयन्तो मां ये जनाः पर्युपासते ।\nतेषां नित्याभियुक्तानां योगक्षेमं वहाम्यहम् ॥ ९.२२ ॥',
    transliteration: 'ananyāś cintayanto māṃ ye janāḥ paryupāsate |\nteṣāṃ nityābhiyuktānāṃ yoga-kṣemaṃ vahāmy aham || 9.22 ||',
    translation: 'Those who contemplate Me with single-minded devotion, worshiping without distraction—to those steadfast seekers, I personally provide and protect all that they need.',
    readerUrl: '/read/bhagavad-gita?c=9&v=22',
    theme: 'Devotional Assurance & Divine Care',
    icon: '🏹'
  },

  // 18. Nyāya (Brahma Sūtras)
  {
    id: 'nyaya-bs-2-1-14',
    pillar: 'Nyāya Prasthāna',
    pillarSanskrit: 'न्याय प्रस्थान • ब्रह्मसूत्राणि',
    canon: 'Brahma Sūtras',
    source: 'Brahma Sūtras 2.1.14',
    sanskrit: 'तदनन्यत्वमारम्भणशब्दादिभ्यः ॥ २.१.१४ ॥',
    transliteration: 'tad-ananyatvam ārambhaṇa-śabdādibhyaḥ || 2.1.14 ||',
    translation: 'The non-difference between the effect (the world) and its ultimate cause (Brahman) is established from Vedic passages such as those beginning with ‘vākya-ārambhaṇa’.',
    readerUrl: '/read/brahmasutra?c=5&v=14',
    theme: 'Non-Duality of Cause and Effect',
    icon: '⚖️'
  },

  // 19. Śruti (Muṇḍaka)
  {
    id: 'sruti-mundaka-3-1-6',
    pillar: 'Śruti Prasthāna',
    pillarSanskrit: 'श्रुति प्रस्थान • उपनिषदः',
    canon: 'Upaniṣad',
    source: 'Muṇḍaka Upaniṣad 3.1.6',
    sanskrit: 'सत्यमेव जयते नानृतं सत्येन पन्था विततो देवयानः ।\nयेनाक्रमन्त्यृषयो ह्याप्तकामा यत्र तत्सत्यस्य परमं निधानम् ॥ ६ ॥',
    transliteration: 'satyameva jayate nānṛtaṃ satyena panthā vitato devayānaḥ |\nyenākramanty ṛṣayo hy āptakāmā yatra tat satyasya paramaṃ nidhānam || 6 ||',
    translation: 'Truth alone triumphs, never falsehood. By Truth the divine path is unfolded, by which illumined seers whose aspirations are fulfilled journey to that Supreme Treasure of Truth.',
    readerUrl: '/read/upanishad-mundaka?c=3&v=6',
    theme: 'Satyameva Jayate (Victory of Truth)',
    icon: '📜'
  },

  // 20. Smṛti (Bhagavad Gītā)
  {
    id: 'smrti-gita-18-66',
    pillar: 'Smṛti Prasthāna',
    pillarSanskrit: 'स्मृति प्रस्थान • श्रीमद्भगवद्गीता',
    canon: 'Bhagavad Gītā',
    source: 'Śrīmad Bhagavad Gītā 18.66',
    sanskrit: 'सर्वधर्मान्परित्यज्य मामेकं शरणं व्रज ।\nअहं त्वां सर्वपापेभ्यो मोक्षयिष्यामि मा शुचः ॥ १८.६६ ॥',
    transliteration: 'sarva-dharmān parityajya mām ekaṃ śaraṇaṃ vraja |\nahaṃ tvāṃ sarva-pāpebhyo mokṣayiṣyāmi mā śucaḥ || 18.66 ||',
    translation: 'Renouncing all duties and relative dharmas, take refuge in Me alone. I shall release you from all bondages and impurities. Grieve not.',
    readerUrl: '/read/bhagavad-gita?c=18&v=66',
    theme: 'The Ultimate Surrender (Carama Śloka)',
    icon: '🏹'
  },

  // 21. Nyāya (Brahma Sūtras)
  {
    id: 'nyaya-bs-3-2-22',
    pillar: 'Nyāya Prasthāna',
    pillarSanskrit: 'न्याय प्रस्थान • ब्रह्मसूत्राणि',
    canon: 'Brahma Sūtras',
    source: 'Brahma Sūtras 3.2.22',
    sanskrit: 'प्रकृतैतावत्त्वं हि प्रतिषेधति ततो ब्रवीति च भूयः ॥ ३.२.२२ ॥',
    transliteration: 'prakṛtaitāvattvaṃ hi pratiṣedhati tato bravīti ca bhūyaḥ || 3.2.22 ||',
    translation: 'The negation ‘Neti, Neti’ (Not this, Not this) denies only that Brahman is limited to finite forms; thereafter scripture declares Brahman as the infinite ground of all.',
    readerUrl: '/read/brahmasutra?c=10&v=22',
    theme: 'Neti Neti — The Transcendence of Brahman',
    icon: '⚖️'
  }
];

/**
 * Returns the deterministic verse of the day based on the calendar day.
 */
export function getVerseOfTheDay(date: Date = new Date()): PrasthanaDailyVerse {
  const year = date.getUTCFullYear();
  const start = new Date(Date.UTC(year, 0, 0));
  const diff = date.getTime() - start.getTime();
  const oneDay = 1000 * 60 * 60 * 24;
  const dayOfYear = Math.floor(diff / oneDay);
  const index = Math.abs(dayOfYear) % PRASTHANATRAYI_VERSES.length;
  return PRASTHANATRAYI_VERSES[index];
}

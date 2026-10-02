import scripturesJson from './scripturesData.json';

export interface ChapterMeta {
  chapter_number: number;
  name: string;
  name_sanskrit: string;
  name_transliterated: string;
  verses_count: number;
  summary: string;
  summary_hindi: string;
}

export interface Scripture {
  id: string;
  name: string;
  name_sanskrit: string;
  category: string;
  tradition: 'advaita' | 'itihasa' | 'purana' | 'yoga';
  traditionLabel: string;
  subcategory: string;
  author: string;
  chapters_count: number;
  total_verses: number;
  description: string;
  chapters: ChapterMeta[];
}

export const scriptures: Scripture[] = scripturesJson as Scripture[];

export const TRADITIONS = [
  {
    id: 'advaita',
    slug: 'advaita-vedanta',
    name: 'Advaita Vedānta',
    sanskrit: 'अद्वैत वेदान्त',
    subtitle: 'The Non-Dual Ultimate Reality',
    description: 'Explore the supreme wisdom of the Upanishads and the foundational Prakarana Granthas expounded by Adi Shankaracharya and illumined masters.',
    icon: '🕉️',
    gradient: 'from-amber-500/20 via-orange-500/10 to-transparent',
    color: '#f26f22',
    count: scriptures.filter(s => s.tradition === 'advaita').length,
    verses: scriptures.filter(s => s.tradition === 'advaita').reduce((acc, s) => acc + s.total_verses, 0)
  },
  {
    id: 'itihasa',
    slug: 'itihasas',
    name: 'Itihāsas (Epics)',
    sanskrit: 'इतिहास',
    subtitle: 'The Song of the Supreme Lord',
    description: 'The monumental discourse between Bhagavan Sri Krishna and Arjuna on the battlefield of Kurukshetra — complete with 18 chapters and traditional commentaries.',
    icon: '⚔️',
    gradient: 'from-orange-500/20 via-amber-500/10 to-transparent',
    color: '#d4af37',
    count: scriptures.filter(s => s.tradition === 'itihasa').length,
    verses: scriptures.filter(s => s.tradition === 'itihasa').reduce((acc, s) => acc + s.total_verses, 0)
  },
  {
    id: 'purana',
    slug: 'puranas',
    name: 'Purāṇas & Hymns',
    sanskrit: 'पुराणानि व स्तोत्राणि',
    subtitle: 'Cosmic Chants & Sacred Lore',
    description: 'Immerse in the timeless vibration of Sri Rudram from the Krishna Yajurveda and the devotional narrative wisdom of the Mahāpurāṇas.',
    icon: '🔱',
    gradient: 'from-yellow-500/20 via-orange-500/10 to-transparent',
    color: '#e5a93b',
    count: scriptures.filter(s => s.tradition === 'purana').length,
    verses: scriptures.filter(s => s.tradition === 'purana').reduce((acc, s) => acc + s.total_verses, 0)
  },
  {
    id: 'yoga',
    slug: 'yoga',
    name: 'Yoga Scriptures',
    sanskrit: 'योग शास्त्राणि',
    subtitle: 'The Science of Meditation & Liberation',
    description: 'Master the classical maps of mind-control, meditative absorption (Samādhi), and spiritual emancipation across the Patañjali Yoga Sūtras and yogic texts.',
    icon: '🧘',
    gradient: 'from-emerald-500/20 via-teal-500/10 to-transparent',
    color: '#10b981',
    count: scriptures.filter(s => s.tradition === 'yoga').length,
    verses: scriptures.filter(s => s.tradition === 'yoga').reduce((acc, s) => acc + s.total_verses, 0)
  }
];

export function getAllScriptures(): Scripture[] {
  return scriptures;
}

export function getScriptureById(id: string): Scripture | undefined {
  return scriptures.find(s => s.id === id);
}

export function getScripturesByTradition(tradition: 'advaita' | 'itihasa' | 'purana' | 'yoga'): Scripture[] {
  return scriptures.filter(s => s.tradition === tradition);
}

export function getFeaturedScriptures(): Scripture[] {
  const featuredIds = [
    'bhagavad-gita',
    'brahmasutra',
    'upanishad-mandukya',
    'prakarana-vivekachudamani',
    'yogasutras',
    'prakarana-ashtavakra-gita'
  ];
  return scriptures.filter(s => featuredIds.includes(s.id));
}

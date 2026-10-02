/**
 * Unified Dictionary Service for VedāntVāṇī
 * Queries 132,466 terms across:
 * - 95,585 terms in Śāṅkara Bhāṣya (bhasya_dictionary)
 * - 36,881 terms in original Mūla verses & sūtras (mula_analysis)
 * Supported via Cloudflare Worker D1 API with automatic static shard fallback.
 */

export interface BhasyaEntry {
  source?: 'bhasya' | 'mula';
  surface: string;
  padaccheda: string;
  grammar: string;
  meaning_en: string;
  confidence?: string;
  meaning_bn?: string;
  work_slug?: string;
  unit_key?: string;
}

// In-memory cache for fast repeat lookups
const memoryCache = new Map<string, BhasyaEntry | null>();
const shardCache = new Map<string, Record<string, any>>();

// Roman to Devanagari transliteration map
const ROMAN_TO_DEVA: Record<string, string> = {
  'a': 'अ', 'aa': 'आ', 'ā': 'आ', 'i': 'इ', 'ii': 'ई', 'ī': 'ई',
  'u': 'उ', 'uu': 'ऊ', 'ū': 'ऊ', 'ri': 'ऋ', 'ṛ': 'ऋ', 'e': 'ए',
  'ai': 'ऐ', 'o': 'ओ', 'au': 'औ', 'am': 'ं', 'aṃ': 'ं', 'ah': 'ः', 'aḥ': 'ः',
  'ka': 'क', 'kha': 'ख', 'ga': 'ग', 'gha': 'घ', 'nga': 'ङ',
  'ca': 'च', 'cha': 'छ', 'ja': 'ज', 'jha': 'झ', 'nya': 'ञ',
  'ta': 'त', 'tha': 'थ', 'da': 'द', 'dha': 'ध', 'na': 'न',
  'pa': 'प', 'pha': 'फ', 'ba': 'ब', 'bha': 'भ', 'ma': 'म',
  'ya': 'य', 'ra': 'र', 'la': 'ल', 'va': 'व',
  'sha': 'श', 'śa': 'श', 'shha': 'ष', 'ṣa': 'ष', 'sa': 'स', 'ha': 'ह'
};

export function toDevanagari(text: string): string {
  if (!text) return '';
  if (/[\u0900-\u097F]/.test(text)) return text;

  let res = text.toLowerCase().trim();
  const keys = Object.keys(ROMAN_TO_DEVA).sort((a, b) => b.length - a.length);
  for (const k of keys) {
    res = res.replaceAll(k, ROMAN_TO_DEVA[k]);
  }
  return res;
}

const BIG_FIRST = new Set(['प', 'स', 'अ', 'व', 'त', 'क', 'न', 'द', 'म', 'य', 'श', 'आ', 'ब', 'ज', 'उ', 'इ', 'भ', 'च', 'ए', 'ग', 'ह', 'र']);

function getShardFilename(term: string): string {
  if (!term) return '';
  const c1 = term[0];
  if (BIG_FIRST.has(c1) && term.length > 1) {
    const c2 = term[1];
    return `u${c1.charCodeAt(0).toString(16).padStart(4, '0')}_u${c2.charCodeAt(0).toString(16).padStart(4, '0')}.json`;
  }
  return `u${c1.charCodeAt(0).toString(16).padStart(4, '0')}.json`;
}

export const DEFAULT_WORKER_URL = 'https://bhashya-dict-worker.anurag-chand88.workers.dev';

export function getWorkerUrl(): string {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('vv_cf_worker_url');
    if (saved !== null) return saved.trim().replace(/\/+$/, '');
  }
  return DEFAULT_WORKER_URL;
}

export function setWorkerUrl(url: string): void {
  if (typeof window !== 'undefined') {
    if (url && url.trim()) {
      localStorage.setItem('vv_cf_worker_url', url.trim());
    } else {
      localStorage.removeItem('vv_cf_worker_url');
    }
  }
}

/**
 * Exact word lookup across Mula and Bhasya
 */
export async function lookupWord(
  rawTerm: string,
  scope: 'all' | 'mula' | 'bhasya' = 'all'
): Promise<BhasyaEntry | null> {
  const term = rawTerm.trim();
  if (!term) return null;

  const cacheKey = `${scope}:${term}`;
  if (memoryCache.has(cacheKey)) {
    return memoryCache.get(cacheKey) || null;
  }

  const workerUrl = getWorkerUrl();

  // 1. Try Cloudflare Worker if URL configured
  if (workerUrl) {
    try {
      const res = await fetch(`${workerUrl}/api/dict/word?term=${encodeURIComponent(term)}&scope=${scope}`);
      if (res.ok) {
        const data = await res.json();
        if (data && data.surface) {
          memoryCache.set(cacheKey, data);
          return data;
        }
      }
    } catch (err) {
      console.warn('Cloudflare Worker request failed, falling back to local shards:', err);
    }
  }

  // 2. Fallback to local static shards
  try {
    const shardFile = getShardFilename(term);
    if (!shardFile) return null;

    let shardData = shardCache.get(shardFile);
    if (!shardData) {
      const res = await fetch(`/data/dict/${shardFile}`);
      if (res.ok) {
        shardData = await res.json();
        shardCache.set(shardFile, shardData!);
      }
    }

    if (shardData && shardData[term]) {
      const raw = shardData[term];
      const entry: BhasyaEntry = {
        source: 'bhasya',
        surface: term,
        padaccheda: raw.p || term,
        grammar: raw.g || '',
        meaning_en: raw.m || '',
        confidence: raw.c || 'h',
        meaning_bn: raw.mb || ''
      };
      memoryCache.set(cacheKey, entry);
      return entry;
    }
  } catch (err) {
    console.error('Local shard lookup error:', err);
  }

  memoryCache.set(cacheKey, null);
  return null;
}

/**
 * Search dictionary across Mula and Bhasya
 */
export async function searchDictionary(
  query: string,
  scope: 'all' | 'mula' | 'bhasya' = 'all',
  category: 'all' | 'noun' | 'verb' | 'avyaya' = 'all',
  limit: number = 30
): Promise<BhasyaEntry[]> {
  const q = query.trim();
  if (!q) return [];

  const workerUrl = getWorkerUrl();

  // 1. If Worker is configured, query Cloudflare D1
  if (workerUrl) {
    try {
      const res = await fetch(
        `${workerUrl}/api/dict/search?q=${encodeURIComponent(q)}&scope=${scope}&category=${category}&limit=${limit}`
      );
      if (res.ok) {
        const results = await res.json();
        if (Array.isArray(results)) {
          return results;
        }
      }
    } catch (err) {
      console.warn('Worker search failed, using local search fallback:', err);
    }
  }

  // 2. Local shard search fallback
  try {
    const devaQ = /[\u0900-\u097F]/.test(q) ? q : toDevanagari(q);
    const shardFile = getShardFilename(devaQ);

    let results: BhasyaEntry[] = [];
    if (shardFile) {
      let shardData = shardCache.get(shardFile);
      if (!shardData) {
        const res = await fetch(`/data/dict/${shardFile}`);
        if (res.ok) {
          shardData = await res.json();
          shardCache.set(shardFile, shardData!);
        }
      }

      if (shardData) {
        for (const [term, val] of Object.entries(shardData)) {
          const mEn = (val.m || '').toLowerCase();
          const p = (val.p || '');
          const g = (val.g || '');

          const matchesQ = term.includes(devaQ) || p.includes(devaQ) || mEn.includes(q.toLowerCase());
          if (!matchesQ) continue;

          if (category === 'avyaya' && !g.includes('अव्यय')) continue;
          if (category === 'verb' && !g.includes('√')) continue;
          if (category === 'noun' && !/[प्रथमा|द्वितीया|तृतीया|चतुर्थी|पञ्चमी|षष्ठी|सप्तमी]/.test(g)) continue;

          results.push({
            source: 'bhasya',
            surface: term,
            padaccheda: val.p || term,
            grammar: val.g || '',
            meaning_en: val.m || '',
            confidence: val.c || 'h',
            meaning_bn: val.mb || ''
          });

          if (results.length >= limit) break;
        }
      }
    }
    return results;
  } catch (err) {
    console.error('Local search error:', err);
    return [];
  }
}

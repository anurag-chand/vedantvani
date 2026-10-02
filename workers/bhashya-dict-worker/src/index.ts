/**
 * Cloudflare Worker: Śāṅkara Bhāṣya & Mūla Complete Lexicon API
 * Fast edge microservice querying 132,466 terms across:
 * - 95,585 terms in Śāṅkara Bhāṣya commentary (bhasya_dictionary)
 * - 36,881 terms in original Mūla verses & sūtras (mula_analysis)
 */

export interface Env {
  DB: D1Database;
}

export interface DictEntry {
  source: 'bhasya' | 'mula';
  surface: string;
  padaccheda: string;
  grammar: string;
  meaning_en: string;
  confidence?: string;
  meaning_bn?: string;
  work_slug?: string;
  unit_key?: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '*';

    // CORS & Cache headers
    const corsHeaders: Record<string, string> = {
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
      'Cache-Control': 'public, max-age=3600, s-maxage=86400',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Health & Info Endpoint
    if (url.pathname === '/' || url.pathname === '/api') {
      return new Response(
        JSON.stringify({
          service: 'Prasthānatrayī Complete Lexicon API',
          version: '2.0.0',
          corpus: 'Śāṅkara Bhāṣya & Canonical Mūla Verses',
          counts: {
            bhasya_terms: 95585,
            mula_terms: 36881,
            total_terms: 132466,
          },
          endpoints: {
            word: '/api/dict/word?term={word}&scope={all|bhasya|mula}',
            search: '/api/dict/search?q={query}&scope={all|bhasya|mula}&category={all|noun|verb|avyaya}&limit=50',
            mula_verse: '/api/dict/mula?work={slug}&ref={ref}',
            suggest: '/api/dict/suggest?prefix={prefix}&limit=10',
          },
        }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      );
    }

    // 1. Mūla Verse Word-by-Word: /api/dict/mula?work=Gita&ref=2.47
    if (url.pathname === '/api/dict/mula') {
      const work = (url.searchParams.get('work') || '').trim();
      const ref = (url.searchParams.get('ref') || '').trim();

      if (!work || !ref) {
        return new Response(JSON.stringify({ error: 'Parameters "work" and "ref" are required' }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      try {
        const stmt = env.DB.prepare(
          'SELECT surface, padaccheda, grammar, meaning_en, confidence, meaning_bn FROM mula_analysis WHERE work_slug = ? AND unit_key = ? ORDER BY id ASC'
        ).bind(work, ref);

        const { results } = await stmt.all();
        return new Response(JSON.stringify(results || []), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      } catch (err: any) {
        return new Response(JSON.stringify({ error: err.message || 'Database error' }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }
    }

    // 2. Unified Word Lookup: /api/dict/word?term=...&scope=all|bhasya|mula
    if (url.pathname === '/api/dict/word') {
      const term = (url.searchParams.get('term') || '').trim();
      const scope = (url.searchParams.get('scope') || 'all').toLowerCase();

      if (!term) {
        return new Response(JSON.stringify({ error: 'Parameter "term" is required' }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      try {
        const foundEntries: DictEntry[] = [];

        // Check Mūla analysis first if scope is 'all' or 'mula'
        if (scope === 'all' || scope === 'mula') {
          const mulaStmt = env.DB.prepare(
            'SELECT work_slug, unit_key, surface, padaccheda, grammar, meaning_en, confidence, meaning_bn FROM mula_analysis WHERE surface = ? OR padaccheda = ? LIMIT 5'
          ).bind(term, term);
          const { results: mResults } = await mulaStmt.all<any>();
          if (mResults && mResults.length > 0) {
            mResults.forEach((r) => {
              foundEntries.push({
                source: 'mula',
                surface: r.surface,
                padaccheda: r.padaccheda,
                grammar: r.grammar,
                meaning_en: r.meaning_en,
                confidence: r.confidence,
                meaning_bn: r.meaning_bn,
                work_slug: r.work_slug,
                unit_key: r.unit_key,
              });
            });
          }
        }

        // Check Bhāṣya dictionary if scope is 'all' or 'bhasya'
        if (scope === 'all' || scope === 'bhasya') {
          const bhasyaStmt = env.DB.prepare(
            'SELECT surface, padaccheda, grammar, meaning_en, confidence, meaning_bn FROM bhasya_dictionary WHERE surface = ? OR padaccheda = ? LIMIT 3'
          ).bind(term, term);
          const { results: bResults } = await bhasyaStmt.all<any>();
          if (bResults && bResults.length > 0) {
            bResults.forEach((r) => {
              foundEntries.push({
                source: 'bhasya',
                surface: r.surface,
                padaccheda: r.padaccheda,
                grammar: r.grammar,
                meaning_en: r.meaning_en,
                confidence: r.confidence,
                meaning_bn: r.meaning_bn,
              });
            });
          }
        }

        return new Response(JSON.stringify(foundEntries[0] || null), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      } catch (err: any) {
        return new Response(JSON.stringify({ error: err.message || 'Lookup error' }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }
    }

    // 3. Search Across Both: /api/dict/search?q=...&scope=all|bhasya|mula&limit=50
    if (url.pathname === '/api/dict/search') {
      const q = (url.searchParams.get('q') || '').trim();
      const scope = (url.searchParams.get('scope') || 'all').toLowerCase();
      const limit = Math.min(parseInt(url.searchParams.get('limit') || '50', 10), 100);
      const category = (url.searchParams.get('category') || 'all').toLowerCase();

      if (!q) {
        return new Response(JSON.stringify([]), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      try {
        let results: DictEntry[] = [];

        // Search Mula
        if (scope === 'all' || scope === 'mula') {
          let mSql = `
            SELECT work_slug, unit_key, surface, padaccheda, grammar, meaning_en, confidence, meaning_bn
            FROM mula_analysis
            WHERE (surface LIKE ?1 OR padaccheda LIKE ?1 OR meaning_en LIKE ?2)
          `;
          if (category === 'avyaya') mSql += " AND grammar LIKE '%अव्यय%'";
          else if (category === 'verb') mSql += " AND grammar LIKE '%√%'";
          else if (category === 'noun') mSql += " AND (grammar LIKE '%प्रथमा%' OR grammar LIKE '%सप्तमी%' OR grammar LIKE '%द्वितीया%')";
          mSql += ' LIMIT ?3';

          const mStmt = env.DB.prepare(mSql).bind(q + '%', '%' + q + '%', Math.ceil(limit / 2));
          const { results: mRes } = await mStmt.all<any>();
          (mRes || []).forEach((r) => {
            results.push({
              source: 'mula',
              surface: r.surface,
              padaccheda: r.padaccheda,
              grammar: r.grammar,
              meaning_en: r.meaning_en,
              confidence: r.confidence,
              meaning_bn: r.meaning_bn,
              work_slug: r.work_slug,
              unit_key: r.unit_key,
            });
          });
        }

        // Search Bhasya
        if (scope === 'all' || scope === 'bhasya') {
          let bSql = `
            SELECT surface, padaccheda, grammar, meaning_en, confidence, meaning_bn
            FROM bhasya_dictionary
            WHERE (surface LIKE ?1 OR padaccheda LIKE ?1 OR meaning_en LIKE ?2)
          `;
          if (category === 'avyaya') bSql += " AND grammar LIKE '%अव्यय%'";
          else if (category === 'verb') bSql += " AND grammar LIKE '%√%'";
          else if (category === 'noun') bSql += " AND (grammar LIKE '%प्रथमा%' OR grammar LIKE '%सप्तमी%' OR grammar LIKE '%द्वितीया%')";
          bSql += ' LIMIT ?3';

          const bStmt = env.DB.prepare(bSql).bind(q + '%', '%' + q + '%', limit - results.length);
          const { results: bRes } = await bStmt.all<any>();
          (bRes || []).forEach((r) => {
            results.push({
              source: 'bhasya',
              surface: r.surface,
              padaccheda: r.padaccheda,
              grammar: r.grammar,
              meaning_en: r.meaning_en,
              confidence: r.confidence,
              meaning_bn: r.meaning_bn,
            });
          });
        }

        return new Response(JSON.stringify(results), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      } catch (err: any) {
        return new Response(JSON.stringify({ error: err.message || 'Search error' }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }
    }

    // 4. Suggestion endpoint
    if (url.pathname === '/api/dict/suggest') {
      const prefix = (url.searchParams.get('prefix') || '').trim();
      const limit = Math.min(parseInt(url.searchParams.get('limit') || '10', 10), 30);

      if (!prefix) {
        return new Response(JSON.stringify([]), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      try {
        const stmt = env.DB.prepare(
          'SELECT DISTINCT surface FROM bhasya_dictionary WHERE surface LIKE ? UNION SELECT DISTINCT surface FROM mula_analysis WHERE surface LIKE ? ORDER BY length(surface) ASC LIMIT ?'
        ).bind(prefix + '%', prefix + '%', limit);

        const { results } = await stmt.all<{ surface: string }>();
        const suggestions = (results || []).map((r) => r.surface);
        return new Response(JSON.stringify(suggestions), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      } catch (err: any) {
        return new Response(JSON.stringify({ error: err.message }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }
    }

    return new Response(JSON.stringify({ error: 'Endpoint not found' }), {
      status: 404,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  },
};

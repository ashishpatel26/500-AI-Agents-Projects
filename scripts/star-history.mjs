#!/usr/bin/env node
/**
 * Generate a star-history SVG from the GitHub API.
 *
 * star-history.com's public API started returning 404/500, which left a broken
 * image in the README. This renders the same chart from data we already own.
 *
 * Reconstructing the curve does not need all N stargazers: asking for
 * `per_page=1&page=N` returns exactly the Nth one, so a few dozen sampled
 * points describe the shape as well as tens of thousands would. That keeps this
 * to ~40 API calls instead of ~350.
 *
 *   GITHUB_TOKEN=... node scripts/star-history.mjs owner/repo images/star-history.svg
 *   node scripts/star-history.mjs --self-check
 */

import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import { pathToFileURL } from 'node:url';

const API = 'https://api.github.com';
const SAMPLES = 40;
const W = 800, H = 400;
const PAD_L = 70, PAD_R = 30, PAD_T = 30, PAD_B = 50;

async function get(url, token, accept = 'application/vnd.github+json') {
  const headers = { Accept: accept, 'User-Agent': 'star-history-generator' };
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(url, { headers });
  if (!res.ok) {
    const err = new Error(`HTTP ${res.status} for ${url}`);
    err.status = res.status;
    throw err;
  }
  return res.json();
}

// Only the stargazers endpoint documents/needs this media type - it's what
// makes starred_at appear in the response. Sending it on other endpoints
// (like /repos/{repo}) is undocumented behaviour we shouldn't rely on.
const STAR_JSON = 'application/vnd.github.star+json';

export async function fetchPoints(repo, token, samples = SAMPLES) {
  const meta = await get(`${API}/repos/${repo}`, token);
  const total = meta.stargazers_count;
  if (!total) return [];

  // Evenly spaced 1-based indices, always including the first and last star.
  let indices;
  if (total <= samples) {
    indices = Array.from({ length: total }, (_, i) => i + 1);
  } else {
    const step = (total - 1) / (samples - 1);
    indices = [...new Set(
      Array.from({ length: samples }, (_, i) => Math.round(1 + i * step))
    )].sort((a, b) => a - b);
  }

  const points = [];
  for (const n of indices) {
    let page;
    try {
      page = await get(`${API}/repos/${repo}/stargazers?per_page=1&page=${n}`, token, STAR_JSON);
    } catch (e) {
      // GitHub caps deep pagination on some endpoints. A gap mid-curve is
      // survivable, so skip rather than abort the whole run.
      console.error(`  skip index ${n}: ${e.message}`);
      continue;
    }
    const at = page?.[0]?.starred_at;
    if (at) points.push([new Date(at), n]);
  }

  points.sort((a, b) => a[0] - b[0]);
  return points;
}

/** Round the axis maximum up to a readable step (1/2/2.5/5 x 10^n). */
export function niceTicks(hi, count = 5) {
  if (hi <= 0) return { ticks: [0], top: 1 };
  const raw = hi / count;
  const mag = 10 ** Math.floor(Math.log10(raw));
  let step = 10 * mag;
  for (const m of [1, 2, 2.5, 5, 10]) {
    if (m * mag >= raw) { step = m * mag; break; }
  }
  const top = Math.round(step * count);
  return { ticks: Array.from({ length: count + 1 }, (_, i) => Math.round(step * i)), top };
}

export function fmt(n) {
  if (n < 1000) return String(n);
  return n % 1000 === 0 ? `${n / 1000}k` : `${(n / 1000).toFixed(1)}k`;
}

const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const monthYear = (d) => `${MONTHS[d.getUTCMonth()]} ${d.getUTCFullYear()}`;

export function renderSvg(points, repo) {
  if (!points.length) {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}"></svg>\n`;
  }

  const t0 = points[0][0], t1 = points[points.length - 1][0];
  const span = Math.max(t1 - t0, 1);
  const { ticks, top } = niceTicks(points[points.length - 1][1]);

  const px = (d) => PAD_L + ((d - t0) / span) * (W - PAD_L - PAD_R);
  const py = (v) => H - PAD_B - (v / top) * (H - PAD_T - PAD_B);

  const line = points.map(([d, v]) => `${px(d).toFixed(1)},${py(v).toFixed(1)}`).join(' ');
  const area = `${PAD_L},${H - PAD_B} ${line} ${px(t1).toFixed(1)},${H - PAD_B}`;

  const grid = ticks.map((t) =>
    `<line x1="${PAD_L}" y1="${py(t).toFixed(1)}" x2="${W - PAD_R}" y2="${py(t).toFixed(1)}" class="grid"/>`
  ).join('\n');

  const ylab = ticks.map((t) =>
    `<text x="${PAD_L - 10}" y="${(py(t) + 4).toFixed(1)}" class="lbl" text-anchor="end">${fmt(t)}</text>`
  ).join('\n');

  const xlab = Array.from({ length: 5 }, (_, i) => {
    const d = new Date(t0.getTime() + (t1 - t0) * (i / 4));
    return `<text x="${px(d).toFixed(1)}" y="${H - PAD_B + 22}" class="lbl" text-anchor="middle">${monthYear(d)}</text>`;
  }).join('\n');

  const stars = points[points.length - 1][1].toLocaleString('en-US');
  const updated = `${new Date().getUTCDate()} ${monthYear(new Date())}`;

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Star history for ${repo}">
<style>
  .bg{fill:#ffffff} .grid{stroke:#d8dee4;stroke-width:1}
  .lbl{fill:#57606a;font:12px -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif}
  .ttl{fill:#1f2328;font:600 14px -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif}
  .ln{fill:none;stroke:#ffc107;stroke-width:2.5;stroke-linejoin:round;stroke-linecap:round}
  .ar{fill:#ffc107;opacity:.15}
  @media (prefers-color-scheme: dark){
    .bg{fill:#0d1117} .grid{stroke:#30363d} .lbl{fill:#8b949e} .ttl{fill:#e6edf3}
  }
</style>
<rect width="${W}" height="${H}" class="bg"/>
${grid}
<polygon points="${area}" class="ar"/>
<polyline points="${line}" class="ln"/>
${ylab}
${xlab}
<text x="${PAD_L}" y="20" class="ttl">${repo} &#183; ${stars} stars</text>
<text x="${W - PAD_R}" y="20" class="lbl" text-anchor="end">updated ${updated}</text>
</svg>
`;
}

/** Smallest thing that fails if the maths breaks. */
function selfCheck() {
  const pts = [
    [new Date('2024-01-01T00:00:00Z'), 1],
    [new Date('2024-06-01T00:00:00Z'), 500],
    [new Date('2025-01-01T00:00:00Z'), 1000],
  ];
  const svg = renderSvg(pts, 'owner/repo');
  const ok = (c, m) => { if (!c) throw new Error(`self-check failed: ${m}`); };

  ok(svg.startsWith('<svg'), 'must emit an svg root');
  ok(svg.includes('1,000 stars'), 'final count must be rendered');
  ok(svg.includes('polyline'), 'curve must be drawn');

  // Monotonic time must map to monotonic x, and stay inside the plot area.
  const xs = svg.match(/<polyline points="([^"]+)"/)[1]
    .split(' ').map((p) => parseFloat(p.split(',')[0]));
  ok(xs.every((x, i) => i === 0 || x >= xs[i - 1]), 'x must increase with time');
  ok(xs.every((x) => x >= PAD_L - 0.5 && x <= W - PAD_R + 0.5), 'curve must stay in frame');

  const ys = svg.match(/<polyline points="([^"]+)"/)[1]
    .split(' ').map((p) => parseFloat(p.split(',')[1]));
  ok(ys.every((y) => y >= PAD_T - 0.5 && y <= H - PAD_B + 0.5), 'curve must stay vertically in frame');

  const { ticks, top } = niceTicks(35133);
  ok(top >= 35133, 'axis must not clip the highest value');
  ok(ticks[0] === 0 && ticks.every((t, i) => i === 0 || t > ticks[i - 1]), 'ticks ascend from zero');

  ok(fmt(1000) === '1k' && fmt(1500) === '1.5k' && fmt(999) === '999', 'number formatting');
  ok(renderSvg([], 'x/y').startsWith('<svg'), 'zero stars must not crash');

  console.log('self-check OK');
}

async function main() {
  if (process.argv.includes('--self-check')) return selfCheck(), 0;

  const repo = process.argv[2] || process.env.GITHUB_REPOSITORY;
  const out = process.argv[3] || 'images/star-history.svg';
  if (!repo) {
    console.error('usage: star-history.mjs owner/repo [out.svg]');
    return 2;
  }

  console.log(`sampling ${repo} ...`);
  const points = await fetchPoints(repo, process.env.GITHUB_TOKEN);
  if (!points.length) {
    console.error('no stargazer data returned');
    return 1;
  }

  mkdirSync(dirname(out) || '.', { recursive: true });
  writeFileSync(out, renderSvg(points, repo), 'utf8');
  console.log(`wrote ${out} from ${points.length} sampled points, ${points[points.length - 1][1]} stars`);
  return 0;
}

// pathToFileURL handles the Windows drive-letter form (file:///d:/...) that
// naive string concatenation gets wrong.
if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.exit(await main());
}

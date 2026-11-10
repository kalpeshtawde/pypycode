/**
 * Post-build step: write dist/<route>.html for the static marketing routes
 * with the correct <title>, meta tags, canonical and JSON-LD baked in.
 *
 * The app is a client-rendered SPA, so without this every route ships the
 * same generic index.html shell. Google renders JS eventually, but Bing,
 * DuckDuckGo, social unfurlers and LLM crawlers largely do not. nginx is
 * configured with `try_files $uri $uri.html /index.html`, so /pricing is
 * served pricing.html when it exists and falls back to the SPA shell
 * otherwise. The React app still hydrates and takes over as normal.
 */
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

import {
  getDefaultMetadata,
  getPricingMetadata,
  getAboutMetadata,
  getContactMetadata,
  getProblemsMetadata,
  getLeaderboardMetadata,
  getTermsMetadata,
  getPrivacyMetadata,
  createOrganizationStructuredData,
  createWebSiteStructuredData,
  createPricingProductStructuredData,
  createFAQStructuredData,
  PRICING_FAQ,
  SITE_NAME,
  type SEOMetadata,
  type StructuredData,
} from "../src/utils/seo";

const DIST = resolve(dirname(fileURLToPath(import.meta.url)), "..", "dist");
const SITE_URL = process.env.VITE_SITE_URL || "https://pypycode.com";
const DEFAULT_IMAGE = `${SITE_URL}/og-image.png`;

type Route = { path: string; file: string; metadata: SEOMetadata; structuredData: StructuredData[] };

const routes: Route[] = [
  {
    path: "/",
    file: "index.html",
    metadata: getDefaultMetadata(),
    structuredData: [createWebSiteStructuredData(), createOrganizationStructuredData()],
  },
  {
    path: "/pricing",
    file: "pricing.html",
    metadata: getPricingMetadata(),
    structuredData: [
      createPricingProductStructuredData({ amount: 30, currency: "usd" }),
      createFAQStructuredData(PRICING_FAQ),
    ],
  },
  { path: "/about", file: "about.html", metadata: getAboutMetadata(), structuredData: [] },
  { path: "/contact", file: "contact.html", metadata: getContactMetadata(), structuredData: [] },
  { path: "/problems", file: "problems.html", metadata: getProblemsMetadata(), structuredData: [] },
  { path: "/leaderboard", file: "leaderboard.html", metadata: getLeaderboardMetadata(), structuredData: [] },
  { path: "/terms", file: "terms.html", metadata: getTermsMetadata(), structuredData: [] },
  { path: "/privacy", file: "privacy.html", metadata: getPrivacyMetadata(), structuredData: [] },
];

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");

function setTag(html: string, pattern: RegExp, replacement: string): string {
  if (!pattern.test(html)) throw new Error(`Tag not found in index.html: ${pattern}`);
  return html.replace(pattern, replacement);
}

function renderHead(template: string, route: Route): string {
  const m = route.metadata;
  const ogTitle = m.ogTitle || m.title;
  const ogDesc = m.ogDescription || m.description;
  const url = m.canonical || SITE_URL;
  let html = template;

  html = setTag(html, /<title>[^<]*<\/title>/, `<title>${esc(m.title)}</title>`);
  html = setTag(html, /<meta name="title" content="[^"]*" \/>/, `<meta name="title" content="${esc(m.title)}" />`);
  html = setTag(html, /<meta name="description" content="[^"]*" \/>/, `<meta name="description" content="${esc(m.description)}" />`);
  if (m.keywords?.length) {
    html = setTag(html, /<meta name="keywords" content="[^"]*" \/>/, `<meta name="keywords" content="${esc(m.keywords.join(", "))}" />`);
  }
  html = setTag(html, /<meta name="robots" content="[^"]*" \/>/, `<meta name="robots" content="${esc(m.robots || "index, follow")}" />`);

  html = setTag(html, /<meta property="og:type" content="[^"]*" \/>/, `<meta property="og:type" content="${esc(m.ogType || "website")}" />`);
  html = setTag(html, /<meta property="og:url" content="[^"]*" \/>/, `<meta property="og:url" content="${esc(url)}" />`);
  html = setTag(html, /<meta property="og:title" content="[^"]*" \/>/, `<meta property="og:title" content="${esc(ogTitle)}" />`);
  html = setTag(html, /<meta property="og:description" content="[^"]*" \/>/, `<meta property="og:description" content="${esc(ogDesc)}" />`);
  html = setTag(html, /<meta property="og:image" content="[^"]*" \/>/, `<meta property="og:image" content="${esc(m.ogImage || DEFAULT_IMAGE)}" />`);
  html = setTag(html, /<meta property="og:site_name" content="[^"]*" \/>/, `<meta property="og:site_name" content="${esc(SITE_NAME)}" />`);

  html = setTag(html, /<meta property="twitter:url" content="[^"]*" \/>/, `<meta property="twitter:url" content="${esc(url)}" />`);
  html = setTag(html, /<meta property="twitter:title" content="[^"]*" \/>/, `<meta property="twitter:title" content="${esc(m.twitterTitle || ogTitle)}" />`);
  html = setTag(html, /<meta property="twitter:description" content="[^"]*" \/>/, `<meta property="twitter:description" content="${esc(m.twitterDescription || ogDesc)}" />`);
  html = setTag(html, /<meta property="twitter:image" content="[^"]*" \/>/, `<meta property="twitter:image" content="${esc(m.twitterImage || DEFAULT_IMAGE)}" />`);

  html = setTag(html, /<link rel="canonical" href="[^"]*" \/>/, `<link rel="canonical" href="${esc(url)}" />`);

  // Match the element ids the runtime uses so React replaces rather than duplicates them.
  const ld = route.structuredData
    .map((block, i) => `<script id="${i === 0 ? "structured-data" : `structured-data-${i}`}" type="application/ld+json">${JSON.stringify(block)}</script>`)
    .join("\n    ");
  if (ld) html = html.replace("</head>", `    ${ld}\n  </head>`);

  return html;
}

const indexPath = resolve(DIST, "index.html");
if (!existsSync(indexPath)) {
  console.error(`prerender-meta: ${indexPath} not found. Run \`vite build\` first.`);
  process.exit(1);
}
const template = readFileSync(indexPath, "utf8");

for (const route of routes) {
  writeFileSync(resolve(DIST, route.file), renderHead(template, route));
  console.log(`prerender-meta: ${route.path.padEnd(13)} -> dist/${route.file}`);
}

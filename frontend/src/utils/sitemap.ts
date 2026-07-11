export interface SitemapUrl {
  loc: string;
  lastmod?: string;
  changefreq?: "always" | "hourly" | "daily" | "weekly" | "monthly" | "yearly" | "never";
  priority?: number;
}

const SITE_URL = "https://pypycode.com";

export const generateSitemapXML = (urls: SitemapUrl[]): string => {
  const xmlHeader = '<?xml version="1.0" encoding="UTF-8"?>';
  const urlsetOpen = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
  const urlsetClose = "</urlset>";

  const urlEntries = urls
    .map(
      (url) => `
  <url>
    <loc>${escapeXml(url.loc)}</loc>
    ${url.lastmod ? `<lastmod>${url.lastmod}</lastmod>` : ""}
    ${url.changefreq ? `<changefreq>${url.changefreq}</changefreq>` : ""}
    ${url.priority !== undefined ? `<priority>${url.priority}</priority>` : ""}
  </url>`
    )
    .join("");

  return `${xmlHeader}\n${urlsetOpen}${urlEntries}\n${urlsetClose}`;
};

export const generateSitemapIndex = (sitemaps: Array<{ loc: string; lastmod?: string }>): string => {
  const xmlHeader = '<?xml version="1.0" encoding="UTF-8"?>';
  const sitemapindexOpen = '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
  const sitemapindexClose = "</sitemapindex>";

  const sitemapEntries = sitemaps
    .map(
      (sitemap) => `
  <sitemap>
    <loc>${escapeXml(sitemap.loc)}</loc>
    ${sitemap.lastmod ? `<lastmod>${sitemap.lastmod}</lastmod>` : ""}
  </sitemap>`
    )
    .join("");

  return `${xmlHeader}\n${sitemapindexOpen}${sitemapEntries}\n${sitemapindexClose}`;
};

export const getStaticSitemapUrls = (): SitemapUrl[] => [
  {
    loc: SITE_URL,
    changefreq: "daily",
    priority: 1.0,
  },
  {
    loc: `${SITE_URL}/problems`,
    changefreq: "daily",
    priority: 0.9,
  },
  {
    loc: `${SITE_URL}/leaderboard`,
    changefreq: "hourly",
    priority: 0.8,
  },
  {
    loc: `${SITE_URL}/pricing`,
    changefreq: "weekly",
    priority: 0.7,
  },
  {
    loc: `${SITE_URL}/about`,
    changefreq: "monthly",
    priority: 0.6,
  },
  {
    loc: `${SITE_URL}/contact`,
    changefreq: "monthly",
    priority: 0.5,
  },
];

export const getProblemSitemapUrls = (problems: Array<{ slug: string; updatedAt?: string }>): SitemapUrl[] => {
  return problems.map((problem) => ({
    loc: `${SITE_URL}/problems/${problem.slug}`,
    lastmod: problem.updatedAt,
    changefreq: "weekly" as const,
    priority: 0.8,
  }));
};

function escapeXml(str: string): string {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

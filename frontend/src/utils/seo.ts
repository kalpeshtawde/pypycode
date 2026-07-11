export interface SEOMetadata {
  title: string;
  description: string;
  keywords?: string[];
  canonical?: string;
  ogTitle?: string;
  ogDescription?: string;
  ogImage?: string;
  ogType?: string;
  twitterCard?: string;
  twitterTitle?: string;
  twitterDescription?: string;
  twitterImage?: string;
  robots?: string;
  author?: string;
  publishedDate?: string;
  modifiedDate?: string;
}

export interface StructuredData {
  "@context": string;
  "@type": string;
  [key: string]: any;
}

const SITE_URL = import.meta.env.VITE_SITE_URL || "https://pypycode.com";
const SITE_NAME = "PyPyCode";
const DEFAULT_IMAGE = `${SITE_URL}/og-image.png`;

export const updateMetaTags = (metadata: SEOMetadata) => {
  // Title
  const titleTag = document.querySelector("title");
  if (titleTag) {
    titleTag.textContent = metadata.title;
  }

  // Meta description
  updateOrCreateMetaTag("description", metadata.description);

  // Keywords
  if (metadata.keywords?.length) {
    updateOrCreateMetaTag("keywords", metadata.keywords.join(", "));
  }

  // Canonical
  if (metadata.canonical) {
    updateOrCreateLinkTag("canonical", metadata.canonical);
  }

  // Open Graph
  updateOrCreateMetaTag("og:title", metadata.ogTitle || metadata.title, "property");
  updateOrCreateMetaTag("og:description", metadata.ogDescription || metadata.description, "property");
  updateOrCreateMetaTag("og:image", metadata.ogImage || DEFAULT_IMAGE, "property");
  updateOrCreateMetaTag("og:type", metadata.ogType || "website", "property");
  updateOrCreateMetaTag("og:site_name", SITE_NAME, "property");
  updateOrCreateMetaTag("og:url", metadata.canonical || SITE_URL, "property");

  // Twitter Card
  updateOrCreateMetaTag("twitter:card", metadata.twitterCard || "summary_large_image");
  updateOrCreateMetaTag("twitter:title", metadata.twitterTitle || metadata.title);
  updateOrCreateMetaTag("twitter:description", metadata.twitterDescription || metadata.description);
  updateOrCreateMetaTag("twitter:image", metadata.twitterImage || DEFAULT_IMAGE);

  // Robots
  if (metadata.robots) {
    updateOrCreateMetaTag("robots", metadata.robots);
  }

  // Author
  if (metadata.author) {
    updateOrCreateMetaTag("author", metadata.author);
  }

  // Article dates
  if (metadata.publishedDate) {
    updateOrCreateMetaTag("article:published_time", metadata.publishedDate, "property");
  }
  if (metadata.modifiedDate) {
    updateOrCreateMetaTag("article:modified_time", metadata.modifiedDate, "property");
  }
};

export const updateStructuredData = (data: StructuredData, id = "structured-data") => {
  let script = document.getElementById(id) as HTMLScriptElement;
  if (!script) {
    script = document.createElement("script");
    script.id = id;
    script.type = "application/ld+json";
    document.head.appendChild(script);
  }
  script.textContent = JSON.stringify(data);
};

export const getDefaultMetadata = (): SEOMetadata => ({
  title: `${SITE_NAME} — Python Challenges`,
  description: "Practice Python. Ship solutions. Climb the ranks. A focused coding platform for Python developers.",
  keywords: ["python", "coding challenges", "leetcode", "algorithms", "practice"],
  canonical: SITE_URL,
  ogType: "website",
});

export const getProblemMetadata = (problem: {
  title: string;
  slug: string;
  difficulty: string;
  description?: string;
}): SEOMetadata => ({
  title: `${problem.title} | ${SITE_NAME}`,
  description: problem.description
    ? problem.description.substring(0, 160)
    : `Solve ${problem.title} on ${SITE_NAME}. Difficulty: ${problem.difficulty}`,
  keywords: [problem.title, problem.difficulty, "python", "algorithm", "coding challenge"],
  canonical: `${SITE_URL}/problems/${problem.slug}`,
  ogTitle: `${problem.title} | ${SITE_NAME}`,
  ogDescription: `Solve ${problem.title} on ${SITE_NAME}`,
  ogType: "article",
});

export const getLeaderboardMetadata = (): SEOMetadata => ({
  title: `Leaderboard | ${SITE_NAME}`,
  description: "View the global leaderboard. See who's solving the most problems and climbing the ranks.",
  keywords: ["leaderboard", "rankings", "python", "coding challenges"],
  canonical: `${SITE_URL}/leaderboard`,
  ogType: "website",
});

export const getProblemsMetadata = (): SEOMetadata => ({
  title: `Problems | ${SITE_NAME}`,
  description: "Browse all Python coding challenges. Filter by difficulty, tags, and more.",
  keywords: ["python problems", "coding challenges", "algorithms", "practice"],
  canonical: `${SITE_URL}/problems`,
  ogType: "website",
});

export const getPricingMetadata = (): SEOMetadata => ({
  title: `Pricing | ${SITE_NAME}`,
  description: "Simple, transparent pricing. Get unlimited access to all Python challenges.",
  keywords: ["pricing", "subscription", "python challenges"],
  canonical: `${SITE_URL}/pricing`,
  ogType: "website",
});

export const getAboutMetadata = (): SEOMetadata => ({
  title: `About | ${SITE_NAME}`,
  description: "Learn about PyPyCode. A Python-focused coding platform built for developers.",
  keywords: ["about", "python", "coding platform"],
  canonical: `${SITE_URL}/about`,
  ogType: "website",
});

export const getContactMetadata = (): SEOMetadata => ({
  title: `Contact | ${SITE_NAME}`,
  description: "Get in touch with the PyPyCode team. We'd love to hear from you.",
  keywords: ["contact", "support"],
  canonical: `${SITE_URL}/contact`,
  ogType: "website",
});

export const createProblemStructuredData = (problem: {
  title: string;
  slug: string;
  difficulty: string;
  description?: string;
  tags?: string[];
}): StructuredData => ({
  "@context": "https://schema.org",
  "@type": "CreativeWork",
  name: problem.title,
  description: problem.description || `Solve ${problem.title}`,
  url: `${SITE_URL}/problems/${problem.slug}`,
  author: {
    "@type": "Organization",
    name: SITE_NAME,
    url: SITE_URL,
  },
  keywords: problem.tags?.join(", ") || "python, algorithm",
  isAccessibleForFree: true,
});

export const createOrganizationStructuredData = (): StructuredData => ({
  "@context": "https://schema.org",
  "@type": "Organization",
  name: SITE_NAME,
  url: SITE_URL,
  logo: `${SITE_URL}/logo.svg`,
  description: "A Python-only coding challenge platform",
  sameAs: [
    "https://twitter.com/pypycode",
    "https://github.com/pypycode",
  ],
  contactPoint: {
    "@type": "ContactPoint",
    contactType: "Customer Service",
    email: "support@pypycode.com",
  },
});

export const createBreadcrumbStructuredData = (items: Array<{ name: string; url: string }>): StructuredData => ({
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  itemListElement: items.map((item, index) => ({
    "@type": "ListItem",
    position: index + 1,
    name: item.name,
    item: item.url,
  })),
});

function updateOrCreateMetaTag(name: string, content: string, attribute = "name") {
  let tag = document.querySelector(`meta[${attribute}="${name}"]`) as HTMLMetaElement;
  if (!tag) {
    tag = document.createElement("meta");
    tag.setAttribute(attribute, name);
    document.head.appendChild(tag);
  }
  tag.content = content;
}

function updateOrCreateLinkTag(rel: string, href: string) {
  let tag = document.querySelector(`link[rel="${rel}"]`) as HTMLLinkElement;
  if (!tag) {
    tag = document.createElement("link");
    tag.rel = rel;
    document.head.appendChild(tag);
  }
  tag.href = href;
}

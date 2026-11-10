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

export const SITE_URL: string = import.meta.env?.VITE_SITE_URL || "https://pypycode.com";
export const SITE_NAME = "PyPyCode";
const DEFAULT_IMAGE = `${SITE_URL}/og-image.png`;

const stripMarkdown = (text: string): string =>
  text
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/`([^`]*)`/g, "$1")
    .replace(/^#{1,6}\s+/gm, "")
    .replace(/[*_~>]/g, "")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\s+/g, " ")
    .trim();

const truncate = (text: string, max: number): string =>
  text.length <= max ? text : `${text.slice(0, max - 1).replace(/\s+\S*$/, "")}…`;

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

  // Canonical (remove any stale one from a previous route when this page has none)
  if (metadata.canonical) {
    updateOrCreateLinkTag("canonical", metadata.canonical);
  } else {
    document.querySelector('link[rel="canonical"]')?.remove();
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

  // Robots (always reset so a noindex from a previous route never leaks into this one)
  updateOrCreateMetaTag("robots", metadata.robots || "index, follow");

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
  tags?: string[];
}): SEOMetadata => {
  const difficulty = problem.difficulty.charAt(0).toUpperCase() + problem.difficulty.slice(1);
  const title = `${problem.title} - Python Solution Practice (${difficulty}) | ${SITE_NAME}`;
  const summary = problem.description ? truncate(stripMarkdown(problem.description), 120) : "";
  const description = summary
    ? `${summary} Solve ${problem.title} in Python with instant sandboxed test feedback.`
    : `Solve ${problem.title} in Python on ${SITE_NAME}. ${difficulty} difficulty with instant sandboxed test feedback.`;
  return {
    title,
    description: truncate(description, 160),
    keywords: [
      `${problem.title} python`,
      `${problem.title} solution`,
      ...(problem.tags ?? []).map((t) => t.replace(/-/g, " ")),
      problem.difficulty,
      "python coding interview question",
      "python algorithm practice",
    ],
    canonical: `${SITE_URL}/problems/${problem.slug}`,
    ogTitle: title,
    ogDescription: `Practice ${problem.title} in Python. ${difficulty} difficulty.`,
    ogType: "article",
  };
};

export const getTermsMetadata = (): SEOMetadata => ({
  title: `Terms and Conditions | ${SITE_NAME}`,
  description: `Terms and conditions for using ${SITE_NAME}, the Python coding practice platform operated by ISHA Systems LLC.`,
  canonical: `${SITE_URL}/terms`,
  ogType: "website",
});

export const getPrivacyMetadata = (): SEOMetadata => ({
  title: `Privacy Policy | ${SITE_NAME}`,
  description: `How ${SITE_NAME} collects, uses, and protects your personal information.`,
  canonical: `${SITE_URL}/privacy`,
  ogType: "website",
});

export const getNotFoundMetadata = (): SEOMetadata => ({
  title: `Page Not Found | ${SITE_NAME}`,
  description: "The page you are looking for does not exist.",
  robots: "noindex, follow",
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

export const PRICING_FAQ: Array<{ question: string; answer: string }> = [
  {
    question: "How much does PyPyCode cost?",
    answer:
      "PyPyCode is $30 per year for unlimited access to every Python coding problem, unlimited runs and submissions, and full leaderboard participation. That is about $2.50 a month.",
  },
  {
    question: "Is PyPyCode cheaper than LeetCode Premium?",
    answer:
      "Yes. LeetCode Premium is $159 per year (or $35 per month). PyPyCode is $30 per year, roughly five times cheaper, for a platform focused entirely on Python interview and algorithm practice.",
  },
  {
    question: "Is there a free trial?",
    answer:
      "Yes. Every new account gets a 15-day free trial with full access to all problems and submissions. No payment details are required to start.",
  },
  {
    question: "Do I need a credit card to start the trial?",
    answer:
      "No. You can start the 15-day trial with just an account. You only add a payment method if you decide to subscribe after the trial.",
  },
  {
    question: "Is there a monthly plan?",
    answer:
      "PyPyCode is billed annually at $30 per year. There is no separate monthly plan; the single annual price keeps the cost far below monthly competitors.",
  },
  {
    question: "What is included in the subscription?",
    answer:
      "Unlimited access to all coding problems, unlimited sandboxed code runs and submissions, full leaderboard participation, and priority access to new problems and features as they are released.",
  },
];

export const getPricingMetadata = (): SEOMetadata => ({
  title: `Pricing: $30/year, 5x Cheaper Than LeetCode Premium | ${SITE_NAME}`,
  description:
    "Unlimited Python coding practice for $30/year. About 5x cheaper than LeetCode Premium ($159/yr). 15-day free trial, no credit card required.",
  keywords: [
    "pricing",
    "leetcode premium alternative",
    "leetcode alternative",
    "cheaper than leetcode",
    "leetcode premium cost",
    "python coding practice",
    "coding interview prep subscription",
  ],
  canonical: `${SITE_URL}/pricing`,
  ogType: "website",
});

export const createPricingProductStructuredData = (price: {
  amount: number;
  currency: string;
}): StructuredData => ({
  "@context": "https://schema.org",
  "@type": "Product",
  name: `${SITE_NAME} All Access`,
  description:
    "Annual subscription with unlimited access to every Python coding problem, unlimited sandboxed runs and submissions, and full leaderboard participation.",
  brand: { "@type": "Brand", name: SITE_NAME },
  url: `${SITE_URL}/pricing`,
  image: DEFAULT_IMAGE,
  offers: {
    "@type": "Offer",
    price: price.amount.toFixed(2),
    priceCurrency: price.currency.toUpperCase(),
    availability: "https://schema.org/InStock",
    url: `${SITE_URL}/pricing`,
    priceSpecification: {
      "@type": "UnitPriceSpecification",
      price: price.amount.toFixed(2),
      priceCurrency: price.currency.toUpperCase(),
      billingDuration: 1,
      billingIncrement: 1,
      unitCode: "ANN",
      referenceQuantity: { "@type": "QuantitativeValue", value: 1, unitCode: "ANN" },
    },
  },
});

export const createFAQStructuredData = (
  faqs: Array<{ question: string; answer: string }>
): StructuredData => ({
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: faqs.map((faq) => ({
    "@type": "Question",
    name: faq.question,
    acceptedAnswer: { "@type": "Answer", text: faq.answer },
  })),
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
  "@type": "LearningResource",
  name: problem.title,
  description: problem.description ? truncate(stripMarkdown(problem.description), 300) : `Solve ${problem.title}`,
  url: `${SITE_URL}/problems/${problem.slug}`,
  learningResourceType: "Coding exercise",
  educationalLevel: problem.difficulty,
  inLanguage: "en",
  about: { "@type": "Thing", name: "Python programming" },
  programmingLanguage: "Python",
  author: {
    "@type": "Organization",
    name: SITE_NAME,
    url: SITE_URL,
  },
  keywords: problem.tags?.map((t) => t.replace(/-/g, " ")).join(", ") || "python, algorithm",
  isAccessibleForFree: true,
});

export const createWebSiteStructuredData = (): StructuredData => ({
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: SITE_NAME,
  url: SITE_URL,
  description: "A Python-only coding challenge platform with instant sandboxed feedback.",
  potentialAction: {
    "@type": "SearchAction",
    target: {
      "@type": "EntryPoint",
      urlTemplate: `${SITE_URL}/problems?search={search_term_string}`,
    },
    "query-input": "required name=search_term_string",
  },
});

export const createOrganizationStructuredData = (): StructuredData => ({
  "@context": "https://schema.org",
  "@type": "Organization",
  name: SITE_NAME,
  url: SITE_URL,
  logo: `${SITE_URL}/logo.svg`,
  description: "A Python-only coding challenge platform",
  sameAs: ["https://github.com/pypycode"],
  contactPoint: {
    "@type": "ContactPoint",
    contactType: "Customer Service",
    email: "support@ishasystems.com",
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

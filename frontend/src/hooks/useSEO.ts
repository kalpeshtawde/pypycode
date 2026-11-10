import { useEffect } from "react";
import {
  updateMetaTags,
  updateStructuredData,
  SEOMetadata,
  StructuredData,
} from "../utils/seo";

type StructuredDataInput = StructuredData | StructuredData[] | undefined | null;

export const useSEO = (metadata: SEOMetadata | null | undefined, structuredData?: StructuredDataInput) => {
  useEffect(() => {
    if (!metadata) return;
    updateMetaTags(metadata);

    if (structuredData) {
      const blocks = Array.isArray(structuredData) ? structuredData : [structuredData];
      blocks.forEach((block, index) => {
        updateStructuredData(block, index === 0 ? "structured-data" : `structured-data-${index}`);
      });
    }

    // Scroll to top
    window.scrollTo(0, 0);
  }, [metadata, structuredData]);
};
